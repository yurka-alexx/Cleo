# ============================================================
#  IMAP-SMTP-MCP Installer — Windows (PowerShell)
#  Version: 2.0  |  Able & Baker GmbH
#
#  Verwendung:
#    .\install_windows.ps1
#    (ohne Argumente — vollständig interaktiv)
#
#  Bei Execution Policy Fehler (einmalig als Admin):
#    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#
#  Credentials werden NICHT in server.py gespeichert,
#  sondern sicher in der Claude Desktop Config hinterlegt.
# ============================================================

$ErrorActionPreference = "Stop"

function ok($msg)   { Write-Host "  ✅  $msg" -ForegroundColor Green }
function info($msg) { Write-Host "  ℹ️   $msg" -ForegroundColor Cyan }
function warn($msg) { Write-Host "  ⚠️   $msg" -ForegroundColor Yellow }
function step($msg) { Write-Host "`n── $msg" -ForegroundColor White }
function fail($msg) { Write-Host "`n  ❌  $msg" -ForegroundColor Red; exit 1 }

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir  = "$env:USERPROFILE\mcp-servers\imap-smtp"
$ConfigFile = "$env:APPDATA\Claude\claude_desktop_config.json"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   IMAP-SMTP-MCP Installer — Windows        v2.0 ║" -ForegroundColor Green
Write-Host "║   Able & Baker GmbH                              ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# ── Schritt 1: Zugangsdaten abfragen ────────────────────────
step "Schritt 1: Zugangsdaten"
Write-Host ""
$ImapHost      = Read-Host "  IMAP-Server    (z.B. mail.example.com)"
$SmtpHostInput = Read-Host "  SMTP-Server    [Enter = gleich wie IMAP]"
$SmtpHost      = if ($SmtpHostInput) { $SmtpHostInput } else { $ImapHost }
$ImapPortInput = Read-Host "  IMAP-Port      [993]"
$ImapPort      = if ($ImapPortInput) { [int]$ImapPortInput } else { 993 }
$SmtpPortInput = Read-Host "  SMTP-Port      [587]"
$SmtpPort      = if ($SmtpPortInput) { [int]$SmtpPortInput } else { 587 }
Write-Host ""
$MailUser      = Read-Host "  E-Mail-Adresse"
$MailPassword  = Read-Host "  Passwort" -AsSecureString
$MailPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($MailPassword))

info "Host: $ImapHost"
info "SMTP: $SmtpHost"
info "User: $MailUser"

# ── Schritt 2: Python prüfen ────────────────────────────────
step "Schritt 2: Python prüfen"
$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "3\.(1[0-9]|[2-9]\d)") { $python = $cmd; break }
    } catch {}
}
if (-not $python) {
    warn "Kein Python >= 3.10 gefunden."
    info "Installation: https://www.python.org/downloads/"
    info "Oder uv: powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`""
    fail "Python >= 3.10 wird benötigt."
}
ok "Python: $python"

# ── Schritt 3: uv prüfen / installieren ─────────────────────
step "Schritt 3: uv prüfen"
$uvPath = $null
try { $uvPath = (Get-Command uv -ErrorAction Stop).Source } catch {}
if (-not $uvPath) {
    warn "uv nicht gefunden — wird installiert..."
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
    try { $uvPath = (Get-Command uv -ErrorAction Stop).Source } catch {
        $uvPath = "$env:USERPROFILE\.local\bin\uv.exe"
    }
}
if (-not $uvPath -or -not (Test-Path $uvPath)) { fail "uv nicht gefunden. Manuell: https://docs.astral.sh/uv/" }
ok "uv: $uvPath"

# ── Schritt 4: IMAP-Verbindung testen + Ordner ermitteln ────
step "Schritt 4: IMAP-Verbindung testen & Ordner erkennen"

