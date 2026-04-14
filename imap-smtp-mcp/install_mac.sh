#!/usr/bin/env bash
# ============================================================
#  IMAP-SMTP-MCP Installer — macOS
#  Version: 1.0  |  Able & Baker GmbH
#
#  Verwendung:
#    bash install_mac.sh \
#      --host w01bf911.kasserver.com \
#      --user user@example.com \
#      --password "MeinPasswort" \
#      [--imap-port 993] \
#      [--smtp-port 587]
#
#  Ohne Argumente: interaktive Eingabe.
# ============================================================

set -euo pipefail

# ── Farben ──────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; RESET='\033[0m'

ok()   { echo -e "${GREEN}✅ $1${RESET}"; }
info() { echo -e "${BLUE}ℹ️  $1${RESET}"; }
warn() { echo -e "${YELLOW}⚠️  $1${RESET}"; }
fail() { echo -e "${RED}❌ $1${RESET}"; exit 1; }
step() { echo -e "\n${BOLD}── $1 ──────────────────────────────────${RESET}"; }

# ── Parameter parsen ────────────────────────────────────────
IMAP_HOST=""; MAIL_USER=""; MAIL_PASSWORD=""
IMAP_PORT=993; SMTP_PORT=587

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)      IMAP_HOST="$2";     shift 2 ;;
    --user)      MAIL_USER="$2";     shift 2 ;;
    --password)  MAIL_PASSWORD="$2"; shift 2 ;;
    --imap-port) IMAP_PORT="$2";     shift 2 ;;
    --smtp-port) SMTP_PORT="$2";     shift 2 ;;
    *) warn "Unbekannter Parameter: $1"; shift ;;
  esac
done

# Interaktiv auffüllen falls fehlend
if [[ -z "$IMAP_HOST" ]]; then
  read -rp "IMAP/SMTP-Host (z.B. mail.example.com): " IMAP_HOST
fi
if [[ -z "$MAIL_USER" ]]; then
  read -rp "E-Mail-Adresse / Benutzername: " MAIL_USER
fi
if [[ -z "$MAIL_PASSWORD" ]]; then
  read -rsp "Passwort: " MAIL_PASSWORD; echo
fi

SMTP_HOST="$IMAP_HOST"
TARGET_DIR="$HOME/mcp-servers/imap-smtp"
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
CURRENT_USER=$(whoami)

echo -e "\n${BOLD}╔══════════════════════════════════════════╗"
echo    "║   IMAP-SMTP-MCP Installer — macOS        ║"
echo -e "╚══════════════════════════════════════════╝${RESET}"
info "Host:     $IMAP_HOST"
info "User:     $MAIL_USER"
info "Zielort:  $TARGET_DIR"

# ── Schritt 1: uv sicherstellen ─────────────────────────────
step "Schritt 1: uv prüfen"
UV_PATH=$(command -v uv 2>/dev/null || echo "")
if [[ -z "$UV_PATH" ]]; then
  warn "uv nicht gefunden — wird jetzt installiert..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  UV_PATH=$(command -v uv 2>/dev/null || echo "$HOME/.local/bin/uv")
  [[ -x "$UV_PATH" ]] || fail "uv Installation fehlgeschlagen. Bitte manuell installieren: https://docs.astral.sh/uv/"
fi
ok "uv gefunden: $UV_PATH"

# ── Schritt 2: Zielordner anlegen ───────────────────────────
step "Schritt 2: Ordner anlegen"
mkdir -p "$TARGET_DIR"
ok "Ordner bereit: $TARGET_DIR"

# ── Schritt 3: IMAP-Verbindung testen + Ordner ermitteln ────
step "Schritt 3: IMAP-Verbindung testen & Ordnernamen ermitteln"

