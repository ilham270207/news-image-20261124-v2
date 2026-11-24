#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE — Tuesday 24 November 2026.

Draws a one-page newspaper front page summing up the world's news of
24 November 2026 as a single 1024x1024 PNG.

Everything is drawn in code with Pillow: masthead, headlines, decks, body
copy and all illustrations (factory fire, ship at sea, globe, protest crowd,
cracked earth, telephone) are vector shapes — no photographs, no network,
no random numbers, no timestamps. Running the program twice writes
byte-identical PNGs.

Usage:
    python3 main.py
    # writes /output/entry.png (or $OUTPUT_PATH; falls back to ./output/entry.png)

License: MIT. Fonts: DejaVu (see fonts/).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 242, 231)      # newsprint cream
INK = (18, 18, 18)           # near-black
RED = (178, 34, 34)          # headline red
DARKRED = (139, 0, 0)
BLUE = (31, 78, 121)
SKY = (135, 190, 220)
SEA = (38, 98, 140)
SAND = (232, 205, 150)
GREY = (110, 110, 110)
LIGHTGREY = (220, 220, 220)
GREEN = (46, 125, 50)
ORANGE = (230, 110, 20)
YELLOW = (245, 190, 40)
RULE = (60, 60, 60)

_HERE = os.path.dirname(os.path.abspath(__file__))


def _font_path(name):
    for base in (os.path.join(_HERE, "fonts"),
                 "/usr/share/fonts/truetype/dejavu"):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    return None


def font(name, size):
    path = _font_path(name)
    if path is None:
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=4):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def headline(draw, x, y, text, size, max_w, fill=INK, leading=2):
    """Serif-bold headline, wrapped; returns y below it."""
    return text_block(draw, x, y, text, SERIF_B(size), max_w, fill, leading)


def kicker(draw, x, y, text, color=RED, size=15):
    draw.text((x, y), text, font=SANS_B(size), fill=color)
    return y + size + 4


def rule(draw, x0, y, x1, w=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=w)


def draw_flame(draw, cx, base_y, s=1.0, smoke=True):
    """Stylised flame: layered polygons, outer orange to pale core."""
    def poly(pts, fill):
        draw.polygon([(cx + dx * s, base_y + dy * s) for dx, dy in pts], fill=fill)
    poly([(-34, 0), (-26, -38), (-12, -58), (-6, -34), (2, -72),
          (12, -44), (24, -62), (30, -28), (34, 0)], ORANGE)
    poly([(-22, 0), (-16, -30), (-6, -44), (0, -26), (8, -52),
          (16, -30), (22, 0)], (240, 150, 30))
    poly([(-12, 0), (-8, -20), (0, -32), (8, -18), (12, 0)], (250, 220, 120))
    # smoke puffs above the flame
    if smoke:
        for dx, dy, r in ((-26, -84, 13), (-6, -100, 16), (16, -82, 12), (2, -118, 10)):
            draw.ellipse([cx + dx * s - r, base_y + dy * s - r,
                          cx + dx * s + r, base_y + dy * s + r], fill=(150, 150, 150))


def draw_factory(draw, x, y, w, h):
    """Factory silhouette with chimney, windows and flame."""
    draw.rectangle([x, y + h * 0.45, x + w, y + h], fill=(70, 70, 78))
    draw.rectangle([x + w * 0.68, y, x + w * 0.82, y + h * 0.55], fill=(90, 90, 98))
    draw.rectangle([x + w * 0.66, y - 8, x + w * 0.84, y], fill=(70, 70, 78))
    for i in range(5):
        wx = x + 12 + i * (w - 24) // 5
        draw.rectangle([wx, y + h * 0.58, wx + 16, y + h * 0.78],
                       fill=(255, 210, 90))
    draw.rectangle([x + w * 0.42, y + h * 0.80, x + w * 0.58, y + h],
                   fill=(40, 40, 46))
    draw_flame(draw, x + w * 0.5, y + h * 0.48, 0.85, smoke=False)


