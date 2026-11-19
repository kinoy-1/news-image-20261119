#!/usr/bin/env python3
"""THE GLOBAL LEDGER -- Thursday 19 November 2026, one page, 35 stories.

Draws a dense newspaper front page with Pillow only. No network, no
timestamps, no unseeded randomness: two runs write byte-identical PNGs.
Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
OUT_NAME = "entry.png"

# --- palette: ink-black masthead, warm newsprint, deep teal + brick red ---
PAPER = (247, 243, 232)
INK = (18, 18, 18)
TEAL = (13, 84, 84)
TEAL_DK = (8, 58, 58)
RED = (178, 34, 28)
GOLD = (198, 138, 28)
GREY = (96, 92, 84)
LINE = (180, 172, 156)
MAP_DOT = (13, 84, 84)
MAP_SEA = (214, 228, 226)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y just below last line."""
    lh = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def num_badge(draw, x, y, n, r=9, fill=RED, fg=(255, 255, 255)):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    t = str(n)
    f = SANS_B(11 if len(t) < 2 else 10)
    tw = draw.textlength(t, font=f)
    draw.text((x - tw / 2, y - f.size / 2 - 1), t, font=f, fill=fg)


# ---------------------------------------------------------------- stories
# 35 verified stories for Thursday 19 November 2026. Each: (number, kicker,
# headline, body). Features 1-3 get big illustrations; 4-21 the story grid;
# 22-35 the "ALSO ON THURSDAY" list.
FEATURES = [
    (1, "MIDDLE EAST",
     "US and Iran exchange fire again as Tehran widens attacks on Gulf states",
     "Washington hit a missile site on Qeshm Island after Iran struck a US "
     "radar site in Bahrain. Iran then hit a US base in Kuwait and ships in "
     "Hormuz."),
    (2, "GAMING",
     "Gamers enter Vice City as Grand Theft Auto VI begins its global rollout",
     "After a 13-year wait, GTA VI launched at midnight in Australia and is "
     "rolling out worldwide. Critics gave it 99 on Metacritic."),
    (3, "UNITED STATES",
     "Jeffries set to become first African-American Speaker of the House",
     "Democrats nominated Hakeem Jeffries, set to become the first "
     "African-American Speaker. Democrats also won in Alaska, securing a "
     "56-44 Senate majority."),
]

