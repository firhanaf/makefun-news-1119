# SPDX-License-Identifier: MIT
"""Render entry.png: a one-page summary of the world's news on Thursday 19 November 2026.

Needs Pillow and the Windows Georgia/Arial fonts. Run: python render.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = "C:/Windows/Fonts/"
PAPER = (247, 242, 230)
INK = (28, 28, 30)
GREY = (95, 95, 100)
RED = (178, 34, 34)
BLUE = (36, 70, 128)
GOLD = (196, 150, 40)
SKY = (214, 226, 238)


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, name, size, width, max_lines, min_size=12):
    """Largest font size (<= size) at which text wraps into max_lines within width."""
    while size > min_size:
        f = font(name, size)
        lines = wrap(d, text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font(name, min_size)
    return f, wrap(d, text, f, width)


def text_block(d, x, y, text, name, size, width, max_lines, fill, gap=1.18):
    f, lines = fit(d, text, name, size, width, max_lines)
    lh = int(f.size * gap)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


# ---------- icons (each drawn inside box x, y, w, h) ----------

def icon_scales(d, x, y, w, h):
    cx = x + w // 2
    d.rectangle([cx - 4, y + 18, cx + 4, y + h - 22], fill=GOLD)
    d.rectangle([cx - 40, y + h - 22, cx + 40, y + h - 10], fill=GOLD)
    d.line([cx - 80, y + 30, cx + 80, y + 30], fill=GOLD, width=7)
    d.ellipse([cx - 10, y + 6, cx + 10, y + 26], fill=GOLD)
    for side in (-1, 1):
        px = cx + side * 80
        d.line([px, y + 30, px - 34, y + 100], fill=GOLD, width=3)
        d.line([px, y + 30, px + 34, y + 100], fill=GOLD, width=3)
        d.chord([px - 42, y + 80, px + 42, y + 124], 0, 180, fill=GOLD)
    d.text((cx, y + h + 4), "ICJ · THE HAGUE", font=font("arialbd.ttf", 15), fill=GREY, anchor="mt")


def icon_summit(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 + 6
    d.ellipse([cx - 46, cy - 22, cx + 46, cy + 22], fill=(150, 110, 70))
    labels = [("US", BLUE, -80), ("CN", RED, 0), ("RU", (60, 60, 140), 80)]
    for lab, col, dx in labels:
        hx = cx + dx
        hy = cy - 42 if dx == 0 else cy - 14
        d.ellipse([hx - 17, hy - 17, hx + 17, hy + 17], fill=col)
        d.text((hx, hy), lab, font=font("arialbd.ttf", 13), fill="white", anchor="mm")


def icon_bridge(d, x, y, w, h):
    base = y + h - 14
    d.rectangle([x + 10, base, x + w - 10, y + h], fill=(80, 130, 175))
    d.rectangle([x + 10, base - 30, x + w - 10, base - 22], fill=INK)
    for i in range(6):
        px = x + 25 + i * (w - 50) // 5
        d.rectangle([px - 3, base - 22, px + 3, base], fill=INK)
    for i in range(1, 5):
        cx0 = x + 10 + i * (w - 20) // 5
        d.arc([cx0 - 34, base - 60, cx0 + 34, base - 4], 180, 360, fill=INK, width=3)
    bx, by = x + w // 2 + 6, base - 34
    pts = []
    for k in range(16):
        r = 28 if k % 2 == 0 else 12
        a = k * math.pi / 8
        pts.append((bx + r * math.cos(a), by + r * math.sin(a)))
    d.polygon(pts, fill=(240, 140, 30))


def icon_tower(d, x, y, w, h):
    cx = x + w // 2
    d.polygon([(cx - 22, y + h), (cx - 14, y + 8), (cx + 14, y + 8), (cx + 22, y + h)], fill=(70, 90, 110))
    for i in range(7):
        yy = y + 18 + i * 11
        d.line([cx - 12, yy, cx + 12, yy], fill=SKY, width=2)
    d.rectangle([cx - 70, y + 50, cx - 36, y + h], fill=(110, 125, 140))
    d.rectangle([cx + 36, y + 40, cx + 62, y + h], fill=(110, 125, 140))
    # missile coming in from the upper left
    d.line([x + 8, y + 4, cx - 30, y + 30], fill=GREY, width=3)
    d.polygon([(cx - 36, y + 24), (cx - 20, y + 36), (cx - 26, y + 22)], fill=RED)
    d.ellipse([cx + 4, y + 18, cx + 24, y + 38], fill=(240, 140, 30))


def icon_chair(d, x, y, w, h):
    cx = x + w // 2
    d.rectangle([cx - 30, y + 6, cx + 30, y + 56], outline=INK, width=4, fill=(120, 40, 40))
    d.rectangle([cx - 36, y + 56, cx + 36, y + 66], fill=INK)
    d.line([cx - 32, y + 66, cx - 32, y + h], fill=INK, width=5)
    d.line([cx + 32, y + 66, cx + 32, y + h], fill=INK, width=5)
    d.text((cx + 60, y + 34), "MN", font=font("arialbd.ttf", 18), fill=RED, anchor="mm")


def icon_envoy(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 60, cy - 24, cx - 6, cy + 24], fill=(65, 137, 221))
    star = [(cx - 33 + 12 * math.cos(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.4),
             cy + 12 * math.sin(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else 0.4)) for k in range(10)]
    d.polygon(star, fill="white")
    d.line([cx + 4, cy, cx + 58, cy], fill=RED, width=6)
    d.polygon([(cx + 58, cy - 12), (cx + 76, cy), (cx + 58, cy + 12)], fill=RED)
    d.text((cx + 40, cy + 24), "UAE", font=font("arialbd.ttf", 14), fill=GREY, anchor="mt")


def icon_ballot(d, x, y, w, h):
    cx = x + w // 2
    d.rectangle([cx - 44, y + 34, cx + 44, y + h], fill=(60, 60, 140), outline=INK, width=2)
    d.rectangle([cx - 24, y + 40, cx + 24, y + 46], fill=INK)
    d.rectangle([cx - 18, y + 4, cx + 18, y + 42], fill="white", outline=INK, width=2)
    d.line([cx - 9, y + 22, cx - 2, y + 30, cx + 10, y + 12], fill=RED, width=4)
    d.text((cx, y + h - 22), "RS", font=font("arialbd.ttf", 14), fill="white", anchor="mm")


STORIES = [
    ("ASIA-PACIFIC", icon_summit, "Trump, Xi and Putin hold first three-way talks at APEC",
     "Shenzhen meeting ends in a joint declaration on nuclear war, oil output and UN reform."),
    ("EUROPE", icon_bridge, "Ukraine hits Kerch Strait bridge for third time this week",
     "Rail traffic halted. Russian strikes on Kyiv kill one and damage the Austrian and Dutch embassies."),
    ("MIDDLE EAST", icon_tower, "Houthi missiles strike Riyadh's financial district",
     "Public Investment Fund tower and other buildings damaged; Saudi officials report no injuries."),
    ("ASIA", icon_chair, "Mongolia's president Khürelsükh resigns",
     "Parliament accepts resignation amid accusations over a 2019 rail project; vote due within four months."),
    ("AFRICA", icon_envoy, "Somalia expels the UAE's ambassador",
     "Mogadishu accuses Abu Dhabi of violating its sovereignty and recalls its own envoy."),
    ("EUROPE", icon_ballot, "Serbia: student movement's speaker becomes interim president",
     "Aleksandar Čupić must organise a presidential election before the end of the year."),
]

BRIEFS = [
    "Tanker catches fire after hitting a mine near the Strait of Hormuz",
    "About 6,000 displaced as Israeli raid on Gaza's Nuseirat camp ends",
    "Philippines and Chile sign a free trade pact at APEC",
    "Bukele files to run for a third term in El Salvador",
    "Colombia: unions hold a second national strike",
]


def render(path="entry.png"):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # masthead
    d.rectangle([0, 0, W, 8], fill=RED)
    d.text((W // 2, 22), "THE WORLD IN ONE PAGE", font=font("georgiab.ttf", 50), fill=INK, anchor="mt")
    d.line([32, 84, W - 32, 84], fill=INK, width=2)
    d.text((W // 2, 92), "THURSDAY 19 NOVEMBER 2026", font=font("arialbd.ttf", 30), fill=RED, anchor="mt")
    d.line([32, 132, W - 32, 132], fill=INK, width=2)

    # lead story
    icon_scales(d, 40, 150, 220, 140)
    lx = 290
    d.text((lx, 150), "LEAD · ASIA / INTERNATIONAL LAW", font=font("arialbd.ttf", 16), fill=RED)
    y = text_block(d, lx, 174, "UN's top court rules Myanmar committed genocide against the Rohingya",
                   "georgiab.ttf", 36, W - lx - 36, 2, INK, 1.12)
    y = text_block(d, lx, y + 6,
                   "First time the ICJ has found a state responsible for genocide. The case, brought by The Gambia "
                   "in 2019, covered the army's 2017 campaign that drove some 700,000 Rohingya into Bangladesh.",
                   "arial.ttf", 18, W - lx - 36, 3, GREY)
    lead_end = max(y, 310) + 10
    d.line([32, lead_end, W - 32, lead_end], fill=INK, width=1)

    # 2 x 3 grid of stories
    top, cols, rows = lead_end + 10, 3, 2
    cw, ch = (W - 64) // cols, 252
    for i, (tag, icon, head, sub) in enumerate(STORIES):
        c, r = i % cols, i // cols
        x0, y0 = 32 + c * cw, top + r * ch
        if c:
            d.line([x0, y0 + 6, x0, y0 + ch - 10], fill=(190, 185, 170), width=1)
        icon(d, x0 + 14, y0 + 8, cw - 28, 84)
        d.text((x0 + 14, y0 + 104), tag, font=font("arialbd.ttf", 14), fill=RED)
        yy = text_block(d, x0 + 14, y0 + 122, head, "georgiab.ttf", 23, cw - 28, 3, INK, 1.1)
        text_block(d, x0 + 14, yy + 4, sub, "arial.ttf", 15, cw - 28, 4, GREY, 1.2)

    # briefs
    by = top + rows * ch + 2
    d.rectangle([32, by, W - 32, by + 30], fill=INK)
    d.text((44, by + 15), "ALSO ON 19 NOVEMBER", font=font("arialbd.ttf", 16), fill=PAPER, anchor="lm")
    # briefs flow down two columns, each line shrunk to fit its column
    colw = (W - 88) // 2
    for i, b in enumerate(BRIEFS):
        col, row = (0, i) if i < 3 else (1, i - 3)
        bx, yy = 44 + col * (colw + 12), by + 40 + row * 24
        f, _ = fit(d, "■ " + b, "arial.ttf", 16, colw, 1)
        d.text((bx, yy), "■ " + b, font=f, fill=INK)
    d.text((W // 2, H - 22), "Events that happened or were first reported on 19 Nov 2026 · "
           "compiled from Reuters, Al Jazeera and wire reports", font=font("ariali.ttf", 13), fill=GREY, anchor="mb")

    d.rectangle([0, H - 8, W, H], fill=RED)
    im.save(path, optimize=True)
    return im


if __name__ == "__main__":
    render()
    print("wrote entry.png")
