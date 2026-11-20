#!/usr/bin/env python3
"""Render entry.png: one image summing up Friday 20 November 2026's world news.

Deterministic: no timestamps, no randomness, fixed fonts, fixed layout.
Run: python3 draw.py  ->  writes entry.png (1024x1024, < 1 MiB).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024

BG = (11, 18, 32)          # deep navy
PANEL = (19, 30, 51)        # panel fill
PANEL_EDGE = (36, 52, 79)   # panel border
WHITE = (244, 246, 250)
MUTED = (199, 208, 224)     # sub-line text
GOLD = (242, 183, 5)
DARK = (11, 18, 32)         # glyph colour on accent circles

FONT_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

ACCENTS = {
    "red": (229, 72, 77),
    "teal": (47, 158, 143),
    "purple": (139, 124, 246),
    "green": (63, 185, 80),
    "amber": (245, 165, 36),
    "pink": (255, 92, 138),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with extra tracking between letters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def star_points(cx, cy, outer, inner, n=12):
    pts = []
    for i in range(n * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon_burst(d, cx, cy):
    d.polygon(star_points(cx, cy, 21, 9), fill=DARK)


def icon_people(d, cx, cy):
    for dx, dy, r in ((-14, 2, 6), (0, -5, 7), (14, 2, 6)):
        d.ellipse((cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r), fill=DARK)
        d.pieslice((cx + dx - 11, cy + dy + 6, cx + dx + 11, cy + dy + 24),
                   180, 360, fill=DARK)


def icon_scales(d, cx, cy):
    d.line((cx, cy - 18, cx, cy + 18), fill=DARK, width=3)
    d.line((cx - 18, cy - 14, cx + 18, cy - 14), fill=DARK, width=3)
    d.polygon([(cx - 18, cy - 14), (cx - 24, cy + 2), (cx - 12, cy + 2)], fill=DARK)
    d.polygon([(cx + 18, cy - 14), (cx + 12, cy + 2), (cx + 24, cy + 2)], fill=DARK)
    d.ellipse((cx - 3, cy - 21, cx + 3, cy - 15), fill=DARK)


def icon_chart(d, cx, cy):
    pts = [(cx - 19, cy - 12), (cx - 7, cy - 3), (cx + 3, cy + 3), (cx + 15, cy + 13)]
    d.line(pts, fill=DARK, width=4, joint="curve")
    d.polygon([(cx + 15, cy + 13), (cx + 5, cy + 11), (cx + 13, cy + 3)], fill=DARK)


def icon_tower(d, cx, cy):
    d.rectangle((cx - 8, cy - 12, cx + 8, cy + 18), fill=DARK)
    d.polygon(star_points(cx, cy - 17, 9, 4, n=8), fill=DARK)
    for wy in (-6, 0, 6, 12):
        d.rectangle((cx - 4, cy + wy, cx - 1, cy + wy + 2), fill=ACCENTS["amber"])
        d.rectangle((cx + 1, cy + wy, cx + 4, cy + wy + 2), fill=ACCENTS["amber"])


def icon_controller(d, cx, cy):
    d.rounded_rectangle((cx - 21, cy - 12, cx + 21, cy + 12), radius=9, fill=DARK)
    d.rectangle((cx - 15, cy - 2, cx - 7, cy + 2), fill=ACCENTS["pink"])
    d.rectangle((cx - 13, cy - 4, cx - 9, cy + 4), fill=ACCENTS["pink"])
    d.ellipse((cx + 8, cy - 6, cx + 13, cy - 1), fill=ACCENTS["pink"])
    d.ellipse((cx + 13, cy + 1, cx + 18, cy + 6), fill=ACCENTS["pink"])


PANELS = [
    {
        "accent": ACCENTS["red"], "icon": icon_burst, "kicker": "UKRAINE WAR",
        "headline": "RUSSIA'S BIGGEST STRIKE",
        "sub": "110+ missiles, ~400 drones hit Ukraine; 8 killed, 28 injured. "
               "Kyiv bridges damaged; Poland scrambled jets.",
    },
    {
        "accent": ACCENTS["teal"], "icon": icon_people, "kicker": "DIPLOMACY",
        "headline": "TRUMP, XI & PUTIN MEET",
        "sub": "First three-way summit in Shenzhen ends with a joint "
               "peace declaration.",
    },
    {
        "accent": ACCENTS["purple"], "icon": icon_scales, "kicker": "JUSTICE",
        "headline": "WORLD COURT RULES",
        "sub": "ICJ finds Myanmar committed genocide against the Rohingya.",
    },
    {
        "accent": ACCENTS["green"], "icon": icon_chart, "kicker": "MARKETS",
        "headline": "ANTHROPIC DEBUTS, MARKETS FALL",
        "sub": "Anthropic closes ~17% above its $83 IPO price on Nasdaq; "
               "US stocks fall a fifth straight day; Nikkei drops 4.8%.",
    },
    {
        "accent": ACCENTS["amber"], "icon": icon_tower, "kicker": "MIDDLE EAST",
        "headline": "RIYADH HIT",
        "sub": "Houthi missiles damage a Riyadh skyscraper, the Saudi "
               "sovereign wealth fund tower.",
    },
    {
        "accent": ACCENTS["pink"], "icon": icon_controller, "kicker": "GAMING",
        "headline": "GTA 6 LAUNCHES",
        "sub": "Grand Theft Auto VI goes on sale worldwide and tops "
               "$2.3 billion in sales.",
    },
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_date = font(FONT_BLACK, 54)
    f_title = font(FONT_BOLD, 25)
    f_kicker = font(FONT_BOLD, 19)
    f_head = font(FONT_BLACK, 29)
    f_sub = font(FONT_REG, 20)

    # ---- header ----
    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 26), date, font=f_date, fill=WHITE)
    title_text = "THE WORLD IN ONE DAY"
    tw = sum(d.textlength(ch, font=f_title) for ch in title_text) + 5 * (len(title_text) - 1)
    rule_gap, rule_len = 18, 110
    d.line((W / 2 - tw / 2 - rule_gap - rule_len, 108,
            W / 2 - tw / 2 - rule_gap, 108), fill=GOLD, width=2)
    d.line((W / 2 + tw / 2 + rule_gap, 108,
            W / 2 + tw / 2 + rule_gap + rule_len, 108), fill=GOLD, width=2)
    draw_spaced(d, W / 2, 94, title_text, f_title, GOLD, tracking=5)

    # ---- panels: 2 columns x 3 rows ----
    margin, gap = 24, 16
    grid_top, grid_bottom = 164, 1004
    pw = (W - 2 * margin - gap) // 2
    ph = (grid_bottom - grid_top - 2 * gap) // 3
    pad = 18
    text_w = pw - 2 * pad

    for i, p in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = grid_top + row * (ph + gap)
        accent = p["accent"]

        d.rounded_rectangle((x, y, x + pw, y + ph), radius=14,
                            fill=PANEL, outline=PANEL_EDGE, width=1)
        # accent tick at panel top
        d.rounded_rectangle((x + pad, y + 14, x + pad + 44, y + 18),
                            radius=2, fill=accent)

        # icon circle + kicker
        cx, cy = x + pad + 27, y + 58
        d.ellipse((cx - 27, cy - 27, cx + 27, cy + 27), fill=accent)
        p["icon"](d, cx, cy)
        d.text((x + pad + 66, cy - 13), p["kicker"], font=f_kicker, fill=accent)

        # headline (up to 2 lines)
        head_lines = wrap(d, p["headline"], f_head, text_w)
        hy = y + 100
        for line in head_lines:
            d.text((x + pad, hy), line, font=f_head, fill=WHITE)
            hy += 37

        # sub (up to 3 lines)
        sub_lines = wrap(d, p["sub"], f_sub, text_w)
        sy = hy + 6
        for line in sub_lines:
            d.text((x + pad, sy), line, font=f_sub, fill=MUTED)
            sy += 26

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
