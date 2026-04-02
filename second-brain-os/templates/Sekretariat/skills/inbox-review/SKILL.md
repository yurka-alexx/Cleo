# Skill: Inbox-Review
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Scannt den Posteingang, klassifiziert jede Mail und erstellt Entwürfe für alles,
was eine Antwort braucht. Zu löschende Mails werden in den Papierkorb verschoben.

E-Mail-System:      {{EMAIL_SYSTEM}}
Firma:              {{FIRMENNAME}}
Review-Zeitfenster: {{INBOX_REVIEW_HOURS}}h (Standard: 24)
Zeitplan:           {{INBOX_REVIEW_SCHEDULE}}
Zusammenfassung an: {{SUMMARY_CHANNEL}}

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

| Kategorie | Kriterium |
|---|---|
| 🗑️ PAPIERKORB | Spam, Werbung, automatische Benachrichtigungen ohne Relevanz |
| 📁 ARCHIVIEREN | Informationsmail, erledigt, kein Handlungsbedarf |
| ✅ ANTWORTEN | Direkte Frage, Auftrag, Anfrage — Entwurf erstellen |
| 📂 VERSCHIEBEN | Mail gehört in einen bestimmten Ordner (→ Ordner-Logik-Skill) |
| 👀 BEOBACHTEN | Relevant, aber kein sofortiger Handlungsbedarf |

### Schritt 3 — Entwürfe erstellen

Für alle Mails mit Status ✅ ANTWORTEN einen Mailentwurf anlegen.

Ton: professionell, freundlich, im Stil von {{FIRMENNAME}}.
Länge: so kurz wie möglich, so ausführlich wie nötig.

[WENN imap-smtp]:
`create_draft(to=ABSENDER, subject="Re: "+BETREFF, text=ENTWURFSTEXT)`

[WENN gmail]:
`gmail_create_draft(to=ABSENDER, subject="Re: "+BETREFF, body=ENTWURFSTEXT)`

### Schritt 4 — Papierkorb & Archiv

🗑️ PAPIERKORB → Mail in Papierkorb verschieben, NICHT permanent löschen:

[WENN imap-smtp]:
`delete_mail(uid=UID, folder="INBOX", permanent=False)`
→ verschiebt in FOLDER_TRASH ({{FOLDER_TRASH}}), kein unwiderrufliches Löschen.

[WENN gmail]:
Label TRASH hinzufügen: `gmail_add_label(message_id=ID, label="TRASH")`

📁 ARCHIVIEREN:

[WENN imap-smtp]:
`archive_mail(uid=UID, folder="INBOX")`

[WENN gmail]:
INBOX-Label entfernen (archiviert in All Mail).

### Schritt 5 — Ordner-Logik (optional)

[WENN ORDNER_LOGIK = true]:
Für alle Mails mit Status 📂 VERSCHIEBEN den Ordner-Logik-Skill aufrufen:
→ `Sekretariat/skills/inbox-review/ordner-logik/SKILL.md`

### Schritt 6 — Zusammenfassung ausgeben & versenden

Tabellarische Übersicht aller bearbeiteten Mails:

| Absender | Betreff | Klassifizierung | Aktion |
|---|---|---|---|
| ... | ... | ✅ ANTWORTEN | Entwurf erstellt |
| ... | ... | 📁 ARCHIVIEREN | Archiviert |
| ... | ... | 🗑️ PAPIERKORB | In Papierkorb |

Kurzfassung: „X Entwürfe erstellt · Y archiviert · Z in Papierkorb"

Zusammenfassung an `{{SUMMARY_CHANNEL}}` senden:

[WENN summary_channel enthält "email:"]:
Mailentwurf mit Inbox-Zusammenfassung anlegen:
- Betreff: „Inbox-Review [DATUM] — [X] Mails bearbeitet"
- Inhalt: Tabelle + Entwurfs-Hinweise
[WENN imap-smtp]: `create_draft(to={{SUMMARY_EMAIL}}, subject=..., text=...)`
[WENN gmail]: `gmail_create_draft(to={{SUMMARY_EMAIL}}, ...)`

[WENN summary_channel enthält "slack:"]:
Slack-Nachricht an `{{SUMMARY_SLACK_CHANNEL}}`:
Kurz-Zusammenfassung: Anzahl pro Kategorie + Hinweis auf erstellte Entwürfe.

[WENN summary_channel = "none"]:
Nur in Claude ausgeben, kein Versand.

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
