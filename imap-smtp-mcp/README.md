# IMAP-SMTP-MCP

Gibt Claude direkten Zugriff auf ein E-Mail-Postfach via IMAP/SMTP.
Kompatibel mit jedem Standard-Mailserver (kasserver, Gmail IMAP, Strato, IONOS, etc.)

## Features

8 Tools direkt in Claude verfügbar:

| Tool | Funktion |
|---|---|
| `fetch_recent_mails` | Letzte N Stunden aus einem Ordner laden |
| `search_mails` | Suche nach Absender, Betreff, ungelesen, Zeitraum |
| `get_mail` | Einzelne Mail per UID vollständig laden |
| `create_draft` | Entwurf in Entwürfe-Ordner anlegen |
| `send_mail` | Mail versenden via SMTP (STARTTLS) |
| `archive_mail` | Mail ins Archiv verschieben |
| `delete_mail` | Mail löschen (Papierkorb oder permanent) |
| `mark_mail` | Mail als gelesen/ungelesen/markiert setzen |

---

## Installation

### macOS

```bash
bash <(curl -sL https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_mac.sh)
```

Oder mit Parametern (für unbeaufsichtigte Installation):

```bash
curl -sL https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_mac.sh | bash -s -- \
  --host "mail.example.com" \
  --user "user@example.com" \
  --password "GeheimesPasswort"
```

### Windows (PowerShell)

```powershell
# Execution Policy setzen (einmalig, als Admin):
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Installieren:
irm https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_windows.ps1 | iex
```

Oder mit Parametern:

```powershell
$script = irm https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_windows.ps1
& ([scriptblock]::Create($script)) -Host "mail.example.com" -User "user@example.com" -Password "GeheimesPasswort"
```

---

## Was das Skript automatisch erledigt

1. `uv` installieren (falls nicht vorhanden)
2. Ordner `~/mcp-servers/imap-smtp/` anlegen
3. IMAP-Verbindung testen & Ordnernamen ermitteln (Entwürfe/Papierkorb/Archiv)
4. `server.py` mit Credentials und korrekten Ordnernamen generieren
5. `claude_desktop_config.json` sicher patchen (bestehende Einträge bleiben erhalten)
6. JSON validieren

**Nach der Installation:** Claude Desktop neu starten — fertig.

---

## Voraussetzungen

- macOS 12+ oder Windows 10/11
- Claude Desktop (claude.ai/download)
- Internetzugang (für uv + Python 3.12, einmalig ~80MB)
- IMAP/SMTP-Zugangsdaten des Postfachs

---

## Sicherheitshinweis

Das generierte `server.py` enthält das Passwort im Klartext unter `~/mcp-servers/imap-smtp/server.py`.
Zugriffsrechte nach der Installation einschränken:

```bash
chmod 600 ~/mcp-servers/imap-smtp/server.py
```

---

## Kompatibilität getestet

| Anbieter | Status |
|---|---|
| kasserver.com | ✅ getestet |
| Gmail (IMAP aktiviert) | ⚠️ App-Passwort erforderlich |
| Strato / IONOS | ✅ sollte funktionieren |
| Exchange / Office 365 | ⚠️ IMAP muss aktiviert sein |
