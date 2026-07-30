#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt ein PLATZHALTER-Raumbild / generates a PLACEHOLDER room image.

Liest die Objekt-Koordinaten direkt aus ``game/script.rpy`` (dieselbe Quelle
wie das Spiel) und zeichnet für jedes der 9 Stücke ein beschriftetes Kästchen
an seine ``pos``. So aktiviert sich der anklickbare Raum sofort, und man kann
die Hotspots gegen die finale Grafik prüfen. **Kein Ersatz für echte Kunst** —
siehe ASSETS.md; das Bild ist deutlich als Platzhalter markiert.

Reads object coordinates straight from ``game/script.rpy`` and draws a labelled
box at each object's ``pos``. This activates the clickable room and lets you
verify hotspot placement. Not a substitute for real art (see ASSETS.md); the
image is clearly watermarked as a placeholder.

Aufruf / run:  python tools/make_placeholder_room.py
Schreibt / writes:  game/images/raum.png  (1280x720)
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from selftest import load_data  # noqa: E402  (reuse the game's data source)

W, H = 1280, 720
OUT = os.path.join(ROOT, "game", "images", "raum.png")

# Gedämpfte Palette aus ASSETS.md: warme Brauntöne, vergilbtes Weiß.
BG_TOP = (58, 50, 42)       # dunkle Schrankwand oben
BG_BOTTOM = (78, 68, 55)    # abgewohnter Teppich unten
LIGHT = (150, 134, 96)      # schräger Lichtstrahl am Fenster
BOX = (222, 210, 180)       # vergilbtes Weiß der Objektkästchen
BOX_EDGE = (120, 96, 62)
INK = (40, 32, 24)
WATERMARK = (150, 120, 90)


def _font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def main():
    _, _, objects = load_data()

    img = Image.new("RGB", (W, H))
    px = img.load()
    # Vertikaler Verlauf: Wand oben -> Teppich unten.
    for y in range(H):
        t = y / (H - 1)
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    draw = ImageDraw.Draw(img, "RGBA")

    # Schräger Lichtstrahl vom Fenster (rechts oben) — Staub im Licht.
    draw.polygon([(760, 0), (1010, 0), (560, H), (330, H)],
                 fill=LIGHT + (26,))

    # Bodenlinie (Wand/Teppich-Kante).
    draw.line([(0, 430), (W, 470)], fill=(30, 24, 18), width=3)

    label_font = _font(19, bold=True)
    id_font = _font(14)

    for o in objects:
        x, y = o["pos"]
        name = o["name"]["de"]
        bw, bh = 150, 54
        # Kästchen an der Ankerposition (oben-links), wie im Spiel-Screen.
        draw.rectangle([x, y, x + bw, y + bh], fill=BOX, outline=BOX_EDGE, width=2)
        # kleiner Zielpunkt genau auf der pos-Koordinate (der Anker).
        draw.line([(x - 6, y), (x + 6, y)], fill=(180, 60, 40), width=2)
        draw.line([(x, y - 6), (x, y + 6)], fill=(180, 60, 40), width=2)
        # Name (umgebrochen, wenn nötig) + technische id/pos.
        words = name.split()
        line1 = words[0]
        line2 = " ".join(words[1:]) if len(words) > 1 else ""
        draw.text((x + 8, y + 6), line1, font=label_font, fill=INK)
        if line2:
            draw.text((x + 8, y + 24), line2, font=label_font, fill=INK)
        draw.text((x + 8, y + 40), "%s  (%d,%d)" % (o["id"], x, y),
                  font=id_font, fill=BOX_EDGE)

    # Titel + deutlicher Platzhalter-Hinweis.
    draw.text((24, 18), "NACHLASS", font=_font(34, bold=True), fill=(230, 222, 200))
    stamp = _font(22, bold=True)
    msg = "PLATZHALTER — ersetzen durch raum.png (siehe ASSETS.md)"
    draw.text((24, 62), msg, font=stamp, fill=WATERMARK)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print("wrote %s  (%dx%d, %d hotspots)" % (OUT, W, H, len(objects)))


if __name__ == "__main__":
    main()
