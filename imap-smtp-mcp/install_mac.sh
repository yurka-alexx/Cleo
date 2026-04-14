#!/usr/bin/env bash
# ============================================================
#  IMAP-SMTP-MCP Installer — macOS
#  Version: 2.0  |  Able & Baker GmbH
#
#  Verwendung:
#    bash install_mac.sh
#    (ohne Argumente — vollständig interaktiv)
#
#  Credentials werden NICHT in server.py gespeichert,
#  sondern sicher in der Claude Desktop Config hinterlegt.
# ============================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; RESET='\033[0m'

ok()   { echo -e "${GREEN}✅  $1${RESET}"; }
info() { echo -e "${BLUE}ℹ️   $1${RESET}"; }
warn() { echo -e "${YELLOW}⚠️   $1${RESET}"; }
fail() { echo -e "${RED}❌  $1${RESET}"; exit 1; }
step() { echo -e "\n${BOLD}── $1${RESET}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/mcp-servers/imap-smtp"
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗"
echo    "║   IMAP-SMTP-MCP Installer — macOS           v2.0 ║"
echo    "║   Able & Baker GmbH                              ║"
echo -e "╚══════════════════════════════════════════════════╝${RESET}"
echo ""

# ── Schritt 1: Zugangsdaten abfragen ────────────────────────
step "Schritt 1: Zugangsdaten"
echo ""
read -rp "  IMAP-Server    (z.B. mail.example.com): " IMAP_HOST
read -rp "  SMTP-Server    [Enter = gleich wie IMAP]: " SMTP_HOST_INPUT
SMTP_HOST="${SMTP_HOST_INPUT:-$IMAP_HOST}"
read -rp "  IMAP-Port      [993]: " IMAP_PORT_INPUT
IMAP_PORT="${IMAP_PORT_INPUT:-993}"
read -rp "  SMTP-Port      [587]: " SMTP_PORT_INPUT
SMTP_PORT="${SMTP_PORT_INPUT:-587}"
echo ""
read -rp "  E-Mail-Adresse: " MAIL_USER
read -rsp "  Passwort:       " MAIL_PASSWORD
echo ""

info "Host:   $IMAP_HOST"
info "SMTP:   $SMTP_HOST"
info "User:   $MAIL_USER"

# ── Schritt 2: uv sicherstellen ─────────────────────────────
step "Schritt 2: uv prüfen"
UV_PATH=$(command -v uv 2>/dev/null || true)
if [[ -z "$UV_PATH" ]]; then
  warn "uv nicht gefunden — wird installiert..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  UV_PATH=$(command -v uv 2>/dev/null || echo "$HOME/.local/bin/uv")
fi
[[ -x "$UV_PATH" ]] || fail "uv nicht gefunden. Manuell: https://docs.astral.sh/uv/"
ok "uv: $UV_PATH"

# ── Schritt 3: IMAP-Verbindung testen + Ordner ermitteln ────
step "Schritt 3: IMAP-Verbindung testen & Ordner erkennen"

FOLDER_JSON=$(python3 - <<PYEOF
import imaplib, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode    = ssl.CERT_NONE
try:
    imap = imaplib.IMAP4_SSL("${IMAP_HOST}", ${IMAP_PORT}, ssl_context=ctx)
    imap.login("${MAIL_USER}", "${MAIL_PASSWORD}")
    _, raw_folders = imap.list()
    imap.logout()
    result = {"drafts": "Drafts", "trash": "Trash", "archive": "Archive"}
    for f in raw_folders:
        line = f.decode()
        if r"\Drafts"  in line: result["drafts"]  = line.split('"/"')[-1].strip().strip('"')
        if r"\Trash"   in line: result["trash"]   = line.split('"/"')[-1].strip().strip('"')
        if r"\Archive" in line: result["archive"] = line.split('"/"')[-1].strip().strip('"')
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e), "drafts": "Drafts", "trash": "Trash", "archive": "Archive"}))
PYEOF
)

FOLDER_DRAFTS=$(python3  -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('drafts','Drafts'))"   "$FOLDER_JSON")
FOLDER_TRASH=$(python3   -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('trash','Trash'))"     "$FOLDER_JSON")
FOLDER_ARCHIVE=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('archive','Archive'))" "$FOLDER_JSON")
HAS_ERROR=$(python3      -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('error',''))"          "$FOLDER_JSON")

if [[ -n "$HAS_ERROR" ]]; then
  fail "IMAP-Verbindung fehlgeschlagen: $HAS_ERROR\nZugangsdaten prüfen und erneut versuchen."
fi

ok "Verbindung erfolgreich"
info "Entwürfe-Ordner : $FOLDER_DRAFTS"
info "Papierkorb-Ordner: $FOLDER_TRASH"
info "Archiv-Ordner   : $FOLDER_ARCHIVE"

# ── Schritt 4: server.py kopieren ───────────────────────────
step "Schritt 4: server.py installieren"
mkdir -p "$TARGET_DIR"

SERVER_SRC="$SCRIPT_DIR/server.py"
if [[ ! -f "$SERVER_SRC" ]]; then
  fail "server.py nicht gefunden in $SCRIPT_DIR\nBitte das gesamte imap-smtp-mcp-Verzeichnis herunterladen."
fi
cp "$SERVER_SRC" "$TARGET_DIR/server.py"
ok "server.py → $TARGET_DIR/server.py"

# ── Schritt 5: Claude Desktop Config schreiben ──────────────
step "Schritt 5: Claude Desktop Config konfigurieren"
mkdir -p "$(dirname "$CONFIG_FILE")"

# Backup
[[ -f "$CONFIG_FILE" ]] && cp "$CONFIG_FILE" "${CONFIG_FILE}.backup" && info "Backup: ${CONFIG_FILE}.backup"

python3 - <<PYEOF
import json, os, sys

config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
config = {}
if os.path.exists(config_path):
    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError:
        pass  # Backup wurde bereits erstellt

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["imap-smtp"] = {
    "command": "${UV_PATH}",
    "args": ["run", "--script", "${TARGET_DIR}/server.py"],
    "env": {
        "IMAP_HOST":      "${IMAP_HOST}",
        "SMTP_HOST":      "${SMTP_HOST}",
        "MAIL_USER":      "${MAIL_USER}",
        "MAIL_PASSWORD":  "${MAIL_PASSWORD}",
        "IMAP_PORT":      "${IMAP_PORT}",
        "SMTP_PORT":      "${SMTP_PORT}",
        "FOLDER_DRAFTS":  "${FOLDER_DRAFTS}",
        "FOLDER_TRASH":   "${FOLDER_TRASH}",
        "FOLDER_ARCHIVE": "${FOLDER_ARCHIVE}"
    }
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print("Config gespeichert.")
PYEOF

python3 -m json.tool "$CONFIG_FILE" > /dev/null && ok "JSON valide" || fail "Ungültiges JSON in der Config!"
ok "Claude Desktop Config aktualisiert"

# ── Fertig ───────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════╗"
echo    "║   ✅  Installation abgeschlossen!                ║"
echo    "║                                                  ║"
echo    "║   → Claude Desktop neu starten (⌘Q → öffnen)    ║"
echo    "║   → Dann: 'zeig mir die letzten Mails' testen   ║"
echo -e "╚══════════════════════════════════════════════════╝${RESET}"
echo ""
info "Credentials wurden sicher in der Claude Config gespeichert."
info "server.py enthält KEINE Passwörter."
echo ""
