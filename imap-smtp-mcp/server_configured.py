#!/usr/bin/env python3
# /// script
# dependencies = ["mcp[cli]"]
# ///
"""
IMAP/SMTP MCP Server — LOKALE TESTKONFIGURATION
⚠️  DIESE DATEI ENTHÄLT ZUGANGSDATEN — NIEMALS COMMITTEN!
    Sie ist in .gitignore eingetragen und dient nur für lokale Tests.
    Für die produktive Version: server.py + install.sh verwenden.

Version: 1.5
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

from mcp.server.fastmcp import FastMCP

# ── Credentials ────────────────────────────────────────────────────────────────
# ⚠️ PLATZHALTER — echte Werte lokal eintragen, NICHT committen!
IMAP_HOST     = "DEIN_MAILSERVER"          # z.B. mail.example.com
IMAP_PORT     = 993
SMTP_HOST     = "DEIN_MAILSERVER"
SMTP_PORT     = 587
MAIL_USER     = "DEINE_EMAIL@DOMAIN.DE"
MAIL_PASSWORD = "DEIN_PASSWORT"

# ── Ordnernamen ────────────────────────────────────────────────────────────────
# Ggf. anpassen (z.B. bei deutschen Mailclients: "Entwürfe", "Papierkorb")
FOLDER_INBOX   = "INBOX"
FOLDER_DRAFTS  = "Drafts"
FOLDER_TRASH   = "Trash"
FOLDER_ARCHIVE = "Archive"

# ── Rest des Codes identisch mit server.py ─────────────────────────────────────
# (Für Produktivbetrieb bitte server.py + install.sh nutzen)

from mcp.server.fastmcp import FastMCP
mcp = FastMCP("imap-smtp")

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

# Tools: identisch mit server.py — hier weggelassen um Datei kurz zu halten.
# Vollständige Implementierung: server.py

if __name__ == "__main__":
    print("⚠️  server_configured.py ist eine lokale Testkonfiguration.")
    print("    Zugangsdaten eintragen (IMAP_HOST, MAIL_USER, MAIL_PASSWORD)")
    print("    und dann: uv run --script server_configured.py")
