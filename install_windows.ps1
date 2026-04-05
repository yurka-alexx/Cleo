# ============================================================
#  Cleo - Installer fuer Windows
#  Schritt 1 von 2: Dateien herunterladen und entpacken
#
#  Ausfuehren: Rechtsklick -> Mit PowerShell ausfuehren
#  Optionen:
#    $env:GH_TOKEN="ghp_..."; .\install_windows.ps1   (privates Repo)
#    $env:CLEO_ZIP="C:\Pfad\Cleo.zip"; .\install_windows.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$RepoOwner = "yurka-alexx"
$RepoName  = "Cleo"
$Branch    = "main"
$RepoUrl   = "https://github.com/$RepoOwner/$RepoName/archive/refs/heads/$Branch.zip"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TmpDir    = Join-Path $env:TEMP ("cleo_install_" + [System.IO.Path]::GetRandomFileName())
$ZipFile   = Join-Path $TmpDir "cleo.zip"

New-Item -ItemType Directory -Path $TmpDir -Force | Out-Null

# -- Banner --------------------------------------------------
Clear-Host
Write-Host ""
Write-Host "  +--------------------------------------------------+"
Write-Host "  |       Cleo - Installation (Windows)              |"
Write-Host "  |       Ihr digitales Sekretariat                  |"
Write-Host "  +--------------------------------------------------+"
Write-Host ""

# -- Zielordner festlegen ------------------------------------
Write-Host "  Wo soll Cleo installiert werden?"
Write-Host "  [Enter] fuer Standard: $env:USERPROFILE\Cleo"
Write-Host ""
$UserDir = Read-Host "  Verzeichnis"
if ([string]::IsNullOrWhiteSpace($UserDir)) {
    $UserDir = Join-Path $env:USERPROFILE "Cleo"
}
$TargetDir = $UserDir
Write-Host ""
Write-Host "  OK: Installationsordner: $TargetDir"
Write-Host ""

# -- Bestehenden Ordner pruefen ------------------------------
if (Test-Path $TargetDir) {
    Write-Host "  WARNUNG: Der Ordner existiert bereits."
    $Confirm = Read-Host "  Ueberschreiben? (j/n)"
    Write-Host ""
    if ($Confirm -notmatch "^[jJ]$") {
        Write-Host "  Abgebrochen."
        Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue
        exit 1
    }
    Remove-Item -Recurse -Force $TargetDir
}

# -- Claude Desktop pruefen ----------------------------------
$ClaudeInstalled = Test-Path "$env:LOCALAPPDATA\Programs\Claude\Claude.exe"
if (-not $ClaudeInstalled) {
    $ClaudeInstalled = Test-Path "$env:ProgramFiles\Claude\Claude.exe"
}
if ($ClaudeInstalled) {
    Write-Host "  OK: Claude Desktop ist installiert."
} else {
    Write-Host "  HINWEIS: Claude Desktop nicht gefunden."
    Write-Host "  -> Bitte jetzt installieren: https://claude.ai/download"
    Write-Host ""
    Write-Host "  Skript laeuft weiter - Claude Desktop vor Schritt 3 installieren."
    Write-Host ""
    Read-Host "  Enter druecken zum Fortfahren"
    Write-Host ""
}

# -- Quelle ermitteln ----------------------------------------
$SourceUsed = ""

# Prio 1: Umgebungsvariable
if ($env:CLEO_ZIP -and (Test-Path $env:CLEO_ZIP)) {
    Copy-Item $env:CLEO_ZIP $ZipFile
    $SourceUsed = "Lokale Datei: $env:CLEO_ZIP"
}

# Prio 2: Cleo.zip lokal suchen
if (-not $SourceUsed) {
    $ZipNames = @("Cleo.zip","cleo.zip","Cleo-main.zip","cleo-main.zip")
    $SearchDirs = @($ScriptDir, "$env:USERPROFILE\Downloads", "$env:USERPROFILE\Desktop")
    foreach ($dir in $SearchDirs) {
        foreach ($name in $ZipNames) {
            $candidate = Join-Path $dir $name
            if (Test-Path $candidate) {
                Copy-Item $candidate $ZipFile
                $SourceUsed = "Lokale Datei: $candidate"
                break
            }
        }
        if ($SourceUsed) { break }
    }
}

