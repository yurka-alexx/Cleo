# ============================================================
#  Cleo — Installer für Windows (PowerShell)
#  Lädt alle Dateien von GitHub und legt den Cleo-Ordner an.
#
#  Ausführen: Rechtsklick → "Mit PowerShell ausführen"
#  Oder im Terminal: powershell -ExecutionPolicy Bypass -File install_windows.ps1
# ============================================================

$ErrorActionPreference = "Stop"

$RepoUrl   = "https://github.com/yurka-alexx/Cleo/archive/refs/heads/main.zip"
$TargetDir = "$env:USERPROFILE\Cleo"
$TmpDir    = "$env:TEMP\cleo_install_$(Get-Random)"
$ZipFile   = "$TmpDir\cleo.zip"

Write-Host ""
Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Cleo — Installation (Windows)    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1 — Zielordner prüfen
if (Test-Path $TargetDir) {
    Write-Host "⚠️  Der Ordner '$TargetDir' existiert bereits." -ForegroundColor Yellow
    $confirm = Read-Host "   Überschreiben? (j/n)"
    if ($confirm -ne "j" -and $confirm -ne "J") {
        Write-Host "❌ Installation abgebrochen." -ForegroundColor Red
        exit 1
    }
    Remove-Item -Recurse -Force $TargetDir
}

# 2 — Temp-Ordner anlegen
New-Item -ItemType Directory -Path $TmpDir | Out-Null

# 3 — Herunterladen
Write-Host "⬇️  Lade Cleo von GitHub herunter..."
try {
    Invoke-WebRequest -Uri $RepoUrl -OutFile $ZipFile -UseBasicParsing
} catch {
    Write-Host "❌ Download fehlgeschlagen. Bitte Internetverbindung prüfen." -ForegroundColor Red
    Remove-Item -Recurse -Force $TmpDir
    exit 1
}
Write-Host "✅ Download abgeschlossen."

# 4 — Entpacken
Write-Host "📦 Entpacke..."
Expand-Archive -Path $ZipFile -DestinationPath $TmpDir -Force

# 5 — cleo/-Unterordner finden
$CleoSubfolder = Get-ChildItem -Path $TmpDir -Recurse -Directory -Filter "cleo" | Select-Object -First 1

if (-not $CleoSubfolder) {
    Write-Host "❌ Fehler: cleo/-Unterordner nicht gefunden. Bitte GitHub-Repo prüfen." -ForegroundColor Red
    Remove-Item -Recurse -Force $TmpDir
    exit 1
}

# 6 — Kopieren
New-Item -ItemType Directory -Path $TargetDir | Out-Null
Copy-Item -Path "$($CleoSubfolder.FullName)\*" -Destination $TargetDir -Recurse
Write-Host "✅ Dateien nach '$TargetDir' kopiert."

# 7 — Temp-Ordner aufräumen
Remove-Item -Recurse -Force $TmpDir

# 8 — Ergebnis
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅  Cleo wurde erfolgreich installiert!                 ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║  Speicherort: $env:USERPROFILE\Cleo" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║  Nächste Schritte:                                       ║" -ForegroundColor Green
Write-Host "║  1. Claude Desktop öffnen                               ║" -ForegroundColor Green
Write-Host "║  2. Ordner Cleo als Arbeitsordner auswählen             ║" -ForegroundColor Green
Write-Host "║  3. Cleo-Installation starten                           ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Read-Host "Drücke Enter zum Beenden"
