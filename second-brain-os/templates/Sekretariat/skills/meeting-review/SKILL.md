# Skill: Meeting-Review
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Vollautomatische Meeting-Nachbereitung. Zieht Kalendereinträge, optional
Pocket-Transkripte, erstellt Zusammenfassungen und sendet sie an den konfigurierten Kanal.

Kalender:           {{CALENDAR_SYSTEM}}
Aufgaben-Tool:      {{TASK_TOOL}}
E-Mail-System:      {{EMAIL_SYSTEM}}
Pocket aktiviert:   {{POCKET_ENABLED}}
Zusammenfassung an: {{SUMMARY_CHANNEL}}

---

## ABLAUF

### Schritt 1 — Heutige Termine laden

[WENN google-kalender]:
`gcal_list_events` für den heutigen Tag (alle Kalender).

[WENN outlook]:
Outlook-Kalender-MCP oder manuelle Eingabe der Termine.

Jeden Termin klassifizieren:
- 👤 KUNDENGESPRÄCH — externe Person(en) anwesend
- 🏢 INTERN — nur interne Teilnehmer
- 🎯 FOKUSZEIT — geblockte Arbeitszeit, kein Meeting
- ❌ ABGESAGT / NICHT STATTGEFUNDEN

### Schritt 2 — Notizen & Transkripte lesen

Für jeden Termin (Status ≠ ❌):

**Schritt 2a — Kalender-Notizen:**
Beschreibungstext und angehängte Dokumente des Termins lesen.

**Schritt 2b — Pocket-Transkript (falls {{POCKET_ENABLED}} = true):**

Pocket nach Aufzeichnung für diesen Termin suchen:
```
search_pocket_conversations_timerange(
  start_date = [TERMIN-START minus 10 min],
  end_date   = [TERMIN-ENDE plus 10 min]
)
```

Falls Treffer:
- Volles Transkript mit `get_pocket_conversation(id=...)` laden
- Action Items mit `search_pocket_actionitems(...)` für diesen Zeitraum laden
- Transkript und Action Items als Grundlage für Zusammenfassung verwenden

Falls kein Treffer in Pocket → nur mit Kalender-Notizen weiterarbeiten.
Hinweis an Nutzer: „Keine Pocket-Aufzeichnung für [TERMIN] gefunden.
Bitte Pocket-App während zukünftiger Meetings aktiv lassen."

### Schritt 3 — Zusammenfassung erstellen

Je nach Termintyp:

**👤 KUNDENGESPRÄCH:**
- Teilnehmer (aus Kalender + Pocket-Transkript)
- Besprochene Themen (3–5 Punkte)
- Getroffene Vereinbarungen / Entscheidungen
- Next Steps mit Verantwortlichkeit und Deadline (aus Pocket Action Items falls vorhanden)
- Entwurf Zusammenfassungsmail an Kunden (Ton: professionell, freundlich)

**🏢 INTERN:**
- Kurze Zusammenfassung (2–3 Sätze)
- To-Do-Liste für das Team (aus Pocket Action Items priorisiert)

### Schritt 4 — Aufgaben anlegen

[WENN notion]:
Für jeden Next Step eine neue Seite in der Notion-Aufgaben-Datenbank:
- Titel: Next Step
- Fälligkeitsdatum: aus Vereinbarung
- Kontext: Verknüpfung zum Meeting

[WENN kein Tool]:
To-Do-Liste als Markdown ausgeben.

### Schritt 5 — Zusammenfassung versenden

Zusammenfassung aller Meetings an `{{SUMMARY_CHANNEL}}` senden:

[WENN summary_channel enthält "email:"]:
Mailentwurf an konfigurierte Adresse anlegen:
- Betreff: „Meeting-Zusammenfassung [DATUM]"
- Inhalt: alle Meetings mit Zusammenfassung + Next Steps

[WENN imap-smtp]: `create_draft(to={{SUMMARY_EMAIL}}, subject=..., text=...)`
[WENN gmail]: `gmail_create_draft(to={{SUMMARY_EMAIL}}, subject=..., body=...)`

[WENN summary_channel enthält "slack:"]:
Slack-Nachricht an `{{SUMMARY_SLACK_CHANNEL}}`:
- Formatiert als strukturierte Zusammenfassung (Markdown)
- Pro Meeting ein Abschnitt mit Titel, Teilnehmer, Key Points, Next Steps

[WENN summary_channel enthält "teams:"]:
Teams-Nachricht an `{{SUMMARY_TEAMS_CHANNEL}}`.

[WENN summary_channel = "none"]:
Zusammenfassung nur in Claude ausgeben.

### Schritt 6 — Mailentwürfe für Kunden

Für jedes KUNDENGESPRÄCH separaten Entwurf an den Kunden anlegen
(zusätzlich zur internen Zusammenfassung aus Schritt 5):
- Betreff: „Zusammenfassung: [TERMINNAME] vom [DATUM]"
- Inhalt: Danke für das Gespräch, besprochene Punkte, vereinbarte Next Steps
- Pocket Action Items falls vorhanden einbauen

[WENN imap-smtp]: `create_draft(...)`
[WENN gmail]: `gmail_create_draft(...)`
