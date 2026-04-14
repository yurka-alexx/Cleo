#!/usr/bin/env python3
# /// script
# dependencies = ["mcp[cli]"]
# ///
"""
IMAP/SMTP MCP Server
Configured for: bewertungsmanagement@mmcompact.de @ w01bf911.kasserver.com
Version: 1.3 — UID-safe: all IMAP operations use conn.uid() instead of sequence numbers
"""

import imaplib
import smtplib
import ssl
import email
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime, timedelta, timezone
import re

from mcp.server.fastmcp import FastMCP

# ── Credentials ────────────────────────────────────────────────────────────────
IMAP_HOST     = "w01bf911.kasserver.com"
IMAP_PORT     = 993
SMTP_HOST     = "w01bf911.kasserver.com"
SMTP_PORT     = 587
MAIL_USER     = "bewertungsmanagement@mmcompact.de"
MAIL_PASSWORD = "zEVj8O_be.TRYGDfLdXh"

# ── Folder names (kasserver default — update if needed after discovery) ────────
FOLDER_INBOX   = "INBOX"
FOLDER_DRAFTS  = "Entw&APw-rfe"   # = Entwürfe (IMAP Modified UTF-7)
FOLDER_TRASH   = "Papierkorb"
FOLDER_ARCHIVE = "Archiv"

# ── MCP Server ────────────────────────────────────────────────────────────────
mcp = FastMCP("imap-smtp")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _imap_connect() -> imaplib.IMAP4_SSL:
    """Open authenticated IMAP connection (TLS, cert check disabled for kasserver)."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    conn.login(MAIL_USER, MAIL_PASSWORD)
    return conn


def _decode_header_str(raw) -> str:
    """Decode RFC2047 encoded header value."""
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
    """Parse raw RFC822 bytes into a dict."""
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
        "body":    body[:4000],  # cap at 4k chars
    }


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def fetch_recent_mails(folder: str = "INBOX", hours: int = 24) -> str:
    """
    Fetch mails received in the last N hours from a given folder.
    Returns a JSON list of mail objects (from, to, subject, date, body, uid).
    UIDs are stable IMAP UIDs — safe to use across operations.
    """
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        since = (datetime.utcnow() - timedelta(hours=hours)).strftime("%d-%b-%Y")
        # uid('SEARCH') returns actual IMAP UIDs (stable, not sequence numbers)
        _, data = conn.uid("SEARCH", None, f'(SINCE "{since}")')
        uids = data[0].split()
        results = []
        for uid in uids[-50:]:  # max 50
            _, raw = conn.uid("FETCH", uid, "(RFC822)")
            if raw and raw[0]:
                parsed = _parse_message(raw[0][1])
                parsed["uid"] = uid.decode()
                results.append(parsed)
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally:
        conn.logout()


@mcp.tool()
def search_mails(
    folder: str = "INBOX",
    from_addr: str = "",
    subject: str = "",
    unread_only: bool = False,
    since_days: int = 30,
) -> str:
    """
    Search mails by sender, subject, unread flag, and date range.
    Returns a JSON list of matching mails with stable UIDs.
    """
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
    """
    Fetch a single mail by UID with full body.
    Returns a JSON object.
    """
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
    """
    Create a draft email in the Drafts folder.
    Returns status and APPENDUID on success.
    """
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
    """
    Send an email via SMTP (STARTTLS on port 587).
    Returns status.
    """
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
    """
    Move a mail to the Archive folder.
    Uses stable IMAP UIDs — safe even when other mails are being moved concurrently.
    """
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
    """
    Delete a mail. If permanent=False, moves to Trash. If permanent=True, deletes directly.
    Uses stable IMAP UIDs.
    """
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
    """
    Mark a mail. action: 'read', 'unread', 'flag', 'unflag'.
    Uses stable IMAP UIDs.
    """
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
    """
    Create a new IMAP folder (top-level or nested with '/' separator).
    Example: name='Kunden' or name='Kunden/MMCompact'
    Returns status and folder name.
    Already-existing folders return status 'already_exists' (not an error).
    """
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
    """
    Move a mail from source_folder to any target folder by name.
    Creates the target folder first if it does not exist.
    Uses stable IMAP UIDs — safe even when multiple mails are moved concurrently.
    Returns status and UIDs.
    """
    conn = _imap_connect()
    try:
        # Ensure target exists (idempotent)
        conn.create(target_folder)

        conn.select(source_folder)
        result = conn.uid("COPY", uid.encode(), target_folder)
        if result[0] == "OK":
            conn.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
            conn.expunge()
            return json.dumps({
                "status": "moved",
                "uid": uid,
                "from": source_folder,
                "to": target_folder,
            })
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def save_to_folder(folder: str, subject: str, text: str, sender_name: str = "Cleo", html: str = "") -> str:
    """
    Save a message directly into any IMAP folder via APPEND (no SMTP, no UID lookup).
    Use this to store Cleo briefings, summaries, or notes into folders like 'Cleo/Briefings'.
    Message is saved as UNREAD so staff immediately notice new briefings.
    Optional: pass html= for an HTML-formatted version (plain text fallback always included).
    Returns status and folder name.
    """
    conn = _imap_connect()
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = f"{sender_name} <{MAIL_USER}>"
        msg["To"]      = MAIL_USER
        msg["Subject"] = subject
        # Plain text always included as fallback
        msg.attach(MIMEText(text, "plain", "utf-8"))
        # HTML part added last — mail clients prefer the last alternative
        if html:
            msg.attach(MIMEText(html, "html", "utf-8"))
        raw = msg.as_bytes()
        # Empty flags string = unread (bold in mail client)
        result = conn.append(
            folder,
            "",
            imaplib.Time2Internaldate(datetime.now(tz=timezone.utc)),
            raw
        )
        if result[0] == "OK":
            return json.dumps({"status": "saved", "folder": folder, "subject": subject})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