GRID = [
    (4, "EUROPE", "EU proposes \u20ac45bn Ukraine loan",
     "Brussels proposes a \u20ac45bn loan to Kyiv, repaid once Russia pays "
     "reparations. Ukraine's 2026 deficit: ~\u20ac70bn."),
    (5, "TECH", "Nvidia chief Huang resigns",
     "Founder Jensen Huang stepped down. Acting chief Colette Kress promises "
     "earlier pay rises and more stock grants."),
    (6, "SPACE", "Voyager 1 reaches one light-day",
     "NASA believes Voyager 1 has reached a one-light-day milestone after "
     "almost 50 years in space. Confirmation today."),
    (7, "UKRAINE WAR", "France confirms troops in Ukraine",
     "Paris confirms it is sending soldiers to Ukraine; Russia's Lavrov "
     "accuses France of directly joining the conflict."),
    (8, "GAZA", "Israeli forces move into central Gaza",
     "Israeli ground forces entered central Gaza in the first ground "
     "operation since the ceasefire began, after evacuation orders."),
    (9, "LAW", "World court rules on Rohingya case",
     "The International Court of Justice delivers its ruling today in The "
     "Gambia v. Myanmar, over the Rohingya."),
    (10, "RELIGION", "Islam set to be largest faith by 2035",
     "Pew projects Islam will become the world's largest religion by 2035, "
     "outnumbering Christians for the first time."),
    (11, "CLIMATE", "Cyclone Akvan bears down on India",
     "Cyclone Akvan is likely to cross India's east coast between "
     "Machilipatnam and Puri. India urges climate justice at COP31."),
    (12, "DIPLOMACY", "Trump, Xi and Putin to meet in Shenzhen",
     "The three leaders will hold trilateral talks at the APEC summit, with "
     "a Trump-Putin one-on-one on Thursday."),
    (13, "MARKETS", "Fed minutes point to more rate rises",
     "Most Fed officials expect further rate hikes if inflation and the "
     "labour market develop as expected. Oil prices fell."),
    (14, "CYBER", "Senators: AI cyber threats outpace defences",
     "US senators warn the White House that AI-enabled cyber threats are "
     "outpacing defences. Palo Alto Networks stock soared."),
    (15, "EUROPE", "M\u00e9lenchon could win, minister says",
     "France's justice minister says hard-left leader M\u00e9lenchon could win "
     "the presidency."),
    (16, "AFRICA", "Somalia accuses UAE of secret bases",
     "Somalia accuses the UAE of secretly building military bases on its "
     "territory without federal approval. Australia sanctioned Israeli "
     "settlers over West Bank expansion."),
    (17, "ASIA", "India and Japan review defence ties",
     "India and Japan hold a 2+2 ministerial defence dialogue in Tokyo. PM "
     "Modi meets the Prince and Princess of Wales; Liu Yunping was elected "
     "House Democratic Caucus chair."),
    (18, "SCIENCE", "Earth is missing a billion years",
     "Scientists may have discovered why Earth is missing over a billion "
     "years of geological history. Merck begins US distribution of a "
     "self-amplifying mRNA rabies vaccine for dogs and cats."),
    (19, "SPORT", "Duckett's 133 puts England on top",
     "Ben Duckett scored 133 as England took a strong position in the 3rd "
     "ODI against Australia. In Tests, Gill's India look to end a 17-year "
     "drought against New Zealand."),
    (20, "AMERICAS", "Hegseth visits Venezuela after Maduro seizure",
     "The US defence secretary made his first Venezuela visit since Maduro's "
     "seizure, hailing the capture as Latin America's most sophisticated "
     "military operation. The US and Venezuela will expand military "
     "cooperation against drug trafficking."),
    (21, "FINANCE", "Deutsche Bank and $582m of Epstein money",
     "Deutsche Bank handled $582 million in transactions linked to Jeffrey "
     "Epstein between 2013 and 2018, an FT expos\u00e9 found. Canada is "
     "adjusting its China ties, Carney says."),
]

ALSO = [
    (22, "Ukrainian drones and missiles badly damage the bridge to Crimea."),
    (23, "Russia plans 20,000,000 drones at Ukraine in 2027, EU defence chief says."),
    (24, "Gaza reconstruction stalled, Peace Council warns, as ceasefire strains."),
    (25, "India's installed renewable capacity hits 299.25 GW at COP31."),
    (26, "Goldman Sachs upgrades India to overweight; Nifty target 28,500 by Dec 2027."),
    (27, "Palo Alto Networks soars as earnings show AI raising cybersecurity stakes."),
    (28, "Microsoft reportedly in talks to sell AI services to ByteDance."),
    (29, "NSA's highly classified internal network suffered an outage, CNN reports."),
    (30, "European Commission accused of sugarcoating \u20ac2.5bn Egypt aid figures."),
    (31, "Iraq sentences six French nationals to life over joining ISIL."),
    (32, "Cocaine and millions of pills seized in eastern Libya."),
    (33, "Saudi Arabia says danger has passed in three southern cities after alerts."),
    (34, "Curry sidelined about a month with an abdominal injury, knee problems behind him."),
    (35, "Mbapp\u00e9 sends a message to a 21-year-old Real Madrid star after a new deal."),
]

NUMBERS = [
    ("\u20ac45bn", "EU loan for Ukraine"),
    ("99", "GTA VI on Metacritic"),
    ("56\u201344", "US Senate majority"),
    ("20,000,000", "Russian drones, 2027"),
    ("1 light-day", "Voyager 1 milestone"),
    ("133", "Duckett's runs, 3rd ODI"),
    ("299.25 GW", "India renewables"),
    ("$582m", "Epstein-linked bank flows"),
]

