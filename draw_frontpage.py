#!/usr/bin/env python3
"""Draw the 20 November 2026 front page for news-image-20261120.

A Pillow-drawn newspaper front page, 1024x1024. Every headline is a real
story reported on 20 November 2026 (or, for events late on 19 Nov UTC,
first reported on 20 November in Asia-Pacific time zones), cross-checked
against BBC / Reuters / NASA / IMD reporting. No network is used here.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (24, 24, 28)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (184, 134, 11)
GREY = (90, 88, 82)
PANEL = (255, 252, 245)
RULE = (200, 192, 175)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph, return y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, width, fill=INK, leading=None):
    return para(draw, x, y, text, fnt, width, fill=fill, leading=leading)


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 15)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 21


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def panel(draw, x, y, w, h, fill=PANEL, outline=RULE):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=fill, outline=outline, width=2)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=INK, width=1)
    for i in range(7):
        draw.rectangle([x, y + i * 2 * h // 13, x + w,
                        y + (i * 2 + 1) * h // 13], fill=(178, 34, 34))
    draw.rectangle([x, y, x + int(w * 0.4), y + 7 * h // 13],
                   fill=(28, 48, 120))
    for r in range(3):
        for c in range(4):
            cx = x + 8 + c * (w * 0.4 - 14) // 3
            cy = y + 6 + r * (7 * h // 13 - 10) // 2
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16),
                   outline=INK, width=1)
    cx, cy = x + w // 5, y + h // 4
    draw.text((cx - 11, cy - 13), "*", font=font(SANS_B, 26),
              fill=(255, 222, 0))
    for dx, dy in [(26, -6), (32, 8), (26, 22), (12, 26)]:
        draw.text((x + dx, y + dy), "*", font=font(SANS_B, 13),
                  fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                       fill=col, outline=INK, width=1)


def draw_summit_scene(draw, x, y, w, h):
    """Three flags over a Shenzhen skyline at dusk."""
    sky = (46, 64, 110)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=sky)
    # stars
    for sx, sy in [(18, 14), (w - 26, 10), (w // 2, 8), (30, 44), (w - 40, 40)]:
        draw.text((x + sx, y + sy), "*", font=font(SANS_B, 12),
                  fill=(255, 235, 160))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 34, 52), (36, 26, 78), (64, 30, 60), (96, 24, 88),
                       (122, 34, 48), (158, 26, 70), (186, 30, 56),
                       (218, 26, 82), (246, 34, 50), (282, 26, 66),
                       (310, 30, 58), (338, 26, 74)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(22, 30, 54))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 5, x + bx + bw - 5, 10):
                draw.rectangle([wx, wy, wx + 4, wy + 5],
                               fill=(255, 214, 120))
    # ground + table
    draw.rectangle([x, base - 26, x + w, base], fill=(58, 44, 34))
    draw.rectangle([x + 60, base - 46, x + w - 60, base - 26],
                   fill=(120, 84, 52))
    # three flags on poles
    fw, fh = 74, 46
    for i, fn in enumerate([flag_us, flag_cn, flag_ru]):
        fx = x + 52 + i * 118
        draw.line([(fx + fw // 2, y + 18), (fx + fw // 2, base - 46)],
                  fill=(220, 220, 220), width=3)
        fn(draw, fx, y + 18, fw, fh)


def draw_court_scene(draw, x, y, w, h):
    bg = (232, 226, 208)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=bg)
    # courthouse: columns + pediment
    cx, cy = x + w // 2, y + 10
    draw.polygon([(cx - 88, cy + 26), (cx + 88, cy + 26), (cx, cy)],
                 fill=(120, 110, 88))
    draw.rectangle([x + 26, cy + 26, x + w - 26, cy + 32], fill=(96, 88, 70))
    for i in range(4):
        px = x + 40 + i * 62
        draw.rectangle([px, cy + 32, px + 16, y + h - 18], fill=(210, 200, 172),
                       outline=(96, 88, 70), width=2)
    draw.rectangle([x + 26, y + h - 18, x + w - 26, y + h - 10],
                   fill=(96, 88, 70))
    # small scales of justice centred between the middle columns
    sx, sy = cx, y + h - 42
    draw.line([(sx, sy - 18), (sx, sy + 10)], fill=INK, width=3)
    draw.line([(sx - 28, sy - 18), (sx + 28, sy - 18)], fill=INK, width=3)
    for s in (-1, 1):
        draw.line([(sx + s * 28, sy - 18), (sx + s * 14, sy - 2)],
                  fill=INK, width=2)
        draw.polygon([(sx + s * 14 - 9, sy - 2), (sx + s * 14 + 9, sy - 2),
                      (sx + s * 14, sy + 8)], fill=GOLD, outline=INK)
    draw.ellipse([sx - 4, sy - 23, sx + 4, sy - 15], fill=GOLD)


def draw_tower_scene(draw, x, y, w, h):
    sky = (214, 196, 168)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=sky)
    # sun haze
    draw.ellipse([x + w - 62, y + 8, x + w - 18, y + 52], fill=(240, 210, 130))
    # PIF tower: straight tapering silhouette with a flat top
    tx = x + w // 2
    pts = [(tx - 46, y + h), (tx - 30, y + 22), (tx - 26, y + 10),
           (tx + 26, y + 10), (tx + 30, y + 22), (tx + 46, y + h)]
    draw.polygon(pts, fill=(52, 66, 92), outline=INK)
    for wy in range(y + 30, y + h - 8, 14):
        t = (wy - y) / h
        half = 26 + t * 18
        draw.line([(tx - half + 5, wy), (tx + half - 5, wy)],
                  fill=(140, 160, 200), width=2)
    # broken windows: a few dark panes on the upper-middle floors
    for bx, by in [(-16, 58), (2, 66), (-8, 80), (10, 88), (-20, 94)]:
        draw.rectangle([tx + bx, y + by, tx + bx + 12, y + by + 9],
                       fill=(18, 18, 22))
    # thin cracks running down from the broken panes
    draw.line([(tx - 10, y + 68), (tx - 18, y + 96)], fill=(18, 18, 22),
              width=2)
    draw.line([(tx + 8, y + 76), (tx + 16, y + 100)], fill=(18, 18, 22),
              width=2)
    # smoke drifting right, clear of the tower
    for i, (sx, sy, r) in enumerate([(tx + 52, y + 52, 8), (tx + 68, y + 44, 10),
                                     (tx + 84, y + 38, 12)]):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 148, 142))
    # street
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 86, 78))


def draw_cyclone_scene(draw, x, y, w, h):
    sea = (36, 88, 130)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=sea)
    # land mass (India east coast, stylised) on the left
    draw.polygon([(x + 8, y + h), (x + 8, y + 24), (x + 62, y + 16),
                  (x + 88, y + 52), (x + 76, y + h)], fill=(196, 164, 110))
    draw.text((x + 12, y + h - 24), "INDIA", font=font(SANS_B, 12),
              fill=(90, 64, 30))
    # small spiral storm over the Bay of Bengal, kept inside the panel
    cx, cy = x + w - 48, y + 56
    for a in range(0, 720, 8):
        ang = math.radians(a)
        r = 4 + (a / 720.0) * 26
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.85
        draw.ellipse([px - 4, py - 4, px + 4, py + 4],
                     fill=(255, 255, 255))
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))
    # rain streaks along the coast
    for rx in range(x + 14, x + 78, 16):
        draw.line([(rx, y + h - 30), (rx - 4, y + h - 16)],
                  fill=(200, 220, 240), width=2)
    # arrow from storm toward the coast
    draw.line([(cx - 34, cy + 22), (x + 92, y + 84)], fill=(255, 220, 80),
              width=3)
    draw.polygon([(x + 92, y + 84), (x + 80, y + 78), (x + 82, y + 92)],
                 fill=(255, 220, 80))
    draw.text((x + 12, y + 8), "BAY OF BENGAL", font=font(SANS_B, 11),
              fill=(220, 235, 245))


def draw_market_scene(draw, x, y, w, h):
    bg = (18, 38, 28)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=bg)
    # grid
    for gy in range(y + 16, y + h - 10, 22):
        draw.line([(x + 10, gy), (x + w - 10, gy)], fill=(40, 70, 52), width=1)
    # rising chart line, kept below the label and above the price lines
    pts = []
    for i in range(9):
        px = x + 16 + i * (w - 32) // 8
        py = y + h - 46 - int((i / 8.0) ** 1.6 * (h - 96)) - (4 if i % 2 else 0)
        pts.append((px, py))
    draw.line(pts, fill=(64, 220, 130), width=4, joint="curve")
    draw.ellipse([pts[-1][0] - 6, pts[-1][1] - 6, pts[-1][0] + 6,
                  pts[-1][1] + 6], fill=(64, 220, 130))
    draw.text((x + 14, y + 8), "ANT  +34%", font=font(SANS_B, 20),
              fill=(64, 220, 130))
    draw.text((x + 12, y + h - 36), "IPO $83", font=font(SANS_B, 12),
              fill=(190, 220, 200))
    draw.text((x + 12, y + h - 20), "OPEN $111.50", font=font(SANS_B, 12),
              fill=(190, 220, 200))


def draw_space_scene(draw, x, y, w, h):
    bg = (10, 12, 34)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=bg)
    for sx, sy, r in [(14, 12, 2), (48, 30, 1), (96, 10, 2), (128, 24, 1),
                      (20, 56, 1), (120, 58, 2), (70, 8, 1), (100, 48, 1)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                     fill=(255, 255, 255))
    # Voyager: bus + dish + boom, all inside the 150 px scene
    cx, cy = x + 52, y + h // 2 + 2
    draw.polygon([(cx - 26, cy - 13), (cx + 4, cy - 13), (cx + 4, cy + 13),
                  (cx - 26, cy + 13)], fill=(200, 200, 210), outline=INK)
    draw.arc([cx + 4, cy - 26, cx + 46, cy + 26], -80, 80,
             fill=(230, 230, 240), width=4)
    draw.line([(cx + 4, cy), (cx + 25, cy)], fill=(230, 230, 240), width=3)
    draw.line([(cx - 26, cy), (cx - 44, cy - 10)], fill=(180, 180, 190),
              width=3)
    draw.ellipse([cx - 48, cy - 14, cx - 40, cy - 6], fill=GOLD)
    # signal rings travelling home (short, inside the scene)
    for r in (12, 20):
        draw.arc([cx + 58 - r, cy - r, cx + 58 + r, cy + r], -55, 55,
                 fill=(120, 200, 255), width=2)
    # Earth, small and far away
    ex, ey = x + w - 18, y + h // 2 + 2
    draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(40, 110, 220))
    draw.arc([ex - 10, ey - 10, ex + 10, ey + 10], 200, 320,
             fill=(120, 200, 120), width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- masthead ----
    d.text((512, 26), "THE WORLD TODAY", font=font(SERIF_B, 64),
           fill=INK, anchor="ma")
    rule(d, 34, 108, 956, color=RED, width=4)
    d.text((34, 120), "FRIDAY 20 NOVEMBER 2026", font=font(SANS_B, 30),
           fill=RED)
    d.text((990, 120), "ONE DAY  •  ONE PAGE", font=font(SANS_B, 17),
           fill=GREY, anchor="ra")
    d.text((990, 146), "THE WORLD'S NEWS", font=font(SANS_B, 17),
           fill=GREY, anchor="ra")
    rule(d, 34, 168, 956, color=INK, width=2)

    # ---- lead story: summit ----
    ly, lh = 182, 268
    panel(d, 30, ly, 964, lh)
    draw_summit_scene(d, 46, ly + 12, 380, 150)
    d.text((46, ly + 168), "SHENZHEN, CHINA  •  APEC SUMMIT",
           font=font(SANS_B, 13), fill=GREY)
    kicker(d, 442, ly + 12, "Lead story — diplomacy")
    y = headline(d, 442, ly + 36,
                 "TRUMP, XI AND PUTIN MEET — AND DECLARE PEACE",
                 font(SERIF_B, 34), 536, leading=38)
    y = para(d, 442, y + 6,
             "The first-ever three-way summit of the US, Chinese and "
             "Russian leaders ends with a joint declaration: nuclear war "
             "\u201ccannot be won and must never be fought\u201d.",
             font(SERIF, 18), 536)
    y = para(d, 442, y + 4,
             "No mention of Ukraine or Iran. No limits on arsenals. "
             "Talks on nuclear risk promised — with no date set.",
             font(SANS, 15), 536, fill=GREY)

    # ---- row 2: ICJ + Riyadh ----
    ry, rh = 466, 236
    # ICJ
    panel(d, 30, ry, 472, rh)
    draw_court_scene(d, 46, ry + 12, 440, 104)
    kicker(d, 46, ry + 124, "The Hague — justice")
    headline(d, 46, ry + 146, "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
             font(SERIF_B, 24), 440, leading=27)
    para(d, 46, ry + 200,
         "First time a state is held responsible for genocide: the 2017 "
         "crackdown on the Rohingya.",
         font(SANS, 14), 440)
    # Riyadh
    panel(d, 522, ry, 472, rh)
    draw_tower_scene(d, 538, ry + 12, 440, 104)
    kicker(d, 538, ry + 124, "Riyadh — Middle East")
    headline(d, 538, ry + 146, "MISSILE HITS RIYADH'S TALLEST TOWER",
             font(SERIF_B, 24), 440, leading=27)
    para(d, 538, ry + 200,
         "Houthi strike blows out windows on 7–8 floors of the PIF Tower. "
         "No injuries reported.",
         font(SANS, 14), 440)

    # ---- row 3: cyclone + markets (body placed below the headline) ----
    cy, ch = 718, 150
    panel(d, 30, cy, 472, ch)
    draw_cyclone_scene(d, 46, cy + 10, 150, 118)
    kicker(d, 210, cy + 10, "India — weather")
    y = headline(d, 210, cy + 32, "CYCLONE AKVAN BEARS DOWN ON ODISHA",
                 font(SERIF_B, 20), 276, leading=23)
    para(d, 210, y + 4,
         "Landfall due about noon today near Gopalpur. Tens of thousands "
         "moved to shelters; winds to 110 km/h.",
         font(SANS, 13), 276)
    panel(d, 522, cy, 472, ch)
    draw_market_scene(d, 538, cy + 10, 150, 118)
    kicker(d, 704, cy + 10, "Markets — AI")
    y = headline(d, 704, cy + 32, "ANTHROPIC SOARS ON STOCK MARKET DEBUT",
                 font(SERIF_B, 20), 274, leading=23)
    para(d, 704, y + 4,
         "Shares open at $111.50, up 34% on the $83 IPO price, in the "
         "biggest listing on record.",
         font(SANS, 13), 274)

    # ---- bottom: Voyager + briefs ----
    by, bh = 884, 108
    panel(d, 30, by, 472, bh)
    draw_space_scene(d, 46, by + 10, 150, 88)
    kicker(d, 210, by + 10, "Space — science")
    y = headline(d, 210, by + 32, "VOYAGER 1: ONE LIGHT-DAY FROM HOME",
                 font(SERIF_B, 19), 276, leading=22)
    para(d, 210, y + 4,
         "First craft ever 16 billion miles out. Its signal took a day "
         "to reach Earth.",
         font(SANS, 13), 276)
    # briefs column
    panel(d, 522, by, 472, bh)
    d.text((538, by + 10), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    y = by + 32
    for item in [
        "GTA VI: about $1.84bn in launch sales — past The Odyssey's box office.",
        "Europe ready for talks with Russia on ending the war in Ukraine.",
        "US Senate rejects an Iran war-powers curb, 51–48.",
    ]:
        d.text((538, y), "•", font=font(SANS_B, 14), fill=RED)
        y = para(d, 554, y, item, font(SANS, 13), 424, leading=16)
        y += 2

    d.text((512, 1002), "Sources: BBC • Reuters • NASA • India Meteorological Department  •  All events reported 20 November 2026",
           font=font(SANS, 12), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, "PNG", optimize=True)
    print("wrote", out)
