# ============================================================
#  IMAP-SMTP-MCP Installer — Windows (PowerShell)
#  Version: 1.0  |  Able & Baker GmbH
#
#  Verwendung:
#    .\install_windows.ps1 `
#      -Host    "mail.example.com" `
#      -User    "user@example.com" `
#      -Password "MeinPasswort" `
#      [-ImapPort 993] `
#      [-SmtpPort 587]
#
#  Als Admin-PowerShell starten falls Execution Policy Fehler:
#    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# ============================================================

param(
    [string]$Host      = "",
    [string]$User      = "",
    [string]$Password  = "",
    [int]   $ImapPort  = 993,
    [int]   $SmtpPort  = 587
)

# ── Farben / Ausgabe-Hilfsfunktionen ────────────────────────
function ok($msg)   { Write-Host "✅ $msg" -ForegroundColor Green }
function info($msg) { Write-Host "ℹ️  $msg" -ForegroundColor Cyan }
function warn($msg) { Write-Host "⚠️  $msg" -ForegroundColor Yellow }
function step($msg) { Write-Host "`n── $msg ──────────────────────────────────" -ForegroundColor White }
function fail($msg) { Write-Host "❌ $msg" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   IMAP-SMTP-MCP Installer — Windows      ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Green

# ── Interaktive Eingabe falls Parameter fehlen ───────────────
if (-not $Host)     { $Host     = Read-Host "IMAP/SMTP-Host (z.B. mail.example.com)" }
if (-not $User)     { $User     = Read-Host "E-Mail-Adresse / Benutzername" }
if (-not $Password) { $Password = Read-Host "Passwort" -AsSecureString | ForEach-Object { [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($_)) } }

$SmtpHost  = $Host
$TargetDir = "$env:USERPROFILE\mcp-servers\imap-smtp"
$ConfigFile = "$env:APPDATA\Claude\claude_desktop_config.json"

info "Host:     $Host"
info "User:     $User"
info "Zielort:  $TargetDir"

# ── Schritt 1: Python prüfen ────────────────────────────────
step "Schritt 1: Python prüfen"
$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "3\.(1[0-9]|[2-9]\d)") {
            $python = $cmd; break
        }
    } catch {}
}
if (-not $python) {
    warn "Kein Python >= 3.10 gefunden."
    info "Bitte Python 3.12 installieren: https://www.python.org/downloads/"
    info "Oder uv installieren (empfohlen): powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`""
    fail "Installation abgebrochen — Python >= 3.10 benötigt."
}
ok "Python gefunden: $python"

# ── Schritt 2: uv prüfen / installieren ─────────────────────
step "Schritt 2: uv prüfen"
$uvPath = $null
try { $uvPath = (Get-Command uv -ErrorAction Stop).Source } catch {}
if (-not $uvPath) {
    warn "uv nicht gefunden — wird installiert..."
    try {
        powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
        # PATH aktualisieren
        $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
        $uvPath = "$env:USERPROFILE\.local\bin\uv.exe"
        if (-not (Test-Path $uvPath)) { $uvPath = (Get-Command uv -ErrorAction SilentlyContinue).Source }
    } catch {
        fail "uv Installation fehlgeschlagen. Manuell installieren: https://docs.astral.sh/uv/"
    }
}
ok "uv gefunden: $uvPath"

# ── Schritt 3: IMAP-Verbindung testen + Ordner ermitteln ────
step "Schritt 3: IMAP-Verbindung testen & Ordnernamen ermitteln"

$folderScript = @"
import imaplib, ssl, json, sys
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode    = ssl.CERT_NONE
try:
    imap = imaplib.IMAP4_SSL('$Host', $ImapPort, ssl_context=ctx)
    imap.login('$User', '$Password')
    _, raw_folders = imap.list()
    imap.logout()
    result = {'drafts': 'Drafts', 'trash': 'Trash', 'archive': 'Archive'}
    for f in raw_folders:
        line = f.decode()
        if r'\Drafts'  in line: result['drafts']  = line.split('"/"')[-1].strip().strip('"')
        if r'\Trash'   in line: result['trash']   = line.split('"/"')[-1].strip().strip('"')
        if r'\Archive' in line: result['archive'] = line.split('"/"')[-1].strip().strip('"')
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({'error': str(e), 'drafts': 'Drafts', 'trash': 'Trash', 'archive': 'Archive'}))
"@

