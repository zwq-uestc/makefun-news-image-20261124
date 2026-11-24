#!/usr/bin/env python3
"""Generate entry.png v2 for news-image-20261124.

Commercial editorial infographic, drawn in code with PIL. Deterministic:
no network, no randomness, no timestamps in the image.

Design: Noto Serif headlines + Noto Sans labels on warm paper, one dark
hero panel for the lead story (Nvidia) with a data chart, then five
number-led story cards. Type is kept large so the image still reads at
~300 px wide: headlines 24-46 pt, body 18-20 pt, nothing below 15 pt.

News verified 2026-11-24 via Reuters / AP / BBC / Just Security / OneTurn.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 244, 238)
INK = (17, 24, 33)
MUTED = (84, 90, 100)
NAVY = (13, 38, 62)
NAVY2 = (19, 55, 88)
GOLD = (212, 164, 65)
RED = (178, 42, 38)
RULE = (196, 188, 172)
CARD = (255, 255, 255)

NOTO = "/usr/share/fonts/truetype/noto"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

def font(path, size):
    return ImageFont.truetype(path, size)

def serif_b(size):
    try:
        return font(f"{NOTO}/NotoSerif-Bold.ttf", size)
    except OSError:
        return font(f"{DEJAVU}/DejaVuSerif-Bold.ttf", size)

def serif(size):
    try:
        return font(f"{NOTO}/NotoSerif-Regular.ttf", size)
    except OSError:
        return font(f"{DEJAVU}/DejaVuSerif.ttf", size)

def sans_b(size):
    try:
        return font(f"{NOTO}/NotoSans-Bold.ttf", size)
    except OSError:
        return font(f"{DEJAVU}/DejaVuSans-Bold.ttf", size)

def sans(size):
    try:
        return font(f"{NOTO}/NotoSans-Regular.ttf", size)
    except OSError:
        return font(f"{DEJAVU}/DejaVuSans.ttf", size)

F_DATE = sans_b(20)
F_TITLE = serif_b(58)
F_SUB = serif(21)
F_KICKER = sans_b(17)
F_HERO_HEAD = serif_b(40)
F_HERO_BODY = sans(20)
F_BIG = sans_b(84)
F_CHART_LAB = sans_b(16)
F_CHART_VAL = sans_b(20)
F_CAT = sans_b(16)
F_HEAD = serif_b(25)
F_BODY = sans(18)
F_STAT = sans_b(34)
F_STAT_LAB = sans_b(14)
F_FOOT = sans(15)

def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, lines, f, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 48  # margin

# ---- Masthead ----
d.text((M, 26), "TUESDAY", font=F_DATE, fill=RED)
date = "24 NOVEMBER 2026"
d.text((W - M, 26), date, font=F_DATE, fill=INK, anchor="ra")
d.line([(M, 58), (W - M, 58)], fill=INK, width=2)
d.text((M, 70), "The World, 24 November", font=F_TITLE, fill=INK)
d.text((M, 138), "Six stories, one day — a chipmaker's comeback, a warship sunk,",
       font=F_SUB, fill=MUTED)
d.text((M, 164), "and a drone over Poland.",
       font=F_SUB, fill=MUTED)
d.line([(M, 198), (W - M, 198)], fill=RULE, width=1)

# ---- Hero: Nvidia (dark panel) ----
hx0, hy0, hx1, hy1 = M, 214, W - M, 492
d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=10, fill=NAVY)
d.text((hx0 + 28, hy0 + 22), "MARKETS  ·  THE LEAD STORY", font=F_KICKER, fill=GOLD)
d.text((hx0 + 28, hy0 + 52), "Nvidia brings back", font=F_HERO_HEAD, fill=(255, 255, 255))
d.text((hx0 + 28, hy0 + 100), "Jensen Huang", font=F_HERO_HEAD, fill=(255, 255, 255))
hero_body = ("The board reinstates the founder as chief executive on Monday, "
             "11 days after he resigned, after US input found no national "
             "security risk.")
text_block(d, hx0 + 28, hy0 + 158, wrap(d, hero_body, F_HERO_BODY, 560),
           F_HERO_BODY, (205, 216, 228), 27)

# Chart, right side of hero: NVDA +31% vs S&P 500 +4.7%
cx = hx1 - 300
d.text((cx, hy0 + 22), "SHARES, MONDAY", font=F_KICKER, fill=(150, 170, 190))
d.text((cx, hy0 + 52), "+31%", font=F_BIG, fill=GOLD)
d.text((cx, hy0 + 148), "NVIDIA, MONDAY", font=F_CHART_LAB, fill=(255, 255, 255))
d.rectangle([cx, hy0 + 172, cx + 260, hy0 + 188], fill=GOLD)
d.text((cx, hy0 + 196), "S&P 500  +4.7%", font=F_CHART_VAL, fill=(205, 216, 228))
d.rectangle([cx, hy0 + 224, cx + 40, hy0 + 240], fill=(120, 140, 160))

# ---- Story cards ----
# Stat sits top-right on the same row as the category; the headline starts
# below that row, full width, so narrow cards do not squeeze it.
def card(x0, y0, x1, y1, color, cat, stat, stat_lab, head, body,
         head_f=None, body_f=None):
    head_f = head_f or F_HEAD
    body_f = body_f or F_BODY
    head_lead = 30 if head_f is F_HEAD else 27
    body_lead = 24 if body_f is F_BODY else 21
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                        outline=(214, 207, 192), width=1)
    d.rectangle([x0 + 14, y0, x1 - 14, y0 + 5], fill=color)
    d.text((x0 + 20, y0 + 18), cat, font=F_CAT, fill=color)
    d.text((x1 - 20, y0 + 14), stat, font=F_STAT, fill=INK, anchor="ra")
    d.text((x1 - 20, y0 + 52), stat_lab, font=F_STAT_LAB, fill=MUTED, anchor="ra")
    y = text_block(d, x0 + 20, y0 + 78, wrap(d, head, head_f, x1 - x0 - 40),
                   head_f, INK, head_lead)
    # Keep the body inside the card: at most two lines.
    lines = wrap(d, body, body_f, x1 - x0 - 40)[:2]
    text_block(d, x0 + 20, y + 4, lines, body_f, MUTED, body_lead)

# Row A: two wide cards
card(M, 512, 500, 716, (0, 110, 110), "WAR AT SEA  ·  LIBYA", "7", "NAVAL DRONES",
     "Ukraine says it sank a Russian warship",
     "Kyiv says drones sank the corvette Merkury at Benghazi; the UN wants a probe.")
card(524, 512, W - M, 716, RED, "NATO  ·  POLAND", "1", "DRONE",
     "Russian drone breaches Polish airspace",
     "Warsaw calls it intentional. NATO will send an AWACS aircraft to Poland.")

# Row B: three cards, smaller type, shorter copy
F_HEAD_S = serif_b(22)
F_BODY_S = sans(16)
card(M, 736, 340, 940, (146, 90, 20), "UKRAINE", "40", "WOUNDED",
     "Strike hits Zaporizhzhia",
     "Overnight attack kills 2, wounds 40 — four are children.",
     head_f=F_HEAD_S, body_f=F_BODY_S)
card(356, 736, 668, 940, (96, 48, 130), "MIDDLE EAST  ·  GAZA", "7", "KILLED",
     "Strikes kill Hamas security chief",
     "Naeem Abu Nahel and six others killed in Gaza, medics say.",
     head_f=F_HEAD_S, body_f=F_BODY_S)
card(684, 736, W - M, 940, (18, 110, 70), "ENERGY  ·  ASIA", "3", "TANKERS",
     "Tankers hit mines; fire kills 26",
     "Iran says three tankers hit mines; a fire in Indonesia kills 26.",
     head_f=F_HEAD_S, body_f=F_BODY_S)

# ---- Footer ----
d.line([(M, 962), (W - M, 962)], fill=RULE, width=1)
d.text((M, 974), "Reported by Reuters, AP, BBC and others", font=F_FOOT, fill=MUTED)
d.text((W - M, 974), "24 NOVEMBER 2026  ·  6 STORIES", font=F_FOOT, fill=MUTED, anchor="ra")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), img.size)
