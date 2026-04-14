#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# IMAP/SMTP MCP Server — Interactive Installer
# Configures credentials and updates Claude Desktop config
# ─────────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║        IMAP/SMTP MCP Server — Setup                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Zugangsdaten werden NUR lokal in der Claude-Konfiguration"
echo "gespeichert — niemals im Code oder auf GitHub."
echo ""

# ── Credentials abfragen ──────────────────────────────────────────
read -p "IMAP/SMTP-Server (z.B. mail.example.com): " IMAP_HOST
read -p "E-Mail-Adresse: " MAIL_USER
read -s -p "Passwort: " MAIL_PASSWORD
echo ""
read -p "IMAP-Port [993]: " IMAP_PORT
IMAP_PORT="${IMAP_PORT:-993}"
read -p "SMTP-Port [587]: " SMTP_PORT
SMTP_PORT="${SMTP_PORT:-587}"

echo ""
echo "── Ordnernamen (Enter = Standard übernehmen) ────────────────"
read -p "Posteingang [INBOX]: " FOLDER_INBOX
FOLDER_INBOX="${FOLDER_INBOX:-INBOX}"
read -p "Entwürfe [Drafts]: " FOLDER_DRAFTS
FOLDER_DRAFTS="${FOLDER_DRAFTS:-Drafts}"
read -p "Papierkorb [Trash]: " FOLDER_TRASH
FOLDER_TRASH="${FOLDER_TRASH:-Trash}"
read -p "Archiv [Archive]: " FOLDER_ARCHIVE
FOLDER_ARCHIVE="${FOLDER_ARCHIVE:-Archive}"

# ── Claude Desktop Config aktualisieren ───────────────────────────
echo ""
echo "Aktualisiere Claude Desktop Konfiguration..."

# Backup
if [ -f "$CLAUDE_CONFIG" ]; then
    cp "$CLAUDE_CONFIG" "${CLAUDE_CONFIG}.backup"
    echo "  ✓ Backup erstellt: ${CLAUDE_CONFIG}.backup"
fi

# Python zum Einbinden in JSON (sicheres Escaping)
python3 << PYEOF
import json, os, sys

config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")

# Bestehende Config laden oder neu erstellen
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
else:
    config = {}

if "mcpServers" not in config:
    config["mcpServers"] = {}

script_dir = "$SCRIPT_DIR"

config["mcpServers"]["imap-smtp"] = {
    "command": "uv",
    "args": ["run", "--script", os.path.join(script_dir, "server.py")],
    "env": {
        "IMAP_HOST":      "$IMAP_HOST",
        "MAIL_USER":      "$MAIL_USER",
        "MAIL_PASSWORD":  "$MAIL_PASSWORD",
        "IMAP_PORT":      "$IMAP_PORT",
        "SMTP_PORT":      "$SMTP_PORT",
        "FOLDER_INBOX":   "$FOLDER_INBOX",
        "FOLDER_DRAFTS":  "$FOLDER_DRAFTS",
        "FOLDER_TRASH":   "$FOLDER_TRASH",
        "FOLDER_ARCHIVE": "$FOLDER_ARCHIVE",
    }
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"  ✓ Konfiguration gespeichert: {config_path}")
PYEOF

# ── Verbindungstest ───────────────────────────────────────────────
echo ""
echo "Teste IMAP-Verbindung..."
python3 << PYEOF
import imaplib, ssl, sys

try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = imaplib.IMAP4_SSL("$IMAP_HOST", $IMAP_PORT, ssl_context=ctx)
    conn.login("$MAIL_USER", "$MAIL_PASSWORD")
    conn.logout()
    print("  ✓ IMAP-Verbindung erfolgreich")
except Exception as e:
    print(f"  ✗ Verbindung fehlgeschlagen: {e}")
    print("  → Zugangsdaten prüfen und install.sh erneut ausführen")
    sys.exit(1)
PYEOF

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✓ Setup abgeschlossen!                                  ║"
echo "║                                                          ║"
echo "║  Claude Desktop neu starten, damit der MCP-Server       ║"
echo "║  mit den neuen Zugangsdaten geladen wird.                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
