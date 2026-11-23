#!/usr/bin/env python3
"""Render entry.png — front-page newspaper, WORLD NEWS, Monday 23 Nov 2026.
Deterministic PIL render. All facts/text taken ONLY from research.md.
Palette: paper / ink / red (3 main colours). Fonts: Anton (display) +
DejaVu Sans (body/tags) — 2 families, per Headline Studio V3.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (166, 30, 30)
GREY = (96, 92, 84)

ANTON = "/home/hatch/.fonts/Anton-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

M = 44  # margin

def font(path, size):
    return ImageFont.truetype(path, size)

def tracked_width(draw, text, fnt, tracking):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking

def draw_tracked(draw, x, y, text, fnt, fill, tracking=2):
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking

def draw_tracked_center(draw, cx, y, text, fnt, fill, tracking=2):
    w = tracked_width(draw, text, fnt, tracking)
    draw_tracked(draw, cx - w / 2, y, text, fnt, fill, tracking)

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ---------------- pictograms (simple PIL line art, ink + red accent) -------
def icon_globe(d, x, y, s, ink, red):
    d.ellipse([x, y, x + s, y + s], outline=ink, width=5)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=ink, width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=ink, width=3)
    d.arc([x, y + s * 0.12, x + s, y + s * 0.88], 200, 340, fill=ink, width=3)
    d.arc([x, y + s * 0.12, x + s, y + s * 0.88], 20, 160, fill=ink, width=3)

def icon_ship(d, x, y, s, ink, red):
    # hull
    d.polygon([(x + 2, y + s * 0.55), (x + s - 2, y + s * 0.55),
               (x + s * 0.82, y + s * 0.78), (x + s * 0.18, y + s * 0.78)],
              outline=ink, width=4)
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.55], fill=ink, width=4)
    d.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.78, y + s * 0.20),
               (x + s * 0.5, y + s * 0.30)], fill=red)
    d.arc([x, y + s * 0.82, x + s * 0.45, y + s + 6], 180, 360, fill=ink, width=3)
    d.arc([x + s * 0.55, y + s * 0.82, x + s, y + s + 6], 180, 360, fill=ink, width=3)

def icon_dome(d, x, y, s, ink, red):
    d.chord([x + s * 0.18, y + s * 0.02, x + s * 0.82, y + s * 0.62], 180, 360,
            outline=ink, width=4)
    d.rectangle([x + s * 0.10, y + s * 0.62, x + s * 0.90, y + s * 0.72],
                outline=ink, width=3)
    for cx in (0.24, 0.40, 0.56, 0.72):
        d.line([x + s * cx, y + s * 0.72, x + s * cx, y + s * 0.92],
               fill=ink, width=3)
    d.rectangle([x + s * 0.06, y + s * 0.92, x + s * 0.94, y + s * 0.98],
                fill=ink)
    d.line([x + s * 0.5, y, x + s * 0.5, y + s * 0.06], fill=ink, width=3)
    d.polygon([(x + s * 0.5, y), (x + s * 0.68, y + s * 0.05),
               (x + s * 0.5, y + s * 0.10)], fill=red)

def icon_drop(d, x, y, s, ink, red):
    d.polygon([(x + s * 0.5, y + s * 0.02), (x + s * 0.82, y + s * 0.48),
               (x + s * 0.18, y + s * 0.48)], fill=red)
    d.chord([x + s * 0.18, y + s * 0.30, x + s * 0.82, y + s * 0.94], 0, 180,
            fill=red)
    d.arc([x, y + s * 0.86, x + s, y + s + 4], 180, 360, fill=ink, width=3)

def icon_building(d, x, y, s, ink, red):
    d.rectangle([x + s * 0.12, y + s * 0.18, x + s * 0.55, y + s * 0.95],
                outline=ink, width=4)
    d.rectangle([x + s * 0.60, y + s * 0.38, x + s * 0.88, y + s * 0.95],
                outline=ink, width=4)
    for wy in (0.32, 0.52, 0.72):
        d.line([x + s * 0.20, y + s * wy, x + s * 0.47, y + s * wy],
               fill=ink, width=2)
    # crack in red
    d.line([(x + s * 0.34, y + s * 0.18), (x + s * 0.28, y + s * 0.40),
            (x + s * 0.38, y + s * 0.55), (x + s * 0.30, y + s * 0.75),
            (x + s * 0.36, y + s * 0.95)], fill=red, width=4, joint="curve")

def icon_chart(d, x, y, s, ink, red):
    d.line([x + s * 0.08, y + s * 0.08, x + s * 0.08, y + s * 0.92,
            x + s * 0.95, y + s * 0.92], fill=ink, width=4)
    pts = [(x + s * 0.14, y + s * 0.30), (x + s * 0.36, y + s * 0.42),
           (x + s * 0.52, y + s * 0.36), (x + s * 0.74, y + s * 0.62),
           (x + s * 0.90, y + s * 0.78)]
    d.line(pts, fill=red, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=red)

def icon_ball(d, x, y, s, ink, red):
    d.ellipse([x, y, x + s, y + s], outline=ink, width=4)
    cx, cy, r = x + s * 0.5, y + s * 0.5, s * 0.16
    d.regular_polygon((cx, cy, r), 5, outline=ink, width=3)
    for ang in (90, 162, 234, 306, 18):
        import math
        a = math.radians(ang)
        x2 = cx + (r + s * 0.22) * math.cos(a)
        y2 = cy - (r + s * 0.22) * math.sin(a)
        d.line([cx + r * math.cos(a), cy - r * math.sin(a), x2, y2],
               fill=ink, width=2)
    d.regular_polygon((cx, cy, r * 0.55), 5, fill=red)

# ---------------- content (verbatim facts from research.md) ---------------
LEAD = dict(
    tag="CLIMATE  ·  ANTALYA, TURKEY",
    headline="COP31 COLLAPSES WITHOUT A DEAL",
    summary="Countries fail to agree on moving away from fossil fuels",
    icon=icon_globe,
)
ROWS = [
    dict(tag="UKRAINE WAR  ·  LIBYA",
         headline="UKRAINE SAYS IT SANK RUSSIAN CORVETTE MERKURY",
         summary="Kyiv says seven naval drones sank the ship off Benghazi",
         icon=icon_ship),
    dict(tag="U.S. POLITICS",
         headline="DEMOCRATS WIN AT LEAST 258 HOUSE SEATS",
         summary="Largest majority since 1992; 44 seats flipped so far",
         icon=icon_dome),
    dict(tag="MIDDLE EAST  ·  ENERGY",
         headline="GULF SHIPPING HIT AS TRUMP WARNS IRAN OVER HORMUZ",
         summary="Iran-linked attacks hit tankers and Bahrain; oil flows slow",
         icon=icon_drop),
    dict(tag="UKRAINE WAR  ·  KYIV REGION",
         headline="RUSSIAN DRONE STRIKE ON DYMER KILLS 11",
         summary="Apartment block hit near Kyiv; rescuers still search rubble",
         icon=icon_building),
    dict(tag="MARKETS  ·  TECHNOLOGY",
         headline="NASDAQ SUFFERS WORST WEEK SINCE 2020",
         summary="Nasdaq falls 10% in a week; S&P 500 enters correction",
         icon=icon_chart),
    dict(tag="SPORT  ·  PREMIER LEAGUE",
         headline="LIVERPOOL HAMMER TEN-MAN UNITED 4-0",
         summary="Pochettino's debut as United manager ends in rout at Anfield",
         icon=icon_ball),
]

# ---------------- render ---------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

y = 30
# dateline
f_date = font(SANS_B, 22)
draw_tracked_center(d, W // 2, y, "MONDAY, 23 NOVEMBER 2026", f_date, RED, 4)
y += 34
# thin red rule
d.line([M, y, W - M, y], fill=RED, width=3)
y += 12
# masthead
f_mast = font(ANTON, 118)
draw_tracked_center(d, W // 2, y, "WORLD NEWS", f_mast, INK, 6)
asc, desc = f_mast.getmetrics()
y += asc + desc + 14  # clear the full glyph box before the rules
# double rule
d.line([M, y, W - M, y], fill=INK, width=4)
y += 6
d.line([M, y, W - M, y], fill=INK, width=1)
y += 16

# lead story
f_tag = font(SANS_B, 20)
f_lead = font(ANTON, 46)
f_sum = font(SANS, 22)
lead_icon = 108
lead_text_w = W - 2 * M - lead_icon - 28
draw_tracked(d, M, y, LEAD["tag"], f_tag, RED, 2)
y += 30
lines = wrap(d, LEAD["headline"], f_lead, lead_text_w)
assert len(lines) <= 2, lines
ly = y
for ln in lines:
    d.text((M, ly), ln, font=f_lead, fill=INK)
    ly += 52
lead_mid = y + (len(lines) * 52) // 2
LEAD["icon"](d, W - M - lead_icon, lead_mid - lead_icon // 2 + 8,
             lead_icon, INK, RED)
y = ly + 8
d.text((M, y), LEAD["summary"], font=f_sum, fill=INK)
y += 34
d.line([M, y, W - M, y], fill=INK, width=2)
y += 14

# rows
f_rtag = font(SANS_B, 17)
f_rhead = font(ANTON, 30)
f_rsum = font(SANS, 20)
ROW_H = 88
ICON = 66
tx = M + ICON + 22
text_w = W - M - tx
for row in ROWS:
    ry = y
    row["icon"](d, M, ry + 4, ICON, INK, RED)
    draw_tracked(d, tx, ry, row["tag"], f_rtag, RED, 2)
    # headline: shrink until it fits one line
    size = 30
    while size > 24 and d.textlength(row["headline"], font=font(ANTON, size)) > text_w:
        size -= 1
    d.text((tx, ry + 22), row["headline"], font=font(ANTON, size), fill=INK)
    d.text((tx, ry + 60), row["summary"], font=f_rsum, fill=INK)
    y = ry + ROW_H
    if row is not ROWS[-1]:
        d.line([M, y - 8, W - M, y - 8], fill=(200, 194, 182), width=1)

# footer
f_foot = font(SANS_B, 15)
draw_tracked_center(d, W // 2, H - 34,
                    "SOURCES: REUTERS  ·  CNN  ·  AP  ·  THE TIMES",
                    f_foot, GREY, 2)
d.line([M, H - 52, W - M, H - 52], fill=INK, width=1)

img.save("/home/hatch/workspace/makefun/news-image-20261123/entry.png")
print("saved", img.size)