$folderScript = @"
import imaplib, ssl, json
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode    = ssl.CERT_NONE
try:
    imap = imaplib.IMAP4_SSL('$ImapHost', $ImapPort, ssl_context=ctx)
    imap.login('$MailUser', '$MailPasswordPlain')
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

$folderJson = & $python -c $folderScript 2>&1 | Out-String
try {
    $folders = $folderJson.Trim() | ConvertFrom-Json
    if ($folders.error) { fail "IMAP-Verbindung fehlgeschlagen: $($folders.error)" }
    $FolderDrafts  = $folders.drafts
    $FolderTrash   = $folders.trash
    $FolderArchive = $folders.archive
    ok "Verbindung erfolgreich"
    info "Entwürfe   : $FolderDrafts"
    info "Papierkorb : $FolderTrash"
    info "Archiv     : $FolderArchive"
} catch {
    warn "Ordner konnten nicht erkannt werden — Standardwerte werden verwendet."
    $FolderDrafts  = "Drafts"
    $FolderTrash   = "Trash"
    $FolderArchive = "Archive"
}

# ── Schritt 5: server.py kopieren ───────────────────────────
step "Schritt 5: server.py installieren"
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

$serverSrc = Join-Path $ScriptDir "server.py"
if (-not (Test-Path $serverSrc)) {
    fail "server.py nicht gefunden in $ScriptDir`nBitte das gesamte imap-smtp-mcp-Verzeichnis herunterladen."
}
Copy-Item $serverSrc "$TargetDir\server.py" -Force
ok "server.py → $TargetDir\server.py"

# ── Schritt 6: Claude Desktop Config schreiben ──────────────
step "Schritt 6: Claude Desktop Config konfigurieren"
$configDir = Split-Path $ConfigFile
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

# Backup
if (Test-Path $ConfigFile) {
    Copy-Item $ConfigFile "$ConfigFile.backup" -Force
    info "Backup: $ConfigFile.backup"
}

$newEntry = [PSCustomObject]@{
    command = $uvPath
    args    = @("run", "--script", "$TargetDir\server.py")
    env     = [PSCustomObject]@{
        IMAP_HOST      = $ImapHost
        SMTP_HOST      = $SmtpHost
        MAIL_USER      = $MailUser
        MAIL_PASSWORD  = $MailPasswordPlain
        IMAP_PORT      = "$ImapPort"
        SMTP_PORT      = "$SmtpPort"
        FOLDER_DRAFTS  = $FolderDrafts
        FOLDER_TRASH   = $FolderTrash
        FOLDER_ARCHIVE = $FolderArchive
    }
}

$config = [PSCustomObject]@{ mcpServers = [PSCustomObject]@{} }
if (Test-Path $ConfigFile) {
    try {
        $raw = Get-Content $ConfigFile -Raw
        $config = $raw | ConvertFrom-Json
        if (-not $config.PSObject.Properties["mcpServers"]) {
            $config | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue ([PSCustomObject]@{}) -Force
        }
    } catch { warn "Bestehende Config konnte nicht gelesen werden — neue wird erstellt." }
}

$config.mcpServers | Add-Member -NotePropertyName "imap-smtp" -NotePropertyValue $newEntry -Force
$config | ConvertTo-Json -Depth 10 | Set-Content $ConfigFile -Encoding UTF8
ok "Claude Desktop Config gespeichert"

# ── Fertig ────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅  Installation abgeschlossen!                ║" -ForegroundColor Green
Write-Host "║                                                  ║" -ForegroundColor Green
Write-Host "║   → Claude Desktop neu starten                  ║" -ForegroundColor Green
Write-Host "║     (Taskleiste → Rechtsklick → Beenden)        ║" -ForegroundColor Green
Write-Host "║   → Dann: 'zeig mir die letzten Mails' testen   ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  ℹ️   Credentials wurden sicher in der Claude Config gespeichert." -ForegroundColor Cyan
Write-Host "  ℹ️   server.py enthält KEINE Passwörter." -ForegroundColor Cyan
Write-Host ""
