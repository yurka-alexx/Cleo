# Cleo

Automatisierungsinfrastruktur für Claude — Installationspakete, MCP-Server und Workflow-Tools von Able & Baker.

Jedes Paket ist in einem Befehl installierbar. Keine manuellen Konfigurationsschritte.

---

## Pakete

### [`imap-smtp-mcp/`](./imap-smtp-mcp/)

Gibt Claude direkten Zugriff auf ein E-Mail-Postfach via IMAP/SMTP.

**macOS:**
```bash
bash <(curl -sL https://raw.githubusercontent.com/yurka-alexx/Cleo/main/install_mac.sh)
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/yurka-alexx/Cleo/main/install_windows.ps1 | iex
```

---

### WhatsApp-Kanal (Claude Code Plugin)

Verbindet Claude als Cleo direkt mit WhatsApp — per Linked-Device-Protokoll. Cleo empfängt Nachrichten, transkribiert Sprachnachrichten (via OpenAI Whisper API) und antwortet eigenständig.

**Voraussetzungen:** Claude Code CLI, Bun, OpenAI API Key

Vollständige Einrichtung: [cleo/DOKUMENTATION.md → Phase 11–13](./cleo/DOKUMENTATION.md#8-installationsflow-phasen-013)

---

## Lizenz

Internes Tooling — Able & Baker GmbH
