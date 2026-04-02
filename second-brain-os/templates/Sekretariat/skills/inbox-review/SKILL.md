# Skill: Inbox-Review
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Scannt den Posteingang, klassifiziert jede Mail und erstellt Entwürfe für alles,
was eine Antwort braucht. Zu löschende und Spam-Mails werden in den Papierkorb
verschoben (kein permanentes Löschen). Alte Entwürfe (>30 Tage) werden bereinigt.

E-Mail-System:          {{EMAIL_SYSTEM}}
Firma:                  {{FIRMENNAME}}
Review-Zeitfenster:     {{INBOX_REVIEW_HOURS}}h (Standard: 24)
Zeitplan:               {{INBOX_REVIEW_SCHEDULE}}
Zusammenfassung an:     {{SUMMARY_CHANNEL}}
Briefings-Ordner:       {{BRIEFING_FOLDER}}
Autonomie-Level:        {{AUTONOMOUS_ACTIONS}}
Benachricht. Kontakt:   {{BENACHRICHTIGUNGS_NAME}} ({{BENACHRICHTIGUNGS_POSITION}}) — {{BENACHRICHTIGUNGS_EMAIL}}
Kontakt benachricht.:   {{AUTO_NOTIFY_CONTACT}}

---

## ABLAUF

### Schritt 0 — Alte Entwürfe bereinigen

Vor dem eigentlichen Review den Entwürfe-Ordner aufräumen:

[WENN imap-smtp]:
```
search_mails(folder="DRAFTS", since_days=999, older_than_days=30)
```
Alle Treffer (Entwürfe die älter als 30 Tage sind) in Papierkorb verschieben:
`delete_mail(uid=UID, folder="DRAFTS", permanent=False)`

[WENN gmail]:
```
gmail_search_messages(query="in:drafts older_than:30d")
```
Für jeden Treffer: Gmail TRASH-Label hinzufügen (nicht permanent löschen):
`gmail_add_label(message_id=ID, label="TRASH")`

Hinweis ausgeben: „🗂️ [N] veraltete Entwürfe (>30 Tage) in den Papierkorb verschoben."
Falls keine veralteten Entwürfe: „✅ Keine veralteten Entwürfe gefunden."

---

### Schritt 1 — Posteingang laden

[WENN imap-smtp]:
`fetch_recent_mails(hours={{INBOX_REVIEW_HOURS}})` — Mails der letzten N Stunden.
Für zusätzliche ungelesene Mails aus längerem Zeitraum:
`search_mails(unread_only=True, since_days=7)`

[WENN gmail]:
`gmail_search_messages(query="is:unread newer_than:{{INBOX_REVIEW_HOURS}}h")`
Zusätzlich: `gmail_search_messages(query="is:unread newer_than:7d")` für ältere ungelesene.

[WENN office365 / imap]:
`fetch_recent_mails(hours={{INBOX_REVIEW_HOURS}})`

### Schritt 2 — Jede Mail klassifizieren

| Kategorie | Kriterium | Aktion |
|---|---|---|
| 🚫 SPAM | Eindeutige Spam-Merkmale: unbekannte Absender-Domain, Massenversand, verdächtige Links, Phishing-Anzeichen, keine direkte Adressierung | → Papierkorb (nie permanent löschen) |
| 🗑️ PAPIERKORB | Werbung, Newsleter ohne Mehrwert, automatische System-Benachrichtigungen ohne Relevanz, One-Click-Unsubscribe-Kandidaten | → Papierkorb |
| 📁 ARCHIVIEREN | Informationsmail, erledigt, kein Handlungsbedarf, Bestätigungen | → Archivieren |
| ✅ ANTWORTEN | Direkte Frage, Auftrag, Anfrage, Kundenkommunikation — Antwort per E-Mail sinnvoll | → Entwurf anlegen |
| ✉️ BRIEF | Formelles Schreiben angemessener als E-Mail: Mahnung, Kündigung, Rechtsthemen, Behördenkommunikation, Vertragsangelegenheiten, Situationen wo Schriftform gesetzlich oder dokumentarisch erforderlich | → Brief-Vorschlag erstellen |
| 📂 VERSCHIEBEN | Mail gehört in einen bestimmten Ordner (→ Ordner-Logik-Skill) | → Ordner-Logik |
| 👀 BEOBACHTEN | Relevant, aber kein sofortiger Handlungsbedarf | → Markieren |

