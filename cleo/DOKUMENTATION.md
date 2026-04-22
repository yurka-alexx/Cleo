# Cleo — Produktdokumentation

> Letzte Aktualisierung: April 2026
> Version: 1.4.0
> Installationspartner: Able & Baker GmbH · Yuri A. Bilogor

---

## Inhaltsverzeichnis

1. [Was ist Cleo?](#1-was-ist-cleo)
2. [Architektur & technische Grundlage](#2-architektur--technische-grundlage)
3. [Voraussetzungen](#3-voraussetzungen)
4. [Module im Detail](#4-module-im-detail)
   - 4.1 [Inbox-Review](#41-inbox-review)
   - 4.2 [Meeting-Review](#42-meeting-review)
   - 4.3 [Physischer Briefversand (OB24)](#43-physischer-briefversand-ob24)
   - 4.4 [CRM-Sync](#44-crm-sync)
   - 4.5 [KI-Rechtsassistent](#45-firmenanwalt)
   - 4.6 [WhatsApp-Kanal](#46-whatsapp-kanal)
5. [Autonomie-Level](#5-autonomie-level)
6. [Konfigurationsvariablen](#6-konfigurationsvariablen)
7. [MCP-Integrationen](#7-mcp-integrationen)
8. [Installationsflow (Phasen 0–13)](#8-installationsflow-phasen-013)
9. [Ordnerstruktur nach Installation](#9-ordnerstruktur-nach-installation)
10. [Tägliche Nutzung](#10-tägliche-nutzung)
11. [Troubleshooting](#11-troubleshooting)
12. [BAFA-Förderung](#12-bafa-förderung)
13. [Changelog](#13-changelog)

---

## 1. Was ist Cleo?

Cleo ist ein vollständig vorkonfiguriertes KI-Arbeitsplatzsystem, das auf **Claude Desktop (Cowork-Modus)** läuft und als digitales Sekretariat für kleine und mittlere Unternehmen fungiert.

Der Nutzer spricht mit dem System in normaler Sprache — keine Programmierkenntnisse, keine Befehle. Das System übernimmt:

- **E-Mail-Triage**: Klassifizieren, archivieren, Entwürfe erstellen, Spam erkennen, Briefe vorschlagen
- **Meeting-Nachbereitung**: Kalender + Pocket-Transkripte auswerten, To-Dos anlegen, Kunden informieren
- **Physischer Briefversand**: Briefe per API an OB24 übergeben — digital versenden, physisch ankommen
- **CRM**: Kontakte automatisch aus dem Postfach aufbauen und pflegen
- **Juristische Recherche**: KI-gestützter Recherche- und Verwaltungsassistent für Rechtsfragen (kein Rechtsanwalt-Ersatz)
- **WhatsApp-Kanal**: Cleo ist per WhatsApp erreichbar — Sprachnachrichten, Textnachrichten, Bilder

### Kernversprechen

| Kennzahl | Wert |
|---|---|
| Durchschnittliche tägliche Zeitersparnis | ~2 Stunden |
| Monatliche Betriebskosten | 30–55 EUR |
| Einrichtungszeit | ca. 2–4 Stunden (vollständig geführt) |
| Technische Vorkenntnisse erforderlich | Keine |

---

## 2. Architektur & technische Grundlage

Cleo ist kein eigenständiges Softwareprodukt, sondern ein **Konfigurationssystem** für Claude Desktop. Es besteht aus:

```
┌─────────────────────────────────────────────────────┐
│                   Claude Desktop                     │
│          (Anthropic Claude, Cowork-Modus)            │
├─────────────────────────────────────────────────────┤
│   Cowork-Ordner des Kunden                           │
│   ├── Sekretariat/CLAUDE.md  ←  Identität + CRM     │
│   ├── Sekretariat/MEMORY.md  ←  Sitzungsgedächtnis  │
│   └── Sekretariat/skills/    ←  Skill-Dateien       │
├─────────────────────────────────────────────────────┤
│   MCP-Server (Model Context Protocol)                │
│   ├── imap-smtp / Gmail / Outlook  ←  E-Mail        │
│   ├── Google Calendar / Outlook    ←  Kalender      │
│   ├── Pocket AI                    ←  Transkripte   │
│   ├── Notion / Markdown            ←  Aufgaben      │
│   └── OB24 (via Bash/curl)         ←  Briefe        │
├─────────────────────────────────────────────────────┤
│   Claude Code CLI (optional, für WhatsApp)           │
│   ├── WhatsApp-Plugin (Linked Device)               │
│   └── imap-smtp MCP (in Claude Code registriert)    │
└─────────────────────────────────────────────────────┘
```

### Skill-Dateien (SKILL.md)

Jedes Modul ist als `SKILL.md`-Datei im Cowork-Ordner des Kunden gespeichert. Diese Dateien enthalten:

- **Konfigurationsvariablen** oben im Header (einmal während der Installation gesetzt)
- **Ablaufanweisungen** für Claude (welche Tools aufzurufen sind, in welcher Reihenfolge)
- **Entscheidungslogik** (z.B. Autonomie-Level-Auswertung)

### Gedächtnissystem

- **CLAUDE.md**: Dauerhafte Konfiguration, Firmendaten, Mini-CRM, Rollenidentität des Assistenten
- **MEMORY.md**: Sitzungsübergreifendes Gedächtnis — wird nur auf explizite Nutzeranweisung beschrieben
- **cleo-memory.md** (WhatsApp): Langzeitgedächtnis für den WhatsApp-Kanal — sessionübergreifend

---

## 3. Voraussetzungen

### Hardware

| Gerät | Empfehlung | Preis (ca.) | Pflicht? |
|---|---|---|---|
| Mac Mini M4 | 16 GB RAM, 256 GB SSD | 699 EUR | Empfohlen |
| Alternativ | Beliebiger macOS- oder Windows-PC | — | Ja |
| Monitor | 24" Full HD | 180 EUR | Optional |
| Maus & Tastatur | Beliebig | 50 EUR | Für Setup |
| Pocket AI Gerät | Clip-Pendant oder Smartphone-App | 0–69 EUR | Für Meeting-Review |

### Software & Accounts (vor Installation anlegen)

| Dienst | Zweck | Kosten/Monat | Pflicht? |
|---|---|---|---|
| [Claude Desktop](https://claude.ai/download) | Cowork-Modus (KI-Engine) | 20–25 EUR | ✅ Pflicht |
| [Claude Code CLI](https://claude.ai/download) | WhatsApp-Kanal | kostenlos | Für WhatsApp |
| [Bun](https://bun.sh) | JavaScript-Runtime für WhatsApp-Plugin | kostenlos | Für WhatsApp |
| OpenAI API Key | Sprachtranskription via Whisper API | ~0–2 EUR/Monat | Für WhatsApp |
| [Pocket AI](https://pocket.ai) | Gesprächsaufzeichnung + Transkript | ~10 EUR | Für Meeting-Review |
| [OnlineBrief24](https://www.onlinebrief24.de) | Physischer Briefversand per API | ~1,20–2,50 EUR/Brief | Optional |
| Google Workspace / Gmail | E-Mail + Kalender | 6 EUR/User | Falls Gmail |
| Notion | Aufgaben-Datenbank | 10–15 EUR | Optional |

> ⚠️ **OB24-Konto**: Muss **vor der Installation** angelegt werden. Registrierung unter [onlinebrief24.de](https://www.onlinebrief24.de) (kostenlos, Pay-per-use).

> ⚠️ **RAM-Hinweis für WhatsApp**: Auf Macs mit 16 GB RAM keine lokale Whisper-Installation verwenden. Stattdessen OpenAI Whisper API nutzen (kein lokaler RAM-Verbrauch).

### Netzwerk & Berechtigungen

- Claude Desktop benötigt Internetzugang (HTTPS)
- IMAP/SMTP: Port 993 (IMAP) und 587 (SMTP) müssen offen sein
- Für Gmail/Google Workspace: OAuth-Verbindung in Claude Desktop → Connectors

---

## 4. Module im Detail

### 4.1 Inbox-Review

**Datei:** `Sekretariat/skills/inbox-review/SKILL.md`

**Funktion:** Scannt den E-Mail-Posteingang, klassifiziert jede Mail und erstellt Antwort-Entwürfe oder Brief-Vorschläge.

#### Ablauf

1. **Entwurfs-Cleanup** (Schritt 0): Entwürfe älter als 30 Tage werden in den Papierkorb verschoben (nie permanent gelöscht)
2. **Posteingang laden**: Mails der letzten `INBOX_REVIEW_HOURS` Stunden (Standard: 24h) + ältere ungelesene Mails
3. **Klassifizierung** (jede Mail):

| Symbol | Kategorie | Wann | Aktion |
|---|---|---|---|
| 🚫 | SPAM | Eindeutige Spam-Merkmale, unbekannte Domain, Phishing | → Papierkorb |
| 🗑️ | PAPIERKORB | Werbung, Newsletter, System-Benachrichtigungen | → Papierkorb |
| 📁 | ARCHIVIEREN | Info-Mail, erledigt, kein Handlungsbedarf | → Archiv |
| ✅ | ANTWORTEN | Direkte Frage, Anfrage, Kundenkommunikation | → Entwurf |
| ✉️ | BRIEF | Formelles Schreiben nötig | → Brief-Vorschlag |
| 📂 | VERSCHIEBEN | Gehört in Unterordner | → Ordner-Logik |
| 👀 | BEOBACHTEN | Relevant, kein sofortiger Handlungsbedarf | → Markieren |

4. **Entwürfe erstellen** (✅ ANTWORTEN): Ton professionell, im Stil der Firma
5. **Brief-Vorschläge** (✉️ BRIEF): Briefinhalt vorbereiten, Nutzer bestätigt → OB24-Versand
6. **Zusammenfassung**: Tabelle aller bearbeiteten Mails
7. **Mini-CRM automatisch aktualisieren**: Neue Absender eintragen, bestehende aktualisieren

#### Konfigurationsvariablen

| Variable | Beschreibung | Beispielwert |
|---|---|---|
| `EMAIL_SYSTEM` | E-Mail-System | `imap-smtp` / `gmail` / `office365` |
| `INBOX_REVIEW_HOURS` | Zeitfenster für Review | `24` |
| `INBOX_REVIEW_SCHEDULE` | Zeitplan | `täglich 08:00` |
| `SUMMARY_CHANNEL` | Wohin die Zusammenfassung geht | `email:` / `slack:` / `none` |
| `AUTONOMOUS_ACTIONS` | Autonomie-Level | `1` / `2` / `3` |

---

### 4.2 Meeting-Review

**Datei:** `Sekretariat/skills/meeting-review/SKILL.md`

**Funktion:** Vollautomatische Tages-Nachbereitung aller Meetings und Gespräche.

#### Ablauf

1. Kalendertermine laden (Google Calendar / Outlook)
2. Pocket-Tagestranskripte laden (00:00–23:59 Uhr)
3. Matching: Pocket-Gespräch → Kalendertermin
4. Zusammenfassung je Gesprächstyp
5. To-Dos anlegen (bei Level 3)
6. E-Mail-Entwürfe erstellen (bei Level 2+)
7. Mini-CRM automatisch aktualisieren

---

### 4.3 Physischer Briefversand (OB24)

**Datei:** `Sekretariat/skills/physischen-brief-versenden/SKILL.md`

**Funktion:** Erstellt ein Brief-PDF nach DIN 5008 und versendet es via OnlineBrief24-API.

#### Ablauf

1. Briefdaten erfassen (Empfänger, Betreff, Text)
2. Brief-PDF generieren via `build_brief.py`
3. Preis abfragen (OB24-API) — immer vor Versand
4. Testmodus- oder Echtversand-Abfrage
5. Versand nach Bestätigung
6. Logging in `Postausgang/log.md`

---

### 4.4 CRM-Sync

**Datei:** `Sekretariat/skills/crm-sync/SKILL.md`

**Funktion:** Befüllt das Mini-CRM initial aus dem E-Mail-Postfach (180 Tage). Inbox-Review und Meeting-Review aktualisieren das CRM danach automatisch nach jedem Durchlauf.

---

### 4.5 KI-Rechtsassistent

**Datei:** `Team/Rechtsassistent/CLAUDE.md`

**Funktion:** KI-gestützter Recherche- und Verwaltungsassistent für rechtliche Themen.

> ⚠️ Kein Ersatz für einen zugelassenen Rechtsanwalt. Jede Antwort endet mit dem Hinweis zur anwaltlichen Abstimmung.

---

### 4.6 WhatsApp-Kanal

Cleo ist über WhatsApp per Linked-Device-Protokoll erreichbar — direkt auf der Kundennummer, ohne separate SIM oder zweite App.

#### Wie es funktioniert

Das WhatsApp-Plugin (Claude Code) verbindet sich als verknüpftes Gerät mit der bestehenden WhatsApp-Nummer. Eingehende Nachrichten werden an die Claude-Code-Session weitergeleitet, Cleo antwortet direkt.

#### Fähigkeiten

- **Textnachrichten**: Fragen beantworten, Aufgaben erledigen, Infos aus dem Cowork-Workspace liefern
- **Sprachnachrichten**: Automatische Transkription via OpenAI Whisper API (kein lokaler RAM-Verbrauch)
- **Bilder**: Fotos werden empfangen und direkt verarbeitet
- **Ausgehende Nachrichten**: Cleo kann proaktiv Nachrichten senden (z.B. an eine Liste von Kontakten)
- **E-Mail-Zugriff via WhatsApp**: Wenn imap-smtp in Claude Code registriert ist, kann Cleo den Posteingang auf Anfrage prüfen

#### Sicherheit & Zugriffskontrolle

- **Allowlist**: Nur vorher freigegebene Nummern erreichen Cleo
- **Neue Kontakte**: Werden via Pairing-Code zugefügt (Cleo sendet Code, Nutzer bestätigt)
- **Session-Persistenz**: Auth gespeichert in `~/.whatsapp-channel/.baileys_auth/` — Handy muss nicht eingeschaltet sein

#### Starten

```bash
claude --dangerously-skip-permissions --dangerously-load-development-channels plugin:whatsapp@whatsapp-claude-plugin
```

Nach dem Start einmalig `/whatsapp:status` eingeben, damit Cleo aktiv auf Nachrichten wartet.

#### Langzeitgedächtnis

Cleo liest beim Start jeder Session `~/.whatsapp-channel/cleo-memory.md` — persistente Erinnerungen über Sessions hinweg. Neue Einträge entstehen auf expliziten Wunsch des Nutzers.

---

## 5. Autonomie-Level

Das Autonomie-Level bestimmt, wie eigenständig Cleo in allen Modulen handelt.

| Level | Name | Was passiert automatisch |
|---|---|---|
| **Level 1** | Beobachter | Nur analysieren und zusammenfassen — alle Aktionen werden vorgeschlagen |
| **Level 2** | Assistent | Level 1 + automatisch E-Mail-Entwürfe erstellen |
| **Level 3** | Autopilot | Level 2 + Kalendertermine anlegen, To-Dos anlegen, Benachrichtigungskontakt informieren |

---

## 6. Konfigurationsvariablen

### Sekretariat/CLAUDE.md (global)

| Variable | Beschreibung |
|---|---|
| `FIRMENNAME` | Vollständiger Firmenname |
| `RECHTSFORM` | GmbH / GmbH & Co. KG / AG / Einzelunternehmen etc. |
| `BRANCHE` | Branche des Unternehmens |
| `HAUPTSTANDORT` | Stadt |
| `EMAIL_SYSTEM` | `imap-smtp` / `gmail` / `office365` |
| `EMAIL_ADDRESS` | E-Mail-Adresse des Unternehmens |
| `ASSISTENT_NAME` | Name des Assistenten (z.B. „Clara", „Max") |
| `ASSISTENT_GESCHLECHT` | `weiblich` / `männlich` / `neutral` |
| `BENACHRICHTIGUNGS_NAME` | Name des Benachrichtigungskontakts |
| `BENACHRICHTIGUNGS_EMAIL` | E-Mail des Benachrichtigungskontakts |

### ~/CLAUDE.md (WhatsApp-Kanal)

| Variable | Beschreibung |
|---|---|
| Assistenten-Name | Name der WhatsApp-Instanz (z.B. Cleo) |
| Workspace-Pfad | Absoluter Pfad zum Cowork-Ordner |
| Mini-CRM-Pfad | Absoluter Pfad zur MINI-CRM.md |
| Sprache | Antwortsprache (Standard: Sprache der eingehenden Nachricht) |
| Fähigkeiten | Welche MCPs und Tools Cleo nutzen darf |

---

## 7. MCP-Integrationen

### Claude Desktop (Cowork-Modus)

| MCP | Zweck | Installation |
|---|---|---|
| **imap-smtp-mcp** | Standard-E-Mail (IMAP/SMTP) | Installationsskript (Phase 1) |
| **Gmail-Connector** | Google Gmail / Workspace | Claude Desktop → Connectors |
| **Outlook-Connector** | Microsoft Office 365 | Claude Desktop → Connectors |
| **Google Calendar** | Kalenderintegration | Claude Desktop → Connectors |
| **Pocket AI** | Gesprächstranskripte | Claude Desktop → Connectors |
| **Notion** | Aufgaben-Datenbank | Claude Desktop → Connectors |
| **OB24** | Briefversand (via Bash/curl) | Keine MCP-Installation nötig |

### Claude Code CLI (WhatsApp-Kanal)

| MCP | Zweck | Installation |
|---|---|---|
| **WhatsApp-Plugin** | WhatsApp Linked Device | `claude --dangerously-load-development-channels plugin:whatsapp@whatsapp-claude-plugin` |
| **imap-smtp** | E-Mail-Zugriff via WhatsApp | `claude mcp add imap-smtp ...` (Phase 12) |

> **Hinweis:** Cloud-Konnektoren (Gmail, Calendar, Notion etc.) sind automatisch verfügbar, wenn der Nutzer in Claude Code mit demselben Account eingeloggt ist wie in Claude Desktop.

---

## 8. Installationsflow (Phasen 0–13)

Die vollständige Basis-Installation läuft über **einen einzigen Skill-Aufruf** in Claude Desktop:

> „Führe den Cleo Installationsflow aus."

Der WhatsApp-Kanal (Phasen 11–13) ist optional und wird im Anschluss eingerichtet.

### Basis-Installation (Phasen 0–10)

| Phase | Inhalt | Dauer |
|---|---|---|
| **0.1** | Betriebssystem & Claude Desktop prüfen | 5 Min |
| **0.2** | Kundendaten erfassen (Firma, Branche, Ansprechpartner) | 5 Min |
| **0.2.5** | Assistenz-Identität festlegen (Name + Geschlecht) | 2 Min |
| **0.3** | Benachrichtigungskontakt festlegen | 2 Min |
| **0.4** | Autonomie-Level festlegen (1/2/3) | 5 Min |
| **1** | E-Mail-System verbinden (IMAP/Gmail/Outlook) | 10–20 Min |
| **2** | Ordnerstruktur anlegen | 5 Min |
| **3** | Post-Requisiten: Logo + Signum hochladen, Firmendaten für Briefkopf | 10 Min |
| **4** | Inbox-Review einrichten (Zeitfenster, Zeitplan, Ordner-Logik) | 10 Min |
| **5** | Meeting-Review & Pocket AI (optional) | 15 Min |
| **5b** | IMAP-Ordner anlegen (Morgen-Briefings, Meeting-Zusammenfassungen) | 5 Min |
| **5c** | Autonomie-Variablen in alle Skills übertragen | 5 Min |
| **6** | CRM konfigurieren (externes CRM optional) | 10 Min |
| **7** | Physischen Briefversand einrichten (optional, OB24) | 15 Min |
| **8** | KI-Rechtsassistent einrichten (E-Mail-Scan 180 Tage) | 10 Min |
| **9** | Mini-CRM vorbefüllen (Top-50 Kontakte aus Postfach) | 10–20 Min |
| **10.1** | Installations-Checkliste abhaken | 5 Min |
| **10.2** | Funktionstest E-Mail & CRM | 10 Min |
| **10.3** | Funktionstest Brief-Layout & OB24 (Testmodus) | 10 Min |
| **10.4** | Funktionstest KI-Rechtsassistent | 5 Min |
| **10.5** | Scheduled Tasks anlegen (Inbox-Review + Meeting-Review) | 5 Min |
| **10.6** | Übergabenotiz UEBERGABE.md generieren | 5 Min |

### WhatsApp-Kanal (Phasen 11–13, optional)

| Phase | Inhalt | Dauer |
|---|---|---|
| **11.1** | Claude Code CLI prüfen / installieren | 5 Min |
| **11.2** | Bun installieren (`curl -fsSL https://bun.sh/install \| bash`) | 3 Min |
| **11.3** | WhatsApp-Plugin installieren und aktivieren | 5 Min |
| **11.4** | WhatsApp-Gerät koppeln (Pairing-Code auf dem Handy eingeben) | 5 Min |
| **11.5** | Allowlist einrichten — eigene Nummer zuerst | 3 Min |
| **11.6** | Whisper-Transkription einrichten (OpenAI API, kein lokales Modell) | 10 Min |
| **12.1** | imap-smtp in Claude Code registrieren (`claude mcp add imap-smtp ...`) | 5 Min |
| **13.1** | System-Prompt für WhatsApp-Cleo generieren (interaktiv) | 10 Min |
| **13.2** | `~/.whatsapp-channel/cleo-memory.md` anlegen | 2 Min |
| **13.3** | Funktionstest: Textnachricht + Sprachnachricht senden | 5 Min |

#### Phase 11.6 — Whisper-Transkription (OpenAI API)

```bash
# Python-Umgebung anlegen
uv venv ~/whisper-env --python 3.12
uv pip install mlx-whisper --python ~/whisper-env/bin/python3

# Transkriptions-Script erstellen
cat > ~/whisper-transcribe.sh << EOF
#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

OPENAI_API_KEY="sk-..."   # Hier echten Key eintragen

curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@$1" \
  -F model="whisper-1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text',''))"
EOF
chmod +x ~/whisper-transcribe.sh
```

#### Phase 13.1 — System-Prompt generieren

Der System-Prompt (`~/CLAUDE.md`) wird interaktiv generiert. Folgende Angaben werden abgefragt:

1. Name des Assistenten (z.B. Cleo, Clara, Max)
2. Firmenname und Branche
3. Absoluter Pfad zum Cowork-Ordner
4. Absoluter Pfad zur MINI-CRM.md
5. Sprache (Standard: Sprache der eingehenden Nachricht)
6. Fähigkeiten: welche externen Tools darf Cleo eigenständig nutzen?
7. Regel für externe Tools: immer erst fragen oder direkt handeln?

Ausgabe: fertige `~/CLAUDE.md` mit allen Einstellungen.

---

## 9. Ordnerstruktur nach Installation

```
[Cowork-Hauptordner]/
├── CLAUDE.md                           ← Globale Workspace-Konfiguration
├── MEMORY.md                           ← Sitzungsübergreifendes Gedächtnis
│
├── Sekretariat/
│   ├── CLAUDE.md                       ← Identität, Firmendaten, Mini-CRM
│   ├── MEMORY.md                       ← Sekretariats-Gedächtnis
│   ├── Post-Requisiten/
│   │   ├── logo.png
│   │   ├── signum_[name].png
│   │   └── build_brief.py
│   ├── Postausgang/
│   │   ├── log.md
│   │   └── fehler-log.md
│   └── skills/
│       ├── inbox-review/SKILL.md
│       ├── meeting-review/SKILL.md
│       ├── crm-sync/SKILL.md
│       └── physischen-brief-versenden/SKILL.md
│
└── Team/
    └── KI-Rechtsassistent/
        ├── CLAUDE.md
        ├── MEMORY.md
        └── Fallarchiv/

~/.whatsapp-channel/                    ← WhatsApp-Kanal (lokal auf dem Mac)
├── .baileys_auth/                      ← WhatsApp-Session (nicht löschen!)
├── .env                                ← Telefonnummer mit Ländervorwahl
├── cleo-memory.md                      ← Langzeitgedächtnis (sessionübergreifend)
└── inbox/                              ← Empfangene Fotos (automatisch)

~/CLAUDE.md                             ← System-Prompt für Claude Code / WhatsApp-Kanal
~/whisper-transcribe.sh                 ← Transkriptions-Script (OpenAI API)
~/whisper-env/                          ← Python-Umgebung (Fallback, falls lokal gebraucht)
```

---

## 10. Tägliche Nutzung

### Typischer Arbeitstag

**Morgens:**
```
„Geh durch meinen Posteingang."
→ Cleo klassifiziert Mails, erstellt Entwürfe, zeigt Brief-Vorschläge
```

**Nach Meetings:**
```
„Mach die Meeting-Nachbereitung."
→ Kalender + Pocket-Transkripte, Zusammenfassungen, To-Dos, Kunden-E-Mails
```

**Via WhatsApp (unterwegs):**
```
„Was sind meine Termine heute?" [Sprachnachricht]
→ Cleo transkribiert, liest Kalender, antwortet direkt auf WhatsApp
```

### WhatsApp starten

```bash
claude --dangerously-skip-permissions --dangerously-load-development-channels plugin:whatsapp@whatsapp-claude-plugin
```

Nach dem Start: `/whatsapp:status` eingeben → Cleo ist aktiv.

### Shortcuts / Trigger-Phrasen

| Aktion | Beispielaufruf |
|---|---|
| Inbox-Review | „Geh durch meine E-Mails" |
| Meeting-Nachbereitung | „Mach die Meeting-Nachbereitung" |
| Brief versenden | „Schreib einen Brief an [Name]" |
| CRM aktualisieren | „Sync das CRM" |
| WhatsApp-Cleo starten | Befehl oben im Terminal |

---

## 11. Troubleshooting

| Problem | Mögliche Ursache | Lösung |
|---|---|---|
| E-Mails werden nicht geladen | IMAP-Verbindung unterbrochen | MCP-Server neu starten, Credentials prüfen |
| Pocket-Transkripte fehlen | Pocket-App nicht aktiv | Pocket während Gesprächen aktiv lassen |
| OB24-Versand schlägt fehl | Falscher Benutzername / Passwort / Job-ID | OB24-Dashboard prüfen |
| Kalender nicht erkannt | Google Calendar MCP nicht verbunden | Claude Desktop → Connectors → Google Calendar |
| CRM-Tabelle leer | Phase 9 noch nicht ausgeführt | CRM-Sync-Skill starten |
| Claude „vergisst" Kontext | Neue Session ohne MEMORY.md-Lesen | CLAUDE.md und MEMORY.md im Subfolder prüfen |
| WhatsApp: keine Nachrichten | Session nicht aktiviert | Nach Start: `/whatsapp:status` eingeben |
| WhatsApp: Gerät getrennt | Session abgelaufen | `claude --dangerously-skip-permissions ...` neu starten, ggf. `/whatsapp:configure reset-auth` |
| WhatsApp: Sprachnachricht nicht transkribiert | `~/whisper-transcribe.sh` fehlt oder OpenAI Key ungültig | Script prüfen, Key rotieren |
| WhatsApp: hoher RAM-Verbrauch | Lokales Whisper-Modell geladen | Nur OpenAI API verwenden — kein lokales mlx-whisper |
| WhatsApp: Umlaute falsch (ae/oe statt ä/ö) | Encoding-Problem im Brieftext | `~/CLAUDE.md` enthält Umlaut-Regel — Cleo neu starten |

---

## 12. BAFA-Förderung

Cleo kann über das BAFA-Programm **„Förderung unternehmerischen Know-hows"** als Digitalisierungsberatung teilfinanziert werden.

### Konditionen (Stand: 2024/2025 — vor Antragstellung prüfen)

| | Westdeutschland (inkl. Berlin) | Ostdeutschland* |
|---|---|---|
| Förderquote | 50% | **80%** |
| Max. förderfähige Kosten pro Vorhaben | 3.500 EUR netto | 3.500 EUR netto |
| Max. Zuschuss pro Vorhaben | 1.750 EUR | **2.800 EUR** |

*Ostdeutschland: Brandenburg, Mecklenburg-Vorpommern, Sachsen, Sachsen-Anhalt, Thüringen

### Rechenbeispiel — Neue Bundesländer (80%)

| Position | Betrag |
|---|---|
| Gesamtinstallation (2 Vorhaben à 3.500 EUR) | 7.000 EUR netto |
| BAFA-Zuschuss Phase 1 (80% von 3.500 EUR) | - 2.800 EUR |
| BAFA-Zuschuss Phase 2 (80% von 3.500 EUR) | - 2.800 EUR |
| **Ihre effektiven Kosten** | **1.400 EUR netto** |

> ⚠️ Antrag muss **vor Beginn** der Leistung gestellt werden. Able & Baker GmbH begleitet durch den gesamten Antragsprozess.

---

## 13. Changelog

### v1.4.0 — April 2026
- **NEU**: WhatsApp-Kanal (Modul 4.6) — Cleo per Linked Device erreichbar
- **NEU**: Installationsphasen 11–13 für WhatsApp-Einrichtung
- **NEU**: Sprachtranskription via OpenAI Whisper API (kein lokaler RAM-Verbrauch)
- **NEU**: `~/CLAUDE.md` — System-Prompt für Claude Code / WhatsApp-Kanal
- **NEU**: `~/.whatsapp-channel/cleo-memory.md` — sessionübergreifendes Gedächtnis
- **NEU**: imap-smtp in Claude Code registrierbar (E-Mail-Zugriff via WhatsApp)
- **NEU**: Interaktiver System-Prompt-Generator (Phase 13.1)
- **UPDATE**: Voraussetzungen — Claude Code CLI, Bun, OpenAI API Key ergänzt
- **UPDATE**: Ordnerstruktur — `~/.whatsapp-channel/` dokumentiert
- **UPDATE**: Troubleshooting — WhatsApp-spezifische Einträge ergänzt

### v1.3.1 — April 2026
- **NEU**: Kontinuierliches CRM-Lernen — inbox-review und meeting-review aktualisieren das Mini-CRM automatisch
- **UPDATE**: Alle PDFs — Deutsche Umlaute durchgehend (ä, ö, ü, ß)

### v1.3.0 — April 2026
- **NEU**: Assistenz-Identität — Name & Geschlecht in Installationsflow (Phase 0.2.5)
- **NEU**: Kategorie ✉️ BRIEF in Inbox-Review
- **NEU**: KI-Rechtsassistent-Haftungsausschluss prominenter
- **FIX**: OB24-Credentials in Installation korrigiert

### v1.2.0 — März 2026
- **NEU**: Autonomie-Level 1/2/3 als zentrale Konfigurationsentscheidung
- **NEU**: Spam-Kategorie explizit in Inbox-Review
- **NEU**: Scheduled Tasks am Ende der Installation

### v1.1.0 — März 2026
- **NEU**: Pocket als Tagestranskript
- **NEU**: Ungeplante Gespräche werden erkannt und verarbeitet

### v1.0.0 — Februar 2026
- Erster vollständiger Installationsflow (Phasen 0–10)
- Inbox-Review, Meeting-Review, CRM-Sync, KI-Rechtsassistent
- Physischer Briefversand via OB24-API

---

*Dieses Dokument wird bei jeder Änderung des Systems aktualisiert.*
*Installationspartner: Able & Baker GmbH · Yuri A. Bilogor · able-baker.de*
