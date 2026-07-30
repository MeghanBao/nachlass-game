#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt PLATZHALTER-Grafiken / generates PLACEHOLDER graphics.

Zwei Bilder, beide deutlich als *PLATZHALTER* markiert und jederzeit durch echte
Kunst ersetzbar (siehe ASSETS.md):

* ``game/images/raum.png``  — der anklickbare Raum. Jedes der 9 Stücke bekommt
  ein beschriftetes Kästchen an seiner ``pos`` (direkt aus ``game/script.rpy``
  gelesen), damit sich der Raum sofort testen und die Hotspots prüfen lassen.
* ``game/images/titel.png`` — die Titelkarte, die das Spiel beim Start zeigt,
  solange die Datei vorhanden ist (``renpy.loadable``-abgesichert).

Two images, both clearly watermarked *PLATZHALTER* and replaceable by real art.

Aufruf / run:
    python tools/make_placeholders.py            # beide / both
    python tools/make_placeholders.py room       # nur Raum
    python tools/make_placeholders.py title      # nur Titel

Benötigt Pillow / requires Pillow (``pip install Pillow``).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from selftest import load_data  # noqa: E402  (reuse the game's data source)

W, H = 1280, 720
IMG_DIR = os.path.join(ROOT, "game", "images")

# Gedämpfte Palette aus ASSETS.md: warme Brauntöne, vergilbtes Weiß, kühles
# Restlicht am Fenster.
BG_TOP = (58, 50, 42)       # dunkle Schrankwand oben
BG_BOTTOM = (78, 68, 55)    # abgewohnter Teppich unten
LIGHT = (150, 134, 96)      # schräger Lichtstrahl am Fenster
BOX = (222, 210, 180)       # vergilbtes Weiß der Objektkästchen
BOX_EDGE = (120, 96, 62)
INK = (40, 32, 24)
PALE = (230, 222, 200)
WATERMARK = (150, 120, 90)


def _font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _room_bg():
    """Gemeinsamer Hintergrund: Wandverlauf + Lichtstrahl."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        row = (
            int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t),
            int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t),
            int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t),
        )
        for x in range(W):
            px[x, y] = row
    draw = ImageDraw.Draw(img, "RGBA")
    draw.polygon([(760, 0), (1010, 0), (560, H), (330, H)], fill=LIGHT + (26,))
    return img, draw


def _stamp(draw, y=62):
    draw.text((24, y), "PLATZHALTER — ersetzen (siehe ASSETS.md)",
              font=_font(22, bold=True), fill=WATERMARK)


def generate_room():
    _, _, objects = load_data()
    img, draw = _room_bg()
    draw.line([(0, 430), (W, 470)], fill=(30, 24, 18), width=3)  # Wand/Teppich

    label_font = _font(19, bold=True)
    id_font = _font(14)
    for o in objects:
        x, y = o["pos"]
        bw, bh = 150, 54
        draw.rectangle([x, y, x + bw, y + bh], fill=BOX, outline=BOX_EDGE, width=2)
        # Zielkreuz genau auf der pos-Koordinate (dem Anker).
        draw.line([(x - 6, y), (x + 6, y)], fill=(180, 60, 40), width=2)
        draw.line([(x, y - 6), (x, y + 6)], fill=(180, 60, 40), width=2)
        words = o["name"]["de"].split()
        draw.text((x + 8, y + 6), words[0], font=label_font, fill=INK)
        if len(words) > 1:
            draw.text((x + 8, y + 24), " ".join(words[1:]),
                      font=label_font, fill=INK)
        draw.text((x + 8, y + 40), "%s  (%d,%d)" % (o["id"], x, y),
                  font=id_font, fill=BOX_EDGE)

    draw.text((24, 18), "NACHLASS", font=_font(34, bold=True), fill=PALE)
    _stamp(draw)
    return _save(img, "raum.png"), len(objects)


def _centered(draw, cy, text, font, fill):
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    draw.text(((W - (r - l)) / 2, cy - (b - t) / 2), text, font=font, fill=fill)


def generate_title():
    img, draw = _room_bg()
    draw.rectangle([0, 0, W, H], fill=(20, 16, 12, 60))   # dezente Vignette
    _centered(draw, 300, "NACHLASS", _font(96, bold=True), PALE)
    _centered(draw, 380, "Die letzte Stunde", _font(34), (206, 196, 172))
    _centered(draw, 420, "The Last Hour", _font(26), (150, 140, 120))
    _centered(draw, 560, "Klicken, um zu beginnen · Click to begin",
              _font(20), (150, 140, 120))
    _stamp(draw, y=24)
    return _save(img, "titel.png"), 1


def _save(img, name):
    os.makedirs(IMG_DIR, exist_ok=True)
    path = os.path.join(IMG_DIR, name)
    img.save(path)
    return path


def main(argv):
    what = argv[1] if len(argv) > 1 else "all"
    if what not in ("all", "room", "title"):
        print("usage: make_placeholders.py [all|room|title]")
        return 2
    if what in ("all", "room"):
        path, n = generate_room()
        print("wrote %s  (%dx%d, %d hotspots)" % (path, W, H, n))
    if what in ("all", "title"):
        path, _ = generate_title()
        print("wrote %s  (%dx%d)" % (path, W, H))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
