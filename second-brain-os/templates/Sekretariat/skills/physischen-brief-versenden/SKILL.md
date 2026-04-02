# Skill: Physischen Brief versenden
# ⚙️ TEMPLATE — wird während Installation mit OB24-Credentials befüllt

Erstellt ein Brief-PDF und sendet es über die OB24-API als physischen Brief.

OB24 API-Key: {{OB24_API_KEY}}
OB24 Job-ID: {{OB24_JOB_ID}}
Testmodus: {{OB24_TEST_MODE}}

---

## ABSENDER
Firma: {{FIRMENNAME}}
Straße: {{STRASSE}}
PLZ / Ort: {{PLZ}} {{ORT}}

---

## ABLAUF

### Schritt 1 — Briefdaten erfassen

Falls nicht bereits im Prompt angegeben, abfragen:
- Empfänger: Name, Firma (optional), Straße, PLZ, Ort
- Betreff des Briefes
- Brieftext (oder Entwurf aus vorherigem Schritt übernehmen)

### Schritt 2 — Brief-PDF generieren

Nutze `build_brief.py` aus `Post-Requisiten/` (falls vorhanden) oder erstelle ein einfaches PDF mit:
- Briefkopf: Logo (falls vorhanden) + Firmendaten
- Empfängeradresse
- Datum
- Betreff
- Brieftext
- Grußformel: "Mit freundlichen Grüßen"
- Unterschrift: Signum-Bild (falls vorhanden) + Name

Speichere als `Postausgang/[DATUM]-[EMPFAENGER].pdf`.

### Schritt 3 — OB24-API-Aufruf

```bash
# PDF zu Base64 konvertieren
PDF_BASE64=$(base64 -i "Postausgang/[DATEI].pdf")

# API-Aufruf
curl -X POST https://www.onlinebrief24.de/services/rest/sendDocument \
  -H "Content-Type: application/json" \
  -d '{
    "username": "{{OB24_USERNAME}}",
    "password": "{{OB24_PASSWORD}}",
    "testMode": {{OB24_TEST_MODE}},
    "jobId": {{OB24_JOB_ID}},
    "document": "'$PDF_BASE64'"
  }'
```

### Schritt 4 — Ergebnis prüfen

- Bei Erfolg: Tracking-ID aus Response speichern, in Postausgang vermerken
- Bei Fehler: Fehlermeldung ausgeben + in `Postausgang/fehler-log.md` eintragen

### Schritt 5 — Postausgang-Eintrag

In `Postausgang/log.md` Zeile hinzufügen:
`| [DATUM] | [EMPFÄNGER] | [BETREFF] | [TRACKING-ID] | [TESTMODUS J/N] |`