FOLDER_INFO=$("$UV_PATH" run --python 3.12 --quiet --with "imaplib2" - <<PYEOF 2>/dev/null || python3 - <<PYEOF2
import imaplib, ssl, sys, json

host     = "$IMAP_HOST"
port     = $IMAP_PORT
user     = "$MAIL_USER"
password = "$MAIL_PASSWORD"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode    = ssl.CERT_NONE

try:
    imap = imaplib.IMAP4_SSL(host, port, ssl_context=ctx)
    imap.login(user, password)
    _, raw_folders = imap.list()
    imap.logout()

    result = {"drafts": "Drafts", "trash": "Trash", "archive": "Archive", "raw": []}
    for f in raw_folders:
        line = f.decode()
        result["raw"].append(line)
        if r"\Drafts" in line:
            result["drafts"] = line.split('"/"')[-1].strip().strip('"')
        elif r"\Trash" in line:
            result["trash"] = line.split('"/"')[-1].strip().strip('"')
        elif r"\Archive" in line:
            result["archive"] = line.split('"/"')[-1].strip().strip('"')

    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e), "drafts": "Drafts", "trash": "Trash", "archive": "Archive", "raw": []}))
PYEOF
PYEOF2
)

# Ordnernamen extrahieren (Python-JSON-Parse)
FOLDER_DRAFTS=$(python3 -c "import json,sys; d=json.loads('$FOLDER_INFO'); print(d.get('drafts','Drafts'))" 2>/dev/null || echo "Drafts")
FOLDER_TRASH=$(python3  -c "import json,sys; d=json.loads('$FOLDER_INFO'); print(d.get('trash','Trash'))"   2>/dev/null || echo "Trash")
FOLDER_ARCHIVE=$(python3 -c "import json,sys; d=json.loads('$FOLDER_INFO'); print(d.get('archive','Archive'))" 2>/dev/null || echo "Archive")

ok "Verbindung erfolgreich"
info "Entwürfe-Ordner : $FOLDER_DRAFTS"
info "Papierkorb      : $FOLDER_TRASH"
info "Archiv          : $FOLDER_ARCHIVE"

# ── Schritt 4: server.py schreiben ──────────────────────────
step "Schritt 4: server.py generieren"

