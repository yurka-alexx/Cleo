# Skill: Inbox-Review
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Scannt den Posteingang, klassifiziert jede Mail und erstellt Entwürfe für alles,
was eine Antwort braucht.

E-Mail-System: {{EMAIL_SYSTEM}}
Firma: {{FIRMENNAME}}

---

## ABLAUF

### Schritt 1 — Posteingang laden

[WENN imap-smtp]:
Nutze `fetch_recent_mails(hours=72)` für die letzten 3 Tage.
Für ungelesene Mails: `search_mails(unread_only=True, since_days=14)`.

[WENN gmail]:
`gmail_search_messages(query="is:unread newer_than:3d")` für ungelesene Mails.
`gmail_search_messages(query="newer_than:3d")` für alle Mails der letzten 3 Tage.

[WENN office365 / imap]:
IMAP-MCP mit Office-365-Credentials: `fetch_recent_mails(hours=72)`.

### Schritt 2 — Jede Mail klassifizieren

Für jede Mail eine Entscheidung treffen:

| Kategorie | Kriterium |
|---|---|
| 🗑️ LÖSCHEN | Spam, Werbung, automatische Benachrichtigungen ohne Relevanz |
| 📁 ARCHIVIEREN | Informationsmail, erledigt, kein Handlungsbedarf |
| ✅ ANTWORTEN | Direkte Frage, Auftrag, Anfrage — Entwurf erstellen |
| 👀 BEOBACHTEN | Relevant, aber kein sofortiger Handlungsbedarf |

### Schritt 3 — Entwürfe erstellen

Für alle Mails mit Status ✅ ANTWORTEN einen Mailentwurf anlegen.

Ton: professionell, freundlich, im Stil von {{FIRMENNAME}}.
Länge: so kurz wie möglich, so ausführlich wie nötig.
Signatur: Name des Ansprechpartners aus `Sekretariat/CLAUDE.md`.

[WENN imap-smtp]:
`create_draft(to=ABSENDER, subject="Re: "+BETREFF, text=ENTWURFSTEXT)`

[WENN gmail]:
`gmail_create_draft(to=ABSENDER, subject="Re: "+BETREFF, body=ENTWURFSTEXT)`

### Schritt 4 — Zusammenfassung ausgeben

Tabellarische Übersicht aller bearbeiteten Mails:

| Absender | Betreff | Klassifizierung | Aktion |
|---|---|---|---|
| ... | ... | ✅ ANTWORTEN | Entwurf erstellt |
| ... | ... | 📁 ARCHIVIEREN | — |
| ... | ... | 🗑️ LÖSCHEN | — |

Gesamtanzahl je Kategorie als Kurzfassung am Ende ausgeben.

### Schritt 5 — CRM-Update (optional)

Falls neue Absender erkannt werden, die noch nicht im Mini-CRM stehen:
Hinweis ausgeben: „X neue Kontakte gefunden — soll ich crm-sync ausführen?"
