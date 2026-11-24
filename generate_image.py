#!/usr/bin/env python3
"""Generate entry.png for news-image-20261124.
Draws a clean newspaper front page with PIL. Deterministic: no network,
no randomness, no timestamps in the image.
News verified 2026-11-24 via Reuters / AP / BBC / Just Security / OneTurn.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
BG = (247, 243, 234)
NAVY = (15, 42, 68)
WHITE = (255, 255, 255)
DARK = (20, 28, 38)
GREY = (70, 80, 92)
LIGHT = (210, 220, 230)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

F_TITLE = font("DejaVuSans-Bold.ttf", 52)
F_KICKER = font("DejaVuSans-Bold.ttf", 26)
F_SUB = font("DejaVuSans.ttf", 24)
F_CAT = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 18)

def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
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

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 168], fill=NAVY)
d.text((40, 26), "THE WORLD IN ONE IMAGE", font=F_KICKER, fill=(255, 205, 80))
d.text((40, 62), "TUESDAY 24 NOVEMBER 2026", font=F_TITLE, fill=WHITE)
d.text((40, 126), "Six stories that defined the day - from markets to war at sea", font=F_SUB, fill=LIGHT)

panels = [
    ("MARKETS  ·  TECH", (11, 94, 143), "Nvidia brings back\nJensen Huang",
     "Board reinstates founder as CEO on Monday, 11 days after he resigned. Shares rise 31%; S&P 500 up 4.7%."),
    ("WAR AT SEA  ·  LIBYA", (0, 122, 122), "Ukraine says it sank\na Russian warship",
     "Kyiv says seven naval drones sank the corvette Merkury at Benghazi. UN calls for an independent probe."),
    ("NATO  ·  POLAND", (168, 44, 44), "Russian drone breaches\nPolish airspace",
     "Warsaw calls it intentional. NATO will deploy an AWACS early-warning aircraft to Poland."),
    ("UKRAINE", (146, 90, 20), "Russian strike hits\nZaporizhzhia",
     "Overnight attack kills 2 and wounds 40, including four children, officials say."),
    ("MIDDLE EAST  ·  GAZA", (96, 48, 130), "Israeli strikes kill\nHamas security chief",
     "Naeem Abu Nahel and six others killed in Gaza, medics and police say."),
    ("ENERGY  ·  ASIA", (18, 110, 70), "Tankers hit mines;\nfactory fire kills 26",
     "Iran says three tankers hit mines in the Strait of Hormuz. A factory fire in Indonesia kills 26."),
]

x0, y0 = 32, 192
pw, ph = 464, 238
gapx, gapy = 32, 24
for i, (cat, color, head, body) in enumerate(panels):
    x = x0 + (i % 2) * (pw + gapx)
    y = y0 + (i // 2) * (ph + gapy)
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=14, fill=WHITE, outline=(200, 192, 175), width=2)
    d.rectangle([x, y, x + pw, y + 10], fill=color)
    d.text((x + 20, y + 22), cat, font=F_CAT, fill=color)
    # headline, two lines as given
    hy = y + 54
    for line in head.split("\n"):
        d.text((x + 20, hy), line, font=F_HEAD, fill=DARK)
        hy += 36
    # body wrapped
    lines = wrap(d, body, F_BODY, pw - 40)
    by = hy + 8
    for line in lines[:3]:
        d.text((x + 20, by), line, font=F_BODY, fill=GREY)
        by += 28

d.text((W//2, 972), "24 November 2026  ·  Reported by Reuters, AP, BBC and others", font=F_FOOT, fill=GREY, anchor="mm")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), img.size)
