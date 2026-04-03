#!/usr/bin/env python3
"""
build_brief.py — Briefgenerator für Second Brain OS
Layout-Version: v8 (optimiertes Layout mit symmetrischen Rändern)

Konfiguration: Wird während der Installation mit Firmendaten befüllt.
Verwendung:
    python3 build_brief.py
    → Interaktive Eingabe von Empfänger, Betreff und Brieftext
    → Speichert PDF in Postausgang/

Oder per Import:
    from build_brief import generate_brief
    pdf_path = generate_brief(
        empfaenger={"name": "Max Mustermann", "strasse": "Musterstr. 1",
                    "plz": "12345", "ort": "Musterstadt"},
        betreff="Betreff des Briefes",
        text="Brieftext...",
        aktenzeichen=None  # oder z.B. "2026-001-VERTR" für Anwaltsbriefe
    )
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# ── Firma konfigurieren (wird bei Installation automatisch befüllt) ──────────
FIRMA_NAME    = "{{FIRMENNAME}}"
FIRMA_ZUSATZ  = "{{RECHTSFORM}}"          # z.B. "GmbH" oder leer lassen
FIRMA_STRASSE = "{{STRASSE}}"
FIRMA_PLZ     = "{{PLZ}}"
FIRMA_ORT     = "{{ORT}}"
FIRMA_TEL     = "{{TELEFON}}"
FIRMA_MAIL    = "{{EMAIL_ADDRESS}}"
FIRMA_WEB     = "{{WEBSITE}}"
FIRMA_USTID   = "{{USTID}}"

# ── Pfade ────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
LOGO_PATH     = BASE_DIR / "logo.png"
POSTAUSGANG   = BASE_DIR.parent / "Postausgang"
POSTAUSGANG.mkdir(exist_ok=True)

# ── Layout-Konstanten (v8) ────────────────────────────────────────────────────
# Symmetrische Ränder: Links = Rechts = Unten = 57pt
# Oben = 80pt (Platz für Briefkopf)
# Zeilenabstand: 15pt bei 10pt Schrift

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm, pt
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus.paragraph import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.utils import simpleSplit
    from reportlab.lib import colors
except ImportError:
    print("reportlab fehlt. Installieren mit: pip install reportlab --break-system-packages")
    sys.exit(1)

W, H = A4

# Ränder (v8 — symmetrisch)
LEFT   = 57 * pt
RIGHT  = 57 * pt
BOTTOM = 57 * pt
TOP    = 80 * pt
MAX_W  = W - LEFT - RIGHT
LH     = 15  # Zeilenabstand in pt

# Schriften
FONT_BOLD   = "Helvetica-Bold"
FONT_NORMAL = "Helvetica"
FONT_SIZE   = 10
FONT_SMALL  = 9


def _draw_briefkopf(c: canvas.Canvas, aktenzeichen: str = None):
    """Zeichnet Briefkopf mit Firmenname, Adresse und optionalem Logo."""
    # Logo (oben rechts, falls vorhanden)
    if LOGO_PATH.exists():
        try:
            logo_w = 45 * mm
            logo_h = 15 * mm
            c.drawImage(str(LOGO_PATH),
                        W - RIGHT - logo_w,
                        H - TOP + 10,
                        width=logo_w, height=logo_h,
                        preserveAspectRatio=True, anchor="ne",
                        mask="auto")
        except Exception:
            pass  # Logo fehlt oder fehlerhaft — weiter ohne

    # Firmenname (fett, 11pt)
    c.setFont(FONT_BOLD, 11)
    c.drawString(LEFT, H - 30, FIRMA_NAME + (" " + FIRMA_ZUSATZ if FIRMA_ZUSATZ else ""))

    # Adresszeile (9pt, grau)
    c.setFont(FONT_NORMAL, FONT_SMALL)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    adress_line = f"{FIRMA_STRASSE} · {FIRMA_PLZ} {FIRMA_ORT}"
    if FIRMA_TEL:
        adress_line += f" · Tel: {FIRMA_TEL}"
    if FIRMA_MAIL:
        adress_line += f" · {FIRMA_MAIL}"
    c.drawString(LEFT, H - 44, adress_line)
    c.setFillColorRGB(0, 0, 0)

    # Trennlinie
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.line(LEFT, H - 52, W - RIGHT, H - 52)
    c.setStrokeColorRGB(0, 0, 0)

    # Aktenzeichen (nur bei Anwaltsbriefen)
    if aktenzeichen:
        c.setFont(FONT_NORMAL, FONT_SMALL)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(LEFT, H - 63, f"Aktenzeichen: {aktenzeichen}")
        c.setFillColorRGB(0, 0, 0)


def _draw_empfaenger(c: canvas.Canvas, empf: dict) -> float:
    """Zeichnet Empfängeradresse (DIN 5008) und gibt y-Position danach zurück."""
    # DIN 5008: Anschriftsfeld beginnt bei 45mm vom oberen Rand
    y = H - 45 * mm

    # Rücksendeangabe (kleine Zeile über Empfänger)
    c.setFont(FONT_NORMAL, 7)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    rueck = f"{FIRMA_NAME}, {FIRMA_STRASSE}, {FIRMA_PLZ} {FIRMA_ORT}"
    c.drawString(LEFT, y + 8, rueck[:60])
    c.setFillColorRGB(0, 0, 0)

    # Empfänger
    c.setFont(FONT_NORMAL, FONT_SIZE)
    lines = []
    if empf.get("firma"):
        lines.append(empf["firma"])
    lines.append(empf.get("name", ""))
    lines.append(empf.get("strasse", ""))
    lines.append(f"{empf.get('plz', '')} {empf.get('ort', '')}")
    if empf.get("land") and empf["land"].upper() != "DE":
        lines.append(empf["land"])

    for line in lines:
        if line.strip():
            c.drawString(LEFT, y, line)
            y -= LH

    return y - LH  # Abstand nach Anschrift


def generate_brief(
    empfaenger: dict,
    betreff: str,
    text: str,
    aktenzeichen: str = None,
    grussformel: str = "Mit freundlichen Grüßen",
    unterzeichner: str = None,
    anwalt_modus: bool = False,
    output_path: str = None,
) -> str:
    """
    Generiert ein Brief-PDF.

    Args:
        empfaenger: dict mit keys: name, firma (opt.), strasse, plz, ort, land (opt.)
        betreff: Betreff-Zeile (wird bei Bedarf umgebrochen)
        text: Brieftext (Zeilenumbrüche mit \\n)
        aktenzeichen: Aktenzeichen für Anwaltsbriefe (optional)
        grussformel: Standard "Mit freundlichen Grüßen"
        unterzeichner: Name des Unterzeichners (optional, aus Firmendaten wenn leer)
        anwalt_modus: True für Anwaltsbriefe (Aktenzeichen + Rechtsabt.-Abschluss)
        output_path: Ausgabepfad (auto-generiert wenn None)

    Returns:
        Pfad zur erzeugten PDF-Datei
    """
    if output_path is None:
        datum_str = datetime.now().strftime("%Y-%m-%d")
        empf_kuerzel = empfaenger.get("name", "Brief").replace(" ", "_")[:20]
        output_path = str(POSTAUSGANG / f"{datum_str}-{empf_kuerzel}.pdf")

    c = canvas.Canvas(output_path, pagesize=A4)
    page_num = 1

    def new_page():
        nonlocal page_num
        c.showPage()
        page_num += 1
        _draw_briefkopf(c, aktenzeichen)
        return H - TOP

    # ── Seite 1 ──────────────────────────────────────────────────────────────
    _draw_briefkopf(c, aktenzeichen)

    # Empfängeradresse
    _draw_empfaenger(c, empfaenger)

    # Datum (rechtsbündig)
    datum = datetime.now().strftime("%d.%m.%Y")
    c.setFont(FONT_NORMAL, FONT_SIZE)
    c.drawRightString(W - RIGHT, H - TOP - 10, datum)

    # Betreff (fett, umgebrochen)
    betreff_y = H - TOP - 35
    c.setFont(FONT_BOLD, FONT_SIZE)
    betreff_lines = simpleSplit(betreff, FONT_BOLD, FONT_SIZE, MAX_W)
    for bl in betreff_lines:
        c.drawString(LEFT, betreff_y, bl)
        betreff_y -= LH

    # Brieftext
    text_y = betreff_y - LH
    c.setFont(FONT_NORMAL, FONT_SIZE)

    for paragraph in text.split("\n"):
        if not paragraph.strip():
            text_y -= LH  # Leerzeile
            continue

        text_lines = simpleSplit(paragraph, FONT_NORMAL, FONT_SIZE, MAX_W)
        for tl in text_lines:
            # Seitenumbruch-Prüfung pro Zeile
            if text_y < BOTTOM + LH:
                text_y = new_page()
                c.setFont(FONT_NORMAL, FONT_SIZE)
                text_y -= LH

            c.drawString(LEFT, text_y, tl)
            text_y -= LH

        text_y -= 4  # Absatz-Abstand

    # Grußformel
    sig_y = text_y - LH
    if sig_y < BOTTOM + 60:
        sig_y = new_page()
        c.setFont(FONT_NORMAL, FONT_SIZE)
        sig_y -= LH

    c.setFont(FONT_NORMAL, FONT_SIZE)
    c.drawString(LEFT, sig_y, grussformel)
    sig_y -= LH  # 1× Zeilenabstand (v8: reduzierter Abstand)

    # Unterschrifts-Bild (Signum)
    signum_path = BASE_DIR / "signum.png"
    if not signum_path.exists():
        # Fallback: nach signum_*.png suchen
        signum_files = list(BASE_DIR.glob("signum_*.png"))
        if signum_files:
            signum_path = signum_files[0]

    SIG_BOTTOM = BOTTOM + 43
    if signum_path.exists():
        try:
            c.drawImage(str(signum_path),
                        LEFT, SIG_BOTTOM,
                        width=50 * mm, height=20 * mm,
                        preserveAspectRatio=True, anchor="sw",
                        mask="auto")
        except Exception:
            pass

    # Unterzeichner-Name
    name_y = SIG_BOTTOM - 2
    c.setFont(FONT_NORMAL, FONT_SIZE)
    if unterzeichner:
        c.drawString(LEFT, name_y, unterzeichner)
    elif anwalt_modus:
        # Anwaltsmodus: Rechtsabteilung + Firma
        c.drawString(LEFT, name_y, "Rechtsabteilung, i.A. der Geschäftsführung")
        c.drawString(LEFT, name_y - LH, FIRMA_NAME)
    else:
        c.drawString(LEFT, name_y, FIRMA_NAME)

    # Fußzeile (USt-ID, IBAN falls vorhanden)
    c.setFont(FONT_NORMAL, 7.5)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    footer_parts = []
    if FIRMA_USTID:
        footer_parts.append(f"USt-ID: {FIRMA_USTID}")
    if FIRMA_WEB:
        footer_parts.append(FIRMA_WEB)
    if footer_parts:
        c.drawCentredString(W / 2, BOTTOM - 14, " · ".join(footer_parts))
    c.setFillColorRGB(0, 0, 0)

    c.save()
    return output_path


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Briefgenerator — Second Brain OS ===\n")

    anwalt = input("Anwaltsbrief? (j/n): ").strip().lower() == "j"
    az = None
    if anwalt:
        az = input("Aktenzeichen (z.B. 2026-001-VERTR): ").strip()

    print("\n--- Empfänger ---")
    empf = {
        "name":    input("Name: ").strip(),
        "firma":   input("Firma (optional): ").strip(),
        "strasse": input("Straße + Nr.: ").strip(),
        "plz":     input("PLZ: ").strip(),
        "ort":     input("Ort: ").strip(),
    }

    betreff = input("\nBetreff: ").strip()
    print("Brieftext (leere Zeile = Absatz, zwei leere Zeilen = Ende):")
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
            lines.append("")
        else:
            empty_count = 0
            lines.append(line)

    text = "\n".join(lines)
    unterz = input("\nUnterzeichner-Name (leer = Firmenname): ").strip() or None

    pdf = generate_brief(
        empfaenger=empf,
        betreff=betreff,
        text=text,
        aktenzeichen=az,
        unterzeichner=unterz,
        anwalt_modus=anwalt,
    )

    print(f"\n✅ PDF erstellt: {pdf}")