$folderJson = & $python -c $folderScript 2>&1
try {
    $folders = $folderJson | ConvertFrom-Json
    $folderDrafts  = $folders.drafts
    $folderTrash   = $folders.trash
    $folderArchive = $folders.archive
    ok "Verbindung erfolgreich"
    info "Entwürfe : $folderDrafts"
    info "Papierkorb: $folderTrash"
    info "Archiv    : $folderArchive"
} catch {
    warn "Ordnernamen konnten nicht automatisch ermittelt werden — Standardwerte werden verwendet."
    $folderDrafts  = "Drafts"
    $folderTrash   = "Trash"
    $folderArchive = "Archive"
}

# ── Schritt 4: server.py generieren ─────────────────────────
step "Schritt 4: server.py generieren"
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

$serverPy = @"
#!/usr/bin/env python3
# /// script
# dependencies = ["mcp[cli]"]
# ///
"""
IMAP/SMTP MCP Server
Host: $Host
User: $User
Generated by install_windows.ps1
"""

import imaplib, smtplib, ssl, email, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime, timedelta, timezone
from mcp.server.fastmcp import FastMCP

IMAP_HOST     = "$Host"
IMAP_PORT     = $ImapPort
SMTP_HOST     = "$SmtpHost"
SMTP_PORT     = $SmtpPort
MAIL_USER     = "$User"
MAIL_PASSWORD = "$Password"

FOLDER_INBOX   = "INBOX"
FOLDER_DRAFTS  = "$folderDrafts"
FOLDER_TRASH   = "$folderTrash"
FOLDER_ARCHIVE = "$folderArchive"

mcp = FastMCP("imap-smtp")

def _imap_connect():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    conn.login(MAIL_USER, MAIL_PASSWORD)
    return conn

def _decode_header_str(raw):
    if raw is None: return ""
    parts = decode_header(raw)
    return " ".join(p.decode(c or "utf-8", errors="replace") if isinstance(p, bytes) else str(p) for p, c in parts)

def _parse_message(raw_bytes):
    msg = email.message_from_bytes(raw_bytes)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(part.get_content_charset() or "utf-8", errors="replace"); break
    else:
        payload = msg.get_payload(decode=True)
        if payload: body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
    return {"from": _decode_header_str(msg.get("From")), "to": _decode_header_str(msg.get("To")),
            "subject": _decode_header_str(msg.get("Subject")), "date": msg.get("Date",""), "body": body[:4000]}

@mcp.tool()
def fetch_recent_mails(folder: str = "INBOX", hours: int = 24) -> str:
    """Fetch mails received in the last N hours."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        since = (datetime.utcnow() - timedelta(hours=hours)).strftime("%d-%b-%Y")
        _, data = conn.search(None, f'(SINCE "{since}")')
        results = []
        for uid in data[0].split()[-50:]:
            _, raw = conn.fetch(uid, "(RFC822)")
            if raw and raw[0]:
                parsed = _parse_message(raw[0][1]); parsed["uid"] = uid.decode(); results.append(parsed)
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally: conn.logout()

@mcp.tool()
def search_mails(folder: str = "INBOX", from_addr: str = "", subject: str = "",
                 unread_only: bool = False, since_days: int = 30) -> str:
    """Search mails by sender, subject, unread flag, and date range."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        criteria = [f'SINCE "{(datetime.utcnow() - timedelta(days=since_days)).strftime("%d-%b-%Y")}"']
        if from_addr: criteria.append(f'FROM "{from_addr}"')
        if subject:   criteria.append(f'SUBJECT "{subject}"')
        if unread_only: criteria.append("UNSEEN")
        _, data = conn.search(None, "(" + " ".join(criteria) + ")")
        results = []
        for uid in data[0].split()[-50:]:
            _, raw = conn.fetch(uid, "(RFC822)")
            if raw and raw[0]:
                parsed = _parse_message(raw[0][1]); parsed["uid"] = uid.decode(); results.append(parsed)
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally: conn.logout()

@mcp.tool()
def get_mail(uid: str, folder: str = "INBOX") -> str:
    """Fetch a single mail by UID."""
    conn = _imap_connect()
    try:
        conn.select(folder, readonly=True)
        _, raw = conn.fetch(uid.encode(), "(RFC822)")
        if not raw or not raw[0]: return json.dumps({"error": "Mail not found"})
        parsed = _parse_message(raw[0][1]); parsed["uid"] = uid
        return json.dumps(parsed, ensure_ascii=False, indent=2)
    finally: conn.logout()

@mcp.tool()
def create_draft(to: str, subject: str, text: str, cc: str = "") -> str:
    """Create a draft email in the Drafts folder."""
    conn = _imap_connect()
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = MAIL_USER; msg["To"] = to; msg["Subject"] = subject
        if cc: msg["Cc"] = cc
        msg.attach(MIMEText(text, "plain", "utf-8"))
        result = conn.append(FOLDER_DRAFTS, "", imaplib.Time2Internaldate(datetime.now(tz=timezone.utc)), msg.as_bytes())
        return json.dumps({"status": "ok", "result": str(result)})
    finally: conn.logout()

