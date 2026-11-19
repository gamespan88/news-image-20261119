#!/usr/bin/env python3
"""Entry image for make.fun bounty news-image-20261119.

One-page newspaper digest of Thursday 19 November 2026:
52 stories, 7 regions, 3 drawn lead scenes (the first Trump-Xi-Putin
trilateral in Shenzhen, the Gulf's second day of fire, GTA VI launch
day), a drawn dot world map with the day's places marked, a Day in
Numbers panel, a date-check stamp and a UTC clock timeline.
Every story reported on the day itself. Deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (255, 253, 245)
INK = (22, 22, 22)
GRAY = (90, 90, 90)
RULE = (40, 40, 40)
DATE_RED = (157, 2, 8)
LEAD_BG = (243, 238, 224)
WHITE = (255, 255, 255)
MAP_BG = (233, 238, 242)
LAND = (105, 128, 152)
MARK = (178, 34, 52)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center(s, font, y, fill=INK):
    d.text(((W - text_w(s, font)) / 2, y), s, font=font, fill=fill)

MX = 26
CW = W - 2 * MX

# ---------------------------------------------------------------- data
LEADS = [
    ("SHENZHEN · A FIRST IN HISTORY", (29, 78, 137),
     "Trump, Xi & Putin sit down together",
     "The US, Chinese and Russian leaders met for an hour at Kylin Villa — "
     "the first three-way summit ever held. Trump urged nuclear cuts; "
     "Ukraine and Iran were on the table. (AP/AFP)"),
    ("THE GULF · A SECOND DAY OF FIRE", (179, 84, 30),
     "Iran widens its attacks",
     "Iranian drones struck at Kuwait and Bahrain overnight; a tanker was "
     "hit off Oman and debris damaged Saudi Arabia's PIF tower in Riyadh. "
     "The US rushed more Patriots to the Gulf. (Reuters/UKMTO)"),
    ("LAUNCH DAY · GRAND THEFT AUTO VI", (150, 20, 90),
     "The world's biggest game lands",
     "Rockstar's Grand Theft Auto VI went on sale worldwide on Thursday — "
     "the most anticipated release in gaming history, ending a wait of more "
     "than a decade since GTA V. (Rockstar)"),
]

REGIONS = {
    "ASIA-PACIFIC": ((29, 111, 184), [
        ("Xi opens the APEC plenary",
         "China pledged $20m for APEC cooperation and a new Asia-Pacific studies centre in Shenzhen."),
        ("Trump–Xi: a third meeting this year",
         "Their third meeting this year; the trade truce expires 10 January, rare earths 75% below normal."),
        ("Lee urges reopening North Korea dialogue",
         "Seoul's president urged end-of-war talks and a permanent peace regime for the peninsula."),
        ("India & Japan deepen defence ties",
         "Tokyo 2+2 talks agreed closer maritime security and joint defence manufacturing."),
        ("White House unveils $12bn Philippine Airlines deal",
         "Up to 20 Boeing 787s plus $2bn-plus defence financing, after Trump's Manila talks."),
        ("72,000 flee Cyclone Akvan's path",
         "7,900 shelters readied as the storm, gusting to 110 km/h, aims at Gopalpur for Friday noon."),
    ]),
    "EUROPE & UKRAINE": ((68, 86, 168), [
        ("Kerch Bridge hit for a third time in a week",
         "Night strike on the railway section halted traffic; a 227-metre span fell on 17 Nov."),
        ("Russian strikes kill four in central Odesa",
         "Three strikes on the centre; a market hit in Zlatopol injured 11; Naftogaz sites attacked."),
        ("Europe's coalition gathers in Berlin",
         "30+ leaders with Zelensky as the €45bn loan plan targeted Kyiv's €70bn funding gap."),
        ("Britain pledges 1,000 cruise missiles",
         "Reported as the allies met in Berlin to close Kyiv's funding and air-defence gaps."),
    ]),
    "MIDDLE EAST": ((179, 84, 30), [
        ("Tanker struck off Oman at Hormuz",
         "A projectile hit the engine room 6 nautical miles north of Khasab, Oman (UKMTO 212)."),
        ("Debris damages Saudi PIF tower",
         "Debris from an intercepted Houthi rocket struck Riyadh's PIF tower; the all-clear followed."),
        ("Israeli tanks push west of Gaza's Yellow Line",
         "First ground push since the ceasefire, near Nuseirat and Bureij; medics reported 3 killed."),
        ("IEA: Hormuz is the gravest energy threat ever seen",
         "The agency called the crisis the biggest energy-security threat it has ever recorded."),
    ]),
    "AMERICAS": ((46, 125, 50), [
        ("Trump tells Americans to 'relax'",
         "He called the bank, Microsoft and air-traffic failures unrelated; Rubio saw no link."),
        ("218 signatures force an Epstein files vote",
         "The discharge petition hit 218 as the FAA lifted a nationwide ground stop."),
        ("US & Venezuela restore military ties",
         "Announced by Defense Secretary Hegseth on a visit to Caracas."),
        ("Lula courts investors for Brazil's rare earths",
         "US trade is now just 9.2% of Brazil's total; Canada pledged $400m for forests."),
        ("Pastor convicted over Haiti president's killing",
         "A Miami court convicted him over the 2021 assassination of President Jovenel Moïse."),
    ]),
    "AFRICA": ((166, 124, 0), [
        ("Nigeria's Senate demands answers for 37 dead miners",
         "Lawmakers sought accountability over artisanal miners who died in custody in Minna."),
        ("Dangote refinery IPO upsized to $2.1bn",
         "Demand near $4.5bn lifted the offer from $1.62bn — among Africa's largest listings."),
    ]),
    "OCEANIA": ((0, 131, 143), [
        ("England take the ODI series in Hobart",
         "A 97-run win in the decider sealed the one-day series 2–1 over Australia."),
        ("Canberra holds the line to a silent Voyager",
         "Confirmed by carrier signal alone: no data since 14 Nov; commands take a day each way."),
    ]),
    "CLIMATE · TECH · SPORT · CULTURE": ((106, 27, 154), [
        ("COP31 deadlocked: 21 issues still open",
         "Ministers launched the second Global Stocktake; finance and fossil fuels unresolved."),
        ("Anthropic's $81.3bn IPO is history's largest",
         "Priced at $83 (ticker ANT), the raise values the AI firm at $1.5 trillion."),
        ("Markets slide; gold sinks to a 14-month low",
         "S&P fell a fifth day; gold lost 3.6% to $3,726, Brent near $92, Bitcoin $63,479."),
        ("Vinícius hat-trick as Brazil rout Singapore 7–0",
         "Three first-half goals from Vinícius headlined the friendly rout."),
    ]),
}

BRIEFS = [
    ("SHENZHEN", "Putin backs the draft Shenzhen Declaration"),
    ("APEC", "CEO Summit issues its first-ever Shenzhen Initiative"),
    ("SEOUL", "Lee & Putin chat 10 minutes at the welcome banquet"),
    ("HONG KONG", "John Lee hails five APEC outcomes; Chile deal signed"),
    ("MANILA", "Envoy: 'biggest trade deal' unsigned; 12.5% tariff stands"),
    ("APEC", "Trump champions US economy, opposes global AI rules"),
    ("SEOUL", "Lee & Carney agree energy and AI cooperation"),
    ("BRUSSELS", "EU–UK draft drops the words 'trusted partnership'"),
    ("NUCLEAR", "New START's expiry hangs over the Shenzhen talks"),
    ("COP31", "Adaptation Fund pledges total just $50.2m"),
    ("COP31", "75 countries back the '35x35' electrification push"),
    ("COP31", "Four nations unveil fossil-fuel phaseout roadmaps"),
    ("US", "Emergency Supreme Court filing over Venezuelan TPS"),
    ("MANILA", "US explores a civil nuclear pact with the Philippines"),
    ("TECH", "IEA: datacentre emissions to rise 70% by 2030"),
    ("EUROZONE", "Eurogroup reports ahead of the 26 Nov Euro Summit"),
    ("FOOTBALL", "Chelsea edge PSG 1–0 in Women's Champions League"),
    ("FOOTBALL", "City, Real Madrid & Juventus also reach knockouts"),
    ("SPORT", "Marathon champion Jepchirchir banned over doping"),
    ("AUCTION", "A Van Gogh sells for a record $190.4 million"),
    ("HAITI", "Salvadoran anti-gang troops draw rallies of support"),
    ("UGANDA", "Landslide survivors seek justice at the UN"),
]

NUMBERS = [
    ("1st", "US–China–Russia leaders' summit in history — one hour in Shenzhen"),
    ("72,000", "people evacuated in Odisha as Cyclone Akvan nears landfall"),
    ("$81.3bn", "raised by Anthropic's IPO, the largest ever, at a $1.5tn value"),
    ("1,000", "long-range cruise missiles pledged by Britain to Ukraine"),
    ("$190.4m", "record auction price for a Van Gogh, set on Thursday"),
    ("15%", "drop in shipping through Hormuz, the IEA's gravest-ever threat"),
]

TOTAL = len(LEADS) + sum(len(v[1]) for v in REGIONS.values()) + len(BRIEFS)
print("story count:", TOTAL)
assert TOTAL == 52, TOTAL

# ---------------------------------------------------------------- masthead
center("THE WHOLE DAY'S WORLD NEWS IN A SINGLE IMAGE", F(SANS_B, 11), 8, GRAY)
center("THE WORLD TODAY", F(SERIF_B, 44), 22)
d.line([(MX, 74), (W - MX, 74)], fill=RULE, width=3)
center("Thursday 19 November 2026", F(SERIF_B, 32), 80, DATE_RED)
center("52 stories  ·  7 regions  ·  drawn map & scenes  ·  every story reported on the day itself, date-checked",
       F(SANS, 13), 118, GRAY)
d.line([(MX, 140), (W - MX, 140)], fill=RULE, width=1)

# date-check stamp (drawn on its own layer, rotated, pasted)
stamp = Image.new("RGBA", (176, 48), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([2, 2, 173, 45], outline=(178, 34, 52, 255), width=3)
sd.text((88 - sd.textlength("DATE-CHECKED", font=F(SANS_B, 16)) / 2, 5),
        "DATE-CHECKED", font=F(SANS_B, 16), fill=(178, 34, 52, 255))
sd.text((88 - sd.textlength("THU 19 NOV 2026", font=F(SANS_B, 11)) / 2, 27),
        "THU 19 NOV 2026", font=F(SANS_B, 11), fill=(178, 34, 52, 255))
_rot = stamp.rotate(8, expand=True, resample=Image.BILINEAR)
img.paste(_rot, (836, 12), _rot)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- lead scenes
def draw_flag(x, y, fw, fh, kind):
    if kind == "cn":
        d.rectangle([x, y, x + fw, y + fh], fill=(222, 41, 16))
        d.rectangle([x + 3, y + 3, x + 6, y + 6], fill=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([x, y, x + fw, y + fh // 3], fill=WHITE)
        d.rectangle([x, y + fh // 3, x + fw, y + 2 * fh // 3], fill=(0, 57, 166))
        d.rectangle([x, y + 2 * fh // 3, x + fw, y + fh], fill=(213, 43, 30))
    else:
        for i in range(5):
            d.rectangle([x, y + i * fh // 5, x + fw, y + (i + 1) * fh // 5],
                        fill=(178, 34, 52) if i % 2 == 0 else WHITE)
        d.rectangle([x, y, x + fw // 2, y + fh // 2], fill=(60, 59, 110))

def scene_summit(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 62, 110))
    d.rectangle([x + 4, y + 5, x + w - 4, y + 17], fill=(212, 175, 55))
    d.rectangle([x + 4, y + 7, x + w - 4, y + 9], fill=(38, 62, 110))
    # three flags on poles
    for pf, kind in [(0.14, "us"), (0.44, "cn"), (0.74, "ru")]:
        px = x + int(pf * w)
        d.line([(px, y + h - 26), (px, y + 20)], fill=(220, 220, 225), width=2)
        draw_flag(px + 2, y + 20, int(0.22 * w), int(0.15 * h), kind)
    # summit table
    ty = y + h - 26
    d.rectangle([x + 4, ty, x + w - 4, ty + 7], fill=(96, 62, 38))
    d.rectangle([x + 8, ty + 7, x + 12, ty + 12], fill=(70, 45, 28))
    d.rectangle([x + w - 12, ty + 7, x + w - 8, ty + 12], fill=(70, 45, 28))
    # three seated leaders
    for pf, suit in [(0.17, (30, 30, 34)), (0.47, (24, 24, 40)), (0.77, (34, 30, 30))]:
        cx = x + int(pf * w)
        d.ellipse([cx - 4, ty - 17, cx + 4, ty - 9], fill=(232, 190, 150))
        d.polygon([(cx - 8, ty), (cx + 8, ty), (cx + 5, ty - 9), (cx - 5, ty - 9)], fill=suit)
        d.polygon([(cx - 2, ty - 9), (cx + 2, ty - 9), (cx, ty - 3)], fill=WHITE)

def scene_gulf(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 224, 178))
    d.rectangle([x, y + int(h * 0.45), x + w, y + h], fill=(38, 110, 138))
    d.ellipse([x + 8, y + 6, x + 28, y + 26], fill=(244, 164, 40))
    ty = y + int(h * 0.62)
    d.polygon([(x + 10, ty), (x + w - 8, ty), (x + w - 18, ty + 13), (x + 18, ty + 13)], fill=(35, 35, 40))
    d.rectangle([x + 20, ty - 6, x + w - 22, ty], fill=(90, 90, 96))
    d.rectangle([x + w - 30, ty - 16, x + w - 20, ty - 6], fill=(60, 60, 66))
    d.rectangle([x + w - 27, ty - 21, x + w - 23, ty - 16], fill=(178, 34, 52))
    for cf in [(0.34, 0.16), (0.62, 0.10)]:
        cx, cy = x + int(cf[0] * w), y + int(cf[1] * h)
        d.line([(cx - 5, cy - 3), (cx + 5, cy + 3)], fill=(30, 30, 30), width=2)
        d.line([(cx - 5, cy + 3), (cx + 5, cy - 3)], fill=(30, 30, 30), width=2)
    d.arc([x + int(0.30 * w), y + int(0.14 * h), x + w - 4, y + int(0.72 * h)],
          start=200, end=320, fill=(178, 34, 52), width=2)

def scene_gta(x, y, w, h):
    bands = [(247, 127, 90), (244, 110, 120), (214, 84, 150), (150, 66, 150), (84, 52, 130)]
    bh = h // len(bands) + 1
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    # sun
    sx, sy = x + int(0.62 * w), y + int(0.52 * h)
    d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=(255, 214, 90))
    # sea / street band
    d.rectangle([x, y + int(0.72 * h), x + w, y + h], fill=(40, 26, 66))
    d.line([(x, y + int(0.72 * h)), (x + w, y + int(0.72 * h))], fill=(0, 240, 220), width=2)
    # palm silhouettes
    for pf in (0.14, 0.86):
        px = x + int(pf * w)
        base = y + int(0.72 * h)
        d.line([(px, base), (px + 3, base - int(0.34 * h))], fill=(20, 14, 34), width=3)
        tx, ty = px + 3, base - int(0.34 * h)
        for dx, dy in [(-11, -4), (-6, -8), (0, -10), (7, -8), (12, -4), (-9, 2), (10, 2)]:
            d.line([(tx, ty), (tx + dx, ty + dy)], fill=(20, 14, 34), width=2)
    # sports car silhouette
    cy = y + h - 8
    d.polygon([(x + 16, cy), (x + 22, cy - 6), (x + 34, cy - 7), (x + 42, cy - 12),
               (x + 56, cy - 12), (x + 64, cy - 7), (x + 72, cy - 6), (x + 76, cy)],
              fill=(16, 12, 28))
    d.rectangle([x + 44, cy - 11, x + 54, cy - 8], fill=(0, 240, 220))
    for wx in (x + 26, x + 66):
        d.ellipse([wx - 4, cy - 5, wx + 4, cy + 3], fill=(10, 8, 20), outline=(255, 90, 180))

LY = 148
LW = (CW - 2 * 12) // 3
LH = 108
for i, (kick, col, head, body) in enumerate(LEADS):
    x = MX + i * (LW + 12)
    d.rectangle([x, LY, x + LW, LY + LH], fill=LEAD_BG)
    d.rectangle([x, LY, x + LW, LY + 5], fill=col)
    if i == 0:
        scene_summit(x + 8, LY + 8, 84, LH - 16)
    elif i == 1:
        scene_gulf(x + 8, LY + 8, 84, LH - 16)
    else:
        scene_gta(x + 8, LY + 8, 84, LH - 16)
    tx = x + 100
    d.text((tx, LY + 8), kick, font=F(SANS_B, 11), fill=col)
    yy = LY + 23
    for ln in wrap(head, F(SERIF_B, 15), LW - 108):
        d.text((tx, yy), ln, font=F(SERIF_B, 15), fill=INK)
        yy += 17
    yy += 2
    for ln in wrap(body, F(SANS, 10), LW - 108):
        d.text((tx, yy), ln, font=F(SANS, 10), fill=(45, 45, 45))
        yy += 11.5

# ---------------------------------------------------------------- map + numbers
MY = LY + LH + 8
MH = 168
MAPW = 596
d.rectangle([MX, MY, MX + MAPW, MY + 16], fill=RULE)
d.text((MX + 8, MY + 2), "THE DAY ON THE MAP — WHERE THURSDAY HAPPENED", font=F(SANS_B, 12), fill=WHITE)
d.rectangle([MX, MY + 16, MX + MAPW, MY + MH], fill=MAP_BG)

LAND_SPANS = {
    0: [(3, 6), (11, 16), (26, 29), (47, 60), (64, 78)],
    1: [(1, 8), (10, 21), (25, 28), (37, 37), (43, 46), (48, 79)],
    2: [(9, 22), (39, 40), (41, 46), (47, 78)],
    3: [(8, 23), (38, 45), (47, 56), (57, 67), (71, 73)],
    4: [(8, 23), (38, 39), (42, 43), (44, 47), (48, 50), (51, 55), (58, 67), (68, 69), (70, 72)],
    5: [(9, 20), (13, 17), (37, 46), (47, 49), (50, 52), (53, 55), (56, 58), (59, 66)],
    6: [(12, 16), (36, 47), (48, 51), (56, 59), (60, 62), (63, 66), (67, 67), (68, 69)],
    7: [(14, 15), (36, 47), (48, 50), (56, 58), (59, 62), (67, 68)],
    8: [(23, 28), (36, 48), (49, 50), (57, 57), (59, 61), (62, 65)],
    9: [(23, 29), (37, 46), (60, 68)],
    10: [(23, 30), (37, 45), (62, 67), (69, 71)],
    11: [(24, 31), (38, 44), (66, 72)],
    12: [(24, 30), (38, 43), (46, 46), (64, 74)],
    13: [(25, 29), (38, 41), (63, 73)],
    14: [(25, 28), (38, 39), (67, 73)],
    15: [(25, 26), (78, 80)],
    16: [(25, 26), (77, 78)],
    17: [(25, 25)],
}
MARKS = [
    (66, 6, "SHENZHEN", "l", 0), (68, 7, "MANILA", "r", 0), (63, 8, "ODISHA", "r", 12),
    (47, 3, "KYIV", "l", 0), (45, 2, "BERLIN", "l", 0), (46, 4, None, None, 0),
    (53, 6, "HORMUZ", "r", 11), (50, 6, None, None, 0), (48, 5, None, None, 0),
    (23, 4, "WASHINGTON", "l", 0), (25, 8, None, None, 0), (48, 9, None, None, 0),
    (44, 8, None, None, 0), (74, 15, None, None, 0), (71, 4, None, None, 0),
]
GX, GY = MX + 11, MY + 24
SX, SY = 7.0, 7.2
for row, spans in LAND_SPANS.items():
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            cx, cy = GX + c * SX, GY + row * SY
            d.ellipse([cx - 2.2, cy - 2.2, cx + 2.2, cy + 2.2], fill=LAND)
LF = F(SANS_B, 9)
for c, r, label, side, dy in MARKS:
    cx, cy = GX + c * SX, GY + r * SY
    d.ellipse([cx - 4.5, cy - 4.5, cx + 4.5, cy + 4.5], fill=WHITE)
    d.ellipse([cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2], fill=MARK)
    if label:
        tw = text_w(label, LF)
        lx = cx + 7 if side == "r" else cx - 7 - tw
        d.text((lx, cy - 5 + dy), label, font=LF, fill=INK, stroke_width=2, stroke_fill=MAP_BG)

NX = MX + MAPW + 12
NW = W - MX - NX
d.rectangle([NX, MY, NX + NW, MY + 16], fill=RULE)
d.text((NX + 8, MY + 2), "THE DAY IN NUMBERS", font=F(SANS_B, 12), fill=WHITE)
d.rectangle([NX, MY + 16, NX + NW, MY + MH], fill=LEAD_BG)
NF = F(SERIF_B, 19)
NL = F(SANS, 9)
cell_w = (NW - 24) // 2
for i, (num, lab) in enumerate(NUMBERS):
    cx = NX + 10 + (i % 2) * (cell_w + 8)
    cy = MY + 24 + (i // 2) * 50
    d.text((cx, cy), num, font=NF, fill=DATE_RED)
    yy = cy + 23
    for ln in wrap(lab, NL, cell_w):
        d.text((cx, yy), ln, font=NL, fill=(45, 45, 45))
        yy += 10.5

# ---------------------------------------------------------------- timeline
TY = MY + MH + 8
d.rectangle([MX, TY, W - MX, TY + 24], fill=INK)
TL = ("BY THE CLOCK (UTC)  »  before dawn: Bahrain & Kuwait intercept fresh barrages  »  04:45: Trump–Xi bilateral  »  "
      "07:30: three leaders sit down together — a first  »  all day: APEC plenary, COP31 deadlocked  »  by nightfall: GTA VI on sale")
_tlf = F(SANS_B, 10)
while text_w(TL, _tlf) > CW - 20:
    _tlf = F(SANS_B, _tlf.size - 1)
d.text((MX + 10, TY + 5), TL, font=_tlf, fill=WHITE)

# ---------------------------------------------------------------- regions
LEFT = ["ASIA-PACIFIC", "EUROPE & UKRAINE", "MIDDLE EAST"]
RIGHT = ["AMERICAS", "AFRICA", "OCEANIA", "CLIMATE · TECH · SPORT · CULTURE"]

HF = F(SANS_B, 11)
BF = F(SANS, 9)
SF = F(SANS_B, 12)
HLH, BLH = 11, 10
COLW = (CW - 20) // 2
TOP = TY + 32
BOTTOM = 846

def region_height(name):
    col, stories = REGIONS[name]
    h = 19
    for head, body in stories:
        h += HLH + len(wrap(body, BF, COLW - 10)) * BLH + 1
    return h + 1

def draw_region(name, x, y):
    col, stories = REGIONS[name]
    d.rectangle([x, y, x + COLW, y + 17], fill=col)
    d.text((x + 8, y + 2), name, font=SF, fill=WHITE)
    yy = y + 19
    for head, body in stories:
        d.rectangle([x + 1, yy + 3, x + 5, yy + 9], fill=col)
        d.text((x + 10, yy), head, font=HF, fill=INK)
        yy += HLH
        for ln in wrap(body, BF, COLW - 10):
            d.text((x + 10, yy), ln, font=BF, fill=(60, 60, 60))
            yy += BLH
        yy += 1
    return yy + 1

lh = sum(region_height(r) for r in LEFT)
rh = sum(region_height(r) for r in RIGHT)
print("left col height:", lh, "right col height:", rh, "available:", BOTTOM - TOP)
assert lh <= BOTTOM - TOP and rh <= BOTTOM - TOP, "region overflow"

y = TOP
for r in LEFT:
    y = draw_region(r, MX, y)
y = TOP
for r in RIGHT:
    y = draw_region(r, MX + COLW + 20, y)

# ---------------------------------------------------------------- in brief
BY = 850
d.rectangle([MX, BY, W - MX, BY + 17], fill=RULE)
d.text((MX + 8, BY + 2), "IN BRIEF — 22 MORE STORIES FROM THE DAY", font=F(SANS_B, 12), fill=WHITE)
BCOLW = (CW - 2 * 14) // 3
BF2 = F(SANS_B, 9)
yy = BY + 23
rows = (len(BRIEFS) + 2) // 3
for row in range(rows):
    for cidx in range(3):
        k = row * 3 + cidx
        if k >= len(BRIEFS):
            break
        tag, txt = BRIEFS[k]
        x = MX + cidx * (BCOLW + 14)
        d.rectangle([x + 1, yy + 3, x + 5, yy + 9], fill=RULE)
        line = tag + " · " + txt
        assert text_w(line, BF2) <= BCOLW - 10, line
        d.text((x + 10, yy), line, font=BF2, fill=INK)
    yy += 14

# ---------------------------------------------------------------- footer
FY = 989
d.line([(MX, FY), (W - MX, FY)], fill=RULE, width=2)
center("Every story happened, or was first reported, on Thursday 19 November 2026 in some time zone. Contested claims are attributed as reported.",
       F(SANS_I, 10), FY + 5, GRAY)
center("Sources: Reuters · Associated Press · AFP · USA Today · Al Jazeera · TASS · Yonhap · UKMTO · NASA · The Hindu · BBC Sport · official statements",
       F(SANS, 9), FY + 20, GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_19.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
