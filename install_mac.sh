#!/bin/bash
# ============================================================
#  Cleo — Installer für macOS
#  Schritt 1 von 2: Dateien herunterladen und entpacken
#
#  Ausführen:  bash install_mac.sh
#  Optionen:
#    GH_TOKEN=ghp_... bash install_mac.sh   (privates Repo)
#    CLEO_ZIP=/pfad/zu/Cleo.zip bash install_mac.sh
# ============================================================

set -euo pipefail

REPO_OWNER="yurka-alexx"
REPO_NAME="Cleo"
BRANCH="main"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/archive/refs/heads/${BRANCH}.zip"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"

# ── Banner ───────────────────────────────────────────────────
clear
echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║         Cleo — Installation (macOS)          ║"
echo "  ║         Ihr digitales Sekretariat            ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""

# ── Zielordner festlegen ─────────────────────────────────────
echo "  📂 Wo soll Cleo installiert werden?"
echo "     [Enter] für Standard: ~/Cleo"
echo ""
read -p "  Verzeichnis: " USER_DIR
USER_DIR="${USER_DIR:-$HOME/Cleo}"
# Tilde expandieren
USER_DIR="${USER_DIR/#\~/$HOME}"
TARGET_DIR="$USER_DIR"
echo ""
echo "  ✔ Installationsordner: $TARGET_DIR"
echo ""

# ── Bestehenden Ordner prüfen ────────────────────────────────
if [ -d "$TARGET_DIR" ]; then
  echo "  ⚠️  Der Ordner existiert bereits."
  read -p "  Überschreiben? (j/n): " CONFIRM
  echo ""
  if [[ "$CONFIRM" != "j" && "$CONFIRM" != "J" ]]; then
    echo "  ❌ Installation abgebrochen."
    rm -rf "$TMP_DIR"
    exit 1
  fi
  rm -rf "$TARGET_DIR"
fi

# ── Claude Desktop prüfen ────────────────────────────────────
CLAUDE_INSTALLED=false
if [ -d "/Applications/Claude.app" ] || [ -d "$HOME/Applications/Claude.app" ]; then
  CLAUDE_INSTALLED=true
  echo "  ✔ Claude Desktop ist installiert."
else
  echo "  ⚠️  Claude Desktop nicht gefunden."
  echo "  → Bitte jetzt installieren: https://claude.ai/download"
  echo ""
  echo "  Nach der Installation dieses Skript erneut ausführen"
  echo "  oder mit Enter fortfahren, wenn Claude bereits läuft."
  read -p "  Enter drücken zum Fortfahren... " _
  echo ""
fi

# ── Quelle ermitteln ─────────────────────────────────────────
ZIP_FILE="$TMP_DIR/cleo.zip"
SOURCE_USED=""

# Prio 1: Explizit per Umgebungsvariable
if [ -n "${CLEO_ZIP:-}" ] && [ -f "$CLEO_ZIP" ]; then
  cp "$CLEO_ZIP" "$ZIP_FILE"
  SOURCE_USED="Lokale Datei: $CLEO_ZIP"

# Prio 2: Cleo.zip neben dem Skript oder in ~/Downloads
else
  for name in "Cleo.zip" "cleo.zip" "Cleo-main.zip" "cleo-main.zip"; do
    for search_dir in "$SCRIPT_DIR" "$HOME/Downloads" "$HOME/Desktop"; do
      if [ -f "$search_dir/$name" ]; then
        cp "$search_dir/$name" "$ZIP_FILE"
        SOURCE_USED="Lokale Datei: $search_dir/$name"
        break 2
      fi
    done
  done
fi

# Prio 3: GitHub (öffentlich — funktioniert wenn Repo public ist)
if [ -z "$SOURCE_USED" ]; then
  echo "  ⬇️  Lade Cleo von GitHub herunter..."
  if curl -fsSL --max-time 30 "$REPO_URL" -o "$ZIP_FILE" 2>/dev/null; then
    # Prüfen ob wir wirklich eine ZIP bekommen haben (nicht eine HTML-Fehlerseite)
    if file "$ZIP_FILE" | grep -q "Zip archive"; then
      SOURCE_USED="GitHub (öffentlich)"
    else
      rm -f "$ZIP_FILE"
    fi
  fi
fi

# Prio 4: GitHub mit Token
if [ -z "$SOURCE_USED" ] && [ -n "${GH_TOKEN:-}" ]; then
  echo "  ⬇️  Lade Cleo von GitHub herunter (mit Token)..."
  if curl -fsSL --max-time 60 -H "Authorization: token $GH_TOKEN" "$REPO_URL" -o "$ZIP_FILE"; then
    if file "$ZIP_FILE" | grep -q "Zip archive"; then
      SOURCE_USED="GitHub (Token)"
    else
      rm -f "$ZIP_FILE"
      echo "  ❌ Token ungültig oder kein Zugriff auf das Repository."
    fi
  fi
fi

# Keine Quelle gefunden
if [ -z "$SOURCE_USED" ]; then
  echo ""
  echo "  ❌ Keine Installationsquelle gefunden."
  echo ""
  echo "  Optionen:"
  echo "  1. Lege 'Cleo.zip' neben dieses Skript, in ~/Downloads oder ~/Desktop"
  echo "     → Datei erhältlich bei Able & Baker GmbH"
  echo ""
  echo "  2. GitHub-Token mitgeben:"
  echo "     GH_TOKEN=ghp_... bash install_mac.sh"
  echo ""
  rm -rf "$TMP_DIR"
  exit 1
fi

echo "  ✔ Quelle: $SOURCE_USED"
echo ""

# ── Entpacken ────────────────────────────────────────────────
echo "  📦 Entpacke..."
unzip -q "$ZIP_FILE" -d "$TMP_DIR"

# cleo/-Unterordner finden
EXTRACTED=$(find "$TMP_DIR" -maxdepth 3 -type d -name "cleo" | head -1)

if [ -z "$EXTRACTED" ]; then
  echo "  ❌ Fehler: cleo/-Unterordner nicht in der ZIP gefunden."
  echo "     Bitte eine gültige Cleo.zip von Able & Baker anfordern."
  rm -rf "$TMP_DIR"
  exit 1
fi

# ── Installieren ─────────────────────────────────────────────
mkdir -p "$TARGET_DIR"
cp -r "$EXTRACTED"/. "$TARGET_DIR/"
rm -rf "$TMP_DIR"

echo "  ✔ Dateien installiert."
echo ""

# ── Fertig ───────────────────────────────────────────────────
echo "  ╔══════════════════════════════════════════════════════╗"
echo "  ║  ✅  Cleo wurde erfolgreich installiert!             ║"
echo "  ╠══════════════════════════════════════════════════════╣"
echo "  ║                                                      ║"
printf  "  ║  Speicherort: %-38s║\n" "$TARGET_DIR"
echo "  ║                                                      ║"
echo "  ║  Nächste Schritte:                                   ║"
echo "  ║  1. Claude Desktop öffnen                            ║"
printf  "  ║  2. Ordner öffnen: %-34s║\n" "$TARGET_DIR"
echo "  ║  3. Cleo-Installation starten                        ║"
echo "  ║     (Claude tippt automatisch die Anleitung)         ║"
echo "  ║                                                      ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo ""

# Ordner in Finder öffnen
open "$TARGET_DIR" 2>/dev/null || true
