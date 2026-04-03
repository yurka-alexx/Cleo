# Skill: Physischen Brief versenden
# ⚙️ TEMPLATE — wird während Installation mit OB24-Credentials befüllt

Erstellt ein Brief-PDF und sendet es über die OB24-API als physischen Brief.
Vor dem Versand wird der Briefpreis eingeholt und bestätigt.

OB24 Username: {{OB24_USERNAME}}
OB24 Password: {{OB24_PASSWORD}}
OB24 Job-ID:   {{OB24_JOB_ID}}
Testmodus:     {{OB24_TEST_MODE}}

> ℹ️ **Testmodus-Steuerung:**
> - `{{OB24_TEST_MODE}} = true` → alle Versendungen sind Testversendungen (kein echter Druck)
> - `{{OB24_TEST_MODE}} = false` → Echte Versendungen (kostenpflichtig)
> - **Einmaliger Testversand:** Nutzer kann pro Aufruf mit „sende im Testmodus" oder
>   „Testversand" den aktuellen Versand als Test erzwingen — unabhängig von der Konfiguration.
>   Claude fragt vor JEDEM Versand nach: „Echt versenden oder Testversand?"

---

## ABSENDER
Firma:    {{FIRMENNAME}}
Straße:   {{STRASSE}}
PLZ/Ort:  {{PLZ}} {{ORT}}

---

## ABLAUF

### Schritt 1 — Briefdaten erfassen

Falls nicht bereits im Prompt angegeben, abfragen:
- Empfänger: Name, Firma (optional), Straße, PLZ, Ort, Land (Standard: DE)
- Betreff des Briefes
- Brieftext (oder Entwurf aus vorherigem Schritt übernehmen)
- Brieftyp: Standard / Formelles Schreiben (Aktenzeichen erfragen falls Formelles Schreiben)

### Schritt 2 — Brief-PDF generieren

Nutze `build_brief.py` aus `Post-Requisiten/` (liegt nach Installation dort bereit).

Layout-Standard (v8):
- Ränder: Links/Rechts/Unten = 57pt, Oben = 80pt
- Briefkopf: Logo (oben rechts) + Firmendaten
- Empfängeradresse: DIN 5008-konform, 45mm vom oberen Rand
- Datum: rechtsbündig
- Betreff: LibSans-Bold, 10pt, zeilenumbrochen falls nötig
- Brieftext: LibSans, 10pt, 15pt Zeilenabstand — Seitenumbruch-Prüfung pro Zeile
- Grußformel: "Mit freundlichen Grüßen"
- Unterschrift: Signum-Bild + Name

Bei Formelles Schreibenen zusätzlich:
- Aktenzeichen im Briefkopf (unterhalb Betreff, grau, 9pt)
- Abschluss: "Rechtsabteilung, i.A. der Geschäftsführung\n{{FIRMENNAME}}"

Speichere als `Postausgang/[DATUM]-[EMPFAENGER-KÜRZEL].pdf`.

### Schritt 3 — Briefpreis einholen (PFLICHT vor Versand)

Rufe die OB24-Preisabfrage auf, bevor der Brief versendet wird:

```bash
curl -s -X POST "https://www.onlinebrief24.de/services/rest/getPrice" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "{{OB24_USERNAME}}",
    "password": "{{OB24_PASSWORD}}",
    "jobId": {{OB24_JOB_ID}}
  }'
```

Aus der Response den Preis (Brutto) extrahieren und dem Nutzer anzeigen:

> „Der Brief an [EMPFÄNGER] kostet **X,XX €** (inkl. MwSt., Job: {{OB24_JOB_ID}}).
> Soll ich ihn jetzt versenden?"

⛔ **Nicht weitermachen, bis der Nutzer explizit bestätigt hat** ("ja", "senden", "ok").

Vor der Bestätigungsfrage: Testmodus-Status klar anzeigen:

Falls `{{OB24_TEST_MODE}} = true`:
> „⚠️ Testmodus aktiv — der Brief wird NICHT physisch versendet. Kosten: 0 EUR.
>  Zum echten Versand: `OB24_TEST_MODE` auf `false` setzen."

Falls `{{OB24_TEST_MODE}} = false`:
> „Möchtest du wirklich senden (echte Kosten: X,XX EUR) oder lieber im Testmodus testen?"
> Optionen: „Jetzt senden" / „Testversand" / „Abbrechen"
> → Bei „Testversand": `testMode: true` im API-Call setzen, Konfiguration bleibt unverändert.

### Schritt 4 — Versand (nach Bestätigung)

```bash
PDF_BASE64=$(base64 -i "Postausgang/[DATEI].pdf")

curl -s -X POST "https://www.onlinebrief24.de/services/rest/sendDocument" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "{{OB24_USERNAME}}",
    "password": "{{OB24_PASSWORD}}",
    "testMode": {{OB24_TEST_MODE}},
    "jobId": {{OB24_JOB_ID}},
    "document": "'"$PDF_BASE64"'"
  }'
```

### Schritt 5 — Ergebnis prüfen & loggen

- Bei Erfolg: Tracking-ID aus Response lesen
- Bei Fehler: Fehlermeldung ausgeben + in `Postausgang/fehler-log.md` eintragen

Eintrag in `Postausgang/log.md`:
```
| [DATUM] | [EMPFÄNGER] | [BETREFF] | [PREIS €] | [TRACKING-ID] | [TEST J/N] |
```
