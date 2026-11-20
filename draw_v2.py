"""Render entry.png v2 for the make.fun news-image-20261120 bounty.

A newspaper front page summing up Friday 20 November 2026: masthead,
lead story, and five more stories plus an "also" box. Every pixel is drawn
with Pillow primitives and text; no photos, no network, no randomness.
Deterministic: the same inputs always produce the same bytes.

Run:  python3 draw_v2.py   (writes ./entry.png, 1024x1024)
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28  # side margin

PAPER = (248, 244, 232)
INK = (27, 27, 27)
MUTED = (74, 74, 68)
RED = (176, 30, 36)
BLUE = (47, 111, 178)
GREEN = (46, 125, 50)
ORANGE = (232, 100, 28)
NAVY = (35, 47, 62)
DARK = (20, 28, 38)
RULE = (138, 133, 120)

FD = "/usr/share/fonts/truetype"
SERIF_B = FD + "/noto/NotoSerif-Bold.ttf"
SANS_B = FD + "/noto/NotoSans-Bold.ttf"
SANS_R = FD + "/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Split text into lines that fit max_w at font f."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, f, fill, leading):
    """Draw lines top-left anchored; return the y below the last line."""
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def centre(d, cx, y, text, f, fill):
    d.text((cx, y), text, font=f, fill=fill, anchor="ma")


# ---- small pictograms, each drawn inside a square box (x, y, s) ----

def icon_globe(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 3
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLUE, width=4)
    d.ellipse((cx - r // 2, cy - r, cx + r // 2, cy + r), outline=BLUE, width=3)
    d.line((cx - r, cy, cx + r, cy), fill=BLUE, width=3)
    d.line((cx - r + 6, cy - r // 2, cx + r - 6, cy - r // 2), fill=BLUE, width=2)
    d.line((cx - r + 6, cy + r // 2, cx + r - 6, cy + r // 2), fill=BLUE, width=2)


def icon_cyclone(d, x, y, s):
    for i in range(4):
        inset = 4 + i * 5
        d.arc((x + inset, y + inset, x + s - inset, y + s - inset),
              start=20 + i * 70, end=290 + i * 70, fill=BLUE, width=4)
    d.ellipse((x + s // 2 - 3, y + s // 2 - 3, x + s // 2 + 3, y + s // 2 + 3),
              fill=BLUE)


def icon_virus(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 8
    for k in range(8):
        import math
        a = math.pi * k / 4
        d.line((cx + int(0.55 * r * math.cos(a)), cy + int(0.55 * r * math.sin(a)),
                cx + int(1.0 * r * math.cos(a)), cy + int(1.0 * r * math.sin(a))),
               fill=MUTED, width=4)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=MUTED, width=4)
    d.line((cx - int(0.34 * s), cy, cx - int(0.08 * s), cy + int(0.24 * s)),
           fill=GREEN, width=7)
    d.line((cx - int(0.08 * s), cy + int(0.24 * s), cx + int(0.38 * s),
            cy - int(0.30 * s)), fill=GREEN, width=7)


def icon_baseball(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 3
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255),
              outline=INK, width=3)
    # two curved red seams, like a baseball's stitching
    d.arc((cx - r, cy - r, cx + r, cy + r), start=115, end=245, fill=RED, width=3)
    d.arc((cx - r, cy - r, cx + r, cy + r), start=295, end=65, fill=RED, width=3)


def icon_controller(d, x, y, s):
    d.rounded_rectangle((x + 4, y + 14, x + s - 4, y + s - 14), radius=14,
                        fill=INK)
    # D-pad (plus sign) on the left
    d.rectangle((x + 16, y + s // 2 - 4, x + 32, y + s // 2 + 12), fill=PAPER)
    d.rectangle((x + 20, y + s // 2 - 12, x + 28, y + s // 2 + 20), fill=PAPER)
    # two buttons on the right
    d.ellipse((x + s - 30, y + s // 2 - 12, x + s - 18, y + s // 2), fill=RED)
    d.ellipse((x + s - 30, y + s // 2 + 4, x + s - 18, y + s // 2 + 16),
              fill=ORANGE)


def lead_art(d, x, y, w, h):
    """Kyiv skyline at night under missile streaks. All shapes, no photos."""
    d.rectangle((x, y, x + w, y + h), fill=NAVY)
    # stars
    for sx, sy in ((18, 22), (70, 12), (150, 30), (230, 14), (300, 26),
                   (110, 44), (260, 44)):
        d.ellipse((x + sx, y + sy, x + sx + 3, y + sy + 3), fill=(255, 255, 255))
    # missile streaks (top right to bottom left)
    for (x1, y1, x2, y2) in ((300, 8, 210, 78), (250, 30, 180, 92),
                             (180, 6, 120, 58)):
        d.line((x + x1, y + y1, x + x2, y + y2), fill=(255, 240, 180), width=3)
        d.ellipse((x + x2 - 4, y + y2 - 4, x + x2 + 4, y + y2 + 4),
                  fill=(255, 214, 90))
    # explosion bursts (offsets are absolute: add the box origin x, y)
    for (bx, by, r) in ((120, 70, 16), (235, 105, 12)):
        for k in range(8):
            import math
            a = math.pi * k / 4
            d.line((x + bx + int(0.4 * r * math.cos(a)),
                    y + by + int(0.4 * r * math.sin(a)),
                    x + bx + int(1.5 * r * math.cos(a)),
                    y + by + int(1.5 * r * math.sin(a))),
                   fill=ORANGE, width=3)
        d.ellipse((x + bx - r // 2, y + by - r // 2,
                   x + bx + r // 2, y + by + r // 2),
                  fill=(245, 166, 35))
    # skyline silhouettes along the bottom
    base = y + h
    for (bx, bw, bh) in ((0, 44, 62), (48, 30, 88), (82, 52, 54), (138, 34, 96),
                         (176, 46, 66), (226, 30, 84), (260, 40, 58),
                         (304, 28, 76)):
        d.rectangle((x + bx, base - bh, x + bx + bw, base), fill=DARK)
    # a few lit windows
    for (wx, wy) in ((58, base - 70), (90, base - 40), (150, base - 78),
                     (190, base - 50), (240, base - 66), (312, base - 58)):
        d.rectangle((x + wx, wy, x + wx + 5, wy + 7), fill=(255, 214, 90))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line((M, 16, W - M, 16), fill=INK, width=3)
    d.line((M, 22, W - M, 22), fill=INK, width=1)
    centre(d, W // 2, 30, "THE WORLD IN ONE DAY", F(SERIF_B, 60), INK)
    centre(d, W // 2, 96, "FRIDAY, 20 NOVEMBER 2026", F(SANS_B, 25), INK)
    d.line((M, 126, W - M, 126), fill=INK, width=2)

    # ---------- lead story ----------
    lx, lw = M, 612
    ax, aw = 664, 332
    d.text((lx, 140), "LEAD STORY  ·  KYIV, UKRAINE", font=F(SANS_B, 18), fill=RED)
    head = wrap(d, "RUSSIA'S BIGGEST STRIKE ON UKRAINE", F(SANS_B, 42), lw)
    assert len(head) <= 2, head
    y = block(d, lx, 164, head, F(SANS_B, 42), INK, 48)
    sub = wrap(d, "More than 110 missiles and some 400 drones hit Kyiv "
                  "overnight. Eight killed, 28 hurt, three bridges damaged "
                  "- and Poland scrambles jets.",
               F(SANS_R, 20), lw)
    assert len(sub) <= 3, sub
    block(d, lx, y + 10, sub, F(SANS_R, 20), MUTED, 26)
    lead_art(d, ax, 158, aw, 186)

    # ---------- double rule ----------
    d.line((M, 362, W - M, 362), fill=INK, width=3)
    d.line((M, 368, W - M, 368), fill=INK, width=1)
    d.text((M, 382), "THE DAY IN BRIEF", font=F(SANS_B, 18), fill=INK)

    # ---------- grid: 5 stories + 1 "also" box ----------
    stories = [
        ("CLIMATE  ·  ANTALYA, TURKEY", "COP31 SPILLS INTO OVERTIME",
         "Phase-out stripped from the draft; $120B adaptation target "
         "dropped as talks run past deadline.", icon_globe),
        ("WEATHER  ·  ODISHA, INDIA", "CYCLONE AKVAN HITS ODISHA",
         "Landfall near Gopalpur at 70-90 km/h winds; more than 370,000 "
         "people evacuated to shelters.", icon_cyclone),
        ("HEALTH  ·  KENYA", "KENYA BEATS EBOLA",
         "Last patient discharged 37 days after the first case; 42-day "
         "countdown to Ebola-free status begins.", icon_virus),
        ("SPORT  ·  WASHINGTON, U.S.", "TRUMP PARDONS PETE ROSE",
         "'Complete and total pardon' for baseball's hits leader, banned "
         "since 1989 for betting on games.", icon_baseball),
        ("CULTURE  ·  WORLDWIDE", "GTA 6 TOPS $2.3 BILLION",
         "Grand Theft Auto VI goes on sale - the biggest entertainment "
         "launch ever. A 212 GB download.", icon_controller),
    ]
    col_w, row_h = 314, 260
    xs = [M, M + col_w + 12, M + 2 * (col_w + 12)]
    ys = [410, 682]
    for i, (kicker, headline, sub, icon) in enumerate(stories):
        cx, cy = xs[i % 3], ys[i // 3]
        d.text((cx, cy), kicker, font=F(SANS_B, 16), fill=RED)
        icon(d, cx, cy + 26, 56)
        lines = wrap(d, headline, F(SANS_B, 23), col_w)
        assert len(lines) <= 3, (headline, lines)
        y = block(d, cx, cy + 92, lines, F(SANS_B, 23), INK, 28)
        slines = wrap(d, sub, F(SANS_R, 18), col_w)
        assert len(slines) <= 3, (headline, slines)
        block(d, cx, y + 6, slines, F(SANS_R, 18), MUTED, 22)

    # "also" cell, bottom right
    cx, cy = xs[2], ys[1]
    d.text((cx, cy), "ALSO ON FRIDAY", font=F(SANS_B, 16), fill=RED)
    also = [
        "EU and UK hold their second summit in Brussels",
        "Italy fines Meta \u20ac805 million over photo access",
        "FAA ground stop strands 1.5 million travellers",
    ]
    y = cy + 30
    for item in also:
        d.rectangle((cx, y + 7, cx + 9, y + 16), fill=RED)
        lines = wrap(d, item, F(SANS_R, 18), col_w - 20)
        assert len(lines) <= 2, item
        y = block(d, cx + 18, y, lines, F(SANS_R, 18), INK, 22) + 12

    # column / row separators
    for vx in (xs[1] - 6, xs[2] - 6):
        d.line((vx, ys[0], vx, ys[1] + row_h), fill=RULE, width=1)
    d.line((M, ys[1] - 6, W - M, ys[1] - 6), fill=RULE, width=1)

    # ---------- footer ----------
    d.line((M, 962, W - M, 962), fill=INK, width=2)
    centre(d, W // 2, 974, "THE WORLD IN ONE DAY  ·  FRIDAY 20 NOVEMBER 2026  ·  "
                            "SIX STORIES THAT DEFINED THE DAY",
           F(SANS_R, 15), MUTED)

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
