#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cleo — Mitarbeiteranleitung v2"""

from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
_FONT_DIR = "/sessions/peaceful-pensive-lamport/fonts"
pdfmetrics.registerFont(TTFont("Jakarta-Bold",    _FONT_DIR + "/PlusJakartaSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Jakarta",         _FONT_DIR + "/PlusJakartaSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter",           _FONT_DIR + "/Inter-Regular.ttf"))
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

DARK_BLUE   = HexColor("#1a2e4a")
MID_BLUE    = HexColor("#2d5fa3")
LIGHT_BLUE  = HexColor("#e8f0fb")
TEAL        = HexColor("#00a896")
ORANGE      = HexColor("#f4842d")
GRAY_L      = HexColor("#f5f6f8")
GRAY_M      = HexColor("#8a9ab0")
TEXT        = HexColor("#1f2d3d")
GREEN_L     = HexColor("#e8f8f0")
GREEN_D     = HexColor("#1a7a4a")
PURPLE      = HexColor("#6a5acd")
RED         = HexColor("#c0392b")
GREEN_M     = HexColor("#2e8b57")
AMBER       = HexColor("#d4892a")
OCEAN       = HexColor("#0077b6")

W, H = A4

def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle('TH', fontName='Jakarta-Bold', fontSize=9, leading=12, textColor=white, alignment=TA_CENTER))
    s.add(ParagraphStyle('TC', fontName='Inter', fontSize=8.5, leading=12, textColor=TEXT))
    s.add(ParagraphStyle('TCB', fontName='Jakarta-Bold', fontSize=8.5, leading=12, textColor=TEXT))
    s.add(ParagraphStyle('TR', fontName='Jakarta-Bold', fontSize=9, leading=12, textColor=DARK_BLUE, alignment=TA_RIGHT))
    s.add(ParagraphStyle('OK', fontName='Jakarta-Bold', fontSize=8.5, leading=12, textColor=GREEN_D))
    return s

def hdr(c, pg, title):
    c.setFillColor(DARK_BLUE); c.rect(0, H-30, W, 30, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, H-30, 5, 30, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 9); c.setFillColor(white)
    c.drawString(20, H-19, "Cleo")
    c.setFont("Inter", 9); c.setFillColor(HexColor("#a0b8d8"))
    c.drawString(158, H-19, "|  " + title)
    c.setFont("Inter", 8); c.setFillColor(HexColor("#708090"))
    c.drawRightString(W-18, H-19, "Seite " + str(pg))

def ftr(c):
    c.setStrokeColor(HexColor("#d0d8e8")); c.setLineWidth(0.5)
    c.line(25, 26, W-25, 26)
    c.setFont("Inter", 7.5); c.setFillColor(GRAY_M)
    c.drawString(25, 14, "Cleo — Installations- & Mitarbeiteranleitung  |  Vertraulich")
    c.drawRightString(W-25, 14, "2026")

def sec(c, y, t1, t2=None):
    h = 40 if t2 else 28
    c.setFillColor(DARK_BLUE); c.roundRect(18, y-h, W-36, h, 5, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 12); c.setFillColor(white)
    c.drawString(30, y-(20 if not t2 else 14), t1)
    if t2:
        c.setFont("Inter", 8.5); c.setFillColor(HexColor("#a0c0e0"))
        c.drawString(30, y-34, t2)
    return y - h - 10

def badge(c, x, y, n, col=MID_BLUE):
    c.setFillColor(col); c.circle(x+10, y, 10, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 8 if len(str(n))==1 else 7)
    c.setFillColor(white); c.drawCentredString(x+10, y-4, str(n))

def wrap_text(c, text, font, size, max_w):
    words = text.split()
    line, lines = "", []
    for w in words:
        t = (line + " " + w).strip()
        if c.stringWidth(t, font, size) < max_w: line = t
        else: lines.append(line); line = w
    lines.append(line)
    return lines

# —— COVER ——
def cover(c):
    c.setFillColor(DARK_BLUE); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, 0, 7, H, fill=1, stroke=0)
    p = c.beginPath()
    p.moveTo(0, H*0.50); p.lineTo(W*0.65, H*0.50)
    p.lineTo(W, H*0.64); p.lineTo(0, H*0.64); p.close()
    c.setFillColor(HexColor("#1e3a5f")); c.drawPath(p, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 34); c.setFillColor(white)
    c.drawString(35, H-118, "Cleo")
    c.setFont("Jakarta-Bold", 17); c.setFillColor(HexColor("#7ab8e8"))
    c.drawString(35, H-148, "Installations- & Mitarbeiteranleitung")
    c.setStrokeColor(TEAL); c.setLineWidth(2.5)
    c.line(35, H-162, 320, H-162)
    c.setFont("Inter", 10.5); c.setFillColor(HexColor("#b0c8e0"))
    for i, l in enumerate(["Dein KI-gestuetztes digitales Büro.",
                            "E-Mails | Meetings | Briefe | CRM | Recht",
                            "Vollständig automatisiert — ohne Programmierkenntnisse."]):
        c.drawString(35, H-188-i*17, l)
    feats = ["Postfach-Briefing", "Tagesabschluss", "Briefversand", "KI-Rechtsassistent",
             "Mini-CRM", "Pocket AI", "Autonome Aktionen"]
    px, py = 35, H-268
    c.setFont("Inter", 9)
    for f in feats:
        pw = c.stringWidth(f, "Inter", 9) + 18
        if px+pw > W-35: px = 35; py -= 27
        c.setFillColor(HexColor("#1c3550")); c.roundRect(px, py-5, pw, 18, 4, fill=1, stroke=0)
        c.setFillColor(HexColor("#7ab8e8")); c.drawString(px+9, py+1, f)
        px += pw + 8
    bx, by = 25, H*0.47
    box_w = W - 50
    txt_x = bx + 17
    txt_w = box_w - 34
    c.setFillColor(HexColor("#0d1f35")); c.roundRect(bx, by-84, box_w, 84, 6, fill=1, stroke=0)
    c.setStrokeColor(TEAL); c.setLineWidth(1.5)
    c.roundRect(bx, by-84, box_w, 84, 6, fill=0, stroke=1)
    c.setFont("Jakarta-Bold", 9); c.setFillColor(TEAL)
    c.drawString(txt_x, by-16, "FÜR WEN IST DIESES DOKUMENT?")
    c.setFont("Inter", 9); c.setFillColor(HexColor("#b0c8e0"))
    body = ("Für Mitarbeitende und Installationspartner, die Cleo einrichten oder täglich nutzen. "
            "Technisches Vorwissen ist nicht erforderlich.")
    body_lines = wrap_text(c, body, "Inter", 9, txt_w)
    for k, bl in enumerate(body_lines):
        c.drawString(txt_x, by-32-k*14, bl)
    c.setFont("Inter", 8); c.setFillColor(GRAY_M)
    c.drawString(35, 28, "Version 2.0  |  April 2026  |  Vertraulich — Nur für internen Gebrauch")
    c.showPage()