# Dot-matrix world map, generated deterministically from land ranges.
# Fine grid: 60 cols (lon -180..180, 6 deg each) x 26 rows (lat 75..-55).
# Each entry: row -> list of (col_start, col_end) land spans, inclusive.
_LAND = {
    0: [(5, 15), (21, 24), (34, 57)],
    1: [(4, 16), (20, 25), (30, 58)],
    2: [(4, 17), (20, 24), (29, 58)],
    3: [(4, 16), (29, 33), (37, 57)],
    4: [(5, 15), (29, 33), (36, 56)],
    5: [(6, 14), (29, 33), (36, 55)],
    6: [(7, 13), (29, 32), (36, 54)],
    7: [(8, 12), (29, 31), (42, 52)],
    8: [(9, 12), (30, 35), (43, 50)],
    9: [(10, 12), (30, 36), (44, 49)],
    10: [(11, 13), (31, 36), (44, 48)],
    11: [(12, 14), (31, 35), (45, 48), (50, 52)],
    12: [(15, 19), (32, 34), (46, 48)],
    13: [(15, 20), (32, 34), (47, 49)],
    14: [(16, 21), (32, 34), (48, 51)],
    15: [(16, 21), (32, 34), (49, 53)],
    16: [(16, 21), (33, 34), (50, 55)],
    17: [(16, 20), (51, 55)],
    18: [(17, 20), (51, 55)],
    19: [(17, 20), (51, 54)],
    20: [(17, 19), (52, 54)],
    21: [(18, 19), (53, 54)],
    22: [(18, 19)],
    23: [(18, 18)],
    24: [(18, 18)],
    25: [(18, 18)],
}


def _build_map_rows():
    fine = [[False] * 60 for _ in range(26)]
    for r, spans in _LAND.items():
        for a, b in spans:
            for c in range(a, b + 1):
                fine[r][c] = True
    rows = []
    for r in range(13):  # downsample 2x2 -> 30 cols x 13 rows
        line = ""
        for c in range(30):
            land = any(fine[2 * r + dr][2 * c + dc]
                       for dr in (0, 1) for dc in (0, 1))
            line += "#" if land else " "
        rows.append(line)
    return rows


MAP_ROWS = _build_map_rows()

# (story number, lon, lat) pins on the map
PINS = [
    (1, 52, 27), (2, 133, -25), (3, -77, 39), (4, 12, 52),
    (6, -150, 30), (7, 31, 50), (8, 34, 31), (9, 4, 52),
    (11, 80, 17), (12, 114, 22), (16, 46, 6), (19, 151, -34),
]