# Prio 3: GitHub oeffentlich
if (-not $SourceUsed) {
    Write-Host "  Lade Cleo von GitHub herunter..."
    try {
        $wc = New-Object System.Net.WebClient
        $wc.DownloadFile($RepoUrl, $ZipFile)
        # Pruefen ob echte ZIP (PK-Header)
        $bytes = [System.IO.File]::ReadAllBytes($ZipFile)
        if ($bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4B) {
            $SourceUsed = "GitHub (oeffentlich)"
        } else {
            Remove-Item $ZipFile -ErrorAction SilentlyContinue
        }
    } catch {
        Remove-Item $ZipFile -ErrorAction SilentlyContinue
    }
}

# Prio 4: GitHub mit Token
if (-not $SourceUsed -and $env:GH_TOKEN) {
    Write-Host "  Lade Cleo von GitHub herunter (mit Token)..."
    try {
        $headers = @{ Authorization = "token $env:GH_TOKEN" }
        Invoke-WebRequest -Uri $RepoUrl -Headers $headers -OutFile $ZipFile
        $bytes = [System.IO.File]::ReadAllBytes($ZipFile)
        if ($bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4B) {
            $SourceUsed = "GitHub (Token)"
        } else {
            Remove-Item $ZipFile -ErrorAction SilentlyContinue
            Write-Host "  FEHLER: Token ungueltig oder kein Zugriff."
        }
    } catch {
        Remove-Item $ZipFile -ErrorAction SilentlyContinue
    }
}

if (-not $SourceUsed) {
    Write-Host ""
    Write-Host "  FEHLER: Keine Installationsquelle gefunden."
    Write-Host ""
    Write-Host "  Optionen:"
    Write-Host "  1. Lege Cleo.zip neben dieses Skript, in Downloads oder Desktop"
    Write-Host "     Datei erhaeltlich bei Able & Baker GmbH"
    Write-Host ""
    Write-Host "  2. GitHub-Token mitgeben:"
    Write-Host "     > `$env:GH_TOKEN='ghp_...'; .\install_windows.ps1"
    Write-Host ""
    Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "  OK: Quelle: $SourceUsed"
Write-Host ""

# -- Entpacken -----------------------------------------------
Write-Host "  Entpacke..."
Expand-Archive -Path $ZipFile -DestinationPath $TmpDir -Force

# cleo/-Unterordner finden
$Extracted = Get-ChildItem -Path $TmpDir -Recurse -Directory -Filter "cleo" |
             Where-Object { $_.FullName -notlike "*\.git*" } |
             Select-Object -First 1

if (-not $Extracted) {
    Write-Host "  FEHLER: cleo/-Unterordner nicht in der ZIP gefunden."
    Write-Host "  Bitte eine gueltige Cleo.zip von Able & Baker anfordern."
    Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue
    exit 1
}

# -- Installieren --------------------------------------------
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
Copy-Item -Path (Join-Path $Extracted.FullName "*") -Destination $TargetDir -Recurse -Force
Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue

Write-Host "  OK: Dateien installiert."
Write-Host ""

# -- Fertig --------------------------------------------------
Write-Host "  +--------------------------------------------------+"
Write-Host "  |  FERTIG: Cleo wurde erfolgreich installiert!     |"
Write-Host "  +--------------------------------------------------+"
Write-Host "  |                                                  |"
Write-Host "  |  Speicherort: $TargetDir"
Write-Host "  |                                                  |"
Write-Host "  |  Naechste Schritte:                              |"
Write-Host "  |  1. Claude Desktop oeffnen                       |"
Write-Host "  |  2. Ordner oeffnen: $TargetDir"
Write-Host "  |  3. Cleo-Installation starten                    |"
Write-Host "  |     (Claude tippt automatisch die Anleitung)     |"
Write-Host "  |                                                  |"
Write-Host "  +--------------------------------------------------+"
Write-Host ""

# Ordner im Explorer oeffnen
Start-Process explorer.exe $TargetDir -ErrorAction SilentlyContinue

Read-Host "  Enter druecken zum Schliessen"