# —— HARDWARE / SUBSCRIPTIONS ——
def hardware(c, S):
    hdr(c, 2, "Voraussetzungen — Hardware & Kosten"); ftr(c)
    y = H - 44
    y = sec(c, y, "Was du brauchst — Hardware & Abonnements",
            "Einmalige Investition + laufende Kosten im Überblick")
    y -= 10   # Luft nach Header-Box

    c.setFont("Jakarta-Bold", 10); c.setFillColor(DARK_BLUE)
    c.drawString(22, y, "Hardware — Einmalige Anschaffung"); y -= 14

    hw = [
        [Paragraph("Geraet", S['TH']), Paragraph("Empfehlung", S['TH']),
         Paragraph("Preis", S['TH']), Paragraph("Wozu?", S['TH'])],
        [Paragraph("Mac Mini M4", S['TC']),
         Paragraph("Mac Mini M4 | 16 GB RAM | 256 GB SSD", S['TC']),
         Paragraph("699 EUR", S['TR']),
         Paragraph("Läuft Claude Desktop dauerhaft. Kompakt, lautlos, energiesparend.", S['TC'])],
        [Paragraph("Monitor", S['TC']),
         Paragraph("24\" Full HD (Dell, LG o.Ä.)", S['TC']),
         Paragraph("180 EUR", S['TR']),
         Paragraph("Für Einrichtung und gelegentliche Kontrolle.", S['TC'])],
        [Paragraph("Maus & Tastatur", S['TC']),
         Paragraph("Beliebig (USB oder Bluetooth)", S['TC']),
         Paragraph("50 EUR", S['TR']),
         Paragraph("Für initiale Konfiguration. Danach oft nicht mehr noetig.", S['TC'])],
        [Paragraph("Pocket AI Geraet", S['TC']),
         Paragraph("Pocket AI Pendant (Clip) oder Smartphone (iOS/Android)", S['TC']),
         Paragraph("69 EUR oder 0 EUR", S['TR']),
         Paragraph("Gesprächs- & Meeting-Aufzeichnung. Immer dabei — den ganzen Tag.", S['TC'])],
        [Paragraph("<b>Einmalig gesamt</b>", S['TCB']),
         Paragraph("<i>Je nach vorhandener Ausstattung weniger</i>", S['TC']),
         Paragraph("<b>~1.000 EUR</b>", S['TCB']),
         Paragraph("Ohne Monitor & Zubehoer: ~700 EUR", S['TC'])],
    ]
    ht = Table(hw, colWidths=[88, 160, 72, 186])
    ht.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK_BLUE),
        ('ROWBACKGROUNDS',(0,1),(-1,-2),[white,GRAY_L]),
        ('BACKGROUND',(0,-1),(-1,-1),LIGHT_BLUE),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),0.25,HexColor("#c8d0dc")),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('ROWHEIGHT',(0,1),(-1,-2),30),
    ]))
    f = Frame(18, y-208, W-36, 208, leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    f.addFromList([ht], c); y -= 222

    y -= 10   # Luft zwischen den beiden Tabellen

    c.setFont("Jakarta-Bold", 10); c.setFillColor(DARK_BLUE)
    c.drawString(22, y, "Abonnements — Laufende Kosten pro Monat"); y -= 14

    sub = [
        [Paragraph("Dienst", S['TH']), Paragraph("Plan", S['TH']),
         Paragraph("EUR/Monat", S['TH']), Paragraph("Wozu?", S['TH']),
         Paragraph("Pflicht?", S['TH'])],
        [Paragraph("Claude (Anthropic)", S['TC']),
         Paragraph("Pro oder Team", S['TC']),
         Paragraph("20-25 EUR", S['TR']),
         Paragraph("Das KI-Herz von Cleo — unverzichtbar.", S['TC']),
         Paragraph("PFLICHT", S['OK'])],
        [Paragraph("Pocket AI", S['TC']),
         Paragraph("Pro (nach Free Trial)", S['TC']),
         Paragraph("~10 EUR", S['TR']),
         Paragraph("Meeting- & Gespraecsaufzeichnung + Transkript via MCP.", S['TC']),
         Paragraph("Empfohlen", S['TC'])],
        [Paragraph("OnlineBrief24", S['TC']),
         Paragraph("Pay-per-use", S['TC']),
         Paragraph("~1,20-2,50 EUR\npro Brief", S['TR']),
         Paragraph("Physischer Briefversand per API. Nur bei Nutzung.", S['TC']),
         Paragraph("Optional", S['TC'])],
        [Paragraph("Google Workspace", S['TC']),
         Paragraph("Business Starter", S['TC']),
         Paragraph("6 EUR / User", S['TR']),
         Paragraph("Gmail + Kalender + Drive (oft bereits vorhanden).", S['TC']),
         Paragraph("Falls Gmail", S['TC'])],
        [Paragraph("Notion", S['TC']),
         Paragraph("Plus oder Business", S['TC']),
         Paragraph("10-15 EUR", S['TR']),
         Paragraph("Aufgaben-DB für Tagesabschluss To-Dos.", S['TC']),
         Paragraph("Optional", S['TC'])],
        [Paragraph("<b>Gesamt laufend</b>", S['TCB']),
         Paragraph("<i>Je nach Komponenten</i>", S['TC']),
         Paragraph("<b>30-55 EUR</b>", S['TCB']),
         Paragraph("Claude Pro ist das einzige Pflicht-Abo.", S['TC']),
         Paragraph("", S['TC'])],
    ]
    st = Table(sub, colWidths=[92, 88, 70, 186, 60])
    st.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),MID_BLUE),
        ('ROWBACKGROUNDS',(0,1),(-1,-2),[white,GRAY_L]),
        ('BACKGROUND',(0,-1),(-1,-1),LIGHT_BLUE),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),0.25,HexColor("#c8d0dc")),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('ROWHEIGHT',(0,1),(-1,-2),28),
    ]))
    f2 = Frame(18, y-196, W-36, 196, leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    f2.addFromList([st], c); y -= 204

    c.setFillColor(HexColor("#fff8e8")); c.setStrokeColor(ORANGE)
    c.setLineWidth(1); c.roundRect(18, y-52, W-36, 52, 4, fill=1, stroke=1)
    c.setFillColor(ORANGE); c.roundRect(18, y-52, 5, 52, 2, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 8.5); c.setFillColor(HexColor("#8a3a00"))
    c.drawString(32, y-14, "Tipp zur Kostenminimierung")
    c.setFont("Inter", 8.5)
    c.drawString(32, y-28, "Mac Mini und Monitor sind einmalige Kosten. Claude Pro (20 EUR/Monat) reicht für Einzelnutzer.")
    c.drawString(32, y-41, "Pocket bietet 7 Tage kostenlos — erst danach entscheiden, ob das Abo sinnvoll ist.")
    c.showPage()

# —— OVERVIEW ——
def overview(c):
    hdr(c, 3, "Produkt-Überblick — 7 Module"); ftr(c)
    y = H - 44
    y = sec(c, y, "Was ist Cleo?",
            "7 Module — ein vollständiges, automatisiertes digitales Büro")
    y -= 8   # extra Luft nach Header-Box

    intro = ("Cleo läuft auf Claude Desktop und automatisiert die wichtigsten Büroaufgaben. "
             "Es liest E-Mails, bereitet Meetings nach, versendet Briefe, pflegt Kontakte "
             "und gibt rechtliche Ersteinschätzungen — vollständig ohne Programmierkenntnisse.")
    ls = wrap_text(c, intro, "Inter", 9.5, W-55)
    c.setFont("Inter", 9.5); c.setFillColor(TEXT)
    for i, l in enumerate(ls): c.drawString(22, y-i*14, l)
    y -= len(ls)*14 + 24   # mehr Luft vor dem Rahmen

    mods = [
        ("Postfach-Briefing", MID_BLUE,
         "Scannt täglich den Posteingang. Klassifiziert Mails, erstellt Antwort-Entwürfe "
         "und verschiebt alte Entwürfe (>30 Tage) automatisch in den Papierkorb."),
        ("Tagesabschluss", TEAL,
         "Liest Kalender + alle Pocket-Transkripte des Tages. Ordnet Gespräche zu, erstellt "
         "Zusammenfassungen und legt Termine, To-Dos und Entwürfe an."),
        ("Autonome Aktionen", OCEAN,
         "Nach jedem Meeting: Folge-Termine im Kalender anlegen, To-Dos in Notion erstellen, "
         "Zusammenfassungsmails an Kunden vorbereiten — vollautomatisch, konfigurierbar."),
        ("Briefversand (OB24)", PURPLE,
         "Erstellt professionelle Briefe als PDF und versendet sie physisch über OnlineBrief24. "
         "Preis wird vor dem Versand angezeigt — kein unbeabsichtigter Versand."),
        ("Mini-CRM", GREEN_M,
         "Kontaktdatenbank aus 180 Tagen E-Mail-Verlauf aufgebaut. Name, Firma, letzter Kontakt "
         "und Notizen — immer aktuell, automatisch synchronisiert."),
        ("KI-Rechtsassistent", RED,
         "KI-Rechtsassistent mit deinen Kernrechtsgebieten. Führt Fallakten mit Aktenzeichen, erstellt "
         "Formelles Schreiben und gibt Ersteinschätzungen zu Verträgen und Mahnungen."),
        ("Pocket AI Integration", AMBER,
         "Pocket zeichnet alle Gespräche und Telefonate tagsüber auf. Tagesabschluss holt alle "
         "Transkripte des Tages, ordnet sie Terminen zu und verarbeitet auch ungeplante Gespräche."),
    ]

    tw = (W - 54) / 2; th = 82
    cx = [18, 18 + tw + 10]; ry = y

    GOLD_M        = HexColor("#d4892a")
    GOLD_LIGHT_M  = HexColor("#fff8ed")
    TIME_BADGES_M = {0: "morgens", 1: "abends"}

    # Goldrahmen — nur um erste Zeile, sauber mit Floating-Label
    fr_pad_top = 16
    fr_pad_bot = 5
    fr_x   = 10
    fr_w   = W - 20
    fr_bot = ry - th - fr_pad_bot
    fr_top = ry + fr_pad_top
    fr_h   = fr_top - fr_bot
    c.setFillColor(GOLD_LIGHT_M)
    c.roundRect(fr_x, fr_bot, fr_w, fr_h, 8, fill=1, stroke=0)
    c.setStrokeColor(GOLD_M); c.setLineWidth(1.5)
    c.roundRect(fr_x, fr_bot, fr_w, fr_h, 8, fill=0, stroke=1)
    kf_label = "KERNFUNKTIONEN"
    kf_w = c.stringWidth(kf_label, "Jakarta-Bold", 7) + 18
    kf_x = (W - kf_w) / 2
    kf_y = fr_top - 8
    c.setFillColor(GOLD_LIGHT_M)
    c.rect(kf_x, kf_y - 1, kf_w, 10, fill=1, stroke=0)
    c.setFillColor(GOLD_M)
    c.roundRect(kf_x, kf_y - 1, kf_w, 12, 3, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 7); c.setFillColor(white)
    c.drawCentredString(W/2, kf_y + 2, kf_label)

    for i, (nm, col, desc) in enumerate(mods):
        co = i % 2
        if i > 0 and co == 0: ry -= th + 7
        tx = 18 + (tw+10)/2 if i == 6 else cx[co]
        c.setFillColor(GRAY_L); c.roundRect(tx, ry-th, tw, th, 5, fill=1, stroke=0)
        c.setFillColor(col); c.roundRect(tx, ry-th, 5, th, 3, fill=1, stroke=0)

        # Zeitbadge für Kernfunktionen
        if i in TIME_BADGES_M:
            tb = TIME_BADGES_M[i]
            tbw = c.stringWidth(tb, "Jakarta-Bold", 7) + 12
            c.setFillColor(GOLD_M)
            c.roundRect(tx+tw-tbw-4, ry-20, tbw, 16, 3, fill=1, stroke=0)
            c.setFont("Jakarta-Bold", 7); c.setFillColor(white)
            c.drawCentredString(tx+tw-tbw/2-4, ry-14, tb)

        # Add-on-Badge für KI-Rechtsassistent
        if i == 5:  # Index 5 in Mitarbeiter-Liste
            addon_label = "⊕ Add-on"
            adw = c.stringWidth(addon_label, "Inter", 7) + 12
            c.setFillColor(HexColor("#f0f0f0"))
            c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.5)
            c.roundRect(tx+tw-adw-4, ry-20, adw, 16, 3, fill=1, stroke=1)
            c.setFont("Inter", 7); c.setFillColor(HexColor("#666666"))
            c.drawCentredString(tx+tw-adw/2-4, ry-14, addon_label)

        c.setFont("Jakarta-Bold", 10); c.setFillColor(col)
        c.drawString(tx+14, ry-20, nm)
        c.setFont("Inter", 8.5); c.setFillColor(HexColor("#404858"))
        dls = wrap_text(c, desc, "Inter", 8.5, tw-26)
        for j, dl in enumerate(dls[:4]): c.drawString(tx+14, ry-34-j*12, dl)
    c.showPage()

