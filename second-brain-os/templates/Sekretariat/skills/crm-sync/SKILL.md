# Skill: CRM-Sync
# ⚙️ TEMPLATE — wird während Installation mit Kundenvariablen befüllt

Synchronisiert Kontakte aus dem E-Mail-Postfach ins Mini-CRM (und ggf. externes CRM).
E-Mail-System: {{EMAIL_SYSTEM}}
CRM-System: {{CRM_SYSTEM}}

---

## ABLAUF

### Schritt 1 — Neue Kontakte aus E-Mails extrahieren

Suche neue Absender der letzten 30 Tage:

[WENN imap-smtp]:
`search_mails(since_days=30)` — alle FROM-Adressen sammeln.

[WENN gmail]:
`gmail_search_messages(query="newer_than:30d")` — alle FROM-Adressen sammeln.

### Schritt 2 — Gegen Mini-CRM abgleichen

Bestehende Kontakte aus `Sekretariat/CLAUDE.md` einlesen.
Nur Adressen vorschlagen, die noch NICHT im Mini-CRM sind.
Interne Adressen (eigene Domain) herausfiltern.

### Schritt 3 — Neue Kontakte vorschlagen

Für jeden neuen Kontakt:
- Name (aus E-Mail-Header)
- Firma (aus Domain oder Signatur)
- Letzte E-Mail: Datum + Thema
- Vorgeschlagene Rolle: Kunde / Lieferant / Sonstiges

Yuri / Nutzer bestätigt oder korrigiert Rolle.

### Schritt 4 — Mini-CRM aktualisieren

Neue Einträge in die Tabelle in `Sekretariat/CLAUDE.md` schreiben.

[WENN externes CRM — HubSpot]:
Kontakt über HubSpot-API anlegen:
POST https://api.hubapi.com/crm/v3/objects/contacts
Headers: Authorization: Bearer {{HUBSPOT_API_KEY}}

[WENN externes CRM — Pipedrive]:
POST https://api.pipedrive.com/v1/persons?api_token={{PIPEDRIVE_API_KEY}}

[WENN externes CRM — Salesforce]:
REST API: POST /services/data/vXX.0/sobjects/Contact/
Authorization: Bearer {{SALESFORCE_TOKEN}}

[WENN externes CRM — Close.io]:
POST https://api.close.com/api/v1/contact/
Authorization: Basic {{CLOSE_API_KEY}}

[WENN externes CRM — Custom]:
→ API-Dokumentation aus CLAUDE.md lesen und entsprechend handeln.
→ Falls kein MCP vorhanden: Hinweis ausgeben, dass MCP-Connector gebaut werden muss.
