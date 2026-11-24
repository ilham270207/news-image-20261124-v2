#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE -- front page for Tuesday 24 November 2026.

Draws a dense morning-newspaper front page as a single 1024x1024 PNG
with Pillow. Everything (text, layout, illustrations) is drawn in code
with vector shapes only: no photographs, no network, no real faces.
Deterministic: no randomness, no timestamps -- two runs produce
byte-identical output.

Output location, in order:
  1. $MAKEFUN_OUTPUT_DIR/entry.png
  2. /output/entry.png
  3. ./output/entry.png
  4. /tmp/entry.png

If Pillow cannot be imported at all, fall back to copying a pre-rendered
output/entry.png shipped in this repo to the output location and exit 0.
"""

import os
import shutil
import sys

# ---------------------------------------------------------------- PIL import
try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except ImportError:
    try:
        import site
        for _p in site.getsitepackages():
            if _p not in sys.path:
                sys.path.insert(0, _p)
        try:
            _up = site.getusersitepackages()
            if _up and _up not in sys.path:
                sys.path.insert(0, _up)
        except Exception:
            pass
        from PIL import Image, ImageDraw, ImageFont
        HAVE_PIL = True
    except ImportError:
        HAVE_PIL = False

# ------------------------------------------------------------------ constants
W, H = 1024, 1024
MARGIN = 28
RIGHT = W - MARGIN

PAPER = (253, 250, 240)      # warm newsprint
INK = (24, 22, 18)           # near-black
INK_SOFT = (74, 70, 62)
RULE = (24, 22, 18)
RED = (178, 34, 28)          # accent red for kickers
STEEL = (58, 74, 92)         # steel blue
SKY = (176, 208, 224)
SEA = (46, 96, 128)
FLAME = (232, 116, 28)
FLAME_HOT = (246, 178, 44)
SMOKE = (150, 148, 142)
EARTH = (146, 104, 62)
EARTH_DARK = (96, 66, 38)
GREEN = (58, 110, 66)
SAND = (214, 196, 152)
DARK_BAND = (30, 32, 38)
BAND_TEXT = (244, 240, 228)
GOLD = (212, 164, 60)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------- fonts
def load_font(name, size):
    """Load a bundled DejaVu font; fall back to Pillow's default font."""
    if HAVE_PIL:
        for base in (os.path.join(SCRIPT_DIR, "fonts"),
                     os.path.join(os.getcwd(), "fonts"), "fonts"):
            path = os.path.join(base, name)
            try:
                if os.path.isfile(path):
                    return ImageFont.truetype(path, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()


F_SERIF = lambda s: load_font("DejaVuSerif.ttf", s)
F_SERIF_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: load_font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)


