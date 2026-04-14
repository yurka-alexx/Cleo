#!/usr/bin/env python3
# /// script
# dependencies = ["mcp[cli]"]
# ///
"""
IMAP/SMTP MCP Server
Version: 1.5 — Credentials via environment variables (no hardcoding)

Setup: run install.sh to configure credentials interactively.

Required environment variables:
  IMAP_HOST      — IMAP/SMTP server hostname
  MAIL_USER      — Email address (login)
  MAIL_PASSWORD  — Email password

Optional environment variables (defaults shown):
  IMAP_PORT      — IMAP SSL port (default: 993)
  SMTP_HOST      — SMTP hostname (default: same as IMAP_HOST)
  SMTP_PORT      — SMTP STARTTLS port (default: 587)
  FOLDER_INBOX   — Inbox folder name (default: INBOX)
  FOLDER_DRAFTS  — Drafts folder name (default: Drafts)
  FOLDER_TRASH   — Trash folder name (default: Trash)
  FOLDER_ARCHIVE — Archive folder name (default: Archive)
"""

import imaplib
import smtplib
import ssl
import email
import json
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime, timedelta, timezone

from mcp.server.fastmcp import FastMCP

# ── Credentials (from environment) ────────────────────────────────────────────
def _require_env(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        print(f"ERROR: Required environment variable '{key}' is not set.", file=sys.stderr)
        print("Run install.sh to configure credentials.", file=sys.stderr)
        sys.exit(1)
    return val

IMAP_HOST     = _require_env("IMAP_HOST")
MAIL_USER     = _require_env("MAIL_USER")
MAIL_PASSWORD = _require_env("MAIL_PASSWORD")

IMAP_PORT     = int(os.environ.get("IMAP_PORT", "993"))
SMTP_HOST     = os.environ.get("SMTP_HOST", IMAP_HOST)
SMTP_PORT     = int(os.environ.get("SMTP_PORT", "587"))

# ── Folder names ──────────────────────────────────────────────────────────────
FOLDER_INBOX   = os.environ.get("FOLDER_INBOX",   "INBOX")
FOLDER_DRAFTS  = os.environ.get("FOLDER_DRAFTS",  "Drafts")
FOLDER_TRASH   = os.environ.get("FOLDER_TRASH",   "Trash")
FOLDER_ARCHIVE = os.environ.get("FOLDER_ARCHIVE", "Archive")

# ── MCP Server ────────────────────────────────────────────────────────────────
mcp = FastMCP("imap-smtp")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _imap_connect() -> imaplib.IMAP4_SSL:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    conn.login(MAIL_USER, MAIL_PASSWORD)
    return conn


def _decode_header_str(raw) -> str:
    if raw is None:
        return ""
    parts = decode_header(raw)
    decoded = []
    for part, enc in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            decoded.append(str(part))
    return " ".join(decoded)


def _parse_message(raw_bytes) -> dict:
    msg = email.message_from_bytes(raw_bytes)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
    return {
        "from":    _decode_header_str(msg.get("From")),
        "to":      _decode_header_str(msg.get("To")),
        "subject": _decode_header_str(msg.get("Subject")),
        "date":    msg.get("Date", ""),
        "body":    body[:4000],
    }


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def fetch_recent_mails(folder: str = "INBOX", hours: int = 24) -> str:
    """Fetch mails received in the last N hours. Returns JSON list with stable UIDs."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        since = (datetime.utcnow() - timedelta(hours=hours)).strftime("%d-%b-%Y")
        _, data = conn.uid("SEARCH", None, f'(SINCE "{since}")')
        uids = data[0].split()
        results = []
        for uid in uids[-50:]:
            _, raw = conn.uid("FETCH", uid, "(RFC822)")
            if raw and raw[0]:
                parsed = _parse_message(raw[0][1])
                parsed["uid"] = uid.decode()
                results.append(parsed)
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally:
        conn.logout()


@mcp.tool()
def search_mails(folder: str = "INBOX", from_addr: str = "", subject: str = "",
                 unread_only: bool = False, since_days: int = 30) -> str:
    """Search mails by sender, subject, unread flag, date range. Returns JSON list with stable UIDs."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        criteria = []
        since = (datetime.utcnow() - timedelta(days=since_days)).strftime("%d-%b-%Y")
        criteria.append(f'SINCE "{since}"')
        if from_addr:
            criteria.append(f'FROM "{from_addr}"')
        if subject:
            criteria.append(f'SUBJECT "{subject}"')
        if unread_only:
            criteria.append("UNSEEN")
        query = "(" + " ".join(criteria) + ")"
        _, data = conn.uid("SEARCH", None, query)
        uids = data[0].split()
        results = []
        for uid in uids[-50:]:
            _, raw = conn.uid("FETCH", uid, "(RFC822)")
            if raw and raw[0]:
                parsed = _parse_message(raw[0][1])
                parsed["uid"] = uid.decode()
                results.append(parsed)
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally:
        conn.logout()


@mcp.tool()
def get_mail(uid: str, folder: str = "INBOX") -> str:
    """Fetch a single mail by UID with full body. Returns JSON object."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        _, raw = conn.uid("FETCH", uid.encode(), "(RFC822)")
        if not raw or not raw[0]:
            return json.dumps({"error": "Mail not found"})
        parsed = _parse_message(raw[0][1])
        parsed["uid"] = uid
        return json.dumps(parsed, ensure_ascii=False, indent=2)
    finally:
        conn.logout()


@mcp.tool()
def create_draft(to: str, subject: str, text: str, cc: str = "") -> str:
    """Create a draft email in the Drafts folder."""
    conn = _imap_connect()
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = MAIL_USER
        msg["To"]      = to
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = cc
        msg.attach(MIMEText(text, "plain", "utf-8"))
        raw = msg.as_bytes()
        result = conn.append(FOLDER_DRAFTS, "", imaplib.Time2Internaldate(datetime.now(tz=timezone.utc)), raw)
        return json.dumps({"status": "ok", "result": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def send_mail(to: str, subject: str, text: str, cc: str = "") -> str:
    """Send an email via SMTP (STARTTLS). Returns status."""
    msg = MIMEMultipart("alternative")
    msg["From"]    = MAIL_USER
    msg["To"]      = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    msg.attach(MIMEText(text, "plain", "utf-8"))
    recipients = [to] + ([cc] if cc else [])
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls(context=ctx)
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(MAIL_USER, recipients, msg.as_string())
    return json.dumps({"status": "sent", "to": to, "subject": subject})


@mcp.tool()
def archive_mail(uid: str, folder: str = "INBOX") -> str:
    """Move a mail to the Archive folder. Uses stable IMAP UIDs."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        result = conn.uid("COPY", uid.encode(), FOLDER_ARCHIVE)
        if result[0] == "OK":
            conn.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
            conn.expunge()
            return json.dumps({"status": "archived", "uid": uid})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def delete_mail(uid: str, folder: str = "INBOX", permanent: bool = False) -> str:
    """Delete a mail. permanent=False moves to Trash, permanent=True deletes directly."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        if permanent:
            conn.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
            conn.expunge()
            return json.dumps({"status": "deleted_permanently", "uid": uid})
        else:
            result = conn.uid("COPY", uid.encode(), FOLDER_TRASH)
            if result[0] == "OK":
                conn.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
                conn.expunge()
                return json.dumps({"status": "moved_to_trash", "uid": uid})
            return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def mark_mail(uid: str, action: str, folder: str = "INBOX") -> str:
    """Mark a mail: action = 'read', 'unread', 'flag', 'unflag'. Uses stable UIDs."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        action_map = {
            "read":   ("+FLAGS", "\\Seen"),
            "unread": ("-FLAGS", "\\Seen"),
            "flag":   ("+FLAGS", "\\Flagged"),
            "unflag": ("-FLAGS", "\\Flagged"),
        }
        if action not in action_map:
            return json.dumps({"error": f"Unknown action: {action}. Use: read, unread, flag, unflag"})
        op, flag = action_map[action]
        conn.uid("STORE", uid.encode(), op, flag)
        return json.dumps({"status": "ok", "uid": uid, "action": action})
    finally:
        conn.logout()


