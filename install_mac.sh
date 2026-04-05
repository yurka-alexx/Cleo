#!/bin/bash
# ============================================================
#  Cleo — Installer für macOS
#  Lädt alle Dateien von GitHub und legt den Cleo-Ordner an.
# ============================================================

set -e

REPO_URL="https://github.com/yurka-alexx/Cleo/archive/refs/heads/main.zip"
TARGET_DIR="$HOME/Cleo"
TMP_DIR="$(mktemp -d)"
ZIP_FILE="$TMP_DIR/cleo.zip"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║       Cleo — Installation (macOS)    ║"
echo "╚══════════════════════════════════════╝"
echo ""

# 1 — Zielordner prüfen
if [ -d "$TARGET_DIR" ]; then
  echo "⚠️  Der Ordner '$TARGET_DIR' existiert bereits."
  read -p "   Überschreiben? (j/n): " CONFIRM
  if [[ "$CONFIRM" != "j" && "$CONFIRM" != "J" ]]; then
    echo "❌ Installation abgebrochen."
    exit 1
  fi
  rm -rf "$TARGET_DIR"
fi

# 2 — Herunterladen
echo "⬇️  Lade Cleo von GitHub herunter..."
curl -fsSL "$REPO_URL" -o "$ZIP_FILE"
echo "✅ Download abgeschlossen."

# 3 — Entpacken
echo "📦 Entpacke..."
unzip -q "$ZIP_FILE" -d "$TMP_DIR"

# 4 — Cleo-Unterordner finden und kopieren
EXTRACTED=$(find "$TMP_DIR" -maxdepth 2 -type d -name "cleo" | head -1)

if [ -z "$EXTRACTED" ]; then
  echo "❌ Fehler: cleo/-Unterordner nicht gefunden. Bitte GitHub-Repo prüfen."
  rm -rf "$TMP_DIR"
  exit 1
fi

mkdir -p "$TARGET_DIR"
cp -r "$EXTRACTED"/. "$TARGET_DIR/"
echo "✅ Dateien nach '$TARGET_DIR' kopiert."

# 5 — Temporäre Dateien aufräumen
rm -rf "$TMP_DIR"

# 6 — Ergebnis
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✅  Cleo wurde erfolgreich installiert!                 ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                                                          ║"
echo "║  Speicherort:  ~/Cleo                                   ║"
echo "║                                                          ║"
echo "║  Nächste Schritte:                                       ║"
echo "║  1. Claude Desktop öffnen                               ║"
echo "║  2. Ordner ~/Cleo als Arbeitsordner auswählen           ║"
echo "║  3. Cleo-Installation starten                           ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
