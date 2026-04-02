# Skill: Meeting-Review
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Vollautomatische Meeting-Nachbereitung. Zieht Kalendereinträge, liest alle
Pocket-Tagestranskripte, erstellt Zusammenfassungen und führt konfigurierten
Folgeaktionen durch (Termine, To-Dos, E-Mail-Entwürfe).

Kalender:               {{CALENDAR_SYSTEM}}
Aufgaben-Tool:          {{TASK_TOOL}}
E-Mail-System:          {{EMAIL_SYSTEM}}
Pocket aktiviert:       {{POCKET_ENABLED}}
Zusammenfassung an:     {{SUMMARY_CHANNEL}}
Autonome Aktionen:      {{AUTONOMOUS_ACTIONS}}
  → Termine anlegen:    {{AUTO_CREATE_EVENTS}}
  → To-Dos anlegen:     {{AUTO_CREATE_TODOS}}
  → E-Mail-Entwürfe:    {{AUTO_CREATE_DRAFTS}}

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

---

### Schritt 2 — Alle Transkripte & Notizen des Tages laden

**Schritt 2a — Kalender-Notizen:**
Für jeden Termin (Status ≠ ❌): Beschreibungstext und angehängte Dokumente lesen.

**Schritt 2b — Pocket-Tagestranskripte (falls {{POCKET_ENABLED}} = true):**

Pocket gibt ALLE Gespräche des heutigen Tages zurück — nicht nur Meetings,
sondern auch Telefonate, spontane Gespräche und alles andere, was aufgezeichnet wurde.

```
search_pocket_conversations_timerange(
  start_date = [HEUTE 00:00 Uhr],
  end_date   = [HEUTE 23:59 Uhr]
)
```

Für jeden Treffer:
- Volles Transkript mit `get_pocket_conversation(id=...)` laden
- Action Items mit `search_pocket_actionitems(conversation_id=...)` laden

**Zuordnung Pocket → Kalendertermin:**
Pocket-Gespräch einem Kalendertermin zuordnen wenn zeitliche Überlappung ≥ 5 Minuten.

→ Passendes Meeting gefunden: Transkript diesem Meeting zuordnen
→ Kein passendes Meeting: Gespräch als **ungeplantes Gespräch** separat verarbeiten
   (gleiche Verarbeitungslogik wie KUNDENGESPRÄCH falls externe Person erkennbar,
    sonst INTERN)

Falls heute keine Pocket-Transkripte vorhanden:
→ Hinweis an Nutzer: „Keine Pocket-Aufzeichnungen für heute gefunden.
  Bitte Pocket-App während Gesprächen und Meetings aktiv lassen."
→ Weiterarbeiten mit Kalender-Notizen allein.

---

### Schritt 3 — Zusammenfassungen erstellen

Je nach Gesprächstyp:

**👤 KUNDENGESPRÄCH (geplant oder ungeplant):**
- Teilnehmer (aus Kalender + Pocket-Transkript)
- Besprochene Themen (3–5 Punkte)
- Getroffene Vereinbarungen / Entscheidungen
- Next Steps mit Verantwortlichkeit und Deadline (aus Pocket Action Items falls vorhanden)
- Offene Fragen / Klärungsbedarf

**🏢 INTERN:**
- Kurze Zusammenfassung (2–3 Sätze)
- To-Do-Liste für das Team (aus Pocket Action Items priorisiert)

**🎤 UNGEPLANTES GESPRÄCH (nur in Pocket, kein Kalendereintrag):**
- Gesprächspartner (aus Pocket-Transkript)
- Kurze Zusammenfassung
- Next Steps / Action Items
- Hinweis: „Gespräch war nicht im Kalender — soll ein Nachfolge-Termin angelegt werden?"

---

### Schritt 4a — Aufgaben anlegen

[WENN auto_create_todos = true UND notion]:
Für jeden Next Step eine neue Seite in der Notion-Aufgaben-Datenbank:
- Titel: Next Step
- Fälligkeitsdatum: aus Vereinbarung oder „ohne Datum"
- Kontext: Meeting-Titel + Datum als Notiz
- Verantwortliche Person (falls erkennbar)