@mcp.tool()
def create_folder(name: str) -> str:
    """Create a new IMAP folder. Supports nested folders with '/' separator."""
    conn = _imap_connect()
    try:
        result = conn.create(name)
        if result[0] == "OK":
            return json.dumps({"status": "created", "folder": name})
        detail = str(result)
        if "ALREADYEXISTS" in detail.upper() or "already exists" in detail.lower():
            return json.dumps({"status": "already_exists", "folder": name})
        return json.dumps({"status": "error", "detail": detail})
    finally:
        conn.logout()


@mcp.tool()
def move_to_folder(uid: str, target_folder: str, source_folder: str = "INBOX") -> str:
    """Move a mail to any folder. Creates target folder if it doesn't exist."""
    conn = _imap_connect()
    try:
        conn.create(target_folder)
        conn.select(source_folder)
        result = conn.uid("COPY", uid.encode(), target_folder)
        if result[0] == "OK":
            conn.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
            conn.expunge()
            return json.dumps({"status": "moved", "uid": uid, "from": source_folder, "to": target_folder})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def save_to_folder(folder: str, subject: str, text: str, sender_name: str = "Cleo", html: str = "") -> str:
    """
    Save a message directly into any IMAP folder via APPEND.
    Use for briefings, summaries, notes. Saved as UNREAD.
    Optional html= for HTML-formatted version (plain text fallback always included).
    """
    conn = _imap_connect()
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = f"{sender_name} <{MAIL_USER}>"
        msg["To"]      = MAIL_USER
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "plain", "utf-8"))
        if html:
            msg.attach(MIMEText(html, "html", "utf-8"))
        raw = msg.as_bytes()
        result = conn.append(folder, "", imaplib.Time2Internaldate(datetime.now(tz=timezone.utc)), raw)
        if result[0] == "OK":
            return json.dumps({"status": "saved", "folder": folder, "subject": subject})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