@mcp.tool()
def send_mail(to: str, subject: str, text: str, cc: str = "") -> str:
    """Send an email via SMTP."""
    msg = MIMEMultipart("alternative")
    msg["From"] = MAIL_USER; msg["To"] = to; msg["Subject"] = subject
    if cc: msg["Cc"] = cc
    msg.attach(MIMEText(text, "plain", "utf-8"))
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo(); smtp.starttls(context=ctx); smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(MAIL_USER, [to]+([cc] if cc else []), msg.as_string())
    return json.dumps({"status": "sent", "to": to, "subject": subject})

@mcp.tool()
def archive_mail(uid: str, folder: str = "INBOX") -> str:
    """Move a mail to the Archive folder."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        result = conn.copy(uid.encode(), FOLDER_ARCHIVE)
        if result[0] == "OK":
            conn.store(uid.encode(), "+FLAGS", "\\Deleted"); conn.expunge()
            return json.dumps({"status": "archived", "uid": uid})
        return json.dumps({"status": "error", "detail": str(result)})
    finally: conn.logout()

@mcp.tool()
def delete_mail(uid: str, folder: str = "INBOX", permanent: bool = False) -> str:
    """Delete a mail (permanent=False → Trash, permanent=True → direct delete)."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        if permanent:
            conn.store(uid.encode(), "+FLAGS", "\\Deleted"); conn.expunge()
            return json.dumps({"status": "deleted_permanently", "uid": uid})
        result = conn.copy(uid.encode(), FOLDER_TRASH)
        if result[0] == "OK":
            conn.store(uid.encode(), "+FLAGS", "\\Deleted"); conn.expunge()
            return json.dumps({"status": "moved_to_trash", "uid": uid})
        return json.dumps({"status": "error", "detail": str(result)})
    finally: conn.logout()

@mcp.tool()
def mark_mail(uid: str, action: str, folder: str = "INBOX") -> str:
    """Mark a mail. action: read, unread, flag, unflag."""
    conn = _imap_connect()
    try:
        conn.select(folder)
        action_map = {"read": ("+FLAGS","\\Seen"),"unread": ("-FLAGS","\\Seen"),
                      "flag": ("+FLAGS","\\Flagged"),"unflag": ("-FLAGS","\\Flagged")}
        if action not in action_map: return json.dumps({"error": f"Unknown action: {action}"})
        op, flag = action_map[action]; conn.store(uid.encode(), op, flag)
        return json.dumps({"status": "ok", "uid": uid, "action": action})
    finally: conn.logout()

if __name__ == "__main__":
    mcp.run()
"@

$serverPy | Set-Content -Path "$TargetDir\server.py" -Encoding UTF8
ok "server.py geschrieben: $TargetDir\server.py"

# ── Schritt 5: claude_desktop_config.json patchen ───────────
step "Schritt 5: Claude Desktop Config patchen"

$configDir = Split-Path $ConfigFile
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

$newEntry = @{
    command = $uvPath
    args    = @("run", "--python", "3.12", "--with", "mcp[cli]", "$TargetDir\server.py")
}

if (Test-Path $ConfigFile) {
    $current = Get-Content $ConfigFile -Raw | ConvertFrom-Json
    if (-not $current.mcpServers) {
        $current | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue ([PSCustomObject]@{}) -Force
    }
    $current.mcpServers | Add-Member -NotePropertyName "imap-smtp" -NotePropertyValue $newEntry -Force
    $current | ConvertTo-Json -Depth 10 | Set-Content $ConfigFile -Encoding UTF8
    ok "imap-smtp zur bestehenden Config hinzugefügt"
} else {
    $newConfig = @{ mcpServers = @{ "imap-smtp" = $newEntry } }
    $newConfig | ConvertTo-Json -Depth 10 | Set-Content $ConfigFile -Encoding UTF8
    ok "Neue Config erstellt"
}

# ── Fertig ────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   Installation abgeschlossen! ✅          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
info "Nächster Schritt: Claude Desktop neu starten (Taskleiste → Rechtsklick → Beenden → neu öffnen)"
info "Dann: Cowork öffnen und 'zeig mir die letzten Mails' testen"
Write-Host ""
warn "Sicherheitshinweis: server.py enthält das Passwort im Klartext."
warn "Dateiberechtigungen einschränken empfohlen."