[WENN auto_create_todos = true UND kein Tool]:
To-Do-Liste als Markdown ausgeben mit Checkbox-Format:
```
- [ ] [To-Do] — Deadline: [DATUM] (aus: [MEETING])
```

[WENN auto_create_todos = false]:
Next Steps nur in der Zusammenfassung aufführen, nicht anlegen.

---

### Schritt 4b — Kalendertermine aus Next Steps anlegen

[WENN auto_create_events = true]:

Für jeden Next Step mit konkretem Datum oder Zeitangabe:
- Prüfen ob ein Folge-Termin sinnvoll ist (z.B. "Call nächste Woche", "Meeting am Freitag")
- Termin anlegen:

[WENN google-kalender]:
```
gcal_create_event(
  summary = "[THEMA] — Follow-up mit [NAME]",
  start   = [DATUM + UHRZEIT aus Vereinbarung],
  end     = [START + 1h],
  description = "Folge-Termin aus Meeting vom [DATUM]: [KONTEXT]"
)
```

Nutzern nach Erstellung informieren: „Termin ‚[TITEL]' am [DATUM] angelegt."

[WENN auto_create_events = false]:
Terminvorschläge nur in der Zusammenfassung erwähnen, nicht automatisch anlegen.

---

### Schritt 5 — Zusammenfassung versenden

Zusammenfassung aller Meetings und Gespräche an `{{SUMMARY_CHANNEL}}` senden:

[WENN summary_channel enthält "email:"]:
Mailentwurf an konfigurierte Adresse anlegen:
- Betreff: „Meeting-Zusammenfassung [DATUM]"
- Inhalt: alle Meetings und ungeplanten Gespräche mit Zusammenfassung + Next Steps
  + (falls auto_create_todos/events aktiv) Liste der angelegten To-Dos und Termine

[WENN imap-smtp]: `create_draft(to={{SUMMARY_EMAIL}}, subject=..., text=...)`
[WENN gmail]: `gmail_create_draft(to={{SUMMARY_EMAIL}}, subject=..., body=...)`

[WENN summary_channel enthält "slack:"]:
Slack-Nachricht an `{{SUMMARY_SLACK_CHANNEL}}`:
- Formatiert als strukturierte Zusammenfassung (Markdown)
- Pro Gespräch ein Abschnitt mit Typ, Teilnehmer, Key Points, Next Steps
- Hinweis auf angelegte To-Dos / Termine

[WENN summary_channel enthält "teams:"]:
Teams-Nachricht an `{{SUMMARY_TEAMS_CHANNEL}}`.

[WENN summary_channel = "none"]:
Zusammenfassung nur in Claude ausgeben.

---

### Schritt 6 — E-Mail-Entwürfe für Kunden & Gesprächspartner

[WENN auto_create_drafts = true]:

Für jedes KUNDENGESPRÄCH und jedes ungeplante externe Gespräch:

Mini-CRM aus `Sekretariat/CLAUDE.md` lesen, um korrekte E-Mail-Adresse zu finden.
Falls Kontakt nicht im Mini-CRM: E-Mail-Adresse aus Pocket-Transkript oder Kalender-Einladung entnehmen.

Entwurf anlegen:
- Betreff: „Zusammenfassung: [GESPRÄCHSTHEMA] vom [DATUM]"
- Ton: professionell, freundlich
- Inhalt:
  - Dank für das Gespräch
  - Besprochene Punkte (3–5 Punkte)
  - Vereinbarte Next Steps mit Deadline
  - Falls Termin angelegt: Bestätigung des Folge-Termins
- Pocket Action Items falls vorhanden einbauen

[WENN imap-smtp]: `create_draft(...)`
[WENN gmail]: `gmail_create_draft(...)`

[WENN auto_create_drafts = false]:
Entwurf nur für KUNDENGESPRÄCHE anlegen (manueller Modus).

**Brief-Vorschläge (unabhängig vom Autonomie-Level):**

Nach der E-Mail-Entwurf-Logik: Prüfen ob in einem der Gespräche ein Thema vorliegt,
das einen physischen Brief sinnvoller macht als eine E-Mail:

