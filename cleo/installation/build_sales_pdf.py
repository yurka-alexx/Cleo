#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cleo — Verkaufs-PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
_FONT_DIR = "/sessions/peaceful-pensive-lamport/fonts"
pdfmetrics.registerFont(TTFont("Jakarta-Bold",    _FONT_DIR + "/PlusJakartaSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Jakarta",         _FONT_DIR + "/PlusJakartaSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter",           _FONT_DIR + "/Inter-Regular.ttf"))

from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

W, H = A4

# Farbpalette
DARK        = HexColor("#0D1220")
NAVY        = HexColor("#1A1A2E")
BLUE        = HexColor("#0F7A8A")
TEAL        = HexColor("#0F7A8A")
LIGHT_TEAL  = HexColor("#E5F4F6")
ORANGE      = HexColor("#E8855A")
LIGHT_ORANGE= HexColor("#FDF1EC")
GRAY_L      = HexColor("#F5F5F0")
GRAY_M      = HexColor("#6B6B8A")
GRAY_D      = HexColor("#3A3A5A")
TEXT        = HexColor("#1A1A2E")
WHITE       = white
GREEN       = HexColor("#0F7A8A")
GREEN_L     = HexColor("#E5F4F6")
GOLD        = HexColor("#E8855A")
GOLD_L      = HexColor("#FDF1EC")
PURPLE      = HexColor("#0F7A8A")
PURPLE_L    = HexColor("#E5F4F6")

def wrap(c, text, font, size, max_w):
    words = text.split()
    line, lines = "", []
    for w in words:
        t = (line + " " + w).strip()
        if c.stringWidth(t, font, size) < max_w:
            line = t
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines

def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle('TH', fontName='Jakarta-Bold', fontSize=8.5, leading=11, textColor=WHITE, alignment=TA_CENTER))
    s.add(ParagraphStyle('TC', fontName='Inter', fontSize=8.5, leading=12, textColor=TEXT))
    s.add(ParagraphStyle('TCB', fontName='Jakarta-Bold', fontSize=8.5, leading=12, textColor=TEXT))
    s.add(ParagraphStyle('TBLUE', fontName='Jakarta-Bold', fontSize=8.5, leading=12, textColor=BLUE))
    s.add(ParagraphStyle('TGREEN', fontName='Jakarta-Bold', fontSize=8.5, leading=12, textColor=GREEN))
    return s

def ftr(c, pg):
    c.setStrokeColor(HexColor("#E0E0D8"))
    c.setLineWidth(0.5)
    c.line(30, 24, W-30, 24)
    c.setFont("Inter", 7.5)
    c.setFillColor(GRAY_M)
    c.drawString(30, 13, "Cleo  |  Ihr KI-Sekretariat für den Büroalltag")
    c.drawRightString(W-30, 13, "Seite " + str(pg))