# ------------------------------------------------------- illustrations
def draw_gulf(draw, x, y, w, h):
    """Strait of Hormuz at dusk: sea, tanker, missile arcs, carrier."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 52, 78))
    # dusk sky band
    draw.rectangle([x, y, x + w, y + h // 3], fill=(64, 58, 84))
    sun = (x + w - 34, y + 16)
    draw.ellipse([sun[0] - 13, sun[1] - 13, sun[0] + 13, sun[1] + 13],
                 fill=(232, 150, 60))
    # missile arcs (fixed, deterministic); kept below the top caption
    for cx, cy, r, col in [(x + 40, y + h - 18, 34, (232, 120, 60)),
                           (x + 90, y + h - 14, 40, (240, 180, 80)),
                           (x + 150, y + h - 20, 30, (232, 120, 60))]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=330,
                 fill=col, width=3)
        draw.ellipse([cx - 3, cy - r - 3, cx + 3, cy - r + 3], fill=col)
    # sea lines
    for i, yy in enumerate(range(y + h // 2, y + h - 6, 9)):
        draw.line([(x + 8 + (i % 3) * 12, yy), (x + w - 10 - (i % 2) * 14, yy)],
                  fill=(90, 140, 170), width=1)
    # tanker hull + containers
    hx, hy = x + w // 2 - 52, y + h - 26
    draw.rectangle([hx, hy, hx + 104, hy + 16], fill=(30, 30, 34))
    draw.rectangle([hx + 8, hy - 14, hx + 96, hy], fill=(178, 34, 28))
    draw.rectangle([hx + 14, hy - 14, hx + 30, hy], fill=(198, 138, 28))
    draw.rectangle([hx + 62, hy - 14, hx + 80, hy], fill=(198, 138, 28))
    draw.rectangle([hx + 84, hy - 22, hx + 100, hy], fill=(220, 220, 210))
    # carrier silhouette, far left
    draw.rectangle([x + 10, y + h - 18, x + 58, y + h - 10], fill=(12, 12, 16))
    draw.rectangle([x + 40, y + h - 26, x + 48, y + h - 18], fill=(12, 12, 16))
    draw.text((x + 8, y + 6), "STRAIT OF HORMUZ", font=SANS_B(9),
              fill=(240, 220, 180))


def draw_vice(draw, x, y, w, h):
    """Vice City at night: neon skyline, palm, pink sun, game controller."""
    draw.rectangle([x, y, x + w, y + h], fill=(26, 10, 46))
    # pink sun, low and right of centre so it clears the top caption
    sx, sy = x + w - 58, y + 46
    draw.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], fill=(255, 110, 150))
    for i in range(3):
        yy = sy + 2 + i * 6
        draw.rectangle([sx - 20, yy, sx + 20, yy + 2], fill=(26, 10, 46))
    # skyline
    import random
    rng = random.Random(1911)
    bx = x + 6
    while bx < x + w - 14:
        bw = rng.choice([16, 20, 24, 28])
        bh = rng.choice([34, 48, 60, 72, 44])
        col = rng.choice([(40, 20, 70), (52, 28, 88), (34, 16, 60)])
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=col)
        for wy in range(y + h - bh + 6, y + h - 6, 10):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rng.random() < 0.55:
                    draw.rectangle([wx, wy, wx + 3, wy + 4],
                                   fill=rng.choice([(255, 210, 90),
                                                    (90, 220, 230),
                                                    (255, 110, 150)]))
        bx += bw + 3
    # palm silhouette
    px, py = x + w - 30, y + h - 8
    draw.line([(px, py), (px + 2, py - 34)], fill=(8, 30, 16), width=4)
    for dx, dy in [(-16, -38), (-8, -44), (6, -44), (16, -38), (-20, -30),
                   (20, -30)]:
        draw.line([(px + 2, py - 34), (px + dx, py + dy)],
                  fill=(8, 30, 16), width=3)
    # neon strip
    draw.rectangle([x, y + h - 4, x + w, y + h], fill=(255, 110, 150))
    draw.text((x + 8, y + 6), "VICE CITY  \u2022  99 ON METACRITIC",
              font=SANS_B(9), fill=(255, 210, 90))


def draw_capitol(draw, x, y, w, h):
    """US Capitol dome in flat teal and gold, drawn to fit inside (x,y,w,h)."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 226))
    # sky
    draw.rectangle([x, y, x + w, y + h // 2 + 6], fill=(168, 196, 210))
    # bunting along the top
    for i in range(7):
        bx = x + 14 + i * ((w - 28) // 6)
        draw.polygon([(bx, y + 6), (bx + 8, y + 6), (bx + 4, y + 15)],
                     fill=RED if i % 2 == 0 else TEAL)
    cx = x + w // 2
    base = y + h - 6
    # steps
    for i in range(3):
        draw.rectangle([cx - 72 + i * 8, base - 5 - i * 5,
                        cx + 72 - i * 8, base - i * 5], fill=(120, 118, 110))
    # columns
    for i in range(-2, 3):
        colx = cx + i * 26
        draw.rectangle([colx - 5, base - 34, colx + 5, base - 10],
                       fill=(247, 243, 232))
        draw.rectangle([colx - 7, base - 38, colx + 7, base - 34],
                       fill=(247, 243, 232))
    # entablature + drum
    draw.rectangle([cx - 72, base - 43, cx + 72, base - 38], fill=(232, 226, 210))
    draw.rectangle([cx - 30, base - 54, cx + 30, base - 43], fill=(232, 226, 210))
    # dome (radius 26, top stays inside the box)
    draw.pieslice([cx - 26, base - 80, cx + 26, base - 54], start=180,
                  end=360, fill=(13, 84, 84))
    draw.ellipse([cx - 4, base - 84, cx + 4, base - 76], fill=GOLD)
    draw.text((x + 8, y + 22), "WASHINGTON", font=SANS_B(9), fill=TEAL_DK)


FEATURE_ART = {1: draw_gulf, 2: draw_vice, 3: draw_capitol}


# ------------------------------------------------------- page sections
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 30], fill=INK)
    draw.text((14, 8), "THURSDAY 19 NOVEMBER 2026",
              font=SANS_B(13), fill=(255, 255, 255))
    right = "35 STORIES  \u2022  6 CONTINENTS  \u2022  ONE PAGE"
    draw.text((W - 14 - draw.textlength(right, font=SANS_B(13)), 8), right,
              font=SANS_B(13), fill=(255, 210, 90))
    # masthead
    title = "THE GLOBAL LEDGER"
    tf = SERIF_B(52)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 38), title, font=tf, fill=INK)
    hline(draw, 14, W - 14, 100, fill=INK, width=2)
    sub = "The world in one day \u2014 war in the Gulf, a new Speaker, and Vice City"
    sf = SERIF(15)
    draw.text(((W - draw.textlength(sub, font=sf)) / 2, 106), sub,
              font=sf, fill=GREY)
    hline(draw, 14, W - 14, 130, fill=INK, width=1)
    return 138


