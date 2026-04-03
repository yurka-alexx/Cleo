# Skill: Cleo — Installation

Vollständiger Installationsflow für Cleo beim Kunden. Führt Schritt für Schritt durch alle Phasen — von der ersten Frage bis zum fertigen, einsatzbereiten Arbeitsplatz.

**Ausführen als:** Claude Cowork-Session im Hauptordner des Kunden.

---

## PHASE 0 — Vorbereitung & Pre-flight

### Schritt 0.1 — Betriebssystem & Voraussetzungen prüfen

Frage mit **AskUserQuestion**:
- Betriebssystem: macOS / Windows
- Ist Claude Desktop installiert? (falls nein: https://claude.ai/download — erst installieren, dann weitermachen)
- Ist der Cowork-Ordner bereits in Claude Desktop als Arbeitsordner eingerichtet? (falls nein: Einrichtung erklären)

Merke Betriebssystem für spätere Schritte (macOS vs. Windows entscheidet über Shell-Befehle).

### Schritt 0.2 — Kundendaten erfassen

Frage mit **AskUserQuestion** (Firmeninformationen für spätere CLAUDE.md-Dateien):
- Firmenname (vollständig, z.B. "Muster GmbH")
- Rechtsform (GmbH / GmbH & Co. KG / AG / Einzelunternehmen / Freiberufler / Sonstige)
- Branche (z.B. Handwerk, Marketing, IT, Beratung, Immobilien, Medizin, Recht…)
- Hauptstandort (Stadt)
- Name des Hauptansprechpartners / Geschäftsführers
- E-Mail des Hauptansprechpartners

Alle Werte für spätere CLAUDE.md-Dateien speichern.

---

### Schritt 0.2.3 — Nutzungsprofil für Zeitersparnis-Kalkulation

Frage mit **AskUserQuestion** (wird am Ende für personalisierte Zeitersparnis-Schätzung genutzt):

> „Ein paar kurze Zahlen für dein persönliches System-Profil:"

- **Geschätzte E-Mails pro Tag** (Eingang, Schätzwert genügt — z.B. 20, 50, 100)
- **Termine / Meetings pro Woche** (Schätzwert, z.B. 5, 10, 20)
- **Physische Briefe pro Monat** (Schätzwert — ausgehende Briefe, z.B. 2, 5, 10)
- **Stundensatz oder Stundenwert** (€ — wie viel ist eine Stunde deiner Zeit wert? Schätzwert genügt, z.B. 80€)

Werte speichern:
- `EMAILS_PRO_TAG = [eingabe oder 25 als Standardwert]`
- `TERMINE_PRO_WOCHE = [eingabe oder 5 als Standardwert]`
- `BRIEFE_PRO_MONAT = [eingabe oder 4 als Standardwert]`
- `STUNDENSATZ = [eingabe oder 80 als Standardwert]`

---

### Schritt 0.2.5 — Assistenz-Identität festlegen

Frage mit **AskUserQuestion**:

> „Wie soll Ihr digitales Sekretariat heißen, und mit welchem Geschlecht soll es angesprochen werden?
>  Name und Ansprache erscheinen in allen Zusammenfassungen und Benachrichtigungen."

Bitte eingeben:
- **Geschlecht:** Weiblich / Männlich / Neutral
- **Name** (z.B. „Clara", „Max", „Alex" — oder leer lassen für „Sekretariat")

Werte speichern:
- `ASSISTENT_NAME = [eingabe oder "Sekretariat"]`
- `ASSISTENT_GESCHLECHT = [weiblich/männlich/neutral]`

Identitätssatz je Wahl (für spätere CLAUDE.md-Dateien):
- Weiblich: `Du bist [NAME], die digitale Assistentin von [FIRMENNAME].`
- Männlich: `Du bist [NAME], der digitale Assistent von [FIRMENNAME].`
- Neutral: `Du bist [NAME], das digitale Sekretariat von [FIRMENNAME].`

Hinweis: Der Name erscheint in der Signatur von Morgen-Briefings und Zusammenfassungen.

---

### Schritt 0.3 — Benachrichtigungskontakt festlegen

Frage mit **AskUserQuestion**:

> „Wer soll vom Sekretariat bei täglichen Aufgaben benachrichtigt werden?
> Das ist die Person, die Morgen-Briefings, Meeting-Zusammenfassungen und
> wichtige To-Do-Hinweise erhält."

Bitte eingeben:
- Vorname + Nachname
- Position im Unternehmen (z.B. Geschäftsführer, Office-Managerin, Assistent)
- E-Mail-Adresse

Werte speichern:
- `BENACHRICHTIGUNGS_NAME = [eingabe]`
- `BENACHRICHTIGUNGS_POSITION = [eingabe]`
- `BENACHRICHTIGUNGS_EMAIL = [eingabe]`

In `Sekretariat/CLAUDE.md` unter Abschnitt `BENACHRICHTIGUNG` eintragen:
```markdown
## BENACHRICHTIGUNG
Benachrichtigungskontakt: [NAME] ([POSITION])
E-Mail: [EMAIL]
→ Morgen-Briefings, Meeting-Zusammenfassungen und To-Do-Hinweise gehen an diese Person.
```

---

### Schritt 0.4 — Autonomie-Level festlegen

**Dies ist die wichtigste Konfigurationsentscheidung der gesamten Installation.**
Das gewählte Level bestimmt, wie eigenständig Cleo in allen Modulen handelt.

Erkläre dem Kunden die drei Stufen:

> **Level 1 — Beobachter (Empfehlung für den Start)**
> Cleo liest, analysiert und fasst zusammen — macht aber nichts eigenständig.
> → Mails klassifizieren · Meetings zusammenfassen · Infos aufbereiten
> → Alle Aktionen werden nur vorgeschlagen, du entscheidest selbst.
>
> **Level 2 — Assistent**
> Alles aus Level 1, plus: automatisch Entwürfe erstellen für alle identifizierten Follow-ups.
> → Antwort-Entwürfe für Mails · Meeting-Zusammenfassungsmails an Kunden als Entwurf
> → Du überprüfst und sendest, Claude schreibt.
>
> **Level 3 — Autopilot (Maximale Zeitersparnis)**
> Alles aus Level 2, plus: eigenständig handeln ohne Bestätigung.
> → Folge-Termine im Kalender anlegen · To-Dos in Notion/App anlegen
> → Benachrichtigungskontakt direkt informieren (Morgen-Briefing, Meeting-Zusammenfassung)
> → Vollautomatisch im Hintergrund — du bekommst nur das Ergebnis.

Frage mit **AskUserQuestion** (Einfachauswahl):
> „Welches Autonomie-Level soll Cleo erhalten?"
> - Level 1 — Beobachter: Nur zusammenfassen, ich entscheide alles selbst
> - Level 2 — Assistent: Zusammenfassen + E-Mail-Entwürfe automatisch erstellen
> - Level 3 — Autopilot: Alles automatisch — Termine, To-Dos, Benachrichtigungen

Wert speichern: `AUTONOMIE_LEVEL = [1/2/3]`

Hinweis: Das Level kann jederzeit durch Änderung einer Variable in den jeweiligen SKILL.md-Dateien angepasst werden.

Variablen je nach Level setzen (für alle folgenden Phasen verwenden):

| Variable | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| `AUTO_CREATE_DRAFTS` | false | **true** | true |
| `AUTO_CREATE_EVENTS` | false | false | **true** |
| `AUTO_CREATE_TODOS` | false | false | **true** |
| `AUTO_NOTIFY_CONTACT` | false | false | **true** |

---

## PHASE 1 — E-Mail-System einrichten

### Schritt 1.1 — E-Mail-System abfragen

Frage mit **AskUserQuestion**:

> „Welches E-Mail-System nutzt du?"
> - Standard-IMAP/SMTP (kasserver, Strato, IONOS, Hetzner, eigener Server…)
> - Gmail / Google Workspace
> - Microsoft Office 365 / Outlook
> - Keines / später einrichten

**Verzweigung:**

#### → Standard-IMAP/SMTP
Führe den IMAP-SMTP-MCP-Installationsflow aus (SKILL: `imap-smtp-mcp/installation/SKILL.md`).
Credentials abfragen: Host, E-Mail, Passwort, IMAP-Port (993), SMTP-Port (587).
Merke nach Installation: `EMAIL_SYSTEM = "imap-smtp"`, `EMAIL_ADDRESS = [eingabe]`

#### → Gmail / Google Workspace
Kein IMAP-MCP nötig — Gmail-MCP ist in Claude Desktop als Connector verfügbar.
Anweisen: Claude Desktop → Connectors → Gmail verbinden.
Merke: `EMAIL_SYSTEM = "gmail"`, `EMAIL_ADDRESS = [eingabe]`

#### → Office 365 / Outlook
Kein IMAP-MCP nötig — Outlook-Connector in Claude Desktop verbinden (soweit verfügbar).
Falls kein nativer Connector: IMAP für Office 365 aktivieren und IMAP-MCP-Flow ausführen.
- IMAP-Host: `outlook.office365.com`, Port 993
- SMTP-Host: `smtp.office365.com`, Port 587
Merke: `EMAIL_SYSTEM = "office365"`, `EMAIL_ADDRESS = [eingabe]`

#### → Kein E-Mail-System
Notiz in CLAUDE.md hinterlegen. Inbox-Review-Skill deaktivieren. Weiter mit Phase 2.

---

## PHASE 2 — Ordnerstruktur anlegen

### Schritt 2.1 — Hauptordner erstellen

Erstelle folgende Ordner- und Dateistruktur im aktuellen Cowork-Hauptordner.
Nutze **Write**-Tool für alle CLAUDE.md- und MEMORY.md-Dateien.

```
[Cowork-Hauptordner]/
├── Sekretariat/
│   ├── CLAUDE.md           ← aus Template befüllen (Schritt 2.2)
│   ├── MEMORY.md           ← leer anlegen
│   ├── Post-Requisiten/    ← Logo + Signum werden hier abgelegt (Phase 3)
│   ├── Postausgang/        ← Briefe landen hier
│   └── skills/
│       ├── inbox-review/SKILL.md       ← aus Template (Phase 4)
│       ├── meeting-review/SKILL.md     ← aus Template (Phase 5, falls gewünscht)
│       ├── crm-sync/SKILL.md           ← aus Template (Phase 6)
│       └── physischen-brief-versenden/SKILL.md  ← aus Template (Phase 7)
├── Team/
│   └── KI-Rechtsassistent/
│       ├── CLAUDE.md       ← aus E-Mail-Scan befüllen (Phase 8)
│       ├── MEMORY.md       ← leer anlegen
│       └── Fallarchiv/     ← Ordner für Akten
└── MEMORY.md               ← leer anlegen (falls noch nicht vorhanden)
```

### Schritt 2.2 — Sekretariat/CLAUDE.md befüllen

Schreibe `Sekretariat/CLAUDE.md` mit folgenden Abschnitten:

```markdown
# Sekretariat — [FIRMENNAME]

[IDENTITÄTSSATZ aus Schritt 0.2.5 eintragen]
Du arbeitest für [ANSPRECHPARTNER].

## KONTEXT
- Firma: [FIRMENNAME] ([RECHTSFORM])
- Branche: [BRANCHE]
- Standort: [HAUPTSTANDORT]
- E-Mail-System: [EMAIL_SYSTEM]
- E-Mail-Adresse: [EMAIL_ADDRESS]

## MINI-CRM — KONTAKTE
<!--
  Single Source of Truth für alle Kontaktdaten.
  Wird initial in Phase 9 aus dem E-Mail-Postfach befüllt.
  Danach: kontinuierliches Lernen — inbox-review und meeting-review
  aktualisieren diese Tabelle automatisch nach jedem Durchlauf:
  - Neue Absender/Gesprächspartner werden eingetragen
  - Letzter Kontakt wird nach jeder Interaktion aktualisiert
  - Notizen werden mit Gesprächskontext angereichert
  - Rollenzuordnung wird korrigiert wenn neue Infos vorliegen
-->
| Name | Firma | E-Mail | Rolle | Letzter Kontakt | Notizen |
|---|---|---|---|---|---|

## MEMORY SYSTEM
Lies MEMORY.md zu Beginn jeder Session.
Schreibe nur auf explizite Anweisung ("merke dir", "notiere", "vergiss nicht").

## AKTIVE SKILLS
- inbox-review: Posteingang scannen und aufräumen
- crm-sync: Kontakte aus Postfach synchronisieren
[WENN MEETING-REVIEW]: - meeting-review: Meetings nachbereiten
[WENN BRIEF]: - physischen-brief-versenden: Briefe über OB24 versenden

## SLACK-ROUTING (falls konfiguriert)
<!-- Wird während Installation ergänzt falls Slack verbunden -->
```

---

## PHASE 3 — Post-Requisiten hochladen

### Schritt 3.1 — Logo abfragen

Weise den Nutzer an:

> „Bitte lade jetzt das Firmenlogo als PNG mit transparentem Hintergrund hoch. Wenn du kein transparentes PNG hast, kannst du das Logo später unter `Sekretariat/Post-Requisiten/logo.png` ablegen."

Falls hochgeladen: Datei nach `Sekretariat/Post-Requisiten/logo.png` speichern.
Falls nicht: Hinweis in `Sekretariat/CLAUDE.md` hinterlegen: `LOGO: ⚠️ noch nicht hinterlegt`.

### Schritt 3.2 — Unterschrift / Signum abfragen

> „Bitte lade jetzt das Signum (Unterschrift als PNG, transparenter Hintergrund) des Unterzeichners hoch. Name des Unterzeichners?"

Falls hochgeladen: Datei nach `Sekretariat/Post-Requisiten/signum_[name].png` speichern.
Falls nicht: Hinweis in CLAUDE.md: `SIGNUM: ⚠️ noch nicht hinterlegt`.

### Schritt 3.3 — Firmendaten für Briefkopf

Frage mit **AskUserQuestion**:
- Straße + Hausnummer
- PLZ + Ort
- Telefon
- Website
- Steuernummer / USt-ID (für Rechnungsdokumente)
- IBAN (für Brieffuß, optional)

Alle Werte in `Sekretariat/CLAUDE.md` unter Abschnitt `BRIEFKOPF` eintragen.

---

## PHASE 4 — Inbox-Review konfigurieren

### Schritt 4.1 — Inbox-Review-Skill schreiben

Erstelle `Sekretariat/skills/inbox-review/SKILL.md`:

```markdown
# Skill: Inbox-Review

Scannt den Posteingang und gibt strukturierte Handlungsempfehlungen.
E-Mail-System: [EMAIL_SYSTEM]

## ABLAUF

### Schritt 1 — Posteingang laden
[WENN imap-smtp]:
Nutze `fetch_recent_mails(hours=72)` für die letzten 3 Tage.
Für tiefere Suche: `search_mails(since_days=14, unread_only=True)`.

[WENN gmail]:
Nutze Gmail-MCP: `gmail_search_messages(query="is:unread newer_than:3d")`.

[WENN office365]:
Nutze IMAP-MCP mit Office-365-Credentials oder Outlook-Connector.

### Schritt 2 — Jede Mail klassifizieren
Für jede Mail Entscheidung treffen:
- 🗑️ LÖSCHEN — Spam, Werbung, irrelevant
- 📁 ARCHIVIEREN — erledigt, kein Handlungsbedarf
- ✅ ANTWORTEN — Handlungsbedarf, Entwurf erstellen
- 👀 BEOBACHTEN — relevant, aber kein sofortiger Handlungsbedarf

### Schritt 3 — Entwürfe anlegen
Für alle Mails mit Status ANTWORTEN:
[WENN imap-smtp]: `create_draft(to=..., subject=..., text=...)`
[WENN gmail]: `gmail_create_draft(...)`

Ton: professionell, im Stil der Firma [FIRMENNAME].

### Schritt 4 — Zusammenfassung ausgeben
Tabellarische Übersicht aller Mails mit Klassifizierung und ggf. Link zum Entwurf.
```

---

## PHASE 4b — Inbox-Review Zeitplan & Ordner-Logik

### Schritt 4b.1 — Review-Zeitfenster festlegen

Frage mit **AskUserQuestion**:

> „Wie viele Stunden soll der tägliche Inbox-Review abdecken?"
> - 24 Stunden (empfohlen — ein Review morgens, deckt den Vortag ab)
> - 48 Stunden
> - 72 Stunden
> - Manuell (kein fester Zeitplan)

Wert als `{{INBOX_REVIEW_HOURS}}` in `inbox-review/SKILL.md` eintragen.

### Schritt 4b.2 — Zeitplan einrichten

Frage mit **AskUserQuestion**:

> „Wann soll der Inbox-Review täglich automatisch starten?"
> - Täglich 08:00 Uhr (empfohlen — Arbeitstag mit klarem Posteingang starten)
> - Täglich 07:00 Uhr
> - Täglich abends 18:00 Uhr
> - Manuell (kein automatischer Start)

Falls automatischer Zeitplan gewählt:
→ Scheduled Task via `schedule`-Skill anlegen mit Trigger-Prompt:
  `"Führe den Inbox-Review der letzten {{INBOX_REVIEW_HOURS}} Stunden durch."`
→ Zeitplan als `{{INBOX_REVIEW_SCHEDULE}}` in `inbox-review/SKILL.md` eintragen.

### Schritt 4b.3 — Ordner-Logik einrichten (optional)

Frage mit **AskUserQuestion**:

> „Soll eine intelligente Ordner-Verschiebe-Logik eingerichtet werden?
> Claude liest deine bestehende Ordnerstruktur, leitet Sortierregeln ab und
> verschiebt eingehende Mails automatisch in die richtigen Ordner."
> - Ja, einrichten
> - Nein, überspringen

Falls Ja:
- `inbox-review/ordner-logik/SKILL.md` aus Template anlegen
- In `inbox-review/SKILL.md`: `ORDNER_LOGIK = true` setzen
- Hinweis: Setup-Lauf beim ersten Review-Aufruf — Ordner werden dann live erkannt

---

## PHASE 5 — Meeting-Review (optional)

### Schritt 5.1 — Abfragen ob gewünscht

Frage mit **AskUserQuestion**:
> „Soll Meeting-Review eingerichtet werden? (Besprechungen automatisch nachbereiten, Zusammenfassungen erstellen, Folgeaufgaben anlegen)"
> - Ja, einrichten
> - Nein, überspringen

Falls Nein: weiter mit Phase 5b (Zusammenfassungen) → dann Phase 6.

### Schritt 5.2 — Konfiguration abfragen

Frage mit **AskUserQuestion** (Mehrfachauswahl):
- Kalender verbinden: Google Kalender / Outlook Kalender / Keiner
- Aufgaben-Tool: Notion / keine Aufgabenanbindung

### Schritt 5.3 — Pocket AI (Meeting-Aufzeichnung) — Empfohlen

Erkläre dem Kunden:
> „Mit der **Pocket AI App** (iOS/Android) kannst du Live-Meetings und Telefonate
> aufzeichnen. Claude verbindet sich danach via MCP direkt mit Pocket und zieht
> Transkripte, Zusammenfassungen und Action Items automatisch — kein manuelles
> Copy-Paste. Das ist die empfohlene Lösung für vollständige Meeting-Nachbereitung."

Frage mit **AskUserQuestion**:
> „Soll Pocket AI für Meeting- und Gesprächsaufzeichnung eingerichtet werden?"
> - Ja, empfohlen — Pocket-App installieren + MCP verbinden
> - Nein, ohne Aufzeichnung (nur Kalender-Notizen)

**Falls Ja — Pocket MCP einrichten:**

1. Dem Kunden mitteilen:
   > „Bitte installiere die Pocket AI App auf deinem Smartphone:
   > iOS: https://apps.apple.com/app/pocket-ai/id6504287901
   > Android: https://play.google.com/store/apps/details?id=com.heypocketai.pocket
   > Dann: Pocket → Einstellungen → Developer → API Keys → neuen Key erstellen."

2. Pocket API-Key abfragen (`pk_...`).

3. Pocket MCP in `claude_desktop_config.json` eintragen:
```json
"pocket": {
  "command": "npx",
  "args": [
    "-y",
    "mcp-remote",
    "https://public.heypocketai.com/mcp",
    "--header",
    "Authorization:${AUTH_HEADER}"
  ],
  "env": {
    "AUTH_HEADER": "Bearer {{POCKET_API_KEY}}"
  }
}
```

4. Wert `{{POCKET_ENABLED}} = true` und `{{POCKET_API_KEY}}` in `meeting-review/SKILL.md` eintragen.
5. Hinweis: Nach Claude-Neustart verfügbar. Erste Aufzeichnung mit Pocket-App testen.

### Schritt 5.4 — Meeting-Review-Skill schreiben

Erstelle `Sekretariat/skills/meeting-review/SKILL.md` mit:
- Kalender-Tool je nach Auswahl (gcal_list_events / Outlook)
- Pocket-Integration falls aktiviert (search_pocket_conversations_timerange für gesamten Tag)
- Aufgaben-Erstellung je nach Auswahl (Notion / nur Entwürfe)
- Zusammenfassungsversand via `{{SUMMARY_CHANNEL}}` (wird in Phase 5b gesetzt)
- Autonome Aktionen je nach Wahl in Phase 5c
- Kernfunktionen: Meetings laden → alle Pocket-Transkripte des Tages → zuordnen → Zusammenfassung → autonome Folgeaktionen → Versand

Vorlage aus `templates/Sekretariat/skills/meeting-review/SKILL.md` verwenden und mit Kundenvariablen befüllen.

---

## PHASE 5b — Zusammenfassungsversand konfigurieren

Dieser Schritt gilt für **Inbox-Review-Zusammenfassungen** und **Meeting-Zusammenfassungen**.

### Schritt 5b.1 — Kanal abfragen

Frage mit **AskUserQuestion**:
> „Wohin sollen die täglichen Zusammenfassungen (Inbox-Review, Meeting-Nachbereitung) gesendet werden?"
> - Per E-Mail an mich selbst (empfohlen, funktioniert immer)
> - Slack (Channel oder DM)
> - Microsoft Teams
> - Nur in Claude anzeigen (kein Versand)

Mehrfachauswahl möglich — z.B. E-Mail + Slack.

**Falls E-Mail:**
Ziel-Adresse abfragen (Standard: `{{EMAIL_ADDRESS}}`).
Wert `{{SUMMARY_EMAIL}} = [adresse]` speichern.

**Falls Slack:**
- Prüfen ob Slack MCP verbunden ist (über Claude Desktop Connectors).
- Falls nicht: Anleitung zum Verbinden geben.
- Channel-Name oder DM-Ziel abfragen (z.B. `#general`, `@ich-selbst`).
- Wert `{{SUMMARY_SLACK_CHANNEL}} = [channel]` speichern.
- Wichtig: Zusammenfassungen werden als Miss-Baker-Webhook gesendet falls verfügbar,
  sonst über Slack MCP direkt.

**Falls Teams:**
- Teams-Connector in Claude Desktop verbinden (soweit verfügbar).
- Ziel-Channel abfragen.
- Wert `{{SUMMARY_TEAMS_CHANNEL}} = [channel]` speichern.

### Schritt 5b.2 — E-Mail-Zusammenfassungsordner anlegen (falls E-Mail gewählt)

[WENN summary_channel enthält "email:"]:

Automatisch zwei IMAP-Ordner anlegen, in die Zusammenfassungen verschoben werden:
- **„Morgen-Briefings"** — täglich erstellte Inbox-Review-Zusammenfassungen
- **„Meeting-Zusammenfassungen"** — Meeting-Review-Ergebnisse

**Ordner anlegen:**

[WENN imap-smtp]:
Claude versucht, die Ordner direkt über den IMAP-MCP anzulegen.
Prüfen ob ein Ordner-Erstellungs-Tool verfügbar ist.
Falls nicht: Kunden anweisen:
> „Bitte lege in deinem E-Mail-Programm (Outlook, Thunderbird, Webmailer) manuell
> zwei Ordner an: 'Morgen-Briefings' und 'Meeting-Zusammenfassungen'."

[WENN gmail]:
Gmail-Labels anlegen (entsprechen Ordnern in Gmail):
```
gmail_create_label(name="Morgen-Briefings")
gmail_create_label(name="Meeting-Zusammenfassungen")
```

Nach Anlage:
- In `inbox-review/SKILL.md`: `BRIEFING_FOLDER = "Morgen-Briefings"` eintragen
- In `meeting-review/SKILL.md`: `SUMMARY_FOLDER = "Meeting-Zusammenfassungen"` eintragen
- inbox-review verschiebt die versendete Zusammenfassung nach jedem Run in diesen Ordner
- meeting-review verfährt ebenso

Ziel: Der Benachrichtigungskontakt (aus Schritt 0.3) findet alle Zusammenfassungen
gebündelt in diesen Ordnern — strukturiert und auf einen Blick auffindbar.

### Schritt 5b.3 — Variablen in Skills eintragen

`{{SUMMARY_CHANNEL}}` in beiden Skills setzen:
- `Sekretariat/skills/inbox-review/SKILL.md`
- `Sekretariat/skills/meeting-review/SKILL.md`

Format: `email:[adresse]` / `slack:[channel]` / `teams:[channel]` / `none`
Mehrere Kanäle: kommagetrennt, z.B. `email:chef@firma.de,slack:#posteingang`

Zusätzlich `BENACHRICHTIGUNGS_EMAIL` aus Schritt 0.3 als Standard-Empfänger eintragen,
falls kein abweichender Kanal gewählt wurde.

---

## PHASE 5c — Autonomie-Level in Skills übertragen

Das Autonomie-Level wurde in Phase 0.4 bereits festgelegt.
Dieser Schritt überträgt die Variablen in alle relevanten SKILL.md-Dateien.

### Schritt 5c.1 — Variablen basierend auf Level eintragen

Werte aus `AUTONOMIE_LEVEL` (Schritt 0.4) in die Skills schreiben:

**Level 1 — Beobachter:**
```
AUTONOMOUS_ACTIONS  = false
AUTO_CREATE_DRAFTS  = false
AUTO_CREATE_EVENTS  = false
AUTO_CREATE_TODOS   = false
AUTO_NOTIFY_CONTACT = false
```

**Level 2 — Assistent:**
```
AUTONOMOUS_ACTIONS  = true
AUTO_CREATE_DRAFTS  = true
AUTO_CREATE_EVENTS  = false
AUTO_CREATE_TODOS   = false
AUTO_NOTIFY_CONTACT = false
```

**Level 3 — Autopilot:**
```
AUTONOMOUS_ACTIONS  = true
AUTO_CREATE_DRAFTS  = true
AUTO_CREATE_EVENTS  = true
AUTO_CREATE_TODOS   = true
AUTO_NOTIFY_CONTACT = true
```

Eintragen in:
- `Sekretariat/skills/meeting-review/SKILL.md` — alle fünf Variablen
- `Sekretariat/skills/inbox-review/SKILL.md` — `AUTO_NOTIFY_CONTACT` und `AUTONOMOUS_ACTIONS`

### Schritt 5c.2 — Benachrichtigungskontakt in Skills eintragen

Aus Schritt 0.3 eintragen in beide Skills:
```
BENACHRICHTIGUNGS_NAME     = [NAME]
BENACHRICHTIGUNGS_POSITION = [POSITION]
BENACHRICHTIGUNGS_EMAIL    = [EMAIL]
```

### Schritt 5c.3 — Level in Sekretariat/CLAUDE.md dokumentieren

```markdown
## AUTONOMIE-LEVEL
Level: [1/2/3] — [Beobachter / Assistent / Autopilot]
Benachrichtigungskontakt: [NAME] ([POSITION]) — [EMAIL]
→ Level kann jederzeit in den SKILL.md-Dateien geändert werden.
```

---

## PHASE 6 — CRM-Sync konfigurieren

### Schritt 6.1 — CRM-System abfragen

Frage mit **AskUserQuestion**:
> „Nutzt du ein externes CRM-System?"
> - Nur E-Mail (kein CRM)
> - HubSpot
> - Salesforce
> - Pipedrive
> - Close.io
> - Anderes System

**Falls anderes System:**
> „Bitte nenne den Namen des CRM-Systems und teile die API-Dokumentation oder den API-Endpoint. Hinweis: Für die Vollanbindung muss ein eigener MCP-Connector gebaut werden — das ist ein separates Automatisierungsprojekt."
Notiz in CLAUDE.md: `CRM: [NAME] — MCP-Connector ausstehend`.

**Falls externes CRM gewählt:**
Frage nach API-Key / Token für das gewählte System.

### Schritt 6.2 — CRM-Sync-Skill schreiben

Erstelle `Sekretariat/skills/crm-sync/SKILL.md`:

```markdown
# Skill: CRM-Sync

Synchronisiert Kontakte aus dem E-Mail-Postfach ins Mini-CRM.
CRM-System: [CRM_SYSTEM]
E-Mail-System: [EMAIL_SYSTEM]

## ABLAUF

### Schritt 1 — Neue Kontakte aus E-Mails extrahieren
Suche in den letzten 30 Tagen nach neuen Absendern:
- Alle FROM-Adressen sammeln
- Gegen bestehendes Mini-CRM in Sekretariat/CLAUDE.md abgleichen
- Nur neue Kontakte vorschlagen

### Schritt 2 — Kontakte anreichern
Für jeden neuen Kontakt:
- Name aus E-Mail-Header
- Firma (falls erkennbar aus Domain oder Signatur)
- Letzte E-Mail-Datum
- Thema / Kontext der E-Mail-Konversation

### Schritt 3 — Mini-CRM aktualisieren
Neue Zeilen in die Kontakttabelle in Sekretariat/CLAUDE.md eintragen.

[WENN EXTERNES CRM]:
### Schritt 4 — Mit [CRM_SYSTEM] abgleichen
Neue Kontakte auch im externen CRM anlegen:
- [CRM-SPEZIFISCHE API-ANWEISUNGEN]
```

---

## PHASE 7 — Physischen Brief versenden (optional)

### Schritt 7.1 — Abfragen ob gewünscht

Frage mit **AskUserQuestion**:
> „Soll der physische Briefversand über OB24 eingerichtet werden?"
> - Ja, OB24-Credentials eingeben
> - Nein, überspringen

Falls Nein: weiter mit Phase 8.

### Schritt 7.2 — OB24-Credentials abfragen

> ⚠️ Voraussetzung: Ein OB24-Konto muss **vor der Installation** angelegt werden.
> Registrierung unter: **https://www.onlinebrief24.de** (kostenlose Registrierung, Pay-per-use)
> Nach der Registrierung: Login → Mein Konto → API-Zugangsdaten notieren.

Frage nach:
- OB24 Benutzername (E-Mail-Adresse des OB24-Kontos)
- OB24 Passwort (OB24-Kontopasswort)
- OB24 Job-ID (Briefprodukt-ID aus dem OB24-Dashboard, z.B. 1000 für Standardbrief SW)
- Absenderadresse (Firma, Straße, PLZ, Ort)
- **Testmodus für Installation aktivieren?** (Empfehlung: Ja — kein echter Versand während der Einrichtung)

Werte speichern: `OB24_USERNAME`, `OB24_PASSWORD`, `OB24_JOB_ID`, `OB24_TEST_MODE = true/false`

### Schritt 7.3 — Brief-Skill schreiben

Erstelle `Sekretariat/skills/physischen-brief-versenden/SKILL.md` mit:
- Eingebetteten OB24-Credentials
- Absenderadresse
- Testmodus-Flag
- Anleitung: Brief-PDF generieren → Base64 → OB24-API-POST → Job-ID zurückgeben
- Vorlage aus `templates/` verwenden, Variablen ersetzen.

---

## PHASE 8 — KI-Rechtsassistent einrichten

### Schritt 8.1 — E-Mail-Postfach nach Rechtsthemen durchsuchen

Analysiere die letzten 180 Tage des E-Mail-Postfachs auf:
- Rechtsthemen (Verträge, Mahnungen, Abmahnungen, Kündigungen, Datenschutz, Haftung…)
- Vertragsarten (Dienstleistungsverträge, Kaufverträge, Mietverträge, Arbeitsverträge…)
- Wiederkehrende juristische Formulierungen
- Branchen-spezifische Rechtsgebiete

**Suchbegriffe je nach E-Mail-System:**

[imap-smtp]:
```
search_mails(subject="Vertrag", since_days=180)
search_mails(subject="Mahnung", since_days=180)
search_mails(subject="Kündigung", since_days=180)
search_mails(subject="Abmahnung", since_days=180)
search_mails(subject="Rechnung", since_days=180)
search_mails(subject="Forderung", since_days=180)
```

[gmail]:
```
gmail_search_messages(query="subject:(Vertrag OR Mahnung OR Kündigung OR Abmahnung) newer_than:180d")
```

### Schritt 8.2 — Rechtsgebiete ableiten

Aus den gefundenen E-Mails:
1. Häufige Rechtsthemen extrahieren und gewichten
2. Branchenspezifische Rechtsgebiete ergänzen (aus Schritt 0.2 Branche)
3. Liste der Top-5-Rechtsgebiete dieses Kunden erstellen

Typische Rechtsgebiete je Branche:
- Handwerk: Werkvertragsrecht, VOB, Baurecht, Gewährleistung
- Marketing/Agentur: Urheberrecht, Wettbewerbsrecht, Datenschutz (DSGVO), Dienstleistungsrecht
- IT: Softwarelizenzrecht, Datenschutz, Haftungsrecht, SLA
- Immobilien: Mietrecht, Kaufvertragsrecht, WEG-Recht, Maklerrecht

### Schritt 8.3 — KI-Rechtsassistent CLAUDE.md erstellen

Erstelle `Team/Rechtsassistent/CLAUDE.md`:

```markdown
# KI-Rechtsassistent — [FIRMENNAME]

Du bist der interne Rechtsassistent von [FIRMENNAME] auf Senior-Ebene.
Du hast den Hintergrund eines erfahrenen Rechtsanwalts mit Schwerpunkt auf den
relevanten Rechtsgebieten dieses Unternehmens.

## UNTERNEHMENSPROFIL
- Firma: [FIRMENNAME] ([RECHTSFORM])
- Branche: [BRANCHE]
- Standort: [HAUPTSTANDORT] (deutsches Recht anwendbar)

## DEINE KERNRECHTSGEBIETE
[Aus E-Mail-Analyse und Branche abgeleitet — z.B.:]
1. [RECHTSGEBIET 1] — [Grund: häufig in E-Mails / branchenrelevant]
2. [RECHTSGEBIET 2]
3. [RECHTSGEBIET 3]
4. [RECHTSGEBIET 4]
5. [RECHTSGEBIET 5]

## ARBEITSWEISE
- Führe für jeden Fall eine Akte unter `Fallarchiv/[AKTENZEICHEN]/`
- Aktenzeichen-Format: [JAHR]-[LAUFENDE NUMMER]-[KÜRZEL], z.B. 2026-001-VERTR
- Briefe und Schriftsätze enden mit: "Rechtsabteilung, i.A. der Geschäftsführung, [FIRMENNAME]"
- Immer Disclaimer: Du bist kein zugelassener Rechtsanwalt — bei wesentlichen Entscheidungen Rechtsanwalt hinzuziehen.

## PRÜFERPERSPEKTIVE
Bei Verträgen, Rechnungen und Korrespondenz immer mitdenken:
- Haftungsrisiken für [FIRMENNAME]
- Formvorschriften (Schriftform, Textform)
- Verjährungsfristen
- DSGVO-Konformität

## AKTENFÜHRUNG
Jeder neue Fall bekommt einen Ordner:
```
Fallarchiv/
└── [AKTENZEICHEN]/
    ├── Sachverhalt.md
    ├── Dokumente/
    └── Korrespondenz/
```

## MEMORY SYSTEM
MEMORY.md zu Beginn jeder Session lesen.
Neue Fälle und wichtige Erkenntnisse nur auf explizite Anweisung des Nutzers eintragen.
```

---

## PHASE 9 — Mini-CRM aus Postfach vorbefüllen

### Schritt 9.1 — Kontakte aus 180 Tagen extrahieren

Durchsuche das Postfach der letzten 180 Tage nach eindeutigen Kontakten:

[imap-smtp]:
```python
# Alle Mails der letzten 180 Tage laden
fetch_recent_mails(hours=4320)  # 180 Tage
# Oder:
search_mails(since_days=180)
```

[gmail]:
```
gmail_search_messages(query="newer_than:180d", max_results=200)
```

Für jeden Absender extrahieren:
- Name (aus "From:"-Header)
- E-Mail-Adresse
- Firma (aus Domain oder Signatur, falls erkennbar)
- Letztes Kontaktdatum
- Häufigkeit (wie oft Kontakt?)
- Kontext (was wurde besprochen?)

### Schritt 9.2 — Kontakte deduplicieren und sortieren

- Duplikate zusammenführen (gleiche E-Mail-Adresse)
- Interne Adressen ([FIRMEN-DOMAIN]) herausfiltern
- Sortierung: häufigster Kontakt zuerst
- Top 50 Kontakte für Mini-CRM vorschlagen

### Schritt 9.3 — Mini-CRM eintragen

Mini-CRM-Tabelle in `Sekretariat/CLAUDE.md` befüllen:

```markdown
| Name | Firma | E-Mail | Rolle | Letzter Kontakt | Notizen |
|---|---|---|---|---|---|
| [Name] | [Firma] | [E-Mail] | [Kunde/Lieferant/Sonstiges] | [Datum] | [Kontext] |
```

Den Nutzer nach Rollenklassifizierung fragen wenn unklar.

---

## PHASE 10 — Abschluss & Vollständiger Funktionstest

### Schritt 10.1 — Installations-Checkliste

Prüfe und hake gemeinsam mit dem Mitarbeiter ab:
- [ ] Ordnerstruktur vollständig angelegt
- [ ] Sekretariat/CLAUDE.md ausgefüllt (Firmendaten, Mini-CRM)
- [ ] E-Mail-System verbunden und getestet
- [ ] inbox-review-Skill vorhanden + Zeitplan konfiguriert
- [ ] Ordner-Logik-Skill vorhanden (falls gewählt)
- [ ] crm-sync-Skill vorhanden
- [ ] meeting-review-Skill vorhanden (falls gewählt)
- [ ] brief-versenden-Skill vorhanden (falls gewählt) inkl. build_brief.py
- [ ] KI-Rechtsassistent/CLAUDE.md erstellt mit Rechtsgebieten
- [ ] Mini-CRM mit initialen Kontakten befüllt
- [ ] Post-Requisiten hochgeladen (Logo, Signum) oder als ausstehend markiert

---

### Schritt 10.2 — Funktionstest: E-Mail & CRM

**Test 1 — Posteingang lesen:**
Mitarbeiter gibt ein:
> „Zeig mir die letzten 5 Mails aus meinem Posteingang."

✅ Erwartet: Claude listet 5 Mails mit Absender, Betreff, Datum.
❌ Fehler → IMAP-Verbindung oder MCP prüfen (Troubleshooting Phase).

**Test 2 — Inbox-Review:**
> „Geh durch meinen Posteingang der letzten 24 Stunden."

✅ Erwartet: Claude klassifiziert Mails, erstellt Entwürfe, verschiebt in Papierkorb (kein permanentes Löschen).
❌ Fehler → inbox-review/SKILL.md prüfen, E-Mail-System-Variablen verifizieren.

**Test 3 — CRM:**
> „Wer sind meine 3 häufigsten E-Mail-Kontakte?"

✅ Erwartet: Claude liest Mini-CRM und gibt 3 Namen aus.
❌ Fehler → Sekretariat/CLAUDE.md öffnen, Mini-CRM-Tabelle prüfen.

---

### Schritt 10.3 — Funktionstest: Brief-Layout & Versand

⚠️ Vor diesem Test: Testmodus in `physischen-brief-versenden/SKILL.md` auf `true` prüfen.

**Test 4 — Brief-PDF generieren:**
> „Erstelle einen Testbrief an Max Mustermann, Musterstraße 1, 12345 Musterstadt.
> Inhalt: 'Dies ist ein Testbrief zur Überprüfung des Brieflayouts.'"

✅ Erwartet: Claude generiert ein PDF in `Sekretariat/Postausgang/`, öffnet es zur Prüfung.

Mitarbeiter prüft visuell:
- [ ] Logo oben rechts vorhanden (falls hochgeladen)
- [ ] Firmendaten korrekt
- [ ] Empfängeradresse DIN 5008 korrekt positioniert
- [ ] Datum rechtsbündig
- [ ] Betreff fett, korrekt umgebrochen
- [ ] Ränder ausreichend (links/rechts/unten mind. 57pt)
- [ ] Grußformel + Signum vorhanden (falls hochgeladen)

**Test 5 — OB24 Preisabfrage:**
> „Sende den Testbrief als physischen Brief."

✅ Erwartet: Claude ruft erst den Preis ab und zeigt ihn an (z.B. „Der Brief kostet 1,29 €").
Claude wartet auf Bestätigung — **nicht automatisch senden**.
❌ Fehler → OB24-Credentials in brief-versenden/SKILL.md prüfen.

**Test 6 — OB24 Versand im Testmodus (nach Bestätigung):**
Mitarbeiter bestätigt mit „ja, sende im Testmodus".

Vor dem Versand prüfen: Claude zeigt den Testmodus-Status aus dem Skill-Header an:
> „⚠️ Testmodus aktiv (`OB24_TEST_MODE = true`) — der Brief wird NICHT physisch gedruckt oder versendet.
>  OB24 bestätigt den Auftrag, stellt aber keine Kosten in Rechnung."

Falls `OB24_TEST_MODE = false` eingetragen ist: Claude fragt explizit nach:
> „Der Testmodus ist aktuell DEAKTIVIERT. Soll dieser Versand trotzdem als Testversand ausgeführt werden
>  (einmaliger Test, kein echter Versand), oder soll der Brief wirklich versendet werden?"

✅ Erwartet: Claude sendet im Testmodus, gibt Bestätigung oder Tracking-ID zurück, trägt in log.md ein.
Eintrag in `Postausgang/log.md` prüfen (Spalte „TEST J/N" muss „J" zeigen).

Nach erfolgreichem Test:
> „✅ OB24-Testversand erfolgreich. Zum Aktivieren des Livemodus:
>  In `Sekretariat/skills/physischen-brief-versenden/SKILL.md` `OB24_TEST_MODE` auf `false` setzen."

---

### Schritt 10.4 — Funktionstest: KI-Rechtsassistent

**Test 7 — Rechtsgebiete:**
> „Was sind die wichtigsten Rechtsgebiete für unser Unternehmen?"

✅ Erwartet: KI-Rechtsassistent listet die während Installation erkannten Rechtsgebiete mit Begründung.

**Test 8 — Formelles Schreiben generieren (falls brief-versenden installiert):**
> „Erstelle einen kurzen Formelles Schreiben an Max Mustermann wegen eines offenen Betrags von 500 €.
> Lege eine neue Akte an."

✅ Erwartet:
- Neue Akte in `Team/Rechtsassistent/Fallarchiv/[AKTENZEICHEN]/` angelegt
- Brief mit Aktenzeichen im Briefkopf generiert
- Abschluss: „Rechtsabteilung, i.A. der Geschäftsführung · {{FIRMENNAME}}"

---

### Schritt 10.5 — Scheduled Tasks anlegen

Jetzt da alle Skills und Zeitpläne konfiguriert sind, Scheduled Tasks einrichten.

Frage mit **AskUserQuestion**:
> „Sollen die automatischen Zeitpläne jetzt direkt eingerichtet werden?"
> - Ja, jetzt einrichten (empfohlen)
> - Nein, ich mache das später manuell

**Falls Ja:**

[WENN Inbox-Review-Zeitplan konfiguriert (aus Phase 4b.2)]:
Scheduled Task für Inbox-Review anlegen via `schedule`-Skill:
- Trigger-Zeit: `{{INBOX_REVIEW_SCHEDULE}}` (z.B. täglich 08:00)
- Prompt: „Führe den Inbox-Review der letzten {{INBOX_REVIEW_HOURS}} Stunden durch.
  Nutze den Skill unter `Sekretariat/skills/inbox-review/SKILL.md`."
- Skill-Referenz dynamisch:
  ```bash
  SKILL_PATH=$(find /sessions -name "SKILL.md" -path "*/inbox-review/SKILL.md" 2>/dev/null | head -1)
  ```

[WENN Meeting-Review konfiguriert]:
Scheduled Task für Meeting-Review anlegen:
- Trigger-Zeit: täglich 19:00 Uhr (nach Arbeitsende — deckt alle Meetings des Tages ab)
  Oder: vom Kunden gewünschte Uhrzeit abfragen.
- Prompt: „Führe den Meeting-Review für den heutigen Tag durch.
  Nutze den Skill unter `Sekretariat/skills/meeting-review/SKILL.md`."
- Skill-Referenz dynamisch:
  ```bash
  SKILL_PATH=$(find /sessions -name "SKILL.md" -path "*/meeting-review/SKILL.md" 2>/dev/null | head -1)
  ```

Beide Tasks in ÜBERGABE.md dokumentieren (Zeitplan + manueller Trigger-Befehl).

---

### Schritt 10.6 — Übergabenotiz erstellen

Erstelle `ÜBERGABE.md` im Hauptordner:

```markdown
# Cleo — Übergabe [FIRMENNAME]
Installiert am: [DATUM]
Installiert von: {{INSTALLATIONSPARTNER}}

## Eingerichtete Komponenten
- E-Mail-System: [EMAIL_SYSTEM] ([EMAIL_ADDRESS])
- CRM-System: [CRM_SYSTEM]
- Autonomie-Level: [1/2/3] — [Beobachter / Assistent / Autopilot]
- Benachrichtigungskontakt: [NAME] ([POSITION]) — [EMAIL]
- Meeting-Review: [JA/NEIN] | Pocket AI: [JA/NEIN]
- Briefversand (OB24): [JA/NEIN]
- E-Mail-Ordner: Morgen-Briefings / Meeting-Zusammenfassungen [JA/NEIN]

## Automatische Zeitpläne
- Inbox-Review: täglich [UHRZEIT] Uhr
- Meeting-Review: täglich [UHRZEIT] Uhr

## Erste Schritte für den Nutzer
1. Claude Desktop öffnen
2. Cowork-Ordner auswählen
3. Sagen: "Zeig mir meine letzten Mails"
4. Sagen: "Geh durch meinen Posteingang"

## Manueller Aufruf (ohne Zeitplan)
- Inbox-Review: "Geh durch meinen Posteingang der letzten 24 Stunden"
- Meeting-Review: "Bereite meine heutigen Meetings nach"

## Offene Punkte
[Alle noch ausstehenden Items hier eintragen]

## Support
Bei Fragen: {{INSTALLATIONSPARTNER}} — {{SUPPORT_KONTAKT}}
```

→ **Weiter mit Phase 11 — Willkommens-Sequenz.**

---

## PHASE 11 — Willkommens-Sequenz: Cleo live erleben

Nach erfolgreichem Abschluss von Phase 10 (inkl. Übergabenotiz) startet automatisch die Onboarding-Sequenz. Kein Klick, kein Befehl nötig — sie läuft direkt im Anschluss.

Sage zum Auftakt:

> „Perfekt — Installation abgeschlossen. 🎉
> Ich zeige dir jetzt in 5 kurzen Nachrichten, wie Cleo in deinem Alltag aussehen wird.
> Einfach lesen, staunen — und danach direkt loslegen."

Kurze Pause (1–2 Sätze), dann Nachricht 1:

---

### Nachricht 1 — So wird dein morgendliches Briefing aussehen

Präsentiere ein vollständiges Demo-Briefing — basierend auf den echten Firmen- und Konfigurationsdaten aus der Installation. Zahlen sind Demo-Werte, Struktur ist 1:1 die echte.

> 🌅 **Guten Morgen, {{BENACHRICHTIGUNGS_NAME}}** — [heutiges Datum]
>
> ────────────────────────────────
> 📬 **Posteingang** — 12 neue Mails seit gestern 18:00 Uhr
> ├─ ✅ 3 erledigt (Auto-Archiviert)
> ├─ 💬 4 brauchen eine Antwort → Entwürfe liegen bereit
> ├─ 🗑️ 3 gelöscht (Newsletter / Spam)
> ├─ ✉️ 1 Mahnung → Physischer Brief empfohlen
> └─ 📁 1 archiviert (FYI, kein Handlungsbedarf)
>
> 📅 **Dein heutiger Tag** — 3 Termine
> ├─ 09:30 Kundengespräch Müller GmbH
> ├─ 11:00 Team-Meeting (Protokoll kommt heute Abend)
> └─ 14:00–16:00 Focus-Zeit (geblockt, keine Meetings)
>
> 🔔 **3 offene Aufgaben von gestern**
> ├─ Angebot Müller GmbH bis Freitag nachfassen
> ├─ Eingangsrechnung Lieferant X prüfen
> └─ Datenschutzbeauftragten kontaktieren
>
> Gib einfach ein: *„Geh durch meinen Posteingang"* — ich erledige den Rest.
> ────────────────────────────────
>
> _(Dein echtes Briefing startet täglich um {{INBOX_REVIEW_SCHEDULE}} automatisch.)_

---

### Nachricht 2 — So wird deine Tages-Nachbereitung aussehen

Kurze Überleitung:
> „Und abends, wenn der Tag vorbei ist, läuft die Nachbereitung — ohne dass du etwas tust:"

Präsentiere eine Demo-Nachbereitung mit fiktivem aber realistischem Inhalt:

> 🌙 **Tages-Nachbereitung — [heutiges Datum]**
>
> ────────────────────────────────
> **📞 Kundengespräch: Müller GmbH** (09:30–10:15)
> 📋 Besprochen: Paket L, Starttermin Mai, offene Preisfrage
> ✅ Task: Angebot bis Fr. 17:00 → Kalender-Block Do 14:00 angelegt
> 💬 E-Mail-Entwurf bereit: „Vielen Dank für unser Gespräch heute..."
> 📇 CRM: Müller GmbH → Warm Lead, nächster Kontakt: Freitag
>
> **👥 Team-Meeting** (11:00–12:00)
> 📋 Sprint-Planung, 3 neue Tasks verteilt
> ✅ 2 Web-Tasks an Davit weitergeleitet
> 📄 Protokoll gespeichert: `Team/Meeting-Notes/[Datum].md`
>
> **📊 Tages-Bilanz:**
> 12 Mails bearbeitet · 4 Entwürfe · 2 Tasks erledigt · 1 Brief in Warteschlange
> ────────────────────────────────
>
> _(Meeting-Review läuft täglich automatisch um {{MEETING_REVIEW_SCHEDULE}} Uhr.)_

---

### Nachricht 3 — So würde ein Brief aussehen

[NUR AUSFÜHREN WENN `brief-versenden`-Modul während Installation eingerichtet wurde]

Überleitung:
> „Und jetzt das Beste: Ich kann echte physische Briefe verschicken. Ich zeige es dir — im Testmodus, kostenlos."

**Erstelle jetzt einen echten Demo-Brief im OB24-Testmodus:**

Empfänger:
```
Max Mustermann
Musterstraße 1
12345 Musterstadt
```

Betreff: `Cleo ist aktiv — eine kurze Mitteilung`

Brieftext:
```
Sehr geehrter Herr Mustermann,

dies ist eine automatische Demonstration von Cleo —
dem digitalen Sekretariat von {{FIRMENNAME}}.

Dieser Brief wurde vollautomatisch erstellt, in korrektem DIN-5008-Layout
gerendert und an OnlineBrief24 übermittelt — ohne dass ein Mensch auch nur
eine Zeile getippt hat.

Genau das macht Cleo für {{FIRMENNAME}}: Briefe, E-Mails
und Aufgaben — erledigt, bevor Sie fragen.

Mit freundlichen Grüßen
{{ASSISTENT_NAME}} · Digitales Sekretariat
{{FIRMENNAME}}
```

Führe `physischen-brief-versenden/SKILL.md` aus — Testmodus erzwingen (`OB24_TEST_MODE = true`).

Nach erfolgreichem Versand:
> ✉️ **Brief-Demo abgeschlossen.**
>
> Der Brief liegt als Testauftrag in deinem OB24-Konto —
> dort kannst du Layout, Adressierung und Inhalt prüfen, bevor je ein echter Brief rausgeht.
>
> 👉 [OB24-Dashboard öffnen → Aufträge](https://www.onlinebrief24.de/account/orders)
>
> _(Um echte Briefe zu versenden: `OB24_TEST_MODE` in `physischen-brief-versenden/SKILL.md` auf `false` setzen.)_

Falls `brief-versenden` nicht installiert:
> „Das Brief-Modul ist bei dir nicht eingerichtet — bei Bedarf kann es jederzeit nachinstalliert werden."

---

### Nachricht 4 — So viel Zeit wirst du sparen

Berechne jetzt die personalisierte Zeitersparnis auf Basis der Werte aus Schritt 0.2.3.

**Berechnungsformel:**

```
X_INBOX    = EMAILS_PRO_TAG × 2                          [Minuten/Tag durch Inbox-Review]
X_MEETING  = (TERMINE_PRO_WOCHE × 15) / 5               [Minuten/Tag durch Meeting-Review]
X_BRIEF    = (BRIEFE_PRO_MONAT × 45) / 22               [Minuten/Tag durch Brief-Automatisierung]
X_CRM      = 15                                          [Minuten/Tag Kontaktpflege, fest]

GESAMT_MIN = MAX(60, ROUND(X_INBOX + X_MEETING + X_BRIEF + X_CRM))
GESAMT_H   = GESAMT_MIN / 60  (auf 0.5 runden)
MONAT_H    = GESAMT_H × 22   (Arbeitstage)
WERT_MONAT = MONAT_H × STUNDENSATZ
```

Mindest-Ersparnis: **60 Minuten/Tag** — nie darunter ausgeben.

Präsentiere als persönliche Kalkulation:

> ⏱️ **So viel Zeit gewinnst du zurück — jeden Tag:**
>
> ────────────────────────────────
> 📬 Posteingang & E-Mails:     ~{{X_INBOX}} Min/Tag  ({{EMAILS_PRO_TAG}} Mails tägl.)
> 📅 Meeting-Nachbereitung:     ~{{X_MEETING}} Min/Tag ({{TERMINE_PRO_WOCHE}} Termine/Woche)
> ✉️ Briefversand & Layout:     ~{{X_BRIEF}} Min/Tag  ({{BRIEFE_PRO_MONAT}} Briefe/Monat)
> 📇 CRM & Kontaktpflege:       ~15 Min/Tag  (läuft automatisch mit)
>
> **Gesamt: ~{{GESAMT_MIN}} Minuten pro Tag = {{GESAMT_H}} Stunden täglich**
>
> Das sind **{{MONAT_H}} Stunden pro Monat** — die du stattdessen in
> Akquise, Strategie oder einfach Feierabend investieren kannst.
>
> Bei einem Stundenwert von {{STUNDENSATZ}} €:
> **{{WERT_MONAT}} € Mehrwert pro Monat.**
>
> _(Konservative Schätzung. Erfahrungswerte aus echten Installationen liegen oft höher.)_
> ────────────────────────────────

---

### Nachricht 5 — Willkommen in einer neuen Ära

Abschlussnachricht — persönlich, nicht generisch. Ton: kollegial, ein bisschen stolz, ehrlich.

> 🚀 **Viel Spaß beim Benutzen — willkommen in einer neuen Ära.**
>
> ────────────────────────────────
> **Du kannst mich weiterentwickeln und trainieren.**
> Jede `SKILL.md`, jede `CLAUDE.md` ist lesbar, editierbar, erweiterbar.
> Neue Fähigkeit gewünscht? Sag es mir — ich zeige dir, wie es geht.
>
> **Ich ersetze nahezu vollständig ChatGPT.**
> Kein Copy-Paste mehr zwischen Tools. Alles passiert hier —
> mit deinen echten Daten, deinen echten E-Mails, deinen echten Terminen.
> Und ich lerne mit jedem Gespräch dazu.
>
> **Deine Daten bleiben bei dir.**
> Keine Cloud-Synchronisation, keine Weitergabe, kein Datenschutzrisiko.
> Deine Dokumente und E-Mails verlassen deinen Arbeitsordner nicht.
>
> **Wie du morgen früh startest:**
> → Claude Desktop öffnen
> → Sagen: *„Zeig mir mein Briefing für heute"*
> → Erleben, was ein KI-Sekretariat bedeutet.
>
> Bei Fragen, Erweiterungswünschen oder wenn etwas nicht klappt:
> {{INSTALLATIONSPARTNER}} · {{SUPPORT_KONTAKT}}
>
> — {{ASSISTENT_NAME}}, dein digitales Sekretariat bei {{FIRMENNAME}}
> ────────────────────────────────

---

**Nach der Sequenz:**

Warte kurz, dann frage:
> „Das war dein persönliches Onboarding. Gibt es Fragen zu einem der Features?"

Falls keine Fragen → Session offiziell beenden.
Falls Fragen → beantworten, dann beenden.

---

## FEHLERBEHANDLUNG

| Problem | Ursache | Lösung |
|---|---|---|
| IMAP-Verbindung schlägt fehl | Falsches Passwort / Host | Credentials prüfen, ggf. App-Passwort bei Gmail/O365 erstellen |
| E-Mail-Scan liefert keine Mails | Ordner leer oder Zeitraum zu kurz | `since_days` erhöhen, anderen Ordner prüfen |
| OB24 schlägt fehl | Falscher API-Key oder Job-ID | OB24-Dashboard prüfen, Testmodus aktivieren |
| Rechtsgebiete nicht erkennbar | Zu wenig juristische E-Mails | Branchen-Defaults verwenden + manuell ergänzen |
| Kein Postfach vorhanden | Neues Unternehmen | Mini-CRM leer lassen, Hinweis für spätere Befüllung |
