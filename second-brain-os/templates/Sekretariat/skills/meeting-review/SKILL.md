# Skill: Meeting-Review
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Vollautomatische Meeting-Nachbereitung.
Kalender: {{CALENDAR_SYSTEM}}
Aufgaben-Tool: {{TASK_TOOL}}
E-Mail-System: {{EMAIL_SYSTEM}}

---

## ABLAUF

### Schritt 1 — Heutige Termine laden

[WENN google-kalender]:
Nutze `gcal_list_events` für den heutigen Tag.

[WENN outlook]:
Outlook-Kalender-MCP oder manuelle Eingabe.

Jeden Termin klassifizieren:
- 👤 KUNDENGESPRÄCH — externe Person(en) anwesend
- 🏢 INTERN — nur interne Teilnehmer
- 🎯 FOKUSZEIT — Kein Meeting, geblockte Arbeitszeit
- ❌ ABGESAGT / NICHT STATTGEFUNDEN

### Schritt 2 — Notizen lesen

Für jeden Termin: angefügte Notizen, Links zu geteilten Dokumenten oder Beschreibungstext lesen.

### Schritt 3 — Zusammenfassung erstellen

Je nach Typ:

**KUNDENGESPRÄCH:**
- Kurze Zusammenfassung (3-5 Sätze)
- Besprochene Themen
- Vereinbarungen / Next Steps
- Entwurf: Zusammenfassungsmail an Kunden → `{{EMAIL_SYSTEM}}`

**INTERN:**
- Kurze Zusammenfassung
- To-Dos für das Team

### Schritt 4 — Aufgaben anlegen

[WENN notion]:
Neue Seiten in der Aufgaben-Datenbank anlegen (Tool: Notion-MCP).

[WENN kein Tool]:
To-Do-Liste als Markdown ausgeben.

### Schritt 5 — Mailentwürfe erstellen

Für jedes Kundengespräch einen Mailentwurf anlegen:
- Betreff: "Zusammenfassung: [TERMINNAME] vom [DATUM]"
- Ton: professionell, freundlich
- Inhalt: Danke, Zusammenfassung, Next Steps, Kontaktdaten

[WENN imap-smtp]: `create_draft(...)`
[WENN gmail]: `gmail_create_draft(...)`
