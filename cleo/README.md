# Cleo — Produkt

Vollständiges KI-Arbeitsplatzsystem für Unternehmen, basierend auf Claude Cowork.
Installierbar in einer geführten Session — ein Skill erledigt alles.

## Was nach der Installation vorhanden ist

- **Sekretariat** mit Mini-CRM (aus E-Mail-Postfach vorbefüllt)
- **Inbox-Review** (IMAP, Gmail oder Office 365)
- **Meeting-Review** mit Kalender- und Aufgaben-Anbindung (optional)
- **Physischer Briefversand** via OB24-API (optional)
- **CRM-Sync** aus dem Postfach + externe CRM-Anbindung (HubSpot, Salesforce, Pipedrive, Close.io)
- **KI-Rechtsassistent** — lernt Rechtsgebiete automatisch aus dem Postfach

## Installation beim Kunden

1. Claude Desktop öffnen → Cowork-Modus → Kundenordner auswählen
2. In der Chat-Eingabe:
   > „Führe den Cleo Installationsflow aus."
3. Claude führt durch alle Phasen — dauert ca. 20–30 Minuten

## Dokumentation & Materialien

| Datei | Beschreibung |
|---|---|
| [`DOKUMENTATION.md`](./DOKUMENTATION.md) | Vollständige Produktdokumentation (Module, Variablen, MCP, Changelog) |
| [`installation/Cleo-Mitarbeiter.pdf`](./installation/Cleo-Mitarbeiter.pdf) | Mitarbeiter-Anleitung (Schritt-für-Schritt, Troubleshooting, Tests) |
| [`installation/Cleo-Verkauf.pdf`](./installation/Cleo-Verkauf.pdf) | Verkaufs-PDF für Kunden (Benefits, Autonomie-Level, BAFA-Förderung) |

## Struktur

```
cleo/
├── installation/
│   ├── SKILL.md                          ← Master-Installationsflow (Claude-Skill)
│   ├── Cleo-Mitarbeiter.pdf              ← Druckbare Anleitung für Mitarbeiter
│   └── Cleo-Verkauf.pdf                  ← Verkaufs-PDF für Kunden
└── templates/
    ├── Sekretariat/
    │   └── skills/
    │       ├── inbox-review/SKILL.md
    │       ├── meeting-review/SKILL.md
    │       ├── crm-sync/SKILL.md
    │       └── physischen-brief-versenden/SKILL.md
    └── Team/
        └── KI-Rechtsassistent/CLAUDE.md
```
