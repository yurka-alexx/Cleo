# Cleo — Produkt

Vollständiges KI-Arbeitsplatzsystem für Unternehmen, basierend auf Claude Cowork.
Installierbar in einer geführten Session — ein Skill erledigt alles.

## Was nach der Installation vorhanden ist

- **Sekretariat** mit Mini-CRM (aus E-Mail-Postfach vorbefüllt)
- **Inbox-Review** (IMAP, Gmail oder Office 365)
- **Meeting-Review** mit Kalender- und Aufgaben-Anbindung (optional)
- **Physischer Briefversand** via OB24-API (optional)
- **CRM-Sync** aus dem Postfach + externe CRM-Anbindung (HubSpot, Salesforce, Pipedrive, Close.io)
- **Firmenanwalt** — lernt Rechtsgebiete automatisch aus dem Postfach

## Installation beim Kunden

1. Claude Desktop öffnen → Cowork-Modus → Kundenordner auswählen
2. In der Chat-Eingabe:
   > „Führe den Cleo Installationsflow aus."
3. Claude führt durch alle Phasen — dauert ca. 20–30 Minuten

## Dokumentation & Materialien

| Datei | Beschreibung |
|---|---|
| [`DOKUMENTATION.md`](./DOKUMENTATION.md) | Vollständige Produktdokumentation (Module, Variablen, MCP, Changelog) |
| [`installation/MITARBEITER-ANLEITUNG-Cleo.pdf`](./installation/MITARBEITER-ANLEITUNG-Cleo.pdf) | Mitarbeiter-Anleitung (Schritt-für-Schritt, Troubleshooting, Tests) |
| [`installation/Second-Brain-OS-Verkauf.pdf`](./installation/Second-Brain-OS-Verkauf.pdf) | Verkaufs-PDF für Kunden (Benefits, Autonomie-Level, BAFA-Förderung) |

## Struktur

```
cleo/
├── installation/
│   ├── SKILL.md                          ← Master-Installationsflow (Claude-Skill)
│   └── MITARBEITER-ANLEITUNG-...pdf      ← Druckbare Anleitung für Mitarbeiter
└── templates/
    ├── Sekretariat/
    │   └── skills/
    │       ├── inbox-review/SKILL.md
    │       ├── meeting-review/SKILL.md
    │       ├── crm-sync/SKILL.md
    │       └── physischen-brief-versenden/SKILL.md
    └── Team/
        └── Firmenanwalt/CLAUDE.md
```
