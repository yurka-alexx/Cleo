# ============================================================
#  Cleo — Installer für Windows (PowerShell)
#
#  Variante A (empfohlen): Skript + Cleo.zip im selben Ordner ablegen,
#  dann ausführen. Kein Internet-Zugang nötig.
#
#  Variante B: GitHub-Token als Umgebungsvariable setzen:
#  $env:GH_TOKEN = "ghp_xxx"; .\install_windows.ps1
#
#  Bezugsquelle Cleo.zip: Erhalte die Datei von deinem
#  Installationspartner (Able & Baker GmbH).
#
#  Ausführen: Rechtsklick → "Mit PowerShell ausführen"
#  Oder: powershell -ExecutionPolicy Bypass -File install_windows.ps1
# ============================================================

$ErrorActionPreference = "Stop"

$RepoUrl   = "https://github.com/yurka-alexx/Cleo/archive/refs/heads/main.zip"
$TargetDir = "$env:USERPROFILE\Cleo"
$TmpDir    = "$env:TEMP\cleo_install_$(Get-Random)"
$ZipFile   = "$TmpDir\cleo.zip"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Cleo — Installation (Windows)    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Zielordner prüfen ────────────────────────────────────────
if (Test-Path $TargetDir) {
    Write-Host "⚠️  Der Ordner '$TargetDir' existiert bereits." -ForegroundColor Yellow
    $confirm = Read-Host "   Überschreiben? (j/n)"
    if ($confirm -ne "j" -and $confirm -ne "J") {
        Write-Host "❌ Installation abgebrochen." -ForegroundColor Red
        exit 1
    }
    Remove-Item -Recurse -Force $TargetDir
}

New-Item -ItemType Directory -Path $TmpDir | Out-Null

# ── Quelle ermitteln ─────────────────────────────────────────
$LocalZip = $null
$ZipNames = @("Cleo.zip", "cleo.zip", "Cleo-main.zip", "cleo-main.zip")

# Neben dem Skript suchen
foreach ($name in $ZipNames) {
    $candidate = Join-Path $ScriptDir $name
    if (Test-Path $candidate) {
        $LocalZip = $candidate
        Write-Host "📦 Lokale Datei gefunden: $LocalZip"
        break
    }
}

# Im Downloads-Ordner suchen
if (-not $LocalZip) {
    foreach ($name in $ZipNames) {
        $candidate = Join-Path "$env:USERPROFILE\Downloads" $name
        if (Test-Path $candidate) {
            $LocalZip = $candidate
            Write-Host "📦 Lokale Datei gefunden: $LocalZip"
            break
        }
    }
}

if ($LocalZip) {
    # Variante A — lokale Datei
    Copy-Item $LocalZip $ZipFile
    Write-Host "✅ Lokale Datei wird verwendet."

} elseif ($env:GH_TOKEN) {
    # Variante B — GitHub mit Token
    Write-Host "⬇️  Lade Cleo von GitHub herunter (mit Token)..."
    $headers = @{ Authorization = "token $env:GH_TOKEN" }
    try {
        Invoke-WebRequest -Uri $RepoUrl -OutFile $ZipFile -Headers $headers -UseBasicParsing
        Write-Host "✅ Download abgeschlossen."
    } catch {
        Write-Host "❌ Download fehlgeschlagen. Token prüfen oder lokale Cleo.zip verwenden." -ForegroundColor Red
        Remove-Item -Recurse -Force $TmpDir
        exit 1
    }

} else {
    Write-Host ""
    Write-Host "❌ Keine Installationsquelle gefunden." -ForegroundColor Red
    Write-Host ""
    Write-Host "   Optionen:"
    Write-Host "   1. Lege 'Cleo.zip' neben dieses Skript oder in Downloads"
    Write-Host "      → Datei erhältlich bei Able & Baker GmbH"
    Write-Host ""
    Write-Host "   2. Führe das Skript mit GitHub-Token aus:"
    Write-Host "      `$env:GH_TOKEN = 'ghp_...'; .\install_windows.ps1"
    Write-Host ""
    Remove-Item -Recurse -Force $TmpDir
    Read-Host "Drücke Enter zum Beenden"
    exit 1
}

# ── Entpacken ────────────────────────────────────────────────
Write-Host "📦 Entpacke..."
Expand-Archive -Path $ZipFile -DestinationPath $TmpDir -Force

# cleo/-Unterordner finden
$CleoSubfolder = Get-ChildItem -Path $TmpDir -Recurse -Directory -Filter "cleo" | Select-Object -First 1

if (-not $CleoSubfolder) {
    Write-Host "❌ Fehler: cleo/-Unterordner nicht in der ZIP-Datei gefunden." -ForegroundColor Red
    Write-Host "   Bitte eine gültige Cleo.zip von deinem Installationspartner anfordern."
    Remove-Item -Recurse -Force $TmpDir
    Read-Host "Drücke Enter zum Beenden"
    exit 1
}

# ── Installieren ─────────────────────────────────────────────
New-Item -ItemType Directory -Path $TargetDir | Out-Null
Copy-Item -Path "$($CleoSubfolder.FullName)\*" -Destination $TargetDir -Recurse
Write-Host "✅ Dateien nach '$TargetDir' kopiert."

# ── Aufräumen ────────────────────────────────────────────────
Remove-Item -Recurse -Force $TmpDir

# ── Fertig ───────────────────────────────────────────────────
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