cat > "$TARGET_DIR/server.py" << PYEOF
#!/usr/bin/env python3
# /// script
# dependencies = ["mcp[cli]"]
# ///
"""
IMAP/SMTP MCP Server
Host: ${IMAP_HOST}
User: ${MAIL_USER}
Generated by install_mac.sh
Version: 1.2 — 11 Tools (incl. create_folder, move_to_folder, save_to_folder)
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

IMAP_HOST     = "${IMAP_HOST}"
IMAP_PORT     = ${IMAP_PORT}
SMTP_HOST     = "${SMTP_HOST}"
SMTP_PORT     = ${SMTP_PORT}
MAIL_USER     = "${MAIL_USER}"
MAIL_PASSWORD = "${MAIL_PASSWORD}"

FOLDER_INBOX   = "INBOX"
FOLDER_DRAFTS  = "${FOLDER_DRAFTS}"
FOLDER_TRASH   = "${FOLDER_TRASH}"
FOLDER_ARCHIVE = "${FOLDER_ARCHIVE}"

mcp = FastMCP("imap-smtp")


def _imap_connect():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    conn.login(MAIL_USER, MAIL_PASSWORD)
    return conn


def _decode_header_str(raw):
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


def _parse_message(raw_bytes):
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


@mcp.tool()
def fetch_recent_mails(folder: str = "INBOX", hours: int = 24) -> str:
    """Fetch mails received in the last N hours from a given folder."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        since = (datetime.utcnow() - timedelta(hours=hours)).strftime("%d-%b-%Y")
        _, data = conn.search(None, f'(SINCE "{since}")')
        uids = data[0].split()
        results = []
        for uid in uids[-50:]:
            _, raw = conn.fetch(uid, "(RFC822)")
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
    """Search mails by sender, subject, unread flag, and date range."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        criteria = []
        since = (datetime.utcnow() - timedelta(days=since_days)).strftime("%d-%b-%Y")
        criteria.append(f'SINCE "{since}"')
        if from_addr: criteria.append(f'FROM "{from_addr}"')
        if subject:   criteria.append(f'SUBJECT "{subject}"')
        if unread_only: criteria.append("UNSEEN")
        query = "(" + " ".join(criteria) + ")"
        _, data = conn.search(None, query)
        uids = data[0].split()
        results = []
        for uid in uids[-50:]:
            _, raw = conn.fetch(uid, "(RFC822)")
            if raw and raw[0]:
                parsed = _parse_message(raw[0][1])
                parsed["uid"] = uid.decode()
                results.append(parsed)
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally:
        conn.logout()


@mcp.tool()
def get_mail(uid: str, folder: str = "INBOX") -> str:
    """Fetch a single mail by UID."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        _, raw = conn.fetch(uid.encode(), "(RFC822)")
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
        if cc: msg["Cc"] = cc
        msg.attach(MIMEText(text, "plain", "utf-8"))
        result = conn.append(FOLDER_DRAFTS, "", imaplib.Time2Internaldate(datetime.now(tz=timezone.utc)), msg.as_bytes())
        return json.dumps({"status": "ok", "result": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def send_mail(to: str, subject: str, text: str, cc: str = "") -> str:
    """Send an email via SMTP (STARTTLS on port 587)."""
    msg = MIMEMultipart("alternative")
    msg["From"]    = MAIL_USER
    msg["To"]      = to
    msg["Subject"] = subject
    if cc: msg["Cc"] = cc
    msg.attach(MIMEText(text, "plain", "utf-8"))
    recipients = [to] + ([cc] if cc else [])
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo(); smtp.starttls(context=ctx)
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(MAIL_USER, recipients, msg.as_string())
    return json.dumps({"status": "sent", "to": to, "subject": subject})


@mcp.tool()
def archive_mail(uid: str, folder: str = "INBOX") -> str:
    """Move a mail to the Archive folder."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        result = conn.copy(uid.encode(), FOLDER_ARCHIVE)
        if result[0] == "OK":
            conn.store(uid.encode(), "+FLAGS", "\\\\Deleted")
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
            conn.store(uid.encode(), "+FLAGS", "\\\\Deleted")
            conn.expunge()
            return json.dumps({"status": "deleted_permanently", "uid": uid})
        result = conn.copy(uid.encode(), FOLDER_TRASH)
        if result[0] == "OK":
            conn.store(uid.encode(), "+FLAGS", "\\\\Deleted")
            conn.expunge()
            return json.dumps({"status": "moved_to_trash", "uid": uid})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def mark_mail(uid: str, action: str, folder: str = "INBOX") -> str:
    """Mark a mail. action: read, unread, flag, unflag."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        action_map = {
            "read":   ("+FLAGS", "\\\\Seen"),
            "unread": ("-FLAGS", "\\\\Seen"),
            "flag":   ("+FLAGS", "\\\\Flagged"),
            "unflag": ("-FLAGS", "\\\\Flagged"),
        }
        if action not in action_map:
            return json.dumps({"error": f"Unknown action: {action}"})
        op, flag = action_map[action]
        conn.store(uid.encode(), op, flag)
        return json.dumps({"status": "ok", "uid": uid, "action": action})
    finally:
        conn.logout()



@mcp.tool()
def create_folder(name: str) -> str:
    """
    Create a new IMAP folder (top-level or nested with '/' separator).
    Example: name='Kunden' or name='Kunden/MMCompact'
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
    Use this for custom folder sorting (e.g. 'Kunden/MMCompact', 'Rechnungen').
    """
    conn = _imap_connect()
    try:
        conn.create(target_folder)
        conn.select(source_folder)
        result = conn.copy(uid.encode(), target_folder)
        if result[0] == "OK":
            conn.store(uid.encode(), "+FLAGS", "\\Deleted")
            conn.expunge()
            return json.dumps({"status": "moved", "uid": uid, "from": source_folder, "to": target_folder})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


@mcp.tool()
def save_to_folder(folder: str, subject: str, text: str, sender_name: str = "Cleo") -> str:
    """
    Save a message directly into any IMAP folder via APPEND (no SMTP needed).
    Use this to store Cleo briefings, summaries, or notes into folders like 'Cleo/Briefings'.
    Message is marked as read automatically.
    """
    conn = _imap_connect()
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = f"{sender_name} <{MAIL_USER}>"
        msg["To"]      = MAIL_USER
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "plain", "utf-8"))
        result = conn.append(
            folder,
            "\\Seen",
            imaplib.Time2Internaldate(datetime.now(tz=timezone.utc)),
            msg.as_bytes()
        )
        if result[0] == "OK":
            return json.dumps({"status": "saved", "folder": folder, "subject": subject})
        return json.dumps({"status": "error", "detail": str(result)})
    finally:
        conn.logout()


