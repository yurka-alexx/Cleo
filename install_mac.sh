#!/bin/bash
# ============================================================
#  Cleo — Installer für macOS
#
#  Variante A (empfohlen): Skript + Cleo.zip im selben Ordner ablegen,
#  dann ausführen. Kein Internet-Zugang nötig.
#
#  Variante B: GitHub-Token als Umgebungsvariable setzen:
#  GH_TOKEN=ghp_xxx bash install_mac.sh
#
#  Bezugsquelle Cleo.zip: Erhalte die Datei von deinem
#  Installationspartner (Able & Baker GmbH).
# ============================================================

set -e

TARGET_DIR="$HOME/Cleo"
REPO_URL="https://github.com/yurka-alexx/Cleo/archive/refs/heads/main.zip"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
ZIP_FILE="$TMP_DIR/cleo.zip"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║       Cleo — Installation (macOS)    ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── Zielordner prüfen ────────────────────────────────────────
if [ -d "$TARGET_DIR" ]; then
  echo "⚠️  Der Ordner '$TARGET_DIR' existiert bereits."
  read -p "   Überschreiben? (j/n): " CONFIRM
  if [[ "$CONFIRM" != "j" && "$CONFIRM" != "J" ]]; then
    echo "❌ Installation abgebrochen."
    rm -rf "$TMP_DIR"
    exit 1
  fi
  rm -rf "$TARGET_DIR"
fi

# ── Quelle ermitteln ─────────────────────────────────────────
LOCAL_ZIP=""

# Prüfen ob Cleo.zip neben dem Skript liegt
for name in "Cleo.zip" "cleo.zip" "Cleo-main.zip" "cleo-main.zip"; do
  if [ -f "$SCRIPT_DIR/$name" ]; then
    LOCAL_ZIP="$SCRIPT_DIR/$name"
    echo "📦 Lokale Datei gefunden: $LOCAL_ZIP"
    break
  fi
done

# Prüfen ob Cleo.zip im Downloads-Ordner liegt
if [ -z "$LOCAL_ZIP" ]; then
  for name in "Cleo.zip" "cleo.zip" "Cleo-main.zip" "cleo-main.zip"; do
    if [ -f "$HOME/Downloads/$name" ]; then
      LOCAL_ZIP="$HOME/Downloads/$name"
      echo "📦 Lokale Datei gefunden: $LOCAL_ZIP"
      break
    fi
  done
fi

if [ -n "$LOCAL_ZIP" ]; then
  # Variante A — lokale Datei
  cp "$LOCAL_ZIP" "$ZIP_FILE"
  echo "✅ Lokale Datei wird verwendet."

elif [ -n "$GH_TOKEN" ]; then
  # Variante B — GitHub mit Token
  echo "⬇️  Lade Cleo von GitHub herunter (mit Token)..."
  if ! curl -fsSL -H "Authorization: token $GH_TOKEN" "$REPO_URL" -o "$ZIP_FILE"; then
    echo "❌ Download fehlgeschlagen. Token prüfen oder lokale Cleo.zip verwenden."
    rm -rf "$TMP_DIR"
    exit 1
  fi
  echo "✅ Download abgeschlossen."

else
  echo ""
  echo "❌ Keine Installationsquelle gefunden."
  echo ""
  echo "   Optionen:"
  echo "   1. Lege 'Cleo.zip' neben dieses Skript oder in ~/Downloads"
  echo "      → Datei erhältlich bei Able & Baker GmbH"
  echo ""
  echo "   2. Führe das Skript mit GitHub-Token aus:"
  echo "      GH_TOKEN=ghp_... bash install_mac.sh"
  echo ""
  rm -rf "$TMP_DIR"
  exit 1
fi

# ── Entpacken ────────────────────────────────────────────────
echo "📦 Entpacke..."
unzip -q "$ZIP_FILE" -d "$TMP_DIR"

# cleo/-Unterordner finden (lokal oder aus GitHub-ZIP-Struktur)
EXTRACTED=$(find "$TMP_DIR" -maxdepth 3 -type d -name "cleo" | head -1)

if [ -z "$EXTRACTED" ]; then
  echo "❌ Fehler: cleo/-Unterordner nicht in der ZIP-Datei gefunden."
  echo "   Bitte eine gültige Cleo.zip von deinem Installationspartner anfordern."
  rm -rf "$TMP_DIR"
  exit 1
fi

# ── Installieren ─────────────────────────────────────────────
mkdir -p "$TARGET_DIR"
cp -r "$EXTRACTED"/. "$TARGET_DIR/"
echo "✅ Dateien nach '$TARGET_DIR' kopiert."

# ── Aufräumen ────────────────────────────────────────────────
rm -rf "$TMP_DIR"

# ── Fertig ───────────────────────────────────────────────────
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