# =============================================================================
# SEITE 1 — COVER
# =============================================================================
def cover(c):
    # Hintergrund
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Teal-Akzentstreifen links
    c.setFillColor(TEAL)
    c.rect(0, 0, 7, H, fill=1, stroke=0)

    # Obere Zierflaeche
    p = c.beginPath()
    p.moveTo(0, H); p.lineTo(W, H)
    p.lineTo(W, H*0.62); p.lineTo(0, H*0.74)
    p.close()
    c.setFillColor(HexColor("#0F1A35"))
    c.drawPath(p, fill=1, stroke=0)

    # Dekorationskreis rechts oben
    c.setFillColor(HexColor("#0D1525"))
    c.circle(W-60, H-60, 120, fill=1, stroke=0)
    c.setFillColor(HexColor("#0A1020"))
    c.circle(W-60, H-60, 80, fill=1, stroke=0)

    # Teal-Ring
    c.setStrokeColor(TEAL)
    c.setLineWidth(2)
    c.setFillColor(HexColor("#162040"))
    c.circle(W-60, H-60, 50, fill=1, stroke=1)
    c.setFont("Jakarta-Bold", 11)
    c.setFillColor(TEAL)
    c.drawCentredString(W-60, H-56, "KI-")
    c.drawCentredString(W-60, H-70, "Sekretariat")

    # Badge oben links
    c.setFillColor(TEAL)
    c.roundRect(30, H-52, 160, 22, 4, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 8.5)
    c.setFillColor(WHITE)
    c.drawString(42, H-44, "Digitalisierung leicht gemacht")

    # Haupttitel
    c.setFont("Jakarta-Bold", 40)
    c.setFillColor(WHITE)
    c.drawString(30, H-130, "Cleo")

    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(HexColor("#7FCFD8"))
    c.drawString(30, H-158, "Ihr KI-Sekretariat für den Büroalltag")

    c.setStrokeColor(TEAL)
    c.setLineWidth(2)
    c.line(30, H-172, 360, H-172)

    # Hook-Satz
    c.setFont("Inter", 12)
    c.setFillColor(ORANGE)
    c.drawString(30, H-192, "Stell dir vor, ChatGPT könnte Aufgaben für dich erledigen")
    c.drawString(30, H-208, "— oder sogar Briefe für dich verschicken.")
    c.setFont("Jakarta-Bold", 10)
    c.setFillColor(TEAL)
    c.drawString(30, H-228, "Genau das ist Cleo.")

    # Teasertext
    c.setFont("Inter", 10)
    c.setFillColor(HexColor("#b0c8e0"))
    teaser = [
        "E-Mails bearbeiten. Meetings nachbereiten. Briefe versenden.",
        "Kontakte verwalten. Rechtsfragen klären.",
        "Alles automatisch — während Sie sich ums Wesentliche kümmern.",
    ]
    for i, t in enumerate(teaser):
        c.drawString(30, H-256-i*16, t)

    # Feature-Chips
    chips = ["E-Mail-Analyse", "Tagesabschluss", "Briefversand", "Mini-CRM",
             "KI-Rechtsberatung", "Terminplanung", "To-Do-Erstellung"]
    cx, cy = 30, H-312
    c.setFont("Inter", 9)
    for chip in chips:
        cw = c.stringWidth(chip, "Inter", 9) + 20
        if cx + cw > W - 30:
            cx = 30
            cy -= 26
        c.setFillColor(HexColor("#1c3550"))
        c.roundRect(cx, cy-5, cw, 18, 4, fill=1, stroke=0)
        c.setFillColor(HexColor("#7FCFD8"))
        c.drawString(cx+10, cy+1, chip)
        cx += cw + 8

    # Datenschutz-Highlight-Banner
    banner_y = cy - 28
    banner_h = 28
    c.setFillColor(HexColor("#0D1525"))
    c.roundRect(30, banner_y - banner_h, W - 60, banner_h, 5, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(30, banner_y - banner_h, 4, banner_h, 3, fill=1, stroke=0)
    # Schloss-Icon (einfach gezeichnet)
    lx, ly = 46, banner_y - banner_h/2
    c.setFillColor(TEAL)
    c.roundRect(lx - 5, ly - 5, 10, 8, 1, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.arc(lx - 3, ly - 1, lx + 3, ly + 5, 0, 180)
    # Text
    c.setFont("Jakarta-Bold", 8.5)
    c.setFillColor(TEAL)
    c.drawString(62, banner_y - banner_h/2 - 3, "Lokal gespeichert — ")
    title_w = c.stringWidth("Lokal gespeichert — ", "Jakarta-Bold", 8.5)
    c.setFont("Inter", 8.5)
    c.setFillColor(HexColor("#b0c8e0"))
    c.drawString(62 + title_w, banner_y - banner_h/2 - 3,
                 "Alle Arbeitsdateien bleiben auf Ihrem Computer. Kein Cloud-Zwang. Wie beim echten Sekretariat.")

    # USP-Box unten
    box_y = H * 0.38
    c.setFillColor(HexColor("#0D1525"))
    c.roundRect(22, box_y-90, W-44, 90, 6, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.roundRect(22, box_y-90, W-44, 90, 6, fill=0, stroke=1)

    usps = [
        ("~2h/Tag", "durchschnittlich gesparte Bürozeit"),
        ("30-55 EUR", "monatliche Betriebskosten"),
        ("bis 80%", "BAFA-Förderung möglich"),
    ]
    col_w = (W-44) / 3
    for i, (val, label) in enumerate(usps):
        xi = 22 + i * col_w
        if i > 0:
            c.setStrokeColor(HexColor("#1e3a5f"))
            c.setLineWidth(0.5)
            c.line(xi, box_y-10, xi, box_y-80)
        c.setFont("Jakarta-Bold", 22)
        c.setFillColor(TEAL)
        c.drawCentredString(xi + col_w/2, box_y-38, val)
        c.setFont("Inter", 8.5)
        c.setFillColor(HexColor("#8ab8d8"))
        c.drawCentredString(xi + col_w/2, box_y-56, label)

    # Unten
    c.setFont("Inter", 8)
    c.setFillColor(GRAY_M)
    c.drawString(30, 28, "Installiert und konfiguriert von Ihrem Digitalisierungspartner  |  April 2026")
    c.showPage()


# =============================================================================
# SEITE 2 — DAS PROBLEM
# =============================================================================
def problem(c):
    ftr(c, 2)

    # Header
    c.setFillColor(DARK)
    c.roundRect(18, H-70, W-36, 50, 6, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(32, H-44, "Kommen Ihnen diese Situationen bekannt vor?")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawString(32, H-60, "Das sind die fünf größten Zeitfresser im Büroalltag kleiner Unternehmen")

    y = H - 90

    problems = [
        ("E-Mails fressen den halben Tag",
         "Durchschnittlich 2,5 Stunden täglich für E-Mails — davon ist ein Großteil Spam, "
         "Weiterleitungen und Mails, die sich mit einem Satz beantworten lassen. Echte Arbeit "
         "bleibt auf der Strecke.",
         ORANGE, "2,5h/Tag"),
        ("Meeting-Ergebnisse verschwinden im Nirwana",
         "Das Gespräch war gut, die Notizen rudimentär. Eine Woche später: Was war nochmal "
         "der nächste Schritt? Wer sollte das Angebot schicken? Nachfassen kostet mehr Zeit "
         "als das Original-Meeting.",
         BLUE, "30% Verlust"),
        ("Briefe, Mahnungen, Rechtliche Schreiben — manuell, jedes Mal",
         "Jeder Brief manuell aufgesetzt, formatiert, ausgedruckt oder als PDF gespeichert. "
         "Für eine Mahnung über 200 EUR verbringen manche Unternehmer 45 Minuten.",
         PURPLE, "45 Min/Brief"),
        ("Kontakte verstreut über Notizzettel, Excel, Outlook",
         "Wer war das nochmal — Frau Müller oder Müller? Welche Firma? Wann hatten wir "
         "zuletzt Kontakt? Ohne strukturiertes CRM geht tägliche Suchzeit drauf.",
         HexColor("#c0392b"), "Kein Überblick"),
        ("Rechtsfragen enden mit teuren Anwaltsbesuchen",
         "Standardfragen zu Verträgen, Mahnungen oder DSGVO-Pflichten kosten schnell "
         "200-400 EUR pro Beratungsstunde — auch wenn die Frage in 2 Minuten beantwortbar wäre.",
         HexColor("#d4892a"), "200 EUR/Stunde"),
    ]

    for i, (title, desc, color, stat) in enumerate(problems):
        rh = 68
        bg = GRAY_L if i % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.roundRect(18, y-rh, W-36, rh, 4, fill=1, stroke=0)

        # Farbiger linker Balken
        c.setFillColor(color)
        c.roundRect(18, y-rh, 5, rh, 2, fill=1, stroke=0)

        # Stat-Badge rechts
        c.setFillColor(color)
        badge_w = c.stringWidth(stat, "Jakarta-Bold", 9) + 16
        c.roundRect(W-28-badge_w, y-22, badge_w, 18, 4, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 9)
        c.setFillColor(WHITE)
        c.drawCentredString(W-28-badge_w/2, y-16, stat)

        # Nummer
        c.setFont("Jakarta-Bold", 14)
        c.setFillColor(color)
        c.drawString(30, y-26, str(i+1) + ".")

        # Titel
        c.setFont("Jakarta-Bold", 10)
        c.setFillColor(TEXT)
        c.drawString(50, y-22, title)

        # Beschreibung
        c.setFont("Inter", 8.5)
        c.setFillColor(GRAY_D)
        dlines = wrap(c, desc, "Inter", 8.5, W-100)
        for j, dl in enumerate(dlines[:2]):
            c.drawString(50, y-36-j*12, dl)

        y -= rh + 6

    # Abschlusszeile
    c.setFillColor(LIGHT_TEAL)
    c.roundRect(18, y-42, W-36, 42, 5, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(18, y-42, 5, 42, 2, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 10)
    c.setFillColor(HexColor("#005a50"))
    c.drawString(32, y-16, "Zusammen sind das schnell 3-4 Stunden pro Tag, die Sie nicht in Ihr Kerngeschäft investieren.")
    c.setFont("Inter", 9)
    c.drawString(32, y-32, "Cleo löst genau diese Probleme — vollständig automatisiert, ohne Programmierkenntnisse.")
    c.showPage()


# =============================================================================
# SEITE 3 — DIE LOESUNG
# =============================================================================
def solution(c):
    ftr(c, 3)

    c.setFillColor(DARK)
    c.roundRect(18, H-70, W-36, 50, 6, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(32, H-44, "Cleo — Ihr digitales Büro")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawString(32, H-60, "7 integrierte Module, ein zentrales KI-System, keine technischen Kenntnisse erforderlich")

    y = H - 90

    # Einleitungstext
    c.setFont("Inter", 10)
    c.setFillColor(TEXT)
    intro = ("Cleo ist ein vollständig vorkonfiguriertes KI-System, das auf Claude Desktop läuft "
             "und als Ihr persönliches digitales Sekretariat fungiert. Sie sprechen mit ihm wie mit einem "
             "Mitarbeiter — in normaler Sprache, ohne Befehle oder Technik-Wissen.")
    ilines = wrap(c, intro, "Inter", 10, W-55)
    for i, il in enumerate(ilines):
        c.drawString(22, y-i*15, il)
    y -= len(ilines)*15 + 15

    modules = [
        ("Postfach-Briefing", BLUE,
         "Scannt täglich Ihren Posteingang. Klassifiziert Mails (Spam, Archiv, Antwort), "
         "erstellt Antwort-Entwürfe und legt Zusammenfassungen automatisch im richtigen Ordner ab.",
         "Spart ~1,5h täglich"),
        ("Tagesabschluss", TEAL,
         "Liest Kalender und alle Gesprächs-Transkripte des Tages. Ordnet Pocket-Aufnahmen zu, "
         "erstellt Zusammenfassungen, legt Folge-Termine und To-Dos automatisch an.",
         "Kein Nacharbeiten mehr"),
        ("Physischer Briefversand", PURPLE,
         "Erstellt professionelle Briefe als PDF und versendet sie direkt per Post über "
         "OnlineBrief24 — mit Preisanzeige vor dem Versand. Mahnungen, Anschreiben, alles.",
         "45 Min -> 2 Min"),
        ("Mini-CRM", HexColor("#2e8b57"),
         "Baut aus Ihrem E-Mail-Verlauf (180 Tage) automatisch eine Kontaktdatenbank auf. "
         "Name, Firma, letzter Kontakt, Kontext — immer aktuell, kein manuelles Pflegen.",
         "Volle Übersicht"),
        ("KI-Rechtsassistent", HexColor("#c0392b"),
         "Prüft Verträge, erstellt rechtliche Dokumente mit Aktenzeichen, gibt Ersteinschätzungen "
         "zu DSGVO und Co. Kein Ersatz für einen Rechtsanwalt — rechtliche Hinweise und Vorlagen.",
         "Erspart viele Rechtsberatungskosten"),
        ("Autonome Aktionen", HexColor("#0077b6"),
         "Nach jedem Meeting oder Gespräch: Folge-Termine im Kalender anlegen, To-Dos "
         "in Ihrer Aufgaben-App erstellen, Zusammenfassungsmails an Kunden — ohne Ihr Zutun.",
         "Level 1-3 wählbar"),
        ("CRM-Sync", HexColor("#d4892a"),
         "Synchronisiert neue Kontakte aus dem Postfach ins Mini-CRM und optional in Ihr "
         "externes CRM (HubSpot, Salesforce, Pipedrive, Close.io).",
         "Immer aktuell"),
    ]

    tw = (W - 54) / 2
    th = 86
    cols = [18, 18 + tw + 10]
    ry = y

    GOLD_S       = TEAL
    GOLD_LIGHT_S = LIGHT_TEAL
    TIME_BADGES  = {0: "morgens", 1: "abends"}

    # Goldrahmen — nur um erste Zeile, sauber mit Floating-Label
    fr_pad_top = 10      # Platz oben (für Label)
    fr_pad_bot = 5       # kleiner als 7px Zeilenabstand → kein Overlap
    fr_x   = 10
    fr_w   = W - 20
    fr_bot = ry - th - fr_pad_bot
    fr_top = ry + fr_pad_top
    fr_h   = fr_top - fr_bot
    c.setFillColor(GOLD_LIGHT_S)
    c.roundRect(fr_x, fr_bot, fr_w, fr_h, 8, fill=1, stroke=0)
    c.setStrokeColor(GOLD_S); c.setLineWidth(1.5)
    c.roundRect(fr_x, fr_bot, fr_w, fr_h, 8, fill=0, stroke=1)
    # Floating-Label auf dem oberen Rand, zentriert
    kf_label = "KERNFUNKTIONEN"
    kf_w = c.stringWidth(kf_label, "Jakarta-Bold", 7) + 18
    kf_x = (W - kf_w) / 2
    kf_y = fr_top - 8   # sitzt auf dem oberen Rand
    c.setFillColor(GOLD_LIGHT_S)          # deckt den Rand ab
    c.rect(kf_x, kf_y - 1, kf_w, 10, fill=1, stroke=0)
    c.setFillColor(GOLD_S)
    c.roundRect(kf_x, kf_y - 1, kf_w, 12, 3, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 7); c.setFillColor(WHITE)
    c.drawCentredString(W/2, kf_y + 2, kf_label)

    for i, (nm, col, desc, badge) in enumerate(modules):
        co = i % 2
        if i > 0 and co == 0:
            ry -= th + 7
        if i == 6:
            tx = 18 + (tw + 10) / 2
        else:
            tx = cols[co]

        c.setFillColor(GRAY_L)
        c.roundRect(tx, ry-th, tw, th, 5, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(tx, ry-th, 5, th, 3, fill=1, stroke=0)

        # Haupt-Badge (nicht für Add-on Modul)
        if i != 4:
            bw = c.stringWidth(badge, "Jakarta-Bold", 7.5) + 14
            c.setFillColor(col)
            c.roundRect(tx+tw-bw-4, ry-20, bw, 16, 3, fill=1, stroke=0)
            c.setFont("Jakarta-Bold", 7.5); c.setFillColor(WHITE)
            c.drawCentredString(tx+tw-bw/2-4, ry-14, badge)
        else:
            bw = 0  # kein Haupt-Badge für Add-on

        # Zeitbadge für Kernfunktionen
        if i in TIME_BADGES:
            tb = TIME_BADGES[i]
            tbw = c.stringWidth(tb, "Jakarta-Bold", 7) + 12
            c.setFillColor(GOLD_S)
            c.roundRect(tx+tw-bw-tbw-8, ry-20, tbw, 16, 3, fill=1, stroke=0)
            c.setFont("Jakarta-Bold", 7); c.setFillColor(WHITE)
            c.drawCentredString(tx+tw-bw-tbw/2-8, ry-14, tb)

        # Add-on-Badge für KI-Rechtsassistent (alleiniger Badge)
        if i == 4:
            addon_label = "⊕ Add-on"
            adw = c.stringWidth(addon_label, "Inter", 7) + 12
            c.setFillColor(HexColor("#f0f0f0"))
            c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.5)
            c.roundRect(tx+tw-adw-4, ry-20, adw, 16, 3, fill=1, stroke=1)
            c.setFont("Inter", 7); c.setFillColor(HexColor("#666666"))
            c.drawCentredString(tx+tw-adw/2-4, ry-14, addon_label)

        c.setFont("Jakarta-Bold", 10)
        c.setFillColor(col)
        c.drawString(tx+14, ry-20, nm)

        c.setFont("Inter", 8.5)
        c.setFillColor(GRAY_D)
        dls = wrap(c, desc, "Inter", 8.5, tw-26)
        for j, dl in enumerate(dls[:4]):
            c.drawString(tx+14, ry-34-j*12, dl)

    # ── MacBook Mockup ──────────────────────────────────────────────────────
    mock_bottom_of_modules = ry - th   # unterster Punkt der letzten Modulbox
    mock_w   = 310
    screen_h = 170
    body_h   = 12
    base_w   = mock_w * 1.08
    mx = (W - mock_w) / 2
    my = mock_bottom_of_modules - 22   # Oberkante Mockup

    # Schatten
    c.setFillColor(HexColor("#00000018"))
    c.roundRect(mx + 6, my - screen_h - body_h - 4, mock_w, screen_h + body_h, 10, fill=1, stroke=0)

    # Screen-Bezel (dunkelgrau)
    c.setFillColor(HexColor("#1c1c1e"))
    c.roundRect(mx, my - screen_h, mock_w, screen_h, 8, fill=1, stroke=0)

    # Screen-Inhalt (Cleo-Navy)
    pad = 7
    sc_x = mx + pad
    sc_y = my - screen_h + pad
    sc_w = mock_w - 2*pad
    sc_h = screen_h - 2*pad
    c.setFillColor(NAVY)
    c.roundRect(sc_x, sc_y, sc_w, sc_h, 4, fill=1, stroke=0)

    # Titelleiste
    bar_h = 18
    c.setFillColor(HexColor("#0D1220"))
    c.rect(sc_x, sc_y + sc_h - bar_h, sc_w, bar_h, fill=1, stroke=0)
    # Ampel-Punkte
    for dot_x, dot_col in [(sc_x+10, "#ff5f57"), (sc_x+22, "#febc2e"), (sc_x+34, "#28c840")]:
        c.setFillColor(HexColor(dot_col))
        c.circle(dot_x, sc_y + sc_h - bar_h/2, 4, fill=1, stroke=0)
    # App-Titel "Cleo"
    c.setFont("Jakarta-Bold", 7)
    c.setFillColor(HexColor("#8899aa"))
    c.drawCentredString(sc_x + sc_w/2, sc_y + sc_h - bar_h + 5, "Cleo")

    # Chat-Bereich
    chat_top = sc_y + sc_h - bar_h - 8

    # User-Nachricht (rechts, Cleo-Orange)
    msg_user = "Fass mir mein Postfach zusammen"
    msg_w_u  = c.stringWidth(msg_user, "Inter", 7) + 16
    bubble_x = sc_x + sc_w - msg_w_u - 8
    bubble_y = chat_top - 22
    c.setFillColor(ORANGE)
    c.roundRect(bubble_x, bubble_y, msg_w_u, 14, 4, fill=1, stroke=0)
    c.setFont("Inter", 7)
    c.setFillColor(WHITE)
    c.drawString(bubble_x + 8, bubble_y + 4, msg_user)

    # Cleo-Antwort (links, dunkel)
    reply_lines = ["Ich scanne Ihr Postfach...", "3 neue Anfragen, 1 dringend."]
    c.setFillColor(HexColor("#1e3a4a"))
    r_bx = sc_x + 8
    r_by = bubble_y - 36
    r_bw = c.stringWidth(reply_lines[0], "Inter", 7) + 16
    c.roundRect(r_bx, r_by, r_bw, 28, 4, fill=1, stroke=0)
    c.setFont("Inter", 7)
    c.setFillColor(HexColor("#a0c8d8"))
    for k, rl in enumerate(reply_lines):
        c.drawString(r_bx + 8, r_by + 18 - k*11, rl)

    # Avatar-Punkt "C"
    c.setFillColor(TEAL)
    c.circle(sc_x + 8, r_by + 14, 5, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 5)
    c.setFillColor(WHITE)
    c.drawCentredString(sc_x + 8, r_by + 12, "C")

    # Eingabefeld
    inp_y = sc_y + 6
    c.setFillColor(HexColor("#0D1220"))
    c.roundRect(sc_x + 6, inp_y, sc_w - 12, 13, 4, fill=1, stroke=0)
    c.setFont("Inter", 6.5)
    c.setFillColor(HexColor("#4a6070"))
    c.drawString(sc_x + 14, inp_y + 4, "Nachricht an Cleo...")

    # Unterer Body (Aluminium)
    c.setFillColor(HexColor("#d1d1d6"))
    c.roundRect(mx, my - screen_h - body_h, mock_w, body_h, 2, fill=1, stroke=0)
    # Notch
    notch_w = 40
    c.setFillColor(HexColor("#b0b0b8"))
    c.rect(mx + (mock_w - notch_w)/2, my - screen_h - body_h, notch_w, 3, fill=1, stroke=0)

    # Base/Standfuß
    base_x = mx - (base_w - mock_w)/2
    c.setFillColor(HexColor("#c8c8d0"))
    c.roundRect(base_x, my - screen_h - body_h - 4, base_w, 4, 2, fill=1, stroke=0)

    c.showPage()


# =============================================================================
# SEITE 4 — AUTONOMIE-LEVEL
# =============================================================================
def autonomy(c):
    ftr(c, 4)

    c.setFillColor(DARK)
    c.roundRect(18, H-70, W-36, 50, 6, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(32, H-44, "Sie bestimmen das Tempo — 3 Autonomie-Level")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawString(32, H-60, "Starten Sie konservativ und erweitern Sie nach Belieben")

    y = H - 90

    c.setFont("Inter", 10)
    c.setFillColor(TEXT)
    c.drawString(22, y, "Cleo passt sich Ihrem Vertrauen an. Sie entscheiden, wie viel das System selbstständig erledigt.")
    c.drawString(22, y-14, "Eine einfache Einstellung genügt — Sie können jederzeit wechseln.")
    y -= 36

    levels = [
        ("1", "Beobachter", BLUE, HexColor("#e8f0fb"),
         "Das System liest und analysiert — Sie entscheiden alles selbst.",
         [
             "E-Mails klassifizieren (Spam, Archiv, Antwort)",
             "Meetings zusammenfassen und Key Points aufzeigen",
             "Kontakte und Rechtsthemen identifizieren",
             "Briefentwürfe zur Prüfung vorlegen",
             "Morgen-Briefing und Meeting-Zusammenfassungen erstellen",
         ],
         "Ideal für den Einstieg"),
        ("2", "Assistent", TEAL, LIGHT_TEAL,
         "Alles aus Level 1, plus: das System erstellt automatisch Entwürfe.",
         [
             "Antwort-Entwürfe auf eingehende Mails automatisch anlegen",
             "Nach jedem Kundengespräch: Zusammenfassungsmail-Entwurf",
             "Morgen-Briefing-Entwurf direkt versandbereit",
             "Sie prüfen und klicken auf Senden — fertig",
         ],
         "Empfehlung für die meisten Nutzer"),
        ("3", "Autopilot", ORANGE, LIGHT_ORANGE,
         "Alles aus Level 2, plus: das System handelt eigenständig.",
         [
             "Folge-Termine automatisch im Kalender anlegen",
             "To-Dos in Notion oder anderen Apps erstellen",
             "Benachrichtigungskontakt direkt informieren",
             "Vollautomatisch im Hintergrund — Sie sehen das Ergebnis",
         ],
         "Maximale Zeitersparnis"),
    ]

    for num, title, col, bg, sub, features, badge in levels:
        lh = 30 + len(features) * 16 + 20
        c.setFillColor(bg)
        c.roundRect(18, y-lh, W-36, lh, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(18, y-lh, 5, lh, 3, fill=1, stroke=0)

        # Level-Badge
        c.setFillColor(col)
        c.circle(45, y-20, 14, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 11)
        c.setFillColor(WHITE)
        c.drawCentredString(45, y-25, num)

        # Titel
        c.setFont("Jakarta-Bold", 13)
        c.setFillColor(col)
        c.drawString(70, y-16, "Level " + num + " — " + title)

        # Empfehlungs-Badge
        bw = c.stringWidth(badge, "Jakarta-Bold", 8) + 14
        c.setFillColor(col)
        c.roundRect(W-30-bw, y-22, bw, 16, 3, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 8)
        c.setFillColor(WHITE)
        c.drawCentredString(W-30-bw/2, y-16, badge)

        # Untertitel
        c.setFont("Inter", 9)
        c.setFillColor(GRAY_D)
        c.drawString(70, y-30, sub)

        # Features
        for j, feat in enumerate(features):
            fy = y - 46 - j * 16
            c.setFillColor(col)
            c.circle(34, fy-3, 3, fill=1, stroke=0)
            c.setFont("Inter", 9)
            c.setFillColor(TEXT)
            c.drawString(44, fy-7, feat)

        y -= lh + 10

    # ── Erweiterbarkeit-Block ────────────────────────────────────────────────
    bx  = 18
    bw_ = W - 36
    bt  = y - 12        # Oberkante Box
    bb  = 38            # Unterkante Box (über Fußzeile)
    bh  = bt - bb

    # Hintergrund
    c.setFillColor(DARK)
    c.roundRect(bx, bb, bw_, bh, 6, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(bx, bb, 5, bh, 3, fill=1, stroke=0)

    # Badge zentriert
    ext_badge = "+ Beliebig erweiterbar"
    ebw = c.stringWidth(ext_badge, "Jakarta-Bold", 8) + 16
    badge_x = bx + (bw_ - ebw) / 2
    c.setFillColor(TEAL)
    c.roundRect(badge_x, bt - 18, ebw, 14, 3, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 8)
    c.setFillColor(WHITE)
    c.drawCentredString(bx + bw_ / 2, bt - 14, ext_badge)

    # Überschrift zentriert
    c.setFont("Jakarta-Bold", 14)
    c.setFillColor(WHITE)
    c.drawCentredString(bx + bw_ / 2, bt - 36, "Cleo lernt dazu — wie ein echter Mitarbeiter")

    # Untertitel zentriert
    c.setFont("Inter", 9.5)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawCentredString(bx + bw_ / 2, bt - 52,
        "Das System lässt sich beliebig erweitern und auf Ihre Abläufe trainieren — ohne IT-Kenntnisse.")

    # CTA-Strip (unten)
    cta_h = 32
    cta_y = bb + 6
    c.setFillColor(TEAL)
    c.roundRect(bx + 16, cta_y, bw_ - 32, cta_h, 4, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 10)
    c.setFillColor(WHITE)
    c.drawCentredString(bx + bw_ / 2, cta_y + 11,
        "Wir übernehmen das Training für Sie — schildern Sie uns Ihr Anliegen und Ihre Wünsche.")

    # 3 Feature-Tiles — minimalistisch, nur Teal
    tiles_ext = [
        ("Neue Skills ergänzen",
         "Jederzeit neue Fähigkeiten hinzufügbar — für jede Branche, jeden Prozess, jede Besonderheit."),
        ("Individuelle Workflows",
         "Ihr Unternehmen ist einzigartig — Cleo lernt Ihre Abläufe und Besonderheiten kennen."),
        ("Training durch Able & Baker",
         "Schildern Sie uns Ihr Anliegen. Wir konfigurieren und trainieren — Sie nutzen das Ergebnis."),
    ]

    tile_gap   = 8
    tile_w     = (bw_ - 32 - 2 * tile_gap) / 3
    tile_top   = bt - 66
    tile_bot   = cta_y + cta_h + 10
    tile_h_val = tile_top - tile_bot

    for i, (title, desc) in enumerate(tiles_ext):
        tx = bx + 16 + i * (tile_w + tile_gap)

        # Dunkler Tile-Hintergrund
        c.setFillColor(HexColor("#1c2b44"))
        c.roundRect(tx, tile_bot, tile_w, tile_h_val, 4, fill=1, stroke=0)
        # Teal-Akzentlinie links
        c.setFillColor(TEAL)
        c.roundRect(tx, tile_bot, 4, tile_h_val, 2, fill=1, stroke=0)

        tcx = tx + tile_w / 2   # horizontale Mitte der Tile

        # Nummerierter Teal-Kreis — zentriert
        c.setFillColor(TEAL)
        c.circle(tcx, tile_top - 16, 9, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 9)
        c.setFillColor(WHITE)
        c.drawCentredString(tcx, tile_top - 20, str(i + 1))

        # Titel — zentriert
        c.setFont("Jakarta-Bold", 9.5)
        c.setFillColor(WHITE)
        c.drawCentredString(tcx, tile_top - 46, title)

        # Beschreibung — zentriert
        c.setFont("Inter", 8.2)
        c.setFillColor(HexColor("#a0c0e0"))
        desc_lines = wrap(c, desc, "Inter", 8.2, tile_w - 24)
        for j, dl in enumerate(desc_lines[:4]):
            c.drawCentredString(tcx, tile_top - 62 - j * 12, dl)

    c.showPage()


# =============================================================================
# SEITE 5 — SO FUNKTIONIERTS + ROI
# =============================================================================
def how_it_works(c):
    ftr(c, 5)

    c.setFillColor(DARK)
    c.roundRect(18, H-70, W-36, 50, 6, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(32, H-44, "Einfacher Einstieg in 3 Schritten")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawString(32, H-60, "Von der Erstgespräch bis zum laufenden System in 2-3 Werktagen")

    y = H - 90

    steps = [
        ("1", TEAL,    "Erstgespräch & Bedarfsanalyse",
         "Wir lernen Ihr Unternehmen kennen: Branche, Kommunikationstools, typische Abläufe. "
         "Gemeinsam legen wir das richtige Autonomie-Level und die Module fest.",
         "ca. 1 Stunde", "Kostenlos"),
        ("2", BLUE,    "Installation & Konfiguration",
         "Ihr Digitalisierungspartner richtet alles ein: E-Mail-Anbindung, Ordnerstruktur, "
         "Mini-CRM aus Ihrem Postfach, KI-Rechtsassistent mit Ihren Rechtsthemen, alle Skills.",
         "2-4 Stunden", "Einmalig"),
        ("3", ORANGE,  "Übergabe & Sie legen los",
         "Kurze Einweisung (30 Min.), alle Zugangsdaten in einem Dokument, Ansprechpartner für "
         "Rückfragen. Ab sofort läuft das System — Sie sprechen, Claude erledigt.",
         "30 Minuten", "Dann selbstständig"),
    ]

    sw = (W - 54) / 3
    sx = 18
    for num, col, title, desc, dur, note in steps:
        c.setFillColor(GRAY_L)
        c.roundRect(sx, y-200, sw, 200, 6, fill=1, stroke=0)
        # Farbige Oberflaeche
        c.setFillColor(col)
        c.roundRect(sx, y-60, sw, 60, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.rect(sx, y-40, sw, 20, fill=1, stroke=0)
        # Nummer
        c.setFont("Jakarta-Bold", 28)
        c.setFont("Jakarta-Bold", 26)
        c.setFillColor(WHITE)
        c.drawString(sx+12, y-52, num)
        # Titel
        c.setFont("Jakarta-Bold", 10)
        c.setFillColor(TEXT)
        tls = wrap(c, title, "Jakarta-Bold", 10, sw-20)
        for i, tl in enumerate(tls):
            c.drawString(sx+12, y-76-i*14, tl)
        # Desc
        c.setFont("Inter", 8.5)
        c.setFillColor(GRAY_D)
        dls = wrap(c, desc, "Inter", 8.5, sw-20)
        start = y - 76 - len(tls)*14 - 10
        for i, dl in enumerate(dls[:5]):
            c.drawString(sx+12, start-i*12, dl)
        # Dauer
        c.setFillColor(col)
        c.roundRect(sx+10, y-192, sw-20, 18, 3, fill=1, stroke=0)
        c.setFont("Jakarta-Bold", 8)
        c.setFillColor(WHITE)
        c.drawString(sx+16, y-186, dur + "  |  " + note)

        sx += sw + 9

    y -= 220

    # ROI-Berechnung
    c.setFillColor(DARK)
    c.roundRect(18, y-56, W-36, 50, 5, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 12)
    c.setFillColor(WHITE)
    c.drawString(30, y-28, "Was das bedeutet — der typische ROI")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawString(30, y-43, "Rechnung für einen Selbstständigen oder kleinen Betrieb")
    y -= 68

    roi = [
        ("Gesparte Zeit (konservativ)", "90 Min/Tag x 22 Arbeitstage", "33h/Monat"),
        ("Wert der gesparten Zeit", "33h x 80 EUR/h (Stundensatz Eigenleistung)", "2.640 EUR/Monat"),
        ("Laufende Kosten Cleo", "Claude Pro + Pocket AI + OB24 (ca.)", "35-55 EUR/Monat"),
        ("ROI-Faktor", "2.640 EUR gespart / 55 EUR Kosten", "Faktor 48x"),
    ]

    for i, (label, calc, result) in enumerate(roi):
        rh = 28
        bg = GRAY_L if i % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(18, y-rh, W-36, rh, fill=1, stroke=0)
        c.setFont("Jakarta-Bold" if i == 3 else "Inter", 9)
        c.setFillColor(TEXT)
        c.drawString(28, y-18, label)
        c.setFont("Inter", 8.5)
        c.setFillColor(GRAY_D)
        c.drawString(220, y-18, calc)
        col_res = TEAL if i == 3 else TEXT
        c.setFont("Jakarta-Bold", 9)
        c.setFillColor(col_res)
        c.drawRightString(W-28, y-18, result)
        c.setStrokeColor(HexColor("#d8e0e8"))
        c.setLineWidth(0.3)
        c.line(18, y-rh, W-18, y-rh)
        y -= rh

    # Hinweis
    y -= 8
    c.setFont("Inter", 8)
    c.setFillColor(GRAY_M)
    c.drawString(22, y, "* Individueller ROI abhängig von Nutzungsintensität, Branche und Autonomie-Level. Kein verbindliches Versprechen.")
    c.showPage()


# =============================================================================
# SEITE 6 — BAFA-FOERDERUNG
# =============================================================================
def bafa(c):
    ftr(c, 6)

    # Header
    c.setFillColor(GOLD)
    c.roundRect(18, H-70, W-36, 50, 6, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(DARK)
    c.drawString(32, H-44, "BAFA-Förderung — 50% bis 80% der Kosten zurück")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#5a4000"))
    c.drawString(32, H-60, "Staatliche Förderung für KMU — Förderquote abhängig vom Unternehmensstandort")

    y = H - 90

    # Was ist BAFA?
    c.setFont("Jakarta-Bold", 11)
    c.setFillColor(DARK)
    c.drawString(22, y, "Was ist die BAFA-Unternehmensberatungsförderung?")
    y -= 16

    c.setFont("Inter", 9.5)
    c.setFillColor(GRAY_D)
    text = ("Das Bundesamt für Wirtschaft und Ausfuhrkontrolle (BAFA) fördert Beratungsleistungen "
            "für kleine und mittlere Unternehmen (KMU) sowie Freiberufler in Deutschland. "
            "Die Installation und Einrichtung von Cleo als digitales Verwaltungssystem "
            "kann als Digitalisierungsberatung anerkannt werden und somit förderungsfähig sein.")
    tlines = wrap(c, text, "Inter", 9.5, W-55)
    for i, tl in enumerate(tlines):
        c.drawString(22, y-i*14, tl)
    y -= len(tlines)*14 + 16

    # Förderkonditionen-Tabelle
    c.setFillColor(DARK)
    c.roundRect(18, y-28, W-36, 28, 4, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 10)
    c.setFillColor(WHITE)
    c.drawString(30, y-16, "Förderkonditionen im Überblick (Stand: 2024/2025 — vor Antragstellung prüfen)")
    y -= 32

    konditionen = [
        ("Zuschuss West", "Bis zu 50% der Beratungskosten (alle Bundesländer inkl. Berlin)"),
        ("Zuschuss Ost (80%)", "Brandenburg, Mecklenburg-Vorpommern, Sachsen, Sachsen-Anhalt, Thüringen"),
        ("Max. förderungsfähige Kosten", "Bis 3.500 EUR netto pro Vorhaben"),
        ("Max. Zuschuss West", "Bis zu 1.750 EUR (50% von 3.500 EUR)"),
        ("Max. Zuschuss Ost", "Bis zu 2.800 EUR (80% von 3.500 EUR)"),
        ("Wer fördert", "Bundesamt für Wirtschaft und Ausfuhrkontrolle (BAFA)"),
        ("Voraussetzung", "KMU (<250 MA, <50 Mio. EUR Umsatz) oder Freiberufler"),
        ("Antrag", "VOR Beginn der Beratung stellen — Antrag läuft über Ihren Berater"),
    ]

    for i, (key, val) in enumerate(konditionen):
        rh = 24
        c.setFillColor(GRAY_L if i % 2 == 0 else WHITE)
        c.rect(18, y-rh, W-36, rh, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#d8e0e8"))
        c.setLineWidth(0.3)
        c.line(18, y-rh, W-18, y-rh)
        c.setFont("Jakarta-Bold", 8.5)
        c.setFillColor(DARK)
        c.drawString(26, y-16, key)
        c.setFont("Inter", 8.5)
        c.setFillColor(GRAY_D)
        c.drawString(230, y-16, val[:72] + ("..." if len(val) > 72 else ""))
        y -= rh

    y -= 16

    # Rechenbeispiel
    box_h = 168
    c.setFillColor(GOLD_L)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.roundRect(18, y-box_h, W-36, box_h, 6, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.roundRect(18, y-box_h, 6, box_h, 3, fill=1, stroke=0)

    c.setFont("Jakarta-Bold", 11)
    c.setFillColor(HexColor("#7a4f00"))
    c.drawString(34, y-18, "Rechenbeispiel — Neue Bundesländer (80% Förderung)")

    c.setFont("Inter", 9)
    c.setFillColor(TEXT)
    c.drawString(34, y-36, "Gesamtinstallation Cleo (2 Vorhaben à 3.500 EUR*):")
    c.setFont("Jakarta-Bold", 9)
    c.drawRightString(W-34, y-36, "7.000 EUR netto")

    c.setFont("Inter", 9)
    c.setFillColor(TEXT)
    c.drawString(34, y-52, "BAFA-Zuschuss Phase 1 (80% von 3.500 EUR):")
    c.setFont("Jakarta-Bold", 9)
    c.setFillColor(GREEN)
    c.drawRightString(W-34, y-52, "- 2.800 EUR")

    c.setFont("Inter", 9)
    c.setFillColor(TEXT)
    c.drawString(34, y-66, "BAFA-Zuschuss Phase 2 (80% von 3.500 EUR):")
    c.setFont("Jakarta-Bold", 9)
    c.setFillColor(GREEN)
    c.drawRightString(W-34, y-66, "- 2.800 EUR")

    c.setStrokeColor(HexColor("#c8a820"))
    c.setLineWidth(0.8)
    c.line(34, y-76, W-34, y-76)

    c.setFont("Jakarta-Bold", 11)
    c.setFillColor(DARK)
    c.drawString(34, y-92, "Ihre effektiven Kosten:")
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(TEAL)
    c.drawRightString(W-34, y-92, "1.400 EUR netto")

    c.setFont("Inter", 8)
    c.setFillColor(GRAY_D)
    c.drawString(34, y-112, "* Aufspaltung in 2 separate förderungsfähige Vorhaben (z.B. Installation + Einweisung/Optimierung).")
    c.drawString(34, y-124, "  In Westdeutschland: 50% Förderung → max. 1.750 EUR pro Vorhaben (Eigenanteil: 3.500 EUR gesamt).")
    c.drawString(34, y-136, "  Die Aufspaltung ist vorab mit dem BAFA-Berater abzustimmen — Ihr Installationspartner")
    c.drawString(34, y-148, "  begleitet Sie durch den gesamten Antragsprozess.")

    y -= box_h + 16

    # Wichtige Hinweisbox
    c.setFillColor(HexColor("#fff3e8"))
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1)
    c.roundRect(18, y-60, W-36, 60, 5, fill=1, stroke=1)
    c.setFillColor(ORANGE)
    c.roundRect(18, y-60, 5, 60, 2, fill=1, stroke=0)

    c.setFont("Jakarta-Bold", 9.5)
    c.setFillColor(HexColor("#8a3a00"))
    c.drawString(32, y-16, "Wichtig: Antrag MUSS vor Beginn der Leistung gestellt werden")
    c.setFont("Inter", 9)
    c.drawString(32, y-30, "Die Förderung muss beantragt werden, bevor die Installation beginnt. Rückwirkende Anträge")
    c.drawString(32, y-42, "sind nicht möglich. Sprechen Sie uns an — wir begleiten Sie durch den Antragsprozess.")
    c.setFont("Jakarta-Bold", 9)
    c.setFillColor(BLUE)
    c.drawString(32, y-54, "www.bafa.de  |  Programm: Förderung unternehmerischen Know-hows")
    c.showPage()


# =============================================================================
# SEITE 7 — ZIELGRUPPEN + CTA
# =============================================================================
def cta(c):
    ftr(c, 7)

    c.setFillColor(DARK)
    c.roundRect(18, H-70, W-36, 50, 6, fill=1, stroke=0)
    c.setFont("Jakarta-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(32, H-44, "Für wen ist Cleo gemacht?")
    c.setFont("Inter", 9)
    c.setFillColor(HexColor("#a0c0e0"))
    c.drawString(32, H-60, "Am besten geeignet für diese Unternehmenstypen")

    y = H - 90

    targets = [
        ("Solopreneure & Freelancer", TEAL,
         "Berater, Coaches, Kreative, Trainer — wer alle Rollen allein trägt, profitiert "
         "am meisten. Keine Assistenz leistbar? Cleo ist Ihre.",
         ["Vollständige Admin-Entlastung", "Professioneller Außenauftritt", "CRM ohne manuellen Aufwand"]),
        ("Kleine Agenturen (2-15 MA)", BLUE,
         "Marketing, PR, IT, Recht, Steuer — wo viele Kundengespräche und E-Mails anfallen "
         "und die Admin-Last auf zu wenigen Schultern lastet.",
         ["Meeting-Nachbereitung für alle", "Automatische Kundenkommunikation", "Zentrales Kontaktmanagement"]),
        ("Immobilienmakler & -verwalter", PURPLE,
         "Viele Exposé-Anfragen, Besichtigungstermine, Nachfassen — ideales Einsatzgebiet "
         "für automatisierte E-Mail-Bearbeitung und Meeting-Dokumentation.",
         ["Exposé-Anfragen automatisch bearbeiten", "Terminnachbereitung strukturiert", "Mietverträge + Rechtsthemen"]),
        ("Beratungs- & Dienstleistungsbetriebe", HexColor("#2e8b57"),
         "Steuerberater, Versicherungsmakler, Finanzberater — überall wo viele "
         "Kundenkontakte dokumentiert und nachverfolgt werden müssen.",
         ["Vollständige Dokumentation", "Automatische Folgemails", "Fristen und To-Dos nie vergessen"]),
    ]

    tw = (W - 54) / 2
    th = 132
    cols = [18, 18 + tw + 10]
    ry = y

    for i, (nm, col, desc, feats) in enumerate(targets):
        co = i % 2
        if i > 0 and co == 0:
            ry -= th + 8
        tx = cols[co]

        c.setFillColor(GRAY_L)
        c.roundRect(tx, ry-th, tw, th, 5, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(tx, ry-th, 5, th, 3, fill=1, stroke=0)

        c.setFont("Jakarta-Bold", 10)
        c.setFillColor(col)
        c.drawString(tx+14, ry-18, nm)

        c.setFont("Inter", 8.5)
        c.setFillColor(GRAY_D)
        dls = wrap(c, desc, "Inter", 8.5, tw-24)
        for j, dl in enumerate(dls[:3]):
            c.drawString(tx+14, ry-32-j*12, dl)

        feat_y = ry - 32 - len(dls[:3])*12 - 8
        for feat in feats:
            c.setFillColor(col)
            c.circle(tx+20, feat_y-3, 2.5, fill=1, stroke=0)
            c.setFont("Inter", 8)
            c.setFillColor(TEXT)
            c.drawString(tx+28, feat_y-7, feat)
            feat_y -= 14

    ry -= th + 20

    # CTA Box
    c.setFillColor(DARK)
    c.roundRect(18, ry-110, W-36, 110, 6, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(18, ry-110, 5, 110, 3, fill=1, stroke=0)

    c.setFont("Jakarta-Bold", 14)
    c.setFillColor(WHITE)
    c.drawString(32, ry-24, "Bereit? So starten Sie.")

    c.setFont("Inter", 10)
    c.setFillColor(HexColor("#b0c8e0"))
    c.drawString(32, ry-42, "Kontaktieren Sie uns für ein kostenloses Erstgespräch.")
    c.drawString(32, ry-56, "Wir analysieren Ihren Bedarf, begleiten die BAFA-Antragstellung")
    c.drawString(32, ry-70, "und haben Ihr System in 2-3 Werktagen einsatzbereit.")

    c.setStrokeColor(TEAL)
    c.setLineWidth(0.5)
    c.line(32, ry-82, W-32, ry-82)

    c.setFont("Jakarta-Bold", 9)
    c.setFillColor(TEAL)
    c.drawString(32, ry-96, "Able & Baker GmbH  |  Yuri A. Bilogor")
    c.setFont("Inter", 9)
    c.setFillColor(GRAY_M)
    c.drawRightString(W-32, ry-96, "able-baker.de")

    c.showPage()


# =============================================================================
# MAIN
# =============================================================================
def build(out):
    cv = canvas.Canvas(out, pagesize=A4)
    cv.setTitle("Cleo — Produktinformation")
    cv.setAuthor("Cleo")
    cv.setSubject("KI-Sekretariat für den Büroalltag")
    S = styles()
    cover(cv)
    problem(cv)
    solution(cv)
    autonomy(cv)
    how_it_works(cv)
    bafa(cv)
    cta(cv)
    cv.save()
    print("PDF erstellt: " + out)

build("/sessions/peaceful-pensive-lamport/mnt/Cowork OS/Cleo-Verkauf.pdf")
