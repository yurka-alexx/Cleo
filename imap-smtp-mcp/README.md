# IMAP-SMTP-MCP

Gibt Claude direkten Zugriff auf ein E-Mail-Postfach via IMAP/SMTP — ohne Umwege über Gmail-API oder n8n. Funktioniert mit jedem Standard-Mailserver.

---

## Was du danach kannst

Claude kennt dein Postfach und kann direkt:

| Tool | Was es tut |
|---|---|
| `fetch_recent_mails` | Letzte N Stunden aus einem Ordner laden |
| `search_mails` | Suche nach Absender, Betreff, ungelesen, Zeitraum |
| `get_mail` | Einzelne Mail per UID laden |
| `create_draft` | Entwurf im Entwürfe-Ordner anlegen |
| `send_mail` | Mail versenden (SMTP, STARTTLS) |
| `archive_mail` | Mail ins Archiv verschieben |
| `delete_mail` | Mail löschen (Papierkorb oder permanent) |
| `mark_mail` | Als gelesen / ungelesen / markiert setzen |

---

## Voraussetzungen

- macOS 12+ oder Windows 10/11
- [Claude Desktop](https://claude.ai/download) installiert
- IMAP/SMTP-Zugangsdaten deines Postfachs (Host, E-Mail, Passwort)
- Internetzugang (für uv + Python 3.12, einmalig ~80 MB)

---

## Installation

### macOS — ein Befehl, fertig

```bash
bash <(curl -sL https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_mac.sh)
```

Das Skript fragt interaktiv nach Host, E-Mail und Passwort.

**Oder mit Parametern** (für automatisiertes Rollout beim Kunden):

```bash
bash <(curl -sL https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_mac.sh) \
  --host "mail.example.com" \
  --user "info@example.com" \
  --password "GeheimesPasswort" \
  --imap-port 993 \
  --smtp-port 587
```

---

### Windows — PowerShell

```powershell
# Einmalig als Admin (falls noch nicht geschehen):
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Installation starten:
irm https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_windows.ps1 | iex
```

**Oder mit Parametern:**

```powershell
$s = irm https://raw.githubusercontent.com/yurka-alexx/Second-Brain-OS/main/imap-smtp-mcp/install_windows.ps1
& ([scriptblock]::Create($s)) -Host "mail.example.com" -User "info@example.com" -Password "GeheimesPasswort"
```

---

## Was das Skript im Hintergrund tut

1. **uv prüfen / installieren** — falls nicht vorhanden, wird uv automatisch heruntergeladen
2. **Ordner anlegen** — `~/mcp-servers/imap-smtp/`
3. **IMAP-Verbindung testen** — Zugangsdaten werden sofort geprüft, bevor irgendetwas gespeichert wird
4. **Ordnernamen ermitteln** — Entwürfe, Papierkorb und Archiv werden automatisch erkannt (auch bei deutschen Namen wie „Entwürfe" oder „Papierkorb")
5. **server.py generieren** — vorkonfiguriert mit deinen Daten und korrekten Ordnernamen
6. **claude_desktop_config.json patchen** — bestehende Einträge bleiben erhalten, `imap-smtp` wird ergänzt
7. **JSON validieren** — vor dem Speichern wird die Config auf Fehler geprüft

**Nach der Installation:** Claude Desktop neu starten — die 8 Tools stehen sofort zur Verfügung.

---

## Kompatibilität

| Anbieter | Status |
|---|---|
| kasserver.com | ✅ getestet |
| Strato / IONOS | ✅ Standard-IMAP, sollte funktionieren |
| Gmail | ⚠️ IMAP in Gmail-Einstellungen aktivieren + App-Passwort erstellen |
| Office 365 / Exchange | ⚠️ IMAP muss vom Admin aktiviert sein |
| Postfix / Dovecot (Self-hosted) | ✅ Standard-Ports 993/587 |

---

## Sicherheitshinweis

Das generierte `server.py` enthält das Passwort im Klartext unter `~/mcp-servers/imap-smtp/server.py`.
Nach der Installation empfohlen:

```bash
chmod 600 ~/mcp-servers/imap-smtp/server.py
```

---

## Troubleshooting

| Fehler | Ursache | Lösung |
|---|---|---|
| `AUTHENTICATIONFAILED` | Falsches Passwort | Passwort prüfen — kein Leerzeichen, kein abgeschnittenes Sonderzeichen |
| `No solution found … Python>=3.10` | System-Python zu alt | Skript nutzt `--python 3.12`, uv lädt Python automatisch |
| `Failed to spawn process` | Claude findet uv nicht | Absoluten uv-Pfad prüfen: `which uv` — Skript trägt ihn automatisch ein |
| `[TRYCREATE] Mailbox doesn't exist` | Falscher Ordnername | Skript erkennt Ordner automatisch — Schritt 4 nochmal ausführen |
| MCP-Tool nicht verfügbar | Claude nicht neu gestartet | Claude vollständig beenden (⌘Q) und neu öffnen |
| Config zurückgesetzt | Ungültiges JSON | Skript validiert JSON vor dem Speichern — bei manuellem Eingriff: `python3 -m json.tool config.json` |