def draw_ship(draw, x, y, w, h):
    """Cargo ship on waves with a small fire amidships."""
    sea_y = y + h * 0.62
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(4):
        wy = sea_y + 8 + i * 9
        draw.arc([x + 6, wy - 6, x + w - 6, wy + 10], 0, 180, fill=(200, 225, 240), width=2)
    draw.polygon([(x + 8, sea_y), (x + w - 8, sea_y),
                  (x + w - 26, sea_y - 26), (x + 26, sea_y - 26)], fill=(60, 60, 68))
    for i in range(3):
        cx = x + 34 + i * 34
        draw.rectangle([cx, sea_y - 44, cx + 28, sea_y - 26], fill=(200, 60, 50) if i != 1 else (230, 180, 40))
    draw.rectangle([x + w - 44, sea_y - 58, x + w - 18, sea_y - 26], fill=(240, 240, 240))
    draw_flame(draw, x + w * 0.5, sea_y - 26, 0.30, smoke=False)


def draw_globe(draw, cx, cy, r):
    """Globe: blue disc, meridian lines, green land blobs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200),
                 outline=INK, width=2)
    for k in (-0.55, 0, 0.55):
        draw.arc([cx - r + k * r * 0.9, cy - r, cx + r + k * r * 0.9, cy + r],
                 270, 90, fill=(210, 230, 245), width=2)
        draw.arc([cx - r + k * r * 0.9, cy - r, cx + r + k * r * 0.9, cy + r],
                 90, 270, fill=(210, 230, 245), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(210, 230, 245), width=2)
    for bx, by, br in ((-0.35, -0.3, 0.28), (0.35, 0.25, 0.32), (0.1, -0.55, 0.2)):
        draw.ellipse([cx + bx * r - br * r, cy + by * r - br * r * 0.7,
                      cx + bx * r + br * r, cy + by * r + br * r * 0.7],
                     fill=(90, 170, 90))


def draw_crowd(draw, x, y, w, h):
    """Protest crowd: two rows of heads, raised placards."""
    draw.rectangle([x, y, x + w, y + h], fill=(235, 225, 205))
    colors = [(178, 34, 34), (31, 78, 121), (46, 125, 50), (120, 60, 140), (200, 120, 20)]
    for row, ry in enumerate((h - 14, h - 34)):
        n = 9 if row == 0 else 8
        for i in range(n):
            hx = x + 14 + i * (w - 28) // max(n - 1, 1)
            hy = y + ry
            r = 8
            draw.ellipse([hx - r, hy - r, hx + r, hy + r],
                         fill=colors[(i + row) % len(colors)])
    for px, py, pw, ph, col in ((x + 18, y + 4, 34, 18, RED),
                                (x + w - 58, y + 8, 34, 18, BLUE)):
        draw.line([(px + pw // 2, py + ph), (px + pw // 2, y + h - 20)],
                  fill=INK, width=3)
        draw.rectangle([px, py, px + pw, py + ph], fill=col)


def draw_cracked_earth(draw, x, y, w, h):
    """Dry cracked ground."""
    draw.rectangle([x, y, x + w, y + h], fill=(190, 150, 100))
    cracks = [[(8, 5), (30, 22), (22, 38), (48, 52)],
              [(w - 10, 8), (w - 34, 25), (w - 20, 42), (w - 52, 52)],
              [(w // 2, 3), (w // 2 + 12, 20), (w // 2 - 8, 36), (w // 2 + 6, 52)]]
    for c in cracks:
        draw.line([(x + px, y + py) for px, py in c], fill=(90, 55, 30), width=3)
    for bx, by, br in ((18, h - 16, 7), (w - 24, h - 20, 6), (w // 2, 16, 5)):
        draw.ellipse([x + bx - br, y + by - br, x + bx + br, y + by + br],
                     fill=(120, 80, 45))


def draw_phone(draw, x, y, w, h):
    """Handset with a red no-signal cross."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(40, 40, 48))
    draw.rounded_rectangle([x + 8, y + 12, x + w - 8, y + h - 14], radius=6,
                           fill=(220, 235, 245))
    draw.line([(x + 14, y + 20), (x + w - 14, y + h - 22)], fill=RED, width=5)
    draw.line([(x + w - 14, y + 20), (x + 14, y + h - 22)], fill=RED, width=5)
    draw.rectangle([x + w // 2 - 12, y + h - 10, x + w // 2 + 12, y + h - 5],
                   fill=(150, 150, 150))


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=1)

    # ---------- masthead ----------
    d.rectangle([14, 14, W - 15, 108], fill=INK)
    d.text((W // 2, 24), "THE WORLD IN ONE PAGE",
           font=SERIF_B(52), fill=(247, 242, 231), anchor="ma")
    d.text((W // 2, 84), "TUESDAY, 24 NOVEMBER 2026  •  ONE PAGE  •  THE WHOLE WORLD",
           font=SANS_B(16), fill=(220, 200, 140), anchor="ma")
    d.text((24, 118), "TUESDAY 24 NOVEMBER 2026", font=SANS_B(15), fill=INK)
    d.text((W - 24, 118), "PRICE: ONE READ", font=SANS_B(15), fill=INK, anchor="ra")
    rule(d, 24, 140, W - 24, 2)

    # ---------- lead story: Indonesia factory fire ----------
    lx, lw = 24, 596
    y = kicker(d, lx, 152, "INDONESIA  •  LEAD STORY")
    y = headline(d, lx, y, "FIRE KILLS 24 AT JAVA CANDY FACTORY", 34, lw)
    y = text_block(d, lx, y + 2,
                   "Blaze rips through plant in Banten; rescuers hunt for "
                   "around 30 missing workers.",
                   SANS_B(17), lw, fill=(60, 60, 60), leading=3)
    y = text_block(d, lx, y + 4,
                   "At least 24 people have died after a huge fire tore through "
                   "a candy factory in Banten province, Indonesia. Rescue teams "
                   "are still searching for around 30 workers listed as missing.",
                   SANS(16), lw, leading=4)
    draw_factory(d, lx + 20, 360, 300, 95)
    d.text((lx + 340, 368), "BANTEN, JAVA", font=SANS_B(15), fill=INK)
    text_block(d, lx + 340, 390,
               "The fire broke out at the plant and spread fast through "
               "stock and packaging. Fire crews fought the blaze for hours.",
               SANS(14), 240, leading=3)
    rule(d, lx, 470, lx + lw, 2)

    # ---------- also today: briefs fill the lead column ----------
    y = kicker(d, lx, 482, "ALSO TODAY")
    briefs = [
        ("INDIA–NEPAL", "Saryu-Kamala Express links Ayodhya and Janakpur as Modi "
         "and Nepal's PM flag off the first train."),
        ("TALIBAN", "Women's names erased from official documents in Balkh "
         "province, replaced with the word 'Bibi'."),
        ("MYANMAR", "Military-backed government criticises ASEAN's decision, "
         "calling it unfair and unbalanced."),
        ("SPACE", "BepiColombo reaches Mercury orbit, but operations do not "
         "go exactly as planned, the team says."),
        ("MARKETS", "Sensex falls 1,484 points; Nvidia jumps almost $1tn as "
         "Jensen Huang returns and tech stocks rally."),
    ]
    for tag, txt in briefs:
        d.rectangle([lx, y + 4, lx + 10, y + 14], fill=RED)
        y = text_block(d, lx + 18, y, tag + " — " + txt, SANS(14), lw - 18, leading=3)
        y += 6

    # ---------- right column: Ukraine + COP31 ----------
    rx, rw = 644, 356
    y = kicker(d, rx, 152, "UKRAINE WAR")
    y = headline(d, rx, y, "KYIV HIT AS WAR SPILLS TO THE SEA", 24, rw)
    y = text_block(d, rx, y + 2,
                   "Russian drones strike the Kyiv region; cargo ship Sparta II "
                   "ablaze off Finland; a Russian corvette burns in Libya's "
                   "Benghazi port.",
                   SANS(15), rw, leading=3)
    draw_ship(d, rx, y + 8, rw, 80)
    rule(d, rx, 470, rx + rw, 2)

    y = kicker(d, rx, 482, "CLIMATE  •  COP31, ANTALYA")
    y = headline(d, rx, y, "CLIMATE TALKS END WITH NO FOSSIL-FUEL DEAL", 24, rw)
    y = text_block(d, rx, y + 2,
                   "COP31 closes divided over fossil fuels. Critics call the "
                   "outcome a setback for the planet as the summit ends "
                   "without stronger language.",
                   SANS(15), rw, leading=3)
    draw_globe(d, rx + rw // 2, 700, 40)

    # ---------- middle band: three stories ----------
    rule(d, 24, 748, W - 24, 2)
    cols = [
        (24, 316, "LISBON", "LISBON MARCHES ON LIVING COSTS",
         "Thousands take to the streets of Portugal's capital to protest "
         "rising prices.", "crowd"),
        (360, 316, "GAZA", "GAZA'S LAND, AIR AND WATER 'POISONED'",
         "Oxfam and CEOBS: heavy metals and asbestos threaten life across "
         "the Strip.", "earth"),
        (696, 304, "WASHINGTON", "KIM IGNORES TRUMP'S CALLS",
         "Pyongyang rebuffs US bids to revive talks as it expands its "
         "nuclear arsenal.", "phone"),
    ]
    for cx, cw, kick, head, body, art in cols:
        y = kicker(d, cx, 758, kick)
        y = headline(d, cx, y, head, 19, cw)
        y = text_block(d, cx, y + 2, body, SANS(14), cw, leading=3)
        if art == "crowd":
            draw_crowd(d, cx, y + 4, cw - 20, 54)
        elif art == "earth":
            draw_cracked_earth(d, cx, y + 4, cw - 20, 54)
        else:
            draw_phone(d, cx + 100, y + 2, 56, 60)

    # ---------- sports strip ----------
    rule(d, 24, 920, W - 24, 2)
    d.rectangle([24, 930, 120, 956], fill=INK)
    d.text((72, 933), "SPORT", font=SANS_B(15), fill=(247, 242, 231), anchor="ma")
    sport = ("VERSTAPPEN WINS VEGAS GP  •  ALCARAZ TAKES ATP FINALS  •  "
             "PANT 128  •  GUKESH DEFENDS CROWN")
    d.text((132, 937), sport, font=SANS_B(13), fill=INK)

    # ---------- by the numbers ----------
    rule(d, 24, 964, W - 24, 1)
    nums = [("24", "killed in Banten fire"),
            ("~30", "still missing"),
            ("$1tn", "Nvidia gain"),
            ("1,484", "Sensex fall")]
    for i, (val, lab) in enumerate(nums):
        x = 24 + i * 248
        d.text((x, 972), val, font=SERIF_B(22), fill=RED)
        vw = d.textlength(val, font=SERIF_B(22))
        d.text((x + vw + 8, 978), lab, font=SANS(13), fill=INK)

    # ---------- footer ----------
    d.text((W // 2, 1000), "Sources: Reuters  •  AP  •  CNN  •  The Guardian  •  NDTV  •  WSJ  •  BBC",
           font=SANS(11), fill=GREY, anchor="ma")
    return img


def main():
    out = os.environ.get("OUTPUT_PATH", "/output/entry.png")
    try:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        draw_page().save(out, "PNG")
    except OSError:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "output", "entry.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        draw_page().save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