**Spam-Erkennung — Signale:**
- Absender-Domain nicht im Mini-CRM und völlig unbekannt
- Betreff enthält typische Spam-Phrasen (Gewinn, Erbschaft, Dringend, Kreditangebot…)
- Keine persönliche Anrede oder nur generische Ansprache
- Vollständig bildbasierte Mail ohne Text
- Viele Links zu unbekannten Domains
- SPF/DKIM-Fehler (falls vom E-Mail-System gemeldet)

Wichtig: Im Zweifelsfall lieber 👀 BEOBACHTEN als automatisch in Papierkorb — Spam-Filter
soll konservativ agieren, um keine echten Mails zu verlieren.

### Schritt 3 — Entwürfe und Brief-Vorschläge erstellen

**3a — E-Mail-Entwürfe (Status ✅ ANTWORTEN):**

Für alle Mails mit Status ✅ ANTWORTEN einen Mailentwurf anlegen.
Ton: professionell, freundlich, im Stil von {{FIRMENNAME}}.
Länge: so kurz wie möglich, so ausführlich wie nötig.

[WENN imap-smtp]:
`create_draft(to=ABSENDER, subject="Re: "+BETREFF, text=ENTWURFSTEXT)`

[WENN gmail]:
`gmail_create_draft(to=ABSENDER, subject="Re: "+BETREFF, body=ENTWURFSTEXT)`

**3b — Brief-Vorschläge (Status ✉️ BRIEF):**

Für alle Mails mit Status ✉️ BRIEF:

1. Briefinhalt vorbereiten:
   - Empfänger: Name, Firma, Adresse (aus CRM oder Mail-Signatur entnehmen)
   - Betreff: formell, präzise
   - Brieftext: professionell, rechtssicher formuliert, DIN 5008-konform

2. In der Zusammenfassung ausgeben:
   ```
   ✉️ BRIEF-VORSCHLAG: [BETREFF]
   An: [EMPFÄNGER, ADRESSE falls bekannt]
   Inhalt: [2-3 Sätze Zusammenfassung]
   → Soll ich diesen Brief über OB24 versenden?
   ```

3. Falls `physischen-brief-versenden`-Skill installiert:
   → Briefdaten bereitstellen, Nutzer bestätigt → `physischen-brief-versenden`-Skill aufrufen
   → NICHT automatisch versenden — immer auf explizite Bestätigung warten

4. Falls Brief-Skill nicht installiert:
   → Briefentwurf als Text ausgeben + Hinweis:
   `„Brief-Versand via OB24 nicht eingerichtet — Text kann manuell verwendet werden."`

### Schritt 4 — Papierkorb & Archiv

🚫 SPAM und 🗑️ PAPIERKORB → Mail in Papierkorb verschieben, NIEMALS permanent löschen:

[WENN imap-smtp]:
`delete_mail(uid=UID, folder="INBOX", permanent=False)`
→ verschiebt in FOLDER_TRASH ({{FOLDER_TRASH}}), kein unwiderrufliches Löschen.
→ Gilt für SPAM und PAPIERKORB gleichermaßen.

[WENN gmail]:
Label TRASH hinzufügen: `gmail_add_label(message_id=ID, label="TRASH")`
→ Gilt für SPAM und PAPIERKORB gleichermaßen.

Spam-Mails NIE mit `permanent=True` löschen — der Kunde soll jederzeit
nachschauen können, falls eine legitime Mail fälschlicherweise als Spam erkannt wurde.

📁 ARCHIVIEREN:

[WENN imap-smtp]:
`archive_mail(uid=UID, folder="INBOX")`

[WENN gmail]:
INBOX-Label entfernen (archiviert in All Mail).

### Schritt 5 — Ordner-Logik (optional)

[WENN ORDNER_LOGIK = true]:
Für alle Mails mit Status 📂 VERSCHIEBEN den Ordner-Logik-Skill aufrufen:
→ `Sekretariat/skills/inbox-review/ordner-logik/SKILL.md`

### Schritt 6 — Zusammenfassung ausgeben, versenden & ablegen

Tabellarische Übersicht aller bearbeiteten Mails:

| Absender | Betreff | Klassifizierung | Aktion |
|---|---|---|---|
| ... | ... | ✅ ANTWORTEN | Entwurf erstellt |
| ... | ... | ✉️ BRIEF | Brief-Vorschlag (OB24) |
| ... | ... | 📁 ARCHIVIEREN | Archiviert |
| ... | ... | 🗑️ PAPIERKORB | In Papierkorb |
| ... | ... | 🚫 SPAM | In Papierkorb |