# —— INSTALLATION ——
def installation(c):
    steps = [
        (0, "Vorbereitung & Pre-flight",
         ["Betriebssystem prüfen: macOS oder Windows",
          "Cleo herunterladen: install_mac.sh (macOS) oder install_windows.ps1 — Ordner 'Cleo' wird angelegt",
          "Claude Desktop installieren: claude.ai/download",
          "Cowork-Ordner ('Cleo') in Claude Desktop als Arbeitsordner einrichten",
          "OB24-Konto anlegen (falls Briefversand gewuenscht): onlinebrief24.de",
          "Kundendaten erfassen: Firmenname, Rechtsform, Branche, Standort, Straße/PLZ, Telefon, Website, USt-ID",
          "Assistenz-Identitaet festlegen: Name & Geschlecht (z.B. Clara / weiblich)"]),
        (1, "E-Mail-System verbinden",
         ["Wahl: Standard-IMAP/SMTP  |  Gmail  |  Office 365  |  Keines",
          "IMAP/SMTP: install_mac.sh (macOS) oder install_windows.ps1 ausführen",
          "Gmail / Office 365: Claude Desktop -> Connectors -> verbinden",
          "Test: 'Zeig mir meine letzten 5 Mails'"]),
        (2, "Ordnerstruktur anlegen",
         ["Claude legt alle Ordner automatisch an: Sekretariat/, Team/Rechtsassistent/",
          "CLAUDE.md und MEMORY.md werden befuellt",
          "Firmendaten, Briefkopf und leeres Mini-CRM eingetragen"]),
        (3, "Post-Requisiten hochladen",
         ["Firmenlogo als PNG (transparenter Hintergrund) -> logo.png",
          "Unterschrift/Signum als PNG -> signum_[name].png",
          "Firmendaten (Adresse, USt-ID, IBAN) werden aus Phase 0 übernommen — keine erneute Abfrage"]),
        (4, "Postfach-Briefing einrichten",
         ["Zeitfenster: 24h / 48h / 72h  (Standard: 24h — täglich morgens)",
          "Zeitplan: täglich 08:00 Uhr (empfohlen) oder manuell",
          "Ordner-Logik: Mails automatisch sortieren? Ja -> Sub-Skill wird installiert",
          "Scheduled Task anlegen (falls automatischer Zeitplan gewaehlt)"]),
        ("5", "Tagesabschluss & Pocket AI",
         ["Tagesabschluss aktivieren? Ja/Nein",
          "Kalender verbinden: Google Kalender oder Outlook",
          "Pocket AI App installieren (iOS/Android), API-Key eingeben",
          "Pocket MCP in claude_desktop_config.json eintragen (Claude zeigt Eintrag)",
          "Pocket zeichnet ALLE Gespräche des Tages auf — Tagesabschluss liest alles",
          "Zusammenfassungskanal: E-Mail / Slack / Teams / Nur in Claude"]),
        ("5c", "Autonome Aktionen festlegen",
         ["Option A (empfohlen): Alles automatisch — Termine + To-Dos + Entwürfe",
          "Option B: Individuell — z.B. nur Termine oder nur E-Mail-Entwürfe",
          "Option C: Nur Zusammenfassungen — du entscheidest selbst was folgt"]),
        (6, "CRM konfigurieren",
         ["Externes CRM? HubSpot / Salesforce / Pipedrive / Close.io / Keines",
          "CRM-Sync-Skill mit Kundenvariablen befuellen",
          "API-Key für externes CRM eingeben (falls gewaehlt)"]),
        (7, "Briefversand OB24 (optional)",
         ["Voraussetzung: OB24-Konto vorhanden (onlinebrief24.de -> kostenlos registrieren)",
          "OB24-Zugangsdaten eingeben: Benutzername, Passwort, API-Key (Mein Konto → API-Zugangsdaten)",
          "Hinweis: Job-IDs (Briefprodukte) werden beim Versand gewählt — nicht bei Installation",
          "Testmodus beim ersten Start aktivieren — kein echter Versand während Einrichtung",
          "Preis wird vor jedem Versand angezeigt -> erst mit Bestaetigung senden"]),
        (8, "KI-Rechtsassistent einrichten",
         ["Claude scannt 180 Tage E-Mail-Verlauf auf Rechtsthemen",
          "Top-5-Rechtsgebiete werden abgeleitet (z.B. DSGVO, Vertragsrecht, Mahnwesen)",
          "KI-Rechtsassistent/CLAUDE.md mit Rechtsgebieten und Aktenfuehrung befuellt"]),
        (9, "Mini-CRM vorbefuellen",
         ["Claude scannt 180 Tage E-Mail-Verlauf",
          "Top-50-Kontakte: Name, Firma, E-Mail, letzter Kontakt extrahiert",
          "Kontakttabelle in Sekretariat/CLAUDE.md eingetragen"]),
        (10, "Abschluss & Vollständiger Selbsttest [PFLICHT]",
         ["10 Tests: E-Mail lesen, Postfach-Briefing, CRM, Kalender (falls konfiguriert),",
          "  CRM-Sync, Brief-PDF, OB24-Preis, OB24-Testversand, Rechtsassistent, Formelles Schreiben",
          "Kein Schritt kann übersprungen werden — alle Tests müssen bestanden sein",
          "Uebergabedokument UEBERGABE.md wird automatisch erstellt"]),
        (12, "Cleanup & Abschluss [PFLICHT]",
         ["Installationsdateien (*.py, Temp-Dateien) werden aus dem Cleo-Ordner gelöscht",
          "Claude listet Dateien vor dem Löschen — Bestätigung erforderlich",
          "Abschlussmeldung: Cleo ist einsatzbereit"]),
    ]

    pg = 4
    hdr(c, pg, "Installation — Schritt für Schritt"); ftr(c)
    y = H - 44
    y = sec(c, y, "Installation — Phase 0 bis 10",
            "Gesamtdauer: ca. 2-4 Stunden | Claude führt alle Schritte interaktiv durch")

    for n, t, ss in steps:
        need = 26 + len(ss)*15 + 12
        if y - need < 50:
            c.showPage(); pg += 1
            hdr(c, pg, "Installation (Fortsetzung)"); ftr(c)
            y = H - 44
        c.setFillColor(LIGHT_BLUE); c.roundRect(18, y-22, W-36, 22, 4, fill=1, stroke=0)
        badge(c, 20, y-6, n, MID_BLUE)
        c.setFont("Jakarta-Bold", 10); c.setFillColor(DARK_BLUE)
        c.drawString(48, y-15, t); y -= 28
        for s in ss:
            c.setFillColor(TEAL); c.circle(30, y-5, 2.5, fill=1, stroke=0)
            c.setFont("Inter", 8.5); c.setFillColor(TEXT)
            c.drawString(38, y-9, s); y -= 15
        y -= 10
    c.showPage()