Indikatoren für ✉️ BRIEF-Empfehlung:
- Vereinbarte Kündigung, Abmahnung oder Vertragsbeendigung
- Formelle Bestätigung einer Vereinbarung mit rechtlicher Relevanz
- Mahnung oder Zahlungsaufforderung (nach vorherigen E-Mails ohne Reaktion)
- Behörden- oder Ämterkommunikation
- Gesprächspartner ist bekannt dafür, E-Mails zu ignorieren

Falls solche Themen erkannt werden:
```
✉️ BRIEF-EMPFEHLUNG (aus Meeting: [TITEL])
An: [EMPFÄNGER]
Grund: [Konkrete Begründung, z.B. "Vertragsbestätigung erfordert Schriftform"]
Entwurf: [2-3 Sätze Briefinhalt-Vorschlag]
→ „brief versenden" um Brief via OB24 zu senden
```

Falls `physischen-brief-versenden`-Skill installiert: direkt Brief-Daten bereitstellen.
→ NICHT automatisch versenden — immer auf explizite Bestätigung warten.

---

### Schritt 7 — Mini-CRM kontinuierlich aktualisieren

Das Mini-CRM in `Sekretariat/CLAUDE.md` wird nach jedem Meeting-Review automatisch
aktualisiert — auf Basis aller Gespräche des Tages (Kalender + Pocket).

**7a — Neue Gesprächspartner eintragen:**

Für alle Personen aus heutigen Gesprächen, die noch NICHT im Mini-CRM stehen:
- Name (aus Kalender-Einladung, Pocket-Transkript oder genanntem Namen)
- Firma (aus Kalender oder Transkript erschließen)
- E-Mail (falls in Kalendereinladung oder Transkript vorhanden)
- Rolle: Kunde / Lieferant / Partner / Interessent / Sonstige
- Letzter Kontakt: heutiges Datum
- Notizen: Gesprächsthema + wichtigste Vereinbarung (1–2 Sätze)

**7b — Bestehende Kontakte nach Gespräch anreichern:**

Für alle Gesprächspartner, die bereits im Mini-CRM stehen:
- „Letzter Kontakt" auf heutiges Datum aktualisieren
- Notizen ergänzen: wichtigste Vereinbarung oder neuer Kontext aus dem heutigen Gespräch
- Rolle oder Firma korrigieren falls im Gespräch neue Information erwähnt wurde
  (z.B. Jobwechsel, neue Abteilung, neue Firma)

**7c — Beziehungstiefe aus Pocket-Transkript ableiten:**

Falls Pocket-Transkript vorhanden: Qualität und Inhalt des Gesprächs für CRM nutzen:
- Wurde ein konkretes Angebot besprochen? → Notiz: „Angebot besprochen [DATUM]"
- Wurde ein Abschluss erzielt? → Rolle ggf. auf „Kunde (aktiv)" aktualisieren
- Gibt es offene Forderungen oder Probleme? → Notiz: „Offene Punkte: [KONTEXT]"
- Neues Interesse an Produkt/Dienstleistung erkennbar? → Notiz: „Interesse: [THEMA]"

**7d — Zusammenfassung der CRM-Änderungen ausgeben:**

```
📇 Mini-CRM aktualisiert (Meeting-Review):
  + [X] neue Kontakte aus heutigen Gesprächen eingetragen
  ↻ [Y] bestehende Kontakte aktualisiert (letzter Kontakt, Notizen)
  ✎ [Z] Kontakte mit neuen Gesprächsinfos angereichert
```

---

### Abschluss — Tagesübersicht ausgeben

Tabellarische Übersicht am Ende:

| Gespräch | Typ | Pocket | To-Dos | Termin | Entwurf | Brief |
|---|---|---|---|---|---|---|
| [TITEL] | 👤 Kunde | ✅ | 3 angelegt | 1 angelegt | ✅ Entwurf | — |
| [TITEL] | 🏢 Intern | ✅ | 2 angelegt | — | — | — |
| [TITEL] | 🎤 Ungeplant | ✅ | 1 angelegt | — | ✅ Entwurf | ✉️ Vorschlag |

Kurzzusammenfassung: „X Gespräche · Y To-Dos · Z Termine · W Entwürfe · V Briefe"