def draw_features(draw, y):
    col_w = (W - 28 - 2 * 12) // 3
    x0 = 14
    art_h = 92
    bottom = y
    for i, (n, kicker, head, body) in enumerate(FEATURES):
        x = x0 + i * (col_w + 12)
        FEATURE_ART[n](draw, x, y, col_w, art_h)
        draw.rectangle([x, y, x + col_w, y + art_h], outline=INK, width=1)
        yy = y + art_h + 8
        draw.text((x, yy), kicker, font=SANS_B(10), fill=RED)
        yy += 15
        yy = capped_para(draw, x, yy, head, SERIF_B(14), col_w, 3, leading=17)
        yy += 2
        yy = capped_para(draw, x, yy, body, SANS(10), col_w, 3,
                         fill=(40, 40, 40), leading=13)
        bottom = max(bottom, yy)
        if i < 2:
            draw.line([(x + col_w + 6, y), (x + col_w + 6, y + 196)],
                      fill=LINE, width=1)
    return bottom


def draw_numbers(draw, y):
    draw.rectangle([0, y, W, y + 54], fill=TEAL_DK)
    draw.text((14, y + 4), "BY THE NUMBERS", font=SANS_B(11),
              fill=(255, 210, 90))
    col_w = (W - 28) // 4
    for i, (big, label) in enumerate(NUMBERS):
        cx = 14 + (i % 4) * col_w
        cy = y + 20 + (i // 4) * 18
        bf = SANS_B(15)
        draw.text((cx, cy), big, font=bf, fill=(255, 255, 255))
        lw = draw.textlength(big, font=bf)
        draw.text((cx + lw + 6, cy + 2), label, font=SANS(10),
                  fill=(200, 220, 215))
    return y + 54


def draw_map(draw, y):
    h = 140
    draw.rectangle([0, y, W, y + h], fill=MAP_SEA)
    draw.text((14, y + 6), "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED",
              font=SANS_B(11), fill=TEAL_DK)
    mx0, my0 = 14, y + 24
    cell = 28
    cols, rows = 30, 13
    # scale map to fit width: use cell 28 -> 840 wide, centred
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == '#':
                cx = mx0 + c * cell + cell // 2
                cy = my0 + r * (h - 30) // rows + (h - 30) // rows // 2
                draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=MAP_DOT)
    # pins: lon -180..180 -> x, lat 75..-55 -> y (same grid as the dots:
    # 26 rows over 104 px, so lat maps with factor 104/130)
    for n, lon, lat in PINS:
        px = mx0 + (lon + 180) / 360.0 * (cols * cell)
        py = my0 + (75 - lat) * (104 / 130.0) + 2
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(n)
        f = SANS_B(9)
        tw = draw.textlength(t, font=f)
        draw.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))
    draw.text((14, y + h - 16),
              "Pins: 1 Gulf  \u2022  2 Australia  \u2022  3 Washington  \u2022  4 Brussels  "
              "\u2022  6 Voyager 1  \u2022  7 Kyiv  \u2022  8 Gaza  \u2022  9 The Hague  "
              "\u2022  11 India  \u2022  12 Shenzhen  \u2022  16 Mogadishu  \u2022  19 Sydney",
              font=SANS(8), fill=GREY)
    return y + h