# —— DAILY USAGE ——
def daily(c):
    hdr(c, 6, "Tägliche Nutzung"); ftr(c)
    y = H - 44
    y = sec(c, y, "Tägliche Nutzung — Was du sagst, was Claude macht",
            "Dein Morgenritual mit Cleo: unter 10 Minuten")

    secs = [
        ("Morgen", MID_BLUE, [
            ("'Geh durch meinen Posteingang'",
             "Postfach-Briefing: Mails 24h, Entwürfe erstellen, Entwürfe >30 Tage in Papierkorb"),
            ("(Automatisch bei konfiguriertem Zeitplan)",
             "Postfach-Briefing startet täglich 08:00 Uhr ohne Eingabe"),
        ]),
        ("Nach Meetings", TEAL, [
            ("'Bereite meine heutigen Meetings nach'",
             "Kalender laden, alle Pocket-Transkripte des Tages holen, zuordnen, Zusammenfassungen erstellen"),
            ("(Automatisch falls aktiv)",
             "Termine, To-Dos und Kunden-Entwürfe werden ohne weiteren Eingriff angelegt"),
        ]),
        ("Autonome Aktionen", OCEAN, [
            ("(Läuft automatisch nach Tagesabschluss)",
             "Folge-Termine im Kalender | To-Dos in Notion | Zusammenfassungsmails als Entwurf"),
        ]),
        ("Brief senden", PURPLE, [
            ("'Schreibe einen Brief an [Name], [Adresse]'",
             "PDF erstellen -> Preis via OB24 abfragen -> dir anzeigen -> warten -> versenden"),
        ]),
        ("Rechtsfragen", RED, [
            ("'Prüf diesen Vertrag'  /  'Erstelle einen Mahnbrief wegen [Betrag]'",
             "KI-Rechtsassistent legt Akte an | Ersteinschätzung | Formelles Schreiben mit Aktenzeichen"),
        ]),
        ("CRM & Kontakte", GREEN_M, [
            ("'Wer ist [Name]?'  /  'Zeig meine Top-Kontakte'",
             "Claude liest Mini-CRM aus Sekretariat/CLAUDE.md"),
            ("'Synchronisiere neue Kontakte'",
             "CRM-Sync scannt Postfach, traegt neue Absender ins Mini-CRM ein"),
        ]),
    ]

    for t, col, items in secs:
        c.setFillColor(col); c.roundRect(18, y-20, W-36, 20, 3, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 9); c.setFillColor(white)
        c.drawString(28, y-14, t); y -= 25
        for cmd, res in items:
            c.setFillColor(HexColor("#f0f4fa")); c.setStrokeColor(HexColor("#c8d4e8"))
            c.setLineWidth(0.4); c.roundRect(26, y-15, W-52, 15, 3, fill=1, stroke=1)
            c.setFont("Helvetica-BoldOblique", 8.5); c.setFillColor(DARK_BLUE)
            c.drawString(34, y-11, cmd); y -= 18
            c.setFont("Inter", 8.5); c.setFillColor(GRAY_M)
            c.drawString(36, y-9, "->  " + res); y -= 18
        y -= 5
    c.showPage()