Falls ✉️ BRIEF-Vorschläge vorhanden: Diese nach der Tabelle separat als Block ausgeben:
```
────────────────────────────────────────
✉️ BRIEF-VORSCHLÄGE (X Briefe)
────────────────────────────────────────
1. An: [EMPFÄNGER] | Betreff: [BETREFF]
   Grund: [Warum physischer Brief empfohlen]
   → „brief versenden" um Brief via OB24 zu senden
────────────────────────────────────────
```

Kurzfassung: „X Entwürfe · Y Briefe · Z archiviert · W Papierkorb · V Spam"

Zusammenfassung an `{{SUMMARY_CHANNEL}}` senden:

[WENN summary_channel enthält "email:"]:
Mailentwurf mit Inbox-Zusammenfassung anlegen:
- Empfänger: `{{BENACHRICHTIGUNGS_EMAIL}}` (falls nicht anders konfiguriert)
- Betreff: „Morgen-Briefing [DATUM] — [X] Mails bearbeitet"
- Inhalt: Tabelle + Entwurfs-Hinweise
[WENN imap-smtp]: `create_draft(to={{BENACHRICHTIGUNGS_EMAIL}}, subject=..., text=...)`
[WENN gmail]: `gmail_create_draft(to={{BENACHRICHTIGUNGS_EMAIL}}, ...)`

Zusammenfassung nach Versand / Erstellung in Ordner ablegen:
[WENN {{BRIEFING_FOLDER}} gesetzt]:
→ Erstellten Entwurf/gesendete Mail in Ordner `{{BRIEFING_FOLDER}}` (z.B. "Morgen-Briefings") verschieben:
[WENN imap-smtp]: `archive_mail(uid=UID, folder="Morgen-Briefings")`
[WENN gmail]: entsprechendes Label hinzufügen

[WENN summary_channel enthält "slack:"]:
Slack-Nachricht an `{{SUMMARY_SLACK_CHANNEL}}`:
Kurz-Zusammenfassung: Anzahl pro Kategorie + Hinweis auf erstellte Entwürfe.

[WENN summary_channel = "none"]:
Nur in Claude ausgeben, kein Versand.

[WENN AUTO_NOTIFY_CONTACT = true]:
Falls Benachrichtigungskontakt von Zusammenfassung abweicht oder zusätzlich benachrichtigt
werden soll: separaten kurzen Hinweis an `{{BENACHRICHTIGUNGS_EMAIL}}` senden:
- Betreff: „Morgen-Briefing bereit — [X] Mails, [Y] Entwürfe"
- Inhalt: Kurzübersicht der wichtigsten Punkte (max. 5 Zeilen)

### Schritt 7 — CRM-Hinweis

Falls neue Absender erkannt werden, die noch nicht im Mini-CRM stehen:
> „X neue Kontakte gefunden — soll ich crm-sync ausführen?"

---

## INSTALLATIONSABFRAGEN
# Diese Fragen werden während der Installation (Phase 4) gestellt und
# die Antworten als Variablen in diesen Skill eingetragen.

**Frage 1 — Zeitfenster:**
> „Wie viele Stunden soll der Inbox-Review abdecken?"
> Empfehlung: 24h (Mails der letzten 24 Stunden, ideal für täglichen Morgen-Review)

**Frage 2 — Zeitplan:**
> „Wann soll der tägliche Inbox-Review stattfinden?"
> Empfehlung: Morgens 08:00 Uhr (startet den Arbeitstag strukturiert)
> Optionen: Manuell / Täglich morgens / Täglich abends / Mehrmals täglich

Falls automatischer Zeitplan gewählt:
→ Scheduled Task anlegen via `schedule`-Skill mit dem Trigger-Prompt:
  `"Führe den Inbox-Review der letzten {{INBOX_REVIEW_HOURS}} Stunden durch."`

**Frage 3 — Ordner-Logik:**
> „Soll eine intelligente Ordner-Verschiebe-Logik eingerichtet werden?
> (E-Mails werden automatisch in passende Ordner sortiert)"
> → Falls ja: `ordner-logik/SKILL.md` wird ebenfalls installiert
>   und während Schritt 5 aufgerufen.
