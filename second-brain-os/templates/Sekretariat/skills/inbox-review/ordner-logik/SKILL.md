# Skill: Inbox-Review — Ordner-Logik
# ⚙️ TEMPLATE — Erweiterung des Inbox-Review-Skills

Liest die bestehende Ordnerstruktur des Postfachs, leitet Sortierregeln ab
und verschiebt eingehende Mails automatisch in passende Ordner.

E-Mail-System: {{EMAIL_SYSTEM}}

---

## EINMALIGER SETUP (beim ersten Aufruf)

### Setup-Schritt 1 — Bestehende Ordner einlesen

[WENN imap-smtp]:
IMAP-Ordnerliste laden:
```python
import imaplib, ssl
# → alle Ordner mit imap.list() abrufen
# → Ordnernamen und zugehörige Flags ausgeben
```

[WENN gmail]:
`gmail_list_labels()` — alle Labels (= Ordner) des Gmail-Accounts laden.

Alle Ordner/Labels ausgeben und den Nutzer fragen:
> „Ich habe folgende Ordner in deinem Postfach gefunden: [LISTE]
> Soll ich automatisch Regeln ableiten, oder möchtest du Regeln selbst festlegen?"

### Setup-Schritt 2 — Sortierregeln ableiten oder definieren

**Automatisch (empfohlen):**
Aus den letzten 30 Tagen E-Mails + vorhandenen Ordnern Muster ableiten:
- Mails von bestimmten Domains → bestimmter Ordner
- Mails mit bestimmten Betreff-Schlüsselwörtern → bestimmter Ordner
- Mails von bestimmten Absendern → bestimmter Ordner

Abgeleitete Regeln dem Nutzer zur Bestätigung zeigen:
> „Ich würde folgende Regeln einrichten:
> - Mails von @lieferant.de → Ordner 'Lieferanten'
> - Mails mit Betreff 'Rechnung' → Ordner 'Buchhaltung'
> Bestätigen?"

**Manuell:**
Nutzer legt Regeln im Format `[Absender/Domain/Betreff-Keyword] → [Zielordner]` fest.

### Setup-Schritt 3 — Regeln speichern

Regeln in `Sekretariat/CLAUDE.md` unter Abschnitt `ORDNER-REGELN` eintragen:

```markdown
## ORDNER-REGELN (Inbox-Ordner-Logik)
| Kriterium | Typ | Zielordner |
|---|---|---|
| @rechnungen.de | Domain | Buchhaltung |
| Rechnung | Betreff-Keyword | Buchhaltung |
| newsletter@ | Absender-Prefix | Newsletter |
```

---

## LAUFENDE AUSFÜHRUNG (bei jedem Inbox-Review)

### Schritt 1 — Regeln einlesen

`Sekretariat/CLAUDE.md` → Abschnitt `ORDNER-REGELN` laden.

### Schritt 2 — Mails prüfen

Für jede Mail aus dem aktuellen Review-Lauf:
1. Absender-Domain gegen Domain-Regeln prüfen
2. Absender-Adresse gegen Absender-Regeln prüfen
3. Betreff gegen Keyword-Regeln prüfen (case-insensitive)

Bei Treffer: Mail-Status auf 📂 VERSCHIEBEN setzen + Zielordner merken.

### Schritt 3 — Mails verschieben

[WENN imap-smtp]:
```python
# Mail in Zielordner kopieren + aus INBOX löschen
imap.copy(uid, zielordner)
imap.store(uid, "+FLAGS", "\\Deleted")
imap.expunge()
```

[WENN gmail]:
`gmail_add_label(message_id, label=ZIELORDNER)` + INBOX-Label entfernen.

### Schritt 4 — Protokoll

Pro verschobener Mail einen Eintrag ausgeben:
`📂 [ABSENDER] → [ZIELORDNER] (Regel: [TREFFER-KRITERIUM])`

---

## REGELN PFLEGEN

Der Nutzer kann jederzeit sagen:
- „Füge Regel hinzu: Mails von @firma.de → Ordner Kunden"
- „Zeig mir alle Ordner-Regeln"
- „Lösche die Regel für @firma.de"

Claude aktualisiert dann `Sekretariat/CLAUDE.md` entsprechend.