# —— TROUBLESHOOTING ——
def troubleshooting(c, S):
    hdr(c, 7, "Troubleshooting & Installations-Checkliste"); ftr(c)
    y = H - 44
    y = sec(c, y, "Troubleshooting — Haeufige Probleme & Lösungen")

    problems = [
        ("IMAP-Verbindung schlaegt fehl",
         "Credentials prüfen. Bei Gmail/O365: App-Passwort erstellen, kein normales Passwort!"),
        ("Pocket-Transkripte fehlen",
         "Pocket-App muss während des Gesprächs geoeffnet sein. Benachrichtigungen erlauben."),
        ("Tagesabschluss findet keine Meetings",
         "Claude Desktop -> Connectors -> Google Kalender verbinden. Danach Claude neu starten."),
        ("OB24-Versand schlaegt fehl",
         "OB24-Dashboard: Saldo prüfen, API-Key verifizieren (Mein Konto → API-Zugangsdaten). Testmodus aktivieren."),
        ("Autonome Termine werden nicht angelegt",
         "In meeting-review/SKILL.md: AUTO_CREATE_EVENTS = true setzen und Kalender verbinden."),
        ("Alte Entwürfe werden nicht bereinigt",
         "In inbox-review/SKILL.md: EMAIL_SYSTEM auf imap-smtp oder gmail setzen."),
        ("Claude 'vergisst' Konfiguration",
         "Richtigen Cowork-Ordner in Claude Desktop oeffnen. CLAUDE.md wird dann automatisch gelesen."),
        ("build_brief.py läuft nicht",
         "Im Terminal: pip install reportlab. Liberation Sans TTF muss in Post-Requisiten/ liegen."),
    ]

    c.setFillColor(DARK_BLUE); c.roundRect(18, y-18, W-36, 18, 3, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 8.5); c.setFillColor(white)
    c.drawString(26, y-13, "Problem"); c.drawString(228, y-13, "Lösung"); y -= 20

    for i, (p, s) in enumerate(problems):
        rh = 26
        c.setFillColor(white if i%2==0 else GRAY_L)
        c.rect(18, y-rh, W-36, rh, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#d0d8e8")); c.setLineWidth(0.3)
        c.line(18, y-rh, W-18, y-rh); c.line(224, y, 224, y-rh)
        c.setFont("Jakarta-Bold", 8.5); c.setFillColor(RED)
        c.drawString(25, y-11, p[:33]+("..." if len(p)>33 else ""))
        if len(p)>33:
            c.setFont("Inter", 7.5); c.drawString(25, y-21, p[33:55])
        c.setFont("Inter", 8.5); c.setFillColor(TEXT)
        sl = wrap_text(c, s, "Inter", 8.5, W-260)
        for j, l in enumerate(sl[:2]): c.drawString(231, y-11-j*11, l)
        y -= rh

    y -= 14
    c.setFillColor(MID_BLUE); c.roundRect(18, y-24, W-36, 24, 5, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 11); c.setFillColor(white)
    c.drawString(30, y-16, "Installations-Checkliste"); y -= 32

    items = [
        "Claude Desktop installiert und Cowork-Ordner eingerichtet",
        "E-Mail-System verbunden und getestet",
        "Ordnerstruktur vollständig (Sekretariat/, Team/Rechtsassistent/)",
        "Post-Requisiten hochgeladen (logo.png, signum_[name].png)",
        "Postfach-Briefing: Zeitfenster + Zeitplan + Ordner-Logik konfiguriert",
        "Tagesabschluss: Kalender + Pocket AI + Zusammenfassungskanal",
        "Autonome Aktionen konfiguriert (Termine / To-Dos / Entwürfe)",
        "CRM-Sync konfiguriert",
        "Briefversand OB24 konfiguriert (falls gewuenscht)",
        "KI-Rechtsassistent mit Rechtsgebieten eingerichtet",
        "Mini-CRM aus 180 Tagen E-Mail-Verlauf befuellt",
        "Alle 10 Funktionstests bestanden (Phase 10 vollständig)",
        "Installationsdateien bereinigt (Phase 12 — Cleanup)",
        "Uebergabedokument UEBERGABE.md erstellt",
    ]
    half = (len(items)+1)//2
    for i, item in enumerate(items):
        co = i//half; ro = i%half
        xi = 22 + co*((W-44)//2+2); yi = y - ro*17
        c.setFillColor(white); c.setStrokeColor(MID_BLUE); c.setLineWidth(0.8)
        c.rect(xi, yi-9, 9, 9, fill=1, stroke=1)
        c.setFont("Inter", 8.5); c.setFillColor(TEXT)
        c.drawString(xi+13, yi-8, item)
    c.showPage()

# —— QUICKREF ——
def quickref(c):
    hdr(c, 8, "Schnellreferenz — Die wichtigsten Befehle"); ftr(c)
    y = H - 44
    y = sec(c, y, "Schnellreferenz — Die wichtigsten Befehle",
            "Einfach ausdrucken und am Arbeitsplatz aufhaengen")

    secs = [
        ("E-Mail & Posteingang", MID_BLUE, [
            ("Posteingang reviewen",          "'Geh durch meinen Posteingang'"),
            ("Bestimmte Mail suchen",          "'Suche Mails von [Name]'"),
            ("CRM synchronisieren",            "'Synchronisiere neue Kontakte'"),
            ("Entwürfe bereinigen",            "(läuft automatisch beim Postfach-Briefing)"),
        ]),
        ("Meetings & Pocket", TEAL, [
            ("Heutige Meetings nachbereiten",  "'Bereite meine Meetings von heute nach'"),
            ("Einzelnes Meeting",               "'Bereite das Meeting mit [Name] nach'"),
            ("Termin anlegen",                 "'Leg einen Termin mit [Name] am [Datum] an'"),
            ("Pocket-Aufnahmen suchen",         "'Gibt es Pocket-Aufnahmen von heute?'"),
        ]),
        ("Autonome Aktionen", OCEAN, [
            ("To-Dos anlegen",                 "(automatisch nach Tagesabschluss)"),
            ("Folge-Termin anlegen",            "(automatisch wenn Datum im Meeting genannt)"),
            ("Kunden-Entwurf erstellen",        "(automatisch nach Kundengespraech)"),
        ]),
        ("Briefe & Recht", PURPLE, [
            ("Brief erstellen + senden",        "'Schreibe einen Brief an [Name, Adresse]'"),
            ("Vertrag prüfen",                 "'Prüf diesen Vertrag auf Risiken'"),
            ("Mahnbrief mit Akte",              "'Mahnbrief wegen [Betrag] — Akte anlegen'"),
            ("Rechtsgebiete anzeigen",          "'Welche Rechtsgebiete sind relevant?'"),
        ]),
    ]

    for t, col, cmds in secs:
        c.setFillColor(col); c.roundRect(18, y-20, W-36, 20, 3, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 9); c.setFillColor(white)
        c.drawString(28, y-14, t); y -= 22
        for desc, cmd in cmds:
            c.setFillColor(GRAY_L); c.rect(18, y-17, W-36, 17, fill=1, stroke=0)
            c.setStrokeColor(HexColor("#d0d8e8")); c.setLineWidth(0.2)
            c.line(18, y-17, W-18, y-17)
            c.setFont("Inter", 8.5); c.setFillColor(GRAY_M)
            c.drawString(28, y-12, desc)
            c.setFont("Helvetica-BoldOblique", 8.5); c.setFillColor(DARK_BLUE)
            c.drawRightString(W-26, y-12, cmd)
            y -= 17
        y -= 8

    y -= 8
    c.setFillColor(GREEN_L); c.setStrokeColor(GREEN_D)
    c.setLineWidth(1); c.roundRect(18, y-46, W-36, 46, 5, fill=1, stroke=1)
    c.setFillColor(GREEN_D); c.roundRect(18, y-46, 5, 46, 2, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 9); c.setFillColor(GREEN_D)
    c.drawString(32, y-14, "Support")
    c.setFont("Inter", 8.5); c.setFillColor(TEXT)
    c.drawString(32, y-27, "Bei Fragen zur Installation oder täglichen Nutzung: Installationspartner kontaktieren.")
    c.drawString(32, y-40, "Kontaktdaten: UEBERGABE.md in deinem Cowork-Ordner.")
    c.showPage()

# —— MAIN ——
def install_guide(c):
    """Konkrete Vor-Ort-Installations-Checkliste"""
    hdr(c, 4, "Vor-Ort-Installation — Konkrete Schritte"); ftr(c)
    y = H - 44

    # ── Header-Box ────────────────────────────────────────────────────────
    y = sec(c, y, "Installations-Checkliste — Was auf dem Kunden-Rechner zu tun ist",
            "Schritt für Schritt | Gesamtdauer: ca. 2–4 Stunden")
    y -= 10

    CHCK  = HexColor("#e8f0fb")   # Checkbox-Hintergrund
    DONE  = HexColor("#1a7a4a")   # grüner Haken
    WARN  = HexColor("#f4842d")   # orange Hinweis
    URL   = HexColor("#0077b6")   # Link-Farbe
    STEP_BG = HexColor("#f0f4fa")

    def block(title, num_color, steps, note=None):
        nonlocal y
        # Schritt-Header
        c.setFillColor(num_color)
        c.roundRect(18, y-24, W-36, 24, 4, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 10); c.setFillColor(white)
        c.drawString(30, y-16, title)
        y -= 30

        for item_type, text in steps:
            # Zeilenumbruch falls nötig
            lines = wrap_text(c, text, "Inter", 8.5, W-80)
            row_h = len(lines) * 13 + 8
            if y - row_h < 50:
                return  # overflow guard

            if item_type == "cmd":
                # Code-Zeile
                c.setFillColor(HexColor("#1a2232"))
                c.roundRect(28, y-row_h+2, W-56, row_h, 3, fill=1, stroke=0)
                c.setFont("Inter", 8); c.setFillColor(HexColor("#7dd3a8"))
                for k, l in enumerate(lines):
                    c.drawString(38, y-12-k*13, l)
            elif item_type == "url":
                c.setFillColor(CHCK); c.roundRect(28, y-row_h+2, W-56, row_h, 2, fill=1, stroke=0)
                c.setFillColor(URL); c.circle(38, y-8, 3, fill=1, stroke=0)
                c.setFont("Inter", 8.5); c.setFillColor(URL)
                for k, l in enumerate(lines):
                    c.drawString(46, y-12-k*13, l)
            elif item_type == "warn":
                c.setFillColor(HexColor("#fff3e8")); c.roundRect(28, y-row_h+2, W-56, row_h, 2, fill=1, stroke=0)
                c.setFillColor(WARN); c.rect(28, y-row_h+2, 4, row_h, fill=1, stroke=0)
                c.setFont("Inter", 8.5); c.setFillColor(HexColor("#8a3a00"))
                for k, l in enumerate(lines):
                    c.drawString(38, y-12-k*13, l)
            else:
                # Normaler Schritt mit Checkbox
                c.setFillColor(STEP_BG); c.roundRect(28, y-row_h+2, W-56, row_h, 2, fill=1, stroke=0)
                c.setStrokeColor(GRAY_M); c.setLineWidth(0.8)
                c.roundRect(34, y-13, 9, 9, 1, fill=0, stroke=1)
                c.setFont("Inter", 8.5); c.setFillColor(TEXT)
                for k, l in enumerate(lines):
                    c.drawString(48, y-12-k*13, l)

            y -= row_h + 3

        if note:
            c.setFont("Inter", 7.5); c.setFillColor(GRAY_M)
            c.drawString(30, y, "→ " + note)
            y -= 14
        y -= 8

    # ── BLOCK 1 ───────────────────────────────────────────────────────────
    block("① Vorbereitung  (10 Min.)", DARK_BLUE, [
        ("step", "Cleo herunterladen — Installer aus dem GitHub-Repo ausführen:"),
        ("cmd",  "macOS:   bash install_mac.sh   →  Ordner ~/Cleo wird angelegt"),
        ("cmd",  "Windows: install_windows.ps1 (Rechtsklick → Mit PowerShell ausführen)"),
        ("step", "Claude Desktop herunterladen & installieren"),
        ("url",  "https://claude.ai/download"),
        ("step", "Claude Pro-Abo prüfen: claude.ai → Account → Subscription"),
        ("step", "Claude Desktop → Einstellungen → Ordner hinzufügen → Ordner '~/Cleo' wählen"),
        ("warn", "Installer legt den Cleo-Ordner automatisch an — nichts manuell erstellen"),
    ], note="Ohne aktives Pro-Abo läuft Cleo nicht")

    # ── BLOCK 2 ───────────────────────────────────────────────────────────
    block("② E-Mail verbinden  (10–20 Min.)", MID_BLUE, [
        ("step", "Gmail: Claude Desktop → Connectors → Gmail → verbinden"),
        ("step", "IMAP/SMTP (z.B. Outlook, GMX, 1&1): Terminal öffnen, Skript ausführen:"),
        ("cmd",  "bash <(curl -sL https://raw.githubusercontent.com/yurka-alexx/Cleo/main/imap-smtp-mcp/install_mac.sh)"),
        ("warn", "Windows: PowerShell als Admin → irm [Repo-URL]/install_windows.ps1 | iex"),
        ("step", "Bereithalten: IMAP-Server, Port (993), Benutzername, App-Passwort"),
        ("step", "Test nach Verbindung: 'Zeig mir meine letzten 5 Mails'"),
    ])

    # ── BLOCK 3 ───────────────────────────────────────────────────────────
    block("③ Cleo-Installationsflow starten  (60–90 Min.)", TEAL, [
        ("step", "Claude Desktop öffnen → Cowork-Ordner aktiv (grüner Punkt)"),
        ("step", "Im Chat eingeben:"),
        ("cmd",  "Führe den Cleo Installationsflow aus."),
        ("step", "Kundendaten bereithalten: Firmenname, Rechtsform, Branche, Ansprechpartner"),
        ("step", "Autonomie-Level wählen wenn gefragt: 1 = Vorschläge  /  2 = Entwürfe  /  3 = Vollautomatisch"),
        ("warn", "Claude fragt Schritt für Schritt — einfach antworten, nichts manuell anlegen"),
    ])

    # ── BLOCK 4 ───────────────────────────────────────────────────────────
    block("④ Pocket AI (optional, 15 Min.)", AMBER, [
        ("step", "App installieren: App Store / Google Play → 'Pocket AI'"),
        ("url",  "iOS: apps.apple.com/app/pocket-ai/id6504287901"),
        ("step", "In App: Account erstellen → Einstellungen → API-Key kopieren"),
        ("step", "claude_desktop_config.json öffnen (Claude Desktop → Einstellungen → Erweitert)"),
        ("step", "Pocket-MCP-Eintrag einfügen — Claude zeigt den exakten JSON-Block"),
        ("step", "Claude Desktop neu starten → Pocket-Verbindung testen"),
    ], note="Pocket zeichnet alle Gespräche & Meetings des Tages auf")

    # ── BLOCK 5 ───────────────────────────────────────────────────────────
    block("⑤ Abschluss & Übergabe  (20 Min.)", GREEN_D, [
        ("step", "Firmenlogo (logo.png) + Unterschrift (signum_name.png) in Sekretariat/Post-Requisiten/ ablegen"),
        ("step", "10 Funktionstests: Claude leitet automatisch durch (Phase 10 — PFLICHT, darf nicht verkürzt werden)"),
        ("step", "Cleanup: Claude löscht Installationsdateien (*.py, Temp) nach Bestätigung (Phase 12)"),
        ("step", "Übergabedokument öffnen: UEBERGABE.md im Cowork-Ordner"),
        ("step", "Kurze Einweisung: Wichtigste Befehle zeigen (Seite 8 dieser Anleitung)"),
        ("warn", "Förderung (BAFA): Antrag VOR Installation stellen — rückwirkend nicht möglich!"),
    ])

    c.showPage()


def build(out):
    cv = canvas.Canvas(out, pagesize=A4)
    cv.setTitle("Cleo — Mitarbeiteranleitung v2")
    S = styles()
    cover(cv)
    hardware(cv, S)
    overview(cv)
    install_guide(cv)
    installation(cv)
    daily(cv)
    troubleshooting(cv, S)
    quickref(cv)
    cv.save()
    print("PDF erstellt: " + out)

build("/sessions/peaceful-pensive-lamport/mnt/Cowork OS/Cleo-Mitarbeiter.pdf")