if __name__ == "__main__":
    mcp.run()
PYEOF

ok "server.py geschrieben: $TARGET_DIR/server.py"

# ── Schritt 5: claude_desktop_config.json patchen ───────────
step "Schritt 5: Claude Desktop Config patchen"

CONFIG_DIR="$HOME/Library/Application Support/Claude"
mkdir -p "$CONFIG_DIR"

NEW_MCP_ENTRY="{\"command\": \"$UV_PATH\", \"args\": [\"run\", \"--python\", \"3.12\", \"--with\", \"mcp[cli]\", \"$TARGET_DIR/server.py\"]}"

if [[ -f "$CONFIG_FILE" ]]; then
  # Bestehende Config einlesen und patchen
  CURRENT=$(cat "$CONFIG_FILE")
  # Prüfen ob mcpServers bereits existiert
  if python3 -c "import json,sys; d=json.loads(open('$CONFIG_FILE').read()); sys.exit(0 if 'mcpServers' in d else 1)" 2>/dev/null; then
    # mcpServers existiert — imap-smtp hinzufügen
    python3 - "$CONFIG_FILE" "$UV_PATH" "$TARGET_DIR/server.py" << 'PYEOF'
import json, sys
path, uv, srv = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    d = json.load(f)
d["mcpServers"]["imap-smtp"] = {
    "command": uv,
    "args": ["run", "--python", "3.12", "--with", "mcp[cli]", srv]
}
with open(path, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("patched")
PYEOF
    ok "imap-smtp zu bestehendem mcpServers hinzugefügt"
  else
    # mcpServers fehlt — als neuen Key ergänzen
    python3 - "$CONFIG_FILE" "$UV_PATH" "$TARGET_DIR/server.py" << 'PYEOF'
import json, sys
path, uv, srv = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    d = json.load(f)
d["mcpServers"] = {
    "imap-smtp": {
        "command": uv,
        "args": ["run", "--python", "3.12", "--with", "mcp[cli]", srv]
    }
}
with open(path, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("patched")
PYEOF
    ok "mcpServers-Block zur Config hinzugefügt"
  fi
else
  # Neue Config erstellen
  python3 - "$CONFIG_FILE" "$UV_PATH" "$TARGET_DIR/server.py" << 'PYEOF'
import json, sys
path, uv, srv = sys.argv[1], sys.argv[2], sys.argv[3]
d = {"mcpServers": {"imap-smtp": {"command": uv, "args": ["run", "--python", "3.12", "--with", "mcp[cli]", srv]}}}
with open(path, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("created")
PYEOF
  ok "Neue Config erstellt"
fi

# Validierung
python3 -m json.tool "$CONFIG_FILE" > /dev/null && ok "JSON valide" || fail "Ungültiges JSON in der Config!"

# ── Fertig ───────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════╗"
echo    "║   Installation abgeschlossen! ✅          ║"
echo -e "╚══════════════════════════════════════════╝${RESET}"
echo ""
info "Nächster Schritt: Claude Desktop neu starten (⌘Q → neu öffnen)"
info "Dann: Cowork öffnen und 'zeig mir die letzten Mails' testen"
echo ""
warn "Sicherheitshinweis: server.py enthält das Passwort im Klartext."
warn "Zugriff einschränken: chmod 600 $TARGET_DIR/server.py"