# ------------------------------------------------------- grid + also + footer
def capped_para(draw, x, y, text, fnt, width, max_lines, fill=INK,
                leading=None):
    """Wrapped paragraph capped at max_lines; returns y below it."""
    lh = leading or int(fnt.size * 1.32)
    lines = wrap(draw, text, fnt, width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_grid(draw, y):
    draw.text((14, y), "THE DAY IN BRIEF \u2014 STORIES 4\u201315",
              font=SANS_B(11), fill=TEAL_DK)
    hline(draw, 14, W - 14, y + 16, fill=INK, width=1)
    y += 22
    col_w = (W - 28 - 2 * 12) // 3
    items = GRID[:12]  # stories 4-15
    for row in range(4):
        row_items = items[row * 3:(row + 1) * 3]
        row_h = 0
        for i, (n, kicker, head, body) in enumerate(row_items):
            x = 14 + i * (col_w + 12)
            yy = y
            num_badge(draw, x + 9, yy + 8, n)
            draw.text((x + 22, yy), kicker, font=SANS_B(9), fill=RED)
            yy += 14
            yy = capped_para(draw, x, yy, head, SERIF_B(12), col_w, 2,
                             leading=15)
            yy = capped_para(draw, x, yy + 1, body, SANS(9), col_w, 2,
                             fill=(40, 40, 40), leading=11)
            row_h = max(row_h, yy - y)
        y += row_h + 6
    return y


def draw_also(draw, y):
    draw.text((14, y), "ALSO ON THURSDAY 19 NOVEMBER \u2014 20 MORE STORIES",
              font=SANS_B(11), fill=TEAL_DK)
    hline(draw, 14, W - 14, y + 16, fill=INK, width=1)
    y += 21
    col_w = (W - 28 - 12) // 2
    items = [(n, head) for (n, _k, head, _b) in GRID[12:]] + ALSO
    half = (len(items) + 1) // 2
    for col in range(2):
        x = 14 + col * (col_w + 12)
        yy = y
        for n, text in items[col * half:(col + 1) * half]:
            num_badge(draw, x + 8, yy + 6, n, r=7)
            yy = capped_para(draw, x + 19, yy, text, SANS(9), col_w - 19, 1,
                             fill=(30, 30, 30), leading=12)
            yy += 1
        if col == 0:
            first_col_bottom = yy
    return max(y + half * 13, first_col_bottom)


def draw_footer(draw, y):
    hline(draw, 14, W - 14, y, fill=INK, width=2)
    draw.text((14, y + 6),
              "Sources: Reuters \u2022 AP \u2022 BBC \u2022 AFP \u2022 Financial Times "
              "\u2022 Bloomberg \u2022 CNN \u2022 Pew Research \u2022 NASA \u2022 "
              "Metacritic",
              font=SANS(9), fill=GREY)
    draw.text((14, y + 19),
              "THE GLOBAL LEDGER \u2014 a one-page summary of Thursday 19 November "
              "2026. All stories as reported on the day; contested claims are "
              "attributed in the text.",
              font=SANS(8), fill=GREY)
    return y + 32


# ------------------------------------------------------- main
def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_features(draw, y)
    hline(draw, 14, W - 14, y + 2, fill=INK, width=1)
    y = draw_numbers(draw, y + 6)
    y = draw_map(draw, y + 4)
    y = draw_grid(draw, y + 8)
    y = draw_also(draw, y + 2)
    y = draw_footer(draw, y + 4)
    return img, y


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img, bottom = build()
    assert bottom <= H, "layout overflow: bottom=%d > %d" % (bottom, H)
    path = os.path.join(out_dir, OUT_NAME)
    img.save(path, format="PNG", optimize=True)
    print("wrote %s (%dx%d, bottom=%d)" % (path, W, H, bottom))


if __name__ == "__main__":
    main()
