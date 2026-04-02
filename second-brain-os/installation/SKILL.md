# Skill: Second Brain OS — Installation

Vollständiger Installationsflow für Second Brain OS beim Kunden. Führt Schritt für Schritt durch alle Phasen — von der ersten Frage bis zum fertigen, einsatzbereiten Arbeitsplatz.

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
│   └── Firmenanwalt/
│       ├── CLAUDE.md       ← aus E-Mail-Scan befüllen (Phase 8)
│       ├── MEMORY.md       ← leer anlegen
│       └── Fallarchiv/     ← Ordner für Akten
└── MEMORY.md               ← leer anlegen (falls noch nicht vorhanden)
```

### Schritt 2.2 — Sekretariat/CLAUDE.md befüllen

Schreibe `Sekretariat/CLAUDE.md` mit folgenden Abschnitten:

```markdown
# Sekretariat — [FIRMENNAME]

Du bist das digitale Sekretariat von [FIRMENNAME]. Du arbeitest für [ANSPRECHPARTNER].

## KONTEXT
- Firma: [FIRMENNAME] ([RECHTSFORM])
- Branche: [BRANCHE]
- Standort: [HAUPTSTANDORT]
- E-Mail-System: [EMAIL_SYSTEM]
- E-Mail-Adresse: [EMAIL_ADDRESS]

## MINI-CRM — KONTAKTE
<!-- Wird in Phase 9 aus dem E-Mail-Postfach befüllt -->
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

Falls Nein: weiter mit Phase 6.

### Schritt 5.2 — Konfiguration abfragen

Frage mit **AskUserQuestion** (mehrfachauswahl):
- Kalender verbinden: Google Kalender / Outlook Kalender / Keiner
- Aufgaben-Tool: Notion / keine Aufgabenanbindung

### Schritt 5.3 — Meeting-Review-Skill schreiben

Erstelle `Sekretariat/skills/meeting-review/SKILL.md` mit:
- Kalender-Tool je nach Auswahl (gcal_list_events / Outlook)
- Aufgaben-Erstellung je nach Auswahl (Notion / nur Entwürfe)
- Mailentwürfe für Kunden-Zusammenfassungen via [EMAIL_SYSTEM]
- Kernfunktionen: Meetings laden → klassifizieren → Zusammenfassung → Entwurf → ggf. Aufgabe anlegen

Vorlage aus `templates/Sekretariat/skills/meeting-review/SKILL.md` verwenden und mit Kundenvariablen befüllen.

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

Frage nach:
- OB24 API-Key
- OB24 Job-ID (Briefprodukt, z.B. Standardbrief SW oder Farbe)
- Absenderadresse (Firma, Straße, PLZ, Ort)
- Testmodus aktivieren? (ja/nein)

### Schritt 7.3 — Brief-Skill schreiben

Erstelle `Sekretariat/skills/physischen-brief-versenden/SKILL.md` mit:
- Eingebetteten OB24-Credentials
- Absenderadresse
- Testmodus-Flag
- Anleitung: Brief-PDF generieren → Base64 → OB24-API-POST → Job-ID zurückgeben
- Vorlage aus `templates/` verwenden, Variablen ersetzen.

---

## PHASE 8 — Firmenanwalt einrichten

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

### Schritt 8.3 — Firmenanwalt CLAUDE.md erstellen

Erstelle `Team/Firmenanwalt/CLAUDE.md`:

```markdown
# Firmenanwalt — [FIRMENNAME]

Du bist der interne Firmenanwalt von [FIRMENNAME] auf Senior-Ebene.
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
- [ ] Firmenanwalt/CLAUDE.md erstellt mit Rechtsgebieten
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
Mitarbeiter bestätigt mit „ja".

✅ Erwartet: Claude sendet im Testmodus, gibt Tracking-ID zurück, trägt in log.md ein.
Eintrag in `Postausgang/log.md` prüfen.

---

### Schritt 10.4 — Funktionstest: Firmenanwalt

**Test 7 — Rechtsgebiete:**
> „Was sind die wichtigsten Rechtsgebiete für unser Unternehmen?"

✅ Erwartet: Firmenanwalt listet die während Installation erkannten Rechtsgebiete mit Begründung.

**Test 8 — Anwaltsbrief generieren (falls brief-versenden installiert):**
> „Erstelle einen kurzen Anwaltsbrief an Max Mustermann wegen eines offenen Betrags von 500 €.
> Lege eine neue Akte an."

✅ Erwartet:
- Neue Akte in `Team/Firmenanwalt/Fallarchiv/[AKTENZEICHEN]/` angelegt
- Brief mit Aktenzeichen im Briefkopf generiert
- Abschluss: „Rechtsabteilung, i.A. der Geschäftsführung · {{FIRMENNAME}}"

---

### Schritt 10.5 — Übergabenotiz erstellen

Erstelle `ÜBERGABE.md` im Hauptordner:

```markdown
# Second Brain OS — Übergabe [FIRMENNAME]
Installiert am: [DATUM]
Installiert von: {{INSTALLATIONSPARTNER}}

## Eingerichtete Komponenten
- E-Mail-System: [EMAIL_SYSTEM] ([EMAIL_ADDRESS])
- CRM-System: [CRM_SYSTEM]
- Meeting-Review: [JA/NEIN]
- Briefversand (OB24): [JA/NEIN]

## Erste Schritte für den Nutzer
1. Claude Desktop öffnen
2. Cowork-Ordner auswählen
3. Sagen: "Zeig mir meine letzten Mails"
4. Sagen: "Geh durch meinen Posteingang"

## Offene Punkte
[Alle noch ausstehenden Items hier eintragen]

## Support
Bei Fragen: {{INSTALLATIONSPARTNER}} — {{SUPPORT_KONTAKT}}
```

---

## FEHLERBEHANDLUNG

| Problem | Ursache | Lösung |
|---|---|---|
| IMAP-Verbindung schlägt fehl | Falsches Passwort / Host | Credentials prüfen, ggf. App-Passwort bei Gmail/O365 erstellen |
| E-Mail-Scan liefert keine Mails | Ordner leer oder Zeitraum zu kurz | `since_days` erhöhen, anderen Ordner prüfen |
| OB24 schlägt fehl | Falscher API-Key oder Job-ID | OB24-Dashboard prüfen, Testmodus aktivieren |
| Rechtsgebiete nicht erkennbar | Zu wenig juristische E-Mails | Branchen-Defaults verwenden + manuell ergänzen |
| Kein Postfach vorhanden | Neues Unternehmen | Mini-CRM leer lassen, Hinweis für spätere Befüllung |