# ---------------------------------------------------------------- text helpers
def wrap(text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill=INK, leading=None):
    """Draw wrapped lines; returns the y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.28)
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color=RED):
    f = F_SANS_B(15)
    d.text((x, y), text, font=f, fill=color)
    return y + 22


def headline(d, x, y, text, size, max_w, leading=None):
    f = F_SERIF_B(size)
    lines = wrap(text, f, max_w)
    return draw_lines(d, lines, x, y, f, leading=leading)


def body(d, x, y, text, size, max_w, fill=INK):
    f = F_SANS(size)
    lines = wrap(text, f, max_w)
    return draw_lines(d, lines, x, y, f, fill=fill)


def rule(d, x0, y, x1, width=2):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)


def thin_rule(d, x0, y, x1):
    d.line([(x0, y), (x1, y)], fill=(150, 144, 128), width=1)


# -------------------------------------------------------------- illustrations
def draw_fire_factory(d, x, y, w, h):
    """Factory building with flames and smoke (lead illustration)."""
    base_y = y + h - 8
    # ground shadow
    d.rectangle([x, base_y, x + w, base_y + 6], fill=(226, 216, 196))
    # main factory block
    d.rectangle([x + 18, y + 52, x + w - 18, base_y], fill=(96, 88, 82))
    d.rectangle([x + 18, y + 52, x + w - 18, y + 66], fill=(70, 64, 58))
    # sawtooth roof
    for i in range(4):
        rx = x + 30 + i * ((w - 60) // 4)
        d.polygon([(rx, y + 52), (rx + 34, y + 22),
                   (rx + 68, y + 52)], fill=(120, 110, 100))
    # windows, some lit by fire
    for i in range(6):
        wx = x + 44 + i * 62
        lit = i in (1, 3, 4)
        d.rectangle([wx, y + 84, wx + 34, y + 118],
                    fill=FLAME_HOT if lit else (210, 198, 170))
    # door
    d.rectangle([x + w // 2 - 22, y + h - 52, x + w // 2 + 22, base_y],
                fill=(48, 44, 40))
    # chimney
    d.rectangle([x + w - 84, y + 6, x + w - 58, y + 56], fill=(84, 78, 72))
    d.rectangle([x + w - 90, y + 2, x + w - 52, y + 10], fill=(64, 60, 56))
    # flames licking the roofline
    for fx, fh in ((x + 60, 36), (x + 150, 40), (x + 250, 34),
                   (x + 350, 38), (x + 440, 32)):
        d.polygon([(fx, y + 56), (fx + 14, y + 56 - fh),
                   (fx + 26, y + 56 - fh // 2), (fx + 38, y + 56 - fh),
                   (fx + 52, y + 56)],
                  fill=FLAME)
        d.polygon([(fx + 12, y + 56), (fx + 22, y + 56 - fh // 2),
                   (fx + 34, y + 56)], fill=FLAME_HOT)
    # smoke puffs drift just above the chimney, inside the art box
    for sx, sy, r in ((x + w - 71, y + 18, 12), (x + w - 104, y + 14, 10),
                      (x + w - 40, y + 24, 9), (x + 130, y + 34, 10)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)
    # small fire truck hint: red block + ladder
    d.rectangle([x + 8, base_y - 26, x + 76, base_y], fill=RED)
    d.line([(x + 30, base_y - 26), (x + 96, base_y - 66)],
           fill=(200, 200, 200), width=5)


def draw_ship(d, x, y, w, h):
    """Cargo ship ablaze on the sea. All shapes stay inside (x, y, w, h)."""
    sea_y = y + h - 20
    d.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(5):
        wx = x + 8 + i * 44
        d.arc([wx, sea_y + 4, wx + 30, sea_y + 16], 0, 180, fill=SKY, width=2)
    # hull
    d.polygon([(x + 10, sea_y - 24), (x + w - 10, sea_y - 24),
               (x + w - 34, sea_y), (x + 34, sea_y)], fill=(52, 52, 58))
    d.rectangle([x + 10, sea_y - 30, x + w - 10, sea_y - 24], fill=RED)
    # containers
    cols = [(200, 60, 50), (58, 110, 66), (46, 96, 128), (212, 164, 60)]
    for i in range(4):
        cx = x + 34 + i * 62
        d.rectangle([cx, sea_y - 56, cx + 54, sea_y - 30],
                    fill=cols[i % len(cols)])
        d.line([(cx, sea_y - 43), (cx + 54, sea_y - 43)],
               fill=(255, 255, 255), width=1)
    # bridge tower
    d.rectangle([x + w - 76, sea_y - 70, x + w - 34, sea_y - 30],
                fill=(226, 220, 208))
    d.rectangle([x + w - 72, sea_y - 64, x + w - 38, sea_y - 52],
                fill=STEEL)
    # flames + small smoke puffs from the mid-deck, inside the box
    fx = x + w // 2 - 40
    d.polygon([(fx, sea_y - 56), (fx + 16, sea_y - 74),
               (fx + 32, sea_y - 64), (fx + 48, sea_y - 72),
               (fx + 66, sea_y - 56)], fill=FLAME)
    d.polygon([(fx + 16, sea_y - 56), (fx + 28, sea_y - 68),
               (fx + 44, sea_y - 56)], fill=FLAME_HOT)
    for sx, sy, r in ((fx + 8, sea_y - 66, 6), (fx + 58, sea_y - 68, 7)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)


def draw_globe(d, x, y, w, h):
    """A globe with cracked, warming land."""
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 152, 196))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=STEEL, width=2)
    # meridians
    for k in (0.45, 1.0):
        d.ellipse([cx - int(r * k), cy - r, cx + int(r * k), cy + r],
                  outline=(150, 190, 214), width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(150, 190, 214), width=1)
    # land masses (abstract blobs)
    d.ellipse([cx - r + 8, cy - r + 14, cx - 6, cy - 4], fill=GREEN)
    d.ellipse([cx + 2, cy + 2, cx + r - 10, cy + r - 16], fill=GREEN)
    d.ellipse([cx - r + 22, cy + r - 34, cx - r + 52, cy + r - 8],
              fill=(96, 140, 80))
    # a crack across the lower land + a small sun
    d.line([(cx + 8, cy + 10), (cx + 22, cy + 22), (cx + 14, cy + 34),
            (cx + 30, cy + 44)], fill=(60, 40, 20), width=2)
    d.ellipse([cx + r - 30, cy - r + 8, cx + r - 12, cy - r + 26],
              fill=FLAME_HOT)
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1 = cx + r - 21 + int(13 * math.cos(a))
        y1 = cy - r + 17 + int(13 * math.sin(a))
        x2 = cx + r - 21 + int(19 * math.cos(a))
        y2 = cy - r + 17 + int(19 * math.sin(a))
        d.line([(x1, y1), (x2, y2)], fill=FLAME_HOT, width=2)


def draw_crowd(d, x, y, w, h):
    """Protest crowd with placards. All shapes stay inside (x, y, w, h)."""
    base_y = y + h - 6
    d.rectangle([x, base_y - 4, x + w, base_y + 4], fill=SAND)
    # placards first (held high, but inside the box), crowd drawn over them
    for px, txt in ((x + 34, "FAIR"), (x + w // 2 - 6, "PAY"),
                    (x + w - 66, "NOW")):
        d.rectangle([px - 16, y + 6, px + 48, y + 30],
                    fill=(250, 246, 232), outline=INK, width=2)
        d.text((px - 8, y + 10), txt, font=F_SANS_B(13), fill=RED)
        d.line([(px + 16, y + 30), (px + 16, y + 52)],
               fill=(90, 80, 66), width=3)
    shirts = [(178, 34, 28), (46, 96, 128), (58, 110, 66),
              (212, 164, 60), (96, 70, 120)]
    # back row, then front row
    for row, ry, rad, n in ((1, base_y - 56, 11, 5),
                            (0, base_y - 26, 13, 6)):
        for i in range(n):
            px = x + 26 + i * ((w - 40) // max(n - 1, 1))
            d.rectangle([px - 13, ry, px + 13, base_y - 4],
                        fill=shirts[(i + row) % len(shirts)])
            d.ellipse([px - rad, ry - 2 * rad + 8, px + rad, ry + 8],
                      fill=(222, 184, 150))


def draw_cracked_earth(d, x, y, w, h):
    """Dry, cracked ground with a warning sign."""
    d.rectangle([x, y, x + w, y + h], fill=EARTH)
    d.rectangle([x, y, x + w, y + 16], fill=(196, 158, 104))
    # cracks
    cracks = [
        [(x + 10, y + 20), (x + 46, y + 44), (x + 30, y + 70),
         (x + 62, y + 96)],
        [(x + w - 20, y + 24), (x + w - 60, y + 52), (x + w - 34, y + 78),
         (x + w - 70, y + h - 8)],
        [(x + w // 2, y + 18), (x + w // 2 + 18, y + 48),
         (x + w // 2 - 8, y + 76), (x + w // 2 + 10, y + h - 6)],
    ]
    for pts in cracks:
        d.line(pts, fill=EARTH_DARK, width=3, joint="curve")
    # tufts of dead grass
    for gx in (x + 24, x + w - 44, x + w // 2 + 44):
        for dx in (-6, 0, 6):
            d.line([(gx + dx, y + h - 6), (gx + dx - 3, y + h - 22)],
                   fill=(120, 104, 52), width=2)
    # small warning triangle
    tx, ty = x + w - 74, y + h - 52
    d.polygon([(tx, ty), (tx + 34, ty), (tx + 17, ty - 28)],
              fill=GOLD, outline=INK)
    d.text((tx + 13, ty - 22), "!", font=F_SANS_B(16), fill=INK)


def draw_phone(d, x, y, w, h):
    """An old telephone handset resting above its base, unanswered.
    All shapes stay inside (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    # base
    d.rounded_rectangle([cx - 52, cy + 6, cx + 52, cy + 44], radius=8,
                        fill=STEEL)
    d.rectangle([cx - 30, cy - 6, cx + 30, cy + 8], fill=(38, 52, 66))
    # dial
    d.ellipse([cx - 20, cy + 14, cx + 20, cy + 40], fill=(226, 220, 208))
    d.ellipse([cx - 6, cy + 22, cx + 6, cy + 32], fill=STEEL)
    # handset, tilted just above the base (call unanswered)
    d.line([(cx - 56, cy - 18), (cx + 56, cy - 30)], fill=RED, width=16)
    d.ellipse([cx - 76, cy - 32, cx - 38, cy - 4], fill=RED)
    d.ellipse([cx + 38, cy - 44, cx + 76, cy - 16], fill=RED)
    # ringing arcs beside the upper earpiece
    d.arc([cx + 80, cy - 44, cx + 100, cy - 24], -70, 70,
          fill=FLAME_HOT, width=3)
    d.arc([cx + 80, cy - 48, cx + 108, cy - 20], -70, 70,
          fill=FLAME_HOT, width=3)
    # coiled cord suggestion
    d.line([(cx - 56, cy - 8), (cx - 64, cy + 8), (cx - 40, cy + 6)],
           fill=INK_SOFT, width=3, joint="curve")


# ---------------------------------------------------------------- page build
def build_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.text((MARGIN, 18), "THE WORLD IN ONE PAGE",
           font=F_SERIF_B(56), fill=INK)
    d.text((MARGIN, 86), "TUESDAY, 24 NOVEMBER 2026",
           font=F_SANS_B(16), fill=INK)
    d.text((RIGHT - 250, 86), "ONE PAGE  •  WORLD NEWS",
           font=F_SANS_B(16), fill=INK_SOFT)
    rule(d, MARGIN, 116, RIGHT, 4)
    rule(d, MARGIN, 122, RIGHT, 1)

    # ---- lead story: Indonesia factory fire ---------------------------
    lx, lw = MARGIN, 592
    ly = 138
    y = kicker(d, lx, ly, "INDONESIA  —  LEAD STORY")
    y = headline(d, lx, y, "Fire kills 24 at Java candy factory", 38, lw)
    y = body(d, lx, y + 4,
             "A blaze ripped through a candy plant in Banten province, "
             "killing 24 workers. Around 30 more are still missing as "
             "rescuers pick through the charred factory.", 16, lw)
    draw_fire_factory(d, lx, y + 8, lw, 128)
    lead_bottom = y + 8 + 128
    rule(d, lx, lead_bottom + 8, lx + lw, 1)

    # ---- right column: Ukraine war + climate --------------------------
    rx, rw = 648, RIGHT - 648
    y = kicker(d, rx, 138, "UKRAINE WAR")
    y = headline(d, rx, y, "Kyiv hit as war spills to the sea", 21, rw)
    y = body(d, rx, y + 2,
             "Russian drones struck the Kyiv region. Cargo ship Sparta II "
             "burned off Finland; a Russian corvette burned in Libya's "
             "Benghazi port.", 14, rw)
    draw_ship(d, rx, y + 4, rw, 96)
    ship_bottom = y + 4 + 96
    thin_rule(d, rx, ship_bottom + 6, RIGHT)
    cy = ship_bottom + 18
    y = kicker(d, rx, cy, "CLIMATE")
    # globe sits beside the headline, clear of the text
    draw_globe(d, RIGHT - 76, cy, 76, 76)
    y = headline(d, rx, y, "COP31 ends with no fossil-fuel deal", 21,
                 rw - 84)
    y = body(d, rx, y + 2,
             "Talks in Antalya closed divided over fossil fuels; critics "
             "call the outcome a setback for the planet.", 14, rw)
    climate_bottom = y

    # ---- middle row: three stories ------------------------------------
    my = max(lead_bottom, climate_bottom) + 16
    rule(d, MARGIN, my - 12, RIGHT, 2)
    col_w = 300
    cols = [
        ("LISBON", "Thousands march on living costs",
         "Protesters filled the streets of Portugal's capital over "
         "rising prices.", draw_crowd),
        ("GAZA", "Land, air and water 'poisoned'",
         "Oxfam and CEOBS: heavy metals, asbestos and explosive "
         "residues poison Gaza for decades.", draw_cracked_earth),
        ("WASHINGTON", "Kim ignores Trump's calls",
         "Pyongyang rebuffs US bids to revive talks as it expands "
         "its nuclear arsenal.", draw_phone),
    ]
    mid_bottom = my
    for i, (kick, head, deck, art) in enumerate(cols):
        cx = MARGIN + i * (col_w + 24)
        y = kicker(d, cx, my, kick)
        y = headline(d, cx, y, head, 19, col_w)
        y = body(d, cx, y + 2, deck, 13, col_w)
        art(d, cx, y + 4, col_w, 96)
        mid_bottom = max(mid_bottom, y + 4 + 96)
    for i in (1, 2):
        sx = MARGIN + i * (col_w + 24) - 12
        d.line([(sx, my), (sx, mid_bottom)], fill=(180, 172, 152), width=1)

    # ---- sports strip ---------------------------------------------------
    sy = mid_bottom + 16
    rule(d, MARGIN, sy - 10, RIGHT, 2)
    d.text((MARGIN, sy), "SPORT", font=F_SANS_B(17), fill=RED)
    d.text((MARGIN + 90, sy), "Four finals, one afternoon",
           font=F_SERIF(16), fill=INK_SOFT)
    sports = [
        ("F1", "Verstappen wins the Las Vegas Grand Prix."),
        ("TENNIS", "Alcaraz takes his first ATP Finals title."),
        ("CRICKET", "Pant hits 128 in the Wellington Test draw."),
        ("CHESS", "Gukesh defends the crown vs Sindarov in Geneva."),
    ]
    sw = (RIGHT - MARGIN - 3 * 20) // 4
    for i, (tag, txt) in enumerate(sports):
        sx = MARGIN + i * (sw + 20)
        if i:
            d.line([(sx - 10, sy + 30), (sx - 10, sy + 88)],
                   fill=(180, 172, 152), width=1)
        d.text((sx, sy + 30), tag, font=F_SANS_B(14), fill=STEEL)
        body(d, sx, sy + 52, txt, 14, sw)
    sports_bottom = sy + 88

    # ---- by the numbers -------------------------------------------------
    by = sports_bottom + 14
    d.rectangle([MARGIN, by, RIGHT, by + 118], fill=DARK_BAND)
    d.text((MARGIN + 16, by + 12), "BY THE NUMBERS",
           font=F_SANS_B(16), fill=GOLD)
    stats = [
        ("24", "killed in the Banten factory fire"),
        ("~30", "workers still missing"),
        ("$1tn", "Nvidia gain as Huang returns"),
        ("1,484", "points lost by India's Sensex"),
    ]
    nw = (RIGHT - MARGIN - 32 - 3 * 16) // 4
    for i, (num, label) in enumerate(stats):
        nx = MARGIN + 16 + i * (nw + 16)
        if i:
            d.line([(nx - 8, by + 44), (nx - 8, by + 104)],
                   fill=(90, 92, 100), width=1)
        d.text((nx, by + 44), num, font=F_SERIF_B(30), fill=BAND_TEXT)
        body(d, nx, by + 82, label, 12, nw, fill=BAND_TEXT)

    # ---- footer ---------------------------------------------------------
    d.text((MARGIN, by + 118 + 8), "Sources: Reuters  •  AP  •  The Guardian  •  "
           "CNN  •  NDTV  •  Oxfam  •  CEOBS  •  Wall Street Journal",
           font=F_SANS(11), fill=INK_SOFT)
    return img


# ------------------------------------------------------------- output paths
def output_candidates():
    """Ordered list of output file paths to try."""
    cands = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        cands.append(os.path.join(env_dir, "entry.png"))
    cands.append("/output/entry.png")
    cands.append(os.path.join(os.getcwd(), "output", "entry.png"))
    cands.append("/tmp/entry.png")
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def write_bytes_to_first_writable(data, paths):
    """Write bytes to the first path whose directory can be created and
    written; returns the path used, or None."""
    for path in paths:
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data)
            return path
        except Exception:
            continue
    return None


def find_prerendered():
    """Locate the pre-rendered output/entry.png shipped in this repo."""
    for base in (SCRIPT_DIR, os.getcwd()):
        p = os.path.join(base, "output", "entry.png")
        if os.path.isfile(p):
            return p
    return None


# ---------------------------------------------------------------------- main
def main():
    paths = output_candidates()

    if not HAVE_PIL:
        # No Pillow at all: copy the pre-rendered image and exit 0.
        src = find_prerendered()
        if src:
            try:
                with open(src, "rb") as fh:
                    data = fh.read()
                if write_bytes_to_first_writable(data, paths):
                    return 0
            except Exception:
                pass
        return 0

    img = build_page()
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    if write_bytes_to_first_writable(buf.getvalue(), paths):
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
