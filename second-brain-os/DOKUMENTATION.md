# Cleo — Produktdokumentation

> Letzte Aktualisierung: April 2026
> Version: 1.3.0
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
   - 4.5 [Firmenanwalt](#45-firmenanwalt)
5. [Autonomie-Level](#5-autonomie-level)
6. [Konfigurationsvariablen](#6-konfigurationsvariablen)
7. [MCP-Integrationen](#7-mcp-integrationen)
8. [Installationsflow (Phasen 0–10)](#8-installationsflow-phasen-010)
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
│   ├── Google Calendar / Outlook    ←  Kalender       │
│   ├── Pocket AI                    ←  Transkripte   │
│   ├── Notion / Markdown            ←  Aufgaben      │
│   └── OB24 (via Bash/curl)         ←  Briefe        │
└─────────────────────────────────────────────────────┘
```

### Skill-Dateien (SKILL.md)

Jedes Modul ist als `SKILL.md`-Datei im Cowork-Ordner des Kunden gespeichert. Diese Dateien enthalten:

- **Konfigurationsvariablen** oben im Header (einmal während der Installation gesetzt)
- **Ablaufanweisungen** für Claude (welche Tools aufzurufen sind, in welcher Reihenfolge)
- **Entscheidungslogik** (z.B. Autonomie-Level-Auswertung)

Die SKILL.md-Dateien sind plain-text Markdown — vollständig einsehbar, editierbar und versionierbar.

### Gedächtnissystem

- **CLAUDE.md**: Dauerhafte Konfiguration, Firmendaten, Mini-CRM, Rollenidentität des Assistenten
- **MEMORY.md**: Sitzungsübergreifendes Gedächtnis — wird nur auf explizite Nutzeranweisung beschrieben

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
| [Pocket AI](https://pocket.ai) | Gesprächsaufzeichnung + Transkript | ~10 EUR | Für Meeting-Review |
| [OnlineBrief24](https://www.onlinebrief24.de) | Physischer Briefversand per API | ~1,20–2,50 EUR/Brief | Optional |
| Google Workspace / Gmail | E-Mail + Kalender | 6 EUR/User | Falls Gmail |
| Notion | Aufgaben-Datenbank | 10–15 EUR | Optional |

> ⚠️ **OB24-Konto**: Muss **vor der Installation** angelegt werden. Registrierung unter [onlinebrief24.de](https://www.onlinebrief24.de) (kostenlos, Pay-per-use). Nach Registrierung: Login → API-Zugangsdaten notieren.

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
| ✉️ | BRIEF | Formelles Schreiben nötig (Mahnung, Vertrag, Behörde, Schriftformpflicht) | → Brief-Vorschlag |
| 📂 | VERSCHIEBEN | Gehört in Unterordner | → Ordner-Logik |
| 👀 | BEOBACHTEN | Relevant, kein sofortiger Handlungsbedarf | → Markieren |

4. **Entwürfe erstellen** (✅ ANTWORTEN): Ton professionell, im Stil der Firma
5. **Brief-Vorschläge** (✉️ BRIEF): Briefinhalt vorbereiten, Nutzer bestätigt → OB24-Versand
6. **Zusammenfassung**: Tabelle aller bearbeiteten Mails + Brief-Vorschlagsblock (falls vorhanden)
7. **Mini-CRM automatisch aktualisieren** (Schritt 7 — immer, kein manueller crm-sync nötig):
   - Neue Absender werden direkt eingetragen (Name, Firma, Rolle, Datum, Kontext)
   - Bestehende Kontakte: „Letzter Kontakt" aktualisiert, Notizen bei neuem Kontext ergänzt
   - Signaturblöcke werden ausgewertet: Telefon, Adresse, Titel fließen als Notizen ein
   - Abschluss: `📇 Mini-CRM aktualisiert: +X neu · ↻Y aktualisiert · ✎Z angereichert`

#### Spam-Erkennung (konservativ)

Das System erkennt Spam anhand folgender Signale, handelt aber im Zweifelsfall als 👀 BEOBACHTEN:
- Absender-Domain nicht im Mini-CRM und völlig unbekannt
- Typische Spam-Phrasen (Gewinn, Erbschaft, Kreditangebot)
- Keine persönliche Anrede
- Vollständig bildbasierte Mail
- SPF/DKIM-Fehler

> ⚠️ Spam-Mails werden **nie permanent gelöscht** (`permanent=False`). Der Nutzer kann jederzeit im Papierkorb prüfen.

#### Konfigurationsvariablen

| Variable | Beschreibung | Beispielwert |
|---|---|---|
| `EMAIL_SYSTEM` | E-Mail-System | `imap-smtp` / `gmail` / `office365` |
| `INBOX_REVIEW_HOURS` | Zeitfenster für Review | `24` |
| `INBOX_REVIEW_SCHEDULE` | Zeitplan | `täglich 08:00` |
| `SUMMARY_CHANNEL` | Wohin die Zusammenfassung geht | `email:` / `slack:` / `none` |
| `BRIEFING_FOLDER` | IMAP-Ordner für Briefings | `Morgen-Briefings` |
| `AUTONOMOUS_ACTIONS` | Autonomie-Level | `1` / `2` / `3` |
| `AUTO_NOTIFY_CONTACT` | Benachrichtigungskontakt informieren | `true` / `false` |

---

### 4.2 Meeting-Review

**Datei:** `Sekretariat/skills/meeting-review/SKILL.md`

**Funktion:** Vollautomatische Tages-Nachbereitung aller Meetings und Gespräche.

#### Ablauf

1. **Kalendertermine laden** (Google Calendar / Outlook): Alle Termine des heutigen Tages
2. **Pocket-Tagestranskripte laden**: Alle Gespräche 00:00–23:59 Uhr via `search_pocket_conversations_timerange`
3. **Matching**: Pocket-Gespräch → Kalendertermin bei zeitlicher Überlappung ≥ 5 Minuten. Nicht zuordbare Gespräche → „Ungeplantes Gespräch"
4. **Zusammenfassung** je Gesprächstyp:
   - 👤 Kundengespräch: Themen, Vereinbarungen, Next Steps, offene Fragen
   - 🏢 Intern: Kurzzusammenfassung + To-Do-Liste
   - 🎤 Ungeplant: Teilnehmer, Zusammenfassung, Next Steps
5. **To-Dos anlegen** (bei Level 3): Notion-Datenbank oder Markdown-Checkliste
6. **Kalendertermine anlegen** (bei Level 3): Follow-up-Termine aus vereinbarten Terminen
7. **E-Mail-Entwürfe** (bei Level 2+): Meeting-Zusammenfassung an Kunden
8. **Brief-Empfehlung** (immer): Erkennt ob ein formelles Schreiben nach dem Gespräch sinnvoller ist
9. **Mini-CRM automatisch aktualisieren** (Schritt 7 — immer, auf Basis aller Gespräche des Tages):
   - Neue Gesprächspartner aus Kalender + Pocket-Transkript werden direkt eingetragen
   - Bestehende Kontakte: „Letzter Kontakt" aktualisiert, Gesprächskontext als Notiz ergänzt
   - Beziehungstiefe aus Transkript: Angebot besprochen, Abschluss erzielt, offene Punkte, Interessensignale
   - Rollenwechsel / Jobwechsel die im Gespräch erwähnt werden fließen sofort ein
   - Abschluss: `📇 Mini-CRM aktualisiert: +X neu · ↻Y aktualisiert · ✎Z angereichert`
10. **Tagesübersicht**: Tabelle mit Gespräch | Typ | Pocket | To-Dos | Termin | Entwurf | Brief

#### Pocket-Integration

Pocket AI zeichnet kontinuierlich alle Gespräche des Tages auf — unabhängig vom Kalender. Meeting-Review liest **alle** Pocket-Gespräche des Tages in einem Aufruf:

```
search_pocket_conversations_timerange(start_date="HEUTE 00:00", end_date="HEUTE 23:59")
```

Danach wird für jedes Gespräch:
- Volles Transkript geladen: `get_pocket_conversation(id=...)`
- Action Items geladen: `search_pocket_actionitems(conversation_id=...)`

---

### 4.3 Physischer Briefversand (OB24)

**Datei:** `Sekretariat/skills/physischen-brief-versenden/SKILL.md`

**Funktion:** Erstellt ein Brief-PDF nach DIN 5008 und versendet es via OnlineBrief24-API als physischen Brief.

#### Ablauf

1. **Briefdaten erfassen**: Empfänger, Betreff, Brieftext, Brieftyp (Standard / Anwaltsbrief)
2. **Brief-PDF generieren**: `build_brief.py` (liegt nach Installation in `Post-Requisiten/`)
   - Ränder: Links/Rechts/Unten = 57pt, Oben = 80pt
   - Briefkopf: Logo (oben rechts) + Firmendaten
   - Empfängeradresse: DIN 5008-konform, 45mm vom oberen Rand
   - Datum: rechtsbündig, Betreff: fett
   - Grußformel: „Mit freundlichen Grüßen" + Signum-Bild
3. **Preis abfragen** (OB24-API): Pflicht vor jedem Versand, Preis wird dem Nutzer angezeigt
4. **Testmodus-Abfrage**:
   - `OB24_TEST_MODE = true`: Brief wird simuliert, kein echter Versand, keine Kosten
   - `OB24_TEST_MODE = false`: Claude fragt per Bestätigung: „Echt senden oder Testversand?"
5. **Versand** (nach Bestätigung): Base64-kodiertes PDF an OB24-API → Tracking-ID zurück
6. **Logging**: Eintrag in `Postausgang/log.md` mit Datum, Empfänger, Preis, Tracking-ID, Test J/N

#### OB24-Credentials

| Variable | Beschreibung |
|---|---|
| `OB24_USERNAME` | E-Mail-Adresse des OB24-Kontos |
| `OB24_PASSWORD` | OB24-Kontopasswort |
| `OB24_JOB_ID` | Briefprodukt-ID aus OB24-Dashboard (z.B. 1000 für Standardbrief SW) |
| `OB24_TEST_MODE` | `true` = immer Testmodus, `false` = Echt (mit Rückfrage) |

#### Brieftypen

- **Standardbrief**: Firmenbriefkopf, normaler Abschluss
- **Anwaltsbrief**: Zusätzlich Aktenzeichen im Briefkopf, Abschluss: „Rechtsabteilung, i.A. der Geschäftsführung, [Firma]"

---

### 4.4 CRM-Sync

**Datei:** `Sekretariat/skills/crm-sync/SKILL.md`

**Funktion:** Liest das E-Mail-Postfach aus und füllt das Mini-CRM in `Sekretariat/CLAUDE.md` mit Kontakten.

#### Ablauf

1. E-Mail-Postfach der letzten N Tage durchsuchen (Standard: 180 Tage)
2. Absender-Domains klassifizieren (intern vs. extern)
3. Top-Kontakte extrahieren: Name, Firma, E-Mail, letzter Kontakt, Kontext
4. Mini-CRM-Tabelle in `Sekretariat/CLAUDE.md` aktualisieren
5. Optional: Neue Kontakte in externes CRM (HubSpot, Salesforce, Pipedrive, Close.io) übertragen

#### Mini-CRM-Format

```markdown
| Name | Firma | E-Mail | Rolle | Letzter Kontakt | Notizen |
|---|---|---|---|---|---|
| Max Mustermann | Muster GmbH | max@muster.de | Kunde | 2026-03-15 | Angebot ausstehend |
```

Das Mini-CRM ist die **Single Source of Truth** für alle Skills. Inbox-Review, Meeting-Review und Brief-Versand lesen Kontaktdaten immer frisch aus dieser Tabelle.

#### Kontinuierliches Lernen

Das Mini-CRM wächst und verbessert sich automatisch mit jeder Interaktion — **ohne manuellen crm-sync-Aufruf**:

| Quelle | Was wird gelernt |
|---|---|
| Inbox-Review (täglich) | Neue Absender, Letzter Kontakt, Telefon/Adresse aus Signaturen, Rollenzuordnung |
| Meeting-Review (täglich) | Neue Gesprächspartner, Gesprächskontext, Angebote/Abschlüsse, Jobwechsel |
| CRM-Sync (initial + auf Abruf) | Initialbefüllung aus 180 Tagen Postfach, Abgleich mit externem CRM |

Nach jedem Review wird eine Zusammenfassung der CRM-Änderungen ausgegeben:
```
📇 Mini-CRM aktualisiert:
  + [X] neue Kontakte eingetragen
  ↻ [Y] bestehende Kontakte aktualisiert
  ✎ [Z] Kontakte mit neuen Infos angereichert
```

---

### 4.5 Firmenanwalt

**Datei:** `Team/Firmenanwalt/CLAUDE.md`

**Funktion:** KI-gestützter Recherche- und Verwaltungsassistent für rechtliche Themen.

> ⚠️ **Wichtiger Haftungsausschluss**: Der Firmenanwalt ist **kein zugelassener Rechtsanwalt** und ersetzt keinen. Er dient der Recherche, Strukturierung und Verwaltung von Rechtsvorgängen — nicht der Rechtsberatung im Sinne des RDG (Rechtsdienstleistungsgesetz). Bei jedem Thema mit rechtlicher Tragweite endet jede Antwort mit dem Hinweis: *„Bitte vor verbindlichen Schritten mit einem zugelassenen Rechtsanwalt abstimmen."*

#### Fähigkeiten (KI-Assistent, kein Anwalt)

- Rechtliche Sachverhalte strukturieren und zusammenfassen
- Relevante Gesetze und Urteile recherchieren (BGB, HGB, UStG, DSGVO, UWG, VOB u.a.)
- Vertragsentwürfe als **Arbeitsdokument** vorbereiten
- Schriftverkehr und Fallakten in `Team/Firmenanwalt/Fallarchiv/` organisieren
- Auf mögliche rechtliche Risiken hinweisen (proaktiv, unaufgefordert)

#### Aktenführung

```
Fallarchiv/
└── 2026-001-VERTR/       ← Aktenzeichen: Jahr-Nr-Kürzel
    ├── Sachverhalt.md
    ├── Dokumente/
    └── Korrespondenz/
```

#### Rechtsgebiete

Werden während der Installation automatisch aus dem E-Mail-Postfach (180 Tage) abgeleitet und in `Team/Firmenanwalt/CLAUDE.md` eingetragen. Typische Rechtsgebiete je Branche:

| Branche | Häufige Rechtsgebiete |
|---|---|
| Marketing/Agentur | Urheberrecht, Wettbewerbsrecht, DSGVO, Dienstleistungsrecht |
| Handwerk | Werkvertragsrecht, VOB, Baurecht, Gewährleistung |
| IT | Softwarelizenzrecht, Datenschutz, Haftungsrecht, SLA |
| Immobilien | Mietrecht, Kaufvertragsrecht, WEG-Recht, Maklerrecht |

---

## 5. Autonomie-Level

Das Autonomie-Level ist die **zentrale Konfigurationsentscheidung** der Installation. Es bestimmt, wie eigenständig Cleo in allen Modulen handelt.

| Level | Name | Was passiert automatisch |
|---|---|---|
| **Level 1** | Beobachter | Nur analysieren und zusammenfassen — alle Aktionen werden vorgeschlagen, der Nutzer entscheidet |
| **Level 2** | Assistent | Level 1 + automatisch E-Mail-Entwürfe erstellen (Nutzer sendet selbst) |
| **Level 3** | Autopilot | Level 2 + Kalendertermine anlegen, To-Dos anlegen, Benachrichtigungskontakt informieren |

### Variablen je Level

| Variable | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| `AUTO_CREATE_DRAFTS` | `false` | **`true`** | `true` |
| `AUTO_CREATE_EVENTS` | `false` | `false` | **`true`** |
| `AUTO_CREATE_TODOS` | `false` | `false` | **`true`** |
| `AUTO_NOTIFY_CONTACT` | `false` | `false` | **`true`** |

Das Level kann jederzeit durch Änderung der Variablen in den jeweiligen SKILL.md-Dateien angepasst werden.

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
| `BENACHRICHTIGUNGS_POSITION` | Position (z.B. Geschäftsführer) |
| `BENACHRICHTIGUNGS_EMAIL` | E-Mail des Benachrichtigungskontakts |

### Inbox-Review/SKILL.md

| Variable | Beschreibung | Standard |
|---|---|---|
| `INBOX_REVIEW_HOURS` | Zeitfenster in Stunden | `24` |
| `INBOX_REVIEW_SCHEDULE` | Zeitplan | `täglich 08:00` |
| `SUMMARY_CHANNEL` | Zusammenfassungskanal | `email:` |
| `BRIEFING_FOLDER` | IMAP-Ordner für Briefings | `Morgen-Briefings` |
| `AUTONOMOUS_ACTIONS` | Autonomie-Level | `1` |
| `AUTO_NOTIFY_CONTACT` | Benachrichtigung senden | `false` |
| `FOLDER_TRASH` | IMAP-Papierkorb-Ordner | `Trash` |

### Meeting-Review/SKILL.md

| Variable | Beschreibung | Standard |
|---|---|---|
| `CALENDAR_SYSTEM` | `google-kalender` / `outlook` | `google-kalender` |
| `TASK_TOOL` | `notion` / `none` | `none` |
| `EMAIL_SYSTEM` | E-Mail-System (wie global) | — |
| `POCKET_ENABLED` | Pocket-Integration aktiv | `true` |
| `SUMMARY_CHANNEL` | Zusammenfassungskanal | `email:` |
| `AUTO_CREATE_EVENTS` | Termine automatisch anlegen | `false` |
| `AUTO_CREATE_TODOS` | To-Dos automatisch anlegen | `false` |
| `AUTO_CREATE_DRAFTS` | Entwürfe automatisch erstellen | `false` |

### Brief-Versenden/SKILL.md

| Variable | Beschreibung |
|---|---|
| `OB24_USERNAME` | OB24 Benutzername (E-Mail) |
| `OB24_PASSWORD` | OB24 Passwort |
| `OB24_JOB_ID` | Briefprodukt-ID aus OB24-Dashboard |
| `OB24_TEST_MODE` | `true` = Testmodus (kein echter Versand) |

---

## 7. MCP-Integrationen

Cleo nutzt folgende MCP-Server (Model Context Protocol):

| MCP | Zweck | Installation |
|---|---|---|
| **imap-smtp-mcp** | Standard-E-Mail (IMAP/SMTP) | `npx mcp-remote [URL]` |
| **Gmail-Connector** | Google Gmail / Workspace | Claude Desktop → Connectors |
| **Outlook-Connector** | Microsoft Office 365 | Claude Desktop → Connectors |
| **Google Calendar** | Kalenderintegration | Claude Desktop → Connectors |
| **Pocket AI** | Gesprächstranskripte | `npx mcp-remote https://mcp.pocket.ai` |
| **Notion** | Aufgaben-Datenbank | Claude Desktop → Connectors |
| **OB24** | Briefversand (via Bash/curl) | Keine MCP-Installation nötig |

### Pocket AI — wichtige Details

Pocket AI zeichnet **alle Gespräche des Tages** auf — nicht nur Kalender-Meetings. Meeting-Review nutzt:

```
search_pocket_conversations_timerange(start_date, end_date)
get_pocket_conversation(id)
search_pocket_actionitems(conversation_id)
```

Der `npx mcp-remote`-Eintrag wird in `claude_desktop_config.json` eingetragen:

```json
{
  "mcpServers": {
    "pocket": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.pocket.ai/mcp"],
      "env": { "POCKET_API_KEY": "pk_..." }
    }
  }
}
```

---

## 8. Installationsflow (Phasen 0–10)

Die vollständige Installation läuft über **einen einzigen Skill-Aufruf** in Claude Desktop:

> „Führe den Cleo Installationsflow aus."

Gesamtdauer: ca. 2–4 Stunden | Alle Schritte geführt und interaktiv.

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
| **8** | Firmenanwalt einrichten (E-Mail-Scan 180 Tage) | 10 Min |
| **9** | Mini-CRM vorbefüllen (Top-50 Kontakte aus Postfach) | 10–20 Min |
| **10.1** | Installations-Checkliste abhaken | 5 Min |
| **10.2** | Funktionstest E-Mail & CRM (Tests 1–3) | 10 Min |
| **10.3** | Funktionstest Brief-Layout & OB24 (Tests 4–6, Testmodus) | 10 Min |
| **10.4** | Funktionstest Firmenanwalt (Tests 7–8) | 5 Min |
| **10.5** | Scheduled Tasks anlegen (Inbox-Review + Meeting-Review) | 5 Min |
| **10.6** | Übergabenotiz UEBERGABE.md generieren | 5 Min |

### OB24-Test (Phase 10.3)

Während der Installation ist `OB24_TEST_MODE = true` gesetzt. Der finale Test:

1. Brief-PDF generieren (Testbrief an Max Mustermann)
2. OB24-Preis abfragen (kein echter Versand)
3. Testversand bestätigen: Claude zeigt `„⚠️ Testmodus aktiv — kein echter Versand"`
4. Nach erfolgreichem Test: `OB24_TEST_MODE` auf `false` setzen für echte Nutzung

---

## 9. Ordnerstruktur nach Installation

```
[Cowork-Hauptordner]/
├── CLAUDE.md                           ← Globale Workspace-Konfiguration
├── MEMORY.md                           ← Sitzungsübergreifendes Gedächtnis
│
├── Sekretariat/
│   ├── CLAUDE.md                       ← Identität, Firmendaten, Mini-CRM, Variablen
│   ├── MEMORY.md                       ← Sekretariats-Gedächtnis
│   ├── Post-Requisiten/
│   │   ├── logo.png                    ← Firmenlogo (nach Installation hochgeladen)
│   │   ├── signum_[name].png           ← Unterschrift-Signum
│   │   └── build_brief.py              ← Brief-PDF-Generator
│   ├── Postausgang/
│   │   ├── [DATUM]-[KÜRZEL].pdf        ← Generierte Briefe
│   │   ├── log.md                      ← Versand-Log (Datum, Empfänger, Preis, Tracking)
│   │   └── fehler-log.md               ← OB24-Fehlerprotokoll
│   └── skills/
│       ├── inbox-review/
│       │   ├── SKILL.md                ← Konfiguriert mit Kundenvariablen
│       │   └── ordner-logik/SKILL.md   ← Optional: E-Mail-Sortierlogik
│       ├── meeting-review/SKILL.md
│       ├── crm-sync/SKILL.md
│       └── physischen-brief-versenden/SKILL.md
│
└── Team/
    └── Firmenanwalt/
        ├── CLAUDE.md                   ← Juristischer Assistent (mit Haftungsausschluss)
        ├── MEMORY.md
        └── Fallarchiv/
            └── [AKTENZEICHEN]/
                ├── Sachverhalt.md
                ├── Dokumente/
                └── Korrespondenz/
```

---

## 10. Tägliche Nutzung

### Typischer Arbeitstag mit Cleo

**Morgens (Level 2 / Level 3):**
```
„Geh durch meinen Posteingang."
→ Claude klassifiziert alle Mails, erstellt Entwürfe, zeigt Brief-Vorschläge
→ Morgen-Briefing geht automatisch an Benachrichtigungskontakt
```

**Nach Meetings:**
```
„Mach die Meeting-Nachbereitung."
→ Claude liest Kalender + Pocket-Transkripte, erstellt Zusammenfassungen
→ To-Dos angelegt, Follow-up-Termine vorgeschlagen, Kunden-E-Mails als Entwurf
```

**Brief versenden:**
```
„Schreib eine Mahnung an Müller GmbH, 500 EUR offen seit 30 Tagen."
→ Claude erstellt Brief-PDF, fragt Preis bei OB24 ab, wartet auf Bestätigung, versendet
```

**Rechtsfrage:**
```
„Kann ich einen laufenden Dienstleistungsvertrag fristlos kündigen?"
→ Firmenanwalt recherchiert, strukturiert Sachverhalt, nennt relevante Paragrafen
→ Immer mit Hinweis: „Bitte vor Schritten mit Rechtsanwalt abstimmen"
```

### Shortcuts / Trigger-Phrasen

| Aktion | Beispielaufruf |
|---|---|
| Inbox-Review starten | „Geh durch meine E-Mails" / „Posteingang aufräumen" |
| Meeting-Nachbereitung | „Mach die Meeting-Nachbereitung" / „Was war heute" |
| Brief versenden | „Schreib einen Brief an [Name]" / „brief versenden" |
| CRM aktualisieren | „Sync das CRM" / „Neue Kontakte eintragen" |
| Rechtsfrage stellen | Direkt in `Team/Firmenanwalt/` Subfolder öffnen |

---

## 11. Troubleshooting

| Problem | Mögliche Ursache | Lösung |
|---|---|---|
| E-Mails werden nicht geladen | IMAP-Verbindung unterbrochen | MCP-Server neu starten, Credentials prüfen |
| Pocket-Transkripte fehlen | Pocket-App nicht aktiv | Pocket während Gesprächen aktiv lassen |
| OB24-Versand schlägt fehl | Falscher Benutzername / Passwort / Job-ID | OB24-Dashboard prüfen, Testmodus aktivieren |
| OB24-Saldo leer | Guthaben aufgebraucht | In OB24-Dashboard Guthaben aufladen |
| Kalender nicht erkannt | Google Calendar MCP nicht verbunden | Claude Desktop → Connectors → Google Calendar |
| Brief-Layout stimmt nicht | Logo/Signum fehlt oder falsch | `Post-Requisiten/` prüfen, PNG neu hochladen |
| CRM-Tabelle leer | Phase 9 noch nicht ausgeführt | CRM-Sync-Skill starten |
| Spam-Mail fälschlich archiviert | Zu aggressiver Filter | In Papierkorb nachschauen (nie permanent gelöscht) |
| Claude „vergisst" Kontext | Neue Session ohne MEMORY.md-Lesen | CLAUDE.md und MEMORY.md im Subfolder sicherstellen |

---

## 12. BAFA-Förderung

Cleo kann über das BAFA-Programm **„Förderung unternehmerischen Know-hows"** als Digitalisierungsberatung teilfinanziert werden.

### Konditionen (Stand: 2024/2025 — vor Antragstellung prüfen)

| | Westdeutschland (inkl. Berlin) | Ostdeutschland* |
|---|---|---|
| Förderquote | 50% | **80%** |
| Max. förderfähige Kosten pro Vorhaben | 3.500 EUR netto | 3.500 EUR netto |
| Max. Zuschuss pro Vorhaben | 1.750 EUR | **2.800 EUR** |

*Ostdeutschland (neue Bundesländer): Brandenburg, Mecklenburg-Vorpommern, Sachsen, Sachsen-Anhalt, Thüringen

### Rechenbeispiel — Neue Bundesländer (80%)

| Position | Betrag |
|---|---|
| Gesamtinstallation (2 Vorhaben à 3.500 EUR) | 7.000 EUR netto |
| BAFA-Zuschuss Phase 1 (80% von 3.500 EUR) | - 2.800 EUR |
| BAFA-Zuschuss Phase 2 (80% von 3.500 EUR) | - 2.800 EUR |
| **Ihre effektiven Kosten** | **1.400 EUR netto** |

> ⚠️ Die Aufspaltung in 2 separate Vorhaben (z.B. Installation + Einweisung/Optimierung) muss mit dem BAFA-Berater abgestimmt werden. Able & Baker GmbH begleitet Sie durch den gesamten Antragsprozess.

### Wichtige Regeln

- Der Antrag **muss vor Beginn** der Leistung gestellt werden — rückwirkende Anträge sind nicht möglich
- Voraussetzung: KMU gemäß EU-Definition (< 250 Mitarbeiter, < 50 Mio. EUR Umsatz) oder Freiberufler
- Antrag läuft über einen BAFA-zugelassenen Berater (wird von Able & Baker GmbH gestellt)

Weitere Informationen: [www.bafa.de](https://www.bafa.de) | Programm: Förderung unternehmerischen Know-hows

---

## 13. Changelog

### v1.3.1 — April 2026
- **NEU**: Kontinuierliches CRM-Lernen — inbox-review und meeting-review aktualisieren das Mini-CRM automatisch nach jedem Durchlauf (Schritt 7 in beiden Skills)
  - Neue Kontakte werden direkt eingetragen, kein manueller crm-sync mehr nötig
  - Signaturblöcke (Telefon, Adresse, Titel) werden aus E-Mails extrahiert
  - Meeting-Transkripte liefern Beziehungskontext (Angebote, Abschlüsse, Rollenwechsel)

### v1.3.0 — April 2026
- **NEU**: Assistenz-Identität — Name & Geschlecht in Installationsflow (Phase 0.2.5)
- **NEU**: Kategorie `✉️ BRIEF` in Inbox-Review — physischer Brief als Antwort-Option
- **NEU**: Brief-Empfehlungen in Meeting-Review-Zusammenfassung (neue Spalte „Brief")
- **NEU**: OB24 Testmodus pro Versand wählbar (Session-Override unabhängig von Konfiguration)
- **NEU**: Firmenanwalt-Haftungsausschluss prominenter und umfassender
- **FIX**: OB24-Credentials in Installation korrigiert (Username/Passwort statt API-Key)
- **FIX**: OB24-Konto-Voraussetzung in Phase 0 + Mitarbeiter-PDF ergänzt
- **FIX**: BAFA 80% auf korrekte Bundesländer eingeschränkt (Brandenburg, MV, Sachsen, SA, Thüringen)
- **UPDATE**: Sales-PDF — BAFA Rechenbeispiel 7.000 EUR / 1.400 EUR Eigenanteil (Ost)
- **UPDATE**: Sales-PDF — Able & Baker GmbH / Yuri A. Bilogor als Installationspartner
- **UPDATE**: Alle PDFs — Deutsche Umlaute durchgehend (ä, ö, ü, ß)

### v1.2.0 — März 2026
- **NEU**: Autonomie-Level 1/2/3 als zentrale Konfigurationsentscheidung (Phase 0.4)
- **NEU**: Benachrichtigungskontakt (Phase 0.3) mit eigenem IMAP-Ordner
- **NEU**: IMAP-Ordner automatisch anlegen (Morgen-Briefings, Meeting-Zusammenfassungen)
- **NEU**: Spam-Kategorie explizit in Inbox-Review (konservativ, nie permanent löschen)
- **NEU**: Scheduled Tasks am Ende der Installation (Phase 10.5)
- **FIX**: Autonomie-Variablen werden zentral in Phase 5c in alle Skills übertragen

### v1.1.0 — März 2026
- **NEU**: Pocket als Tagestranskript — alle Gespräche 00:00–23:59, nicht nur Meetings
- **NEU**: Ungeplante Gespräche (in Pocket ohne Kalendereintrag) werden erkannt und verarbeitet
- **NEU**: Autonome Aktionen-Variablen (AUTO_CREATE_EVENTS, AUTO_CREATE_TODOS, AUTO_CREATE_DRAFTS)
- **NEU**: Inbox-Review: Alte Entwürfe (> 30 Tage) in Papierkorb (Schritt 0)
- **NEU**: Mitarbeiter-PDF v2 mit Hardware/Abo-Kostenübersicht und BAFA-Info

### v1.0.0 — Februar 2026
- Erster vollständiger Installationsflow (Phasen 0–10)
- Inbox-Review, Meeting-Review, CRM-Sync, Firmenanwalt
- Physischer Briefversand via OB24-API
- Mitarbeiter-Anleitung als PDF

---

*Dieses Dokument wird bei jeder Änderung des Systems aktualisiert.*
*Installationspartner: Able & Baker GmbH · Yuri A. Bilogor · able-baker.de*
