#!/usr/bin/env python3
"""Generator for the make.fun news-image-20261119 entry image - v3.

Draws a one-page illustrated newspaper front page of Thursday
19 November 2026 with Pillow: masthead with a huge serif date and a
red dek, a region tab strip, a strip of the day's big numbers, three
hero panels with large drawn scenes, ten pictured mid cards, a
dot-matrix world map with numbered markers matching the pictured
stories, one-line briefs for the rest of the day, a date-check box
and a footer. Deterministic: same data, same PNG, every run.
"""
import os
from math import ceil

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
BG = (255, 253, 245)
FG = (22, 22, 22)
MUTED = (90, 90, 90)
RULEC = (40, 40, 40)
RED = (157, 2, 8)
LEADBG = (243, 238, 224)
WHT = (255, 255, 255)
MAPBG = (233, 238, 242)
LANDC = (105, 128, 152)
MARKC = (178, 34, 52)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF_I = FONT_DIR + "LiberationSerif-Italic.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_I = FONT_DIR + "LiberationSans-Italic.ttf"

MARGIN = 24
CONTENT_W = PAGE_W - 2 * MARGIN


def load_font(path, size):
    return ImageFont.truetype(path, size)


canvas = Image.new("RGB", (PAGE_W, PAGE_H), BG)
pen = ImageDraw.Draw(canvas)


def measure(txt, font):
    return pen.textlength(txt, font=font)


def fold(txt, font, limit):
    """Greedy word wrap: split txt into lines no wider than limit."""
    lines = []
    current = ""
    for word in txt.split():
        trial = word if not current else current + " " + word
        if measure(trial, font) <= limit:
            current = trial
        elif current:
            lines.append(current)
            current = word
        else:  # a single word wider than the limit still gets its own line
            lines.append(word)
            current = ""
    if current:
        lines.append(current)
    return lines


def fold_first(txt, font, first_limit, limit):
    """Word wrap where the first line has a different (smaller) limit."""
    words = txt.split()
    lines = []
    current = ""
    cap = first_limit
    for word in words:
        trial = word if not current else current + " " + word
        if measure(trial, font) <= cap:
            current = trial
        elif current:
            lines.append(current)
            current = word
            cap = limit
        else:
            lines.append(word)
            current = ""
            cap = limit
    if current:
        lines.append(current)
    return lines


def centred(txt, font, top, colour=FG):
    pen.text(((PAGE_W - measure(txt, font)) / 2, top), txt, font=font,
             fill=colour)


def text_lines(x, y, lines, font, pitch, fill):
    for line in lines:
        pen.text((x, y), line, font=font, fill=fill)
        y += pitch
    return y


# ------------------------------------------------------------- the day's news
# region keys drive the tab strip; counts are computed from this data.
REGION_ORDER = ["ASIA", "EUROPE", "MIDDLE EAST", "AMERICAS", "AFRICA",
                "OCEANIA", "GLOBAL"]
REGION_COLOURS = {
    "ASIA": (29, 111, 184), "EUROPE": (68, 86, 168),
    "MIDDLE EAST": (179, 84, 30), "AMERICAS": (46, 125, 50),
    "AFRICA": (166, 124, 0), "OCEANIA": (0, 131, 143),
    "GLOBAL": (106, 27, 154),
}

HEROES = [
    dict(num=1, region="ASIA", kicker="SHENZHEN \u00b7 SUMMIT",
         colour=(29, 78, 137), scene="summit",
         headline="Trump, Xi and Putin hold first three-way summit",
         summary="The US, Chinese and Russian leaders met for 90 minutes "
                 "and issued a \u201cDeclaration on Peace\u201d on nuclear "
                 "risk and UN reform; APEC leaders adopted the Shenzhen "
                 "Declaration.",
         source="Reuters \u00b7 AP \u00b7 Xinhua"),
    dict(num=2, region="GLOBAL", kicker="WORLDWIDE \u00b7 GAMES",
         colour=(150, 20, 90), scene="gta",
         headline="GTA VI goes on sale after 13 years",
         summary="Sensor Tower estimates day one at 24.6 million copies "
                 "and $2.36bn including pre-orders \u2014 the biggest "
                 "entertainment launch ever, about three times GTA V's "
                 "first day; Take-Two has not confirmed the figures.",
         source="Sensor Tower"),
    dict(num=3, region="AMERICAS", kicker="NEW YORK \u00b7 MARKETS",
         colour=(106, 27, 154), scene="ant",
         headline="Anthropic starts trading on Nasdaq",
         summary="The maker of the Claude AI models raised $81.3bn "
                 "pricing shares at $83 \u2014 the largest IPO on record; "
                 "Thursday's first trades set the real price.",
         source="AP"),
]

CARDS = [
    dict(num=4, region="EUROPE", kicker="THE HAGUE \u00b7 JUSTICE",
         colour=(0, 110, 100), scene="hague",
         headline="World Court: Myanmar committed genocide",
         summary="By 9 votes to 6 the ICJ found Myanmar guilty of "
                 "genocide against the Rohingya and ordered reparations.",
         source="Al Jazeera \u00b7 UN News"),
    dict(num=5, region="MIDDLE EAST", kicker="ANTALYA \u00b7 CLIMATE",
         colour=(46, 125, 50), scene="cop",
         headline="COP31 draft drops fossil fuels and $120bn aid goal",
         summary="The slimmer text has no figure for adaptation aid; "
                 "talks are due to end on Friday.",
         source="Reuters \u00b7 AFP"),
    dict(num=6, region="MIDDLE EAST", kicker="RIYADH \u00b7 WAR",
         colour=(179, 84, 30), scene="riyadh",
         headline="Saudis shoot down Houthi missiles",
         summary="Debris fell on the capital; no casualties reported.",
         source="Reuters"),
    dict(num=7, region="EUROPE", kicker="CRIMEA \u00b7 WAR",
         colour=(68, 86, 168), scene="crimea",
         headline="Ukraine hits Crimea bridge again",
         summary="Third strike in a week halts trains to Russia.",
         source="Euronews"),
    dict(num=8, region="ASIA", kicker="ODISHA \u00b7 STORM",
         colour=(29, 111, 184), scene="akvan",
         headline="Cyclone Akvan nears India's coast",
         summary="72,000 evacuated in Odisha; landfall is forecast "
                 "for Friday.",
         source="IMD"),
    dict(num=9, region="ASIA", kicker="SEOUL \u00b7 JUSTICE",
         colour=(70, 72, 84), scene="seoul",
         headline="Korea's top court clears ex-PM Han",
         summary="Han Duck-soo's martial-law conviction is overturned.",
         source="AP"),
    dict(num=10, region="AMERICAS", kicker="BOGOT\u00c1 \u00b7 LABOUR",
         colour=(146, 110, 20), scene="bogota",
         headline="Colombia's unions hold national strike",
         summary="Marches in three cities against an economic law.",
         source="Infobae"),
    dict(num=11, region="OCEANIA", kicker="CANBERRA \u00b7 ECONOMY",
         colour=(0, 131, 143), scene="canberra",
         headline="Australia's jobless rate hits 4.9%",
         summary="Highest since 2021; shares and the dollar slide.",
         source="ABC"),
    dict(num=12, region="EUROPE", kicker="GREENLAND \u00b7 SECURITY",
         colour=(40, 110, 140), scene="greenland",
         headline="Denmark backs Arctic pact with US",
         summary="Parliament approves the Greenland security deal 109\u20130.",
         source="AP"),
    dict(num=13, region="AFRICA", kicker="NAIROBI \u00b7 SPORT",
         colour=(178, 60, 40), scene="nairobi",
         headline="Marathon champion banned for doping",
         summary="Kenya's Peres Jepchirchir gets three years.",
         source="ABC"),
]

# (place, what happened, source, region) - numbered from 14 on the page.
BRIEFS = [
    ("Shenzhen", "Xi urges ban on all nuclear arms", "Al Jazeera", "ASIA"),
    ("APEC", "Albanese to Putin: \u201cEnd your war, end it now\u201d",
     "ABC", "ASIA"),
    ("Seoul", "551,864 sit Korea's big exam; flights paused for the "
              "listening test", "Sedaily", "ASIA"),
    ("Jakarta", "Asset-seizure law passes after 18 years", "Kompas", "ASIA"),
    ("Hormuz", "Iran says mines set 5 tankers ablaze", "Al Jazeera",
     "MIDDLE EAST"),
    ("Gaza", "Israel ends tank raid past truce line", "BBC", "MIDDLE EAST"),
    ("Krasnodar", "Kyiv says it hit two oil refineries", "Euronews",
     "EUROPE"),
    ("Brussels", "EU delays methane rules two years", "Euronews", "EUROPE"),
    ("London", "Van Gogh sells for a record $190.4m", "Reuters", "EUROPE"),
    ("Zurich", "Two rivals to challenge FIFA's Infantino", "ABC", "EUROPE"),
    ("Rome", "Author Corrado Augias dies at 91", "Euronews", "EUROPE"),
    ("Mogadishu", "Somalia expels UAE ambassador", "Al Jazeera", "AFRICA"),
    ("Sudan", "Court sentences absent RSF chief to death", "AP", "AFRICA"),
    ("Pretoria", "Central bank holds rate at 7.25%", "SABC", "AFRICA"),
    ("Canaries", "Record 11,000 migrants in 15 days", "Africanews",
     "EUROPE"),
    ("Florida", "Floods shut Broward, Miami schools again", "CBS",
     "AMERICAS"),
    ("Wellington", "Court: pay equity cuts broke rights law", "RNZ",
     "OCEANIA"),
    ("Tonga", "Drought emergency takes effect", "RNZ", "OCEANIA"),
    ("Cook Islands", "Cyclone Xavier weakens to category 4", "RNZ",
     "OCEANIA"),
    ("Space", "Red giant seen eating a Sun-sized star", "Nature", "GLOBAL"),
]

NUMBERS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court genocide vote"),
    ("$2.36bn", "GTA VI estimated first day (Sensor Tower)"),
    ("$81bn", "Anthropic's record IPO"),
    ("109\u20130", "Danish vote on Arctic pact"),
    ("4.9%", "Australian jobless rate"),
]

DATE_CHECK_1 = ("Every story on this page happened, or was first "
                "reported, on Thursday 19 November 2026.")
DATE_CHECK_2 = ("LEFT OUT AS OTHER DAYS' NEWS \u2014 18 NOV: EU's \u20ac45bn "
                "Ukraine loan plan \u00b7 Iran fires on Kuwait and Bahrain \u00b7 "
                "Nvidia results \u00b7 Jeffries named for US speaker \u00b7 Carney "
                "on China ties \u00b7 Anthropic's $83 IPO pricing (Wed) \u00b7 "
                "Voyager 1 one light-day out (Wed)")
FOOTER = ("Claims are attributed, not stated as fact \u00b7 Pictures and map: "
          "original, drawn in code \u00b7 Sources: Reuters, AP, AFP, BBC, "
          "Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature \u00b7 "
          "2026-11-19")


def region_counts(briefs):
    counts = {name: 0 for name in REGION_ORDER}
    for story in HEROES + CARDS:
        counts[story["region"]] += 1
    for brief in briefs:
        counts[brief[3]] += 1
    return counts


# ------------------------------------------------------------- small helpers
def paint_flag(fx, fy, fw, fh, kind):
    if kind == "cn":
        pen.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
        pen.rectangle([fx + 3, fy + 3, fx + 6, fy + 6], fill=(255, 222, 0))
    elif kind == "ru":
        third = fh // 3
        pen.rectangle([fx, fy, fx + fw, fy + third], fill=WHT)
        pen.rectangle([fx, fy + third, fx + fw, fy + 2 * third],
                      fill=(0, 57, 166))
        pen.rectangle([fx, fy + 2 * third, fx + fw, fy + fh],
                      fill=(213, 43, 30))
    elif kind == "dk":
        pen.rectangle([fx, fy, fx + fw, fy + fh], fill=(198, 12, 48))
        pen.rectangle([fx + fw // 3, fy, fx + fw // 3 + 3, fy + fh], fill=WHT)
        pen.rectangle([fx, fy + fh // 2 - 1, fx + fw, fy + fh // 2 + 2],
                      fill=WHT)
    elif kind == "gl":
        pen.rectangle([fx, fy, fx + fw, fy + fh // 2], fill=WHT)
        pen.rectangle([fx, fy + fh // 2, fx + fw, fy + fh],
                      fill=(216, 12, 24))
        cx, cy, r = fx + fh // 2, fy + fh // 2, fh // 4
        pen.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 270,
                     fill=(216, 12, 24))
        pen.pieslice([cx - r, cy - r, cx + r, cy + r], 270, 90, fill=WHT)
    else:  # us: five stripes and a blue canton
        for stripe in range(5):
            y0 = fy + stripe * fh // 5
            pen.rectangle([fx, y0, fx + fw, fy + (stripe + 1) * fh // 5],
                          fill=(178, 34, 52) if stripe % 2 == 0 else WHT)
        pen.rectangle([fx, fy, fx + fw // 2, fy + fh // 2],
                      fill=(60, 59, 110))


def draw_stamp(x, y, text, size=11, angle=-12, colour=MARKC):
    font = load_font(SANS_B, size)
    tw = measure(text, font)
    layer = Image.new("RGBA", (int(tw) + 14, size + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([1, 1, layer.width - 2, layer.height - 2],
                outline=colour + (255,), width=2)
    d.text(((layer.width - tw) / 2, 5), text, font=font,
           fill=colour + (255,))
    tilted = layer.rotate(angle, expand=True, resample=Image.BILINEAR)
    canvas.paste(tilted, (int(x), int(y)), tilted)


def number_chip(x, y, num):
    pen.ellipse([x, y, x + 17, y + 17], fill=MARKC)
    font = load_font(SANS_B, 10)
    label = str(num)
    pen.text((x + (17 - measure(label, font)) / 2, y + 3), label,
             font=font, fill=WHT)


# ------------------------------------------------------------- hero scenes
def scene_summit(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(36, 58, 104))
    pen.rectangle([x, y, x + w, y + 5], fill=(212, 175, 55))
    table_y = y + h - 34
    fracs = (0.20, 0.50, 0.80)
    kinds = ("us", "cn", "ru")
    names = ("TRUMP", "XI", "PUTIN")
    suits = ((30, 30, 34), (24, 24, 40), (34, 30, 30))
    for frac, kind in zip(fracs, kinds):
        pole_x = x + int(frac * w)
        pen.line([(pole_x, table_y - 6), (pole_x, y + 12)],
                 fill=(220, 220, 225), width=2)
        paint_flag(pole_x + 3, y + 12, 34, 23, kind)
    pen.polygon([(x + 8, table_y), (x + w - 8, table_y),
                 (x + w - 2, y + h - 3), (x + 2, y + h - 3)],
                fill=(122, 30, 42))
    pen.rectangle([x + 8, table_y, x + w - 8, table_y + 5],
                  fill=(96, 62, 38))
    plate_font = load_font(SANS_B, 9)
    for frac, name, suit in zip(fracs, names, suits):
        cx = x + int(frac * w)
        pen.ellipse([cx - 9, table_y - 34, cx + 9, table_y - 16],
                    fill=(232, 190, 150))
        pen.polygon([(cx - 14, table_y - 2), (cx + 14, table_y - 2),
                     (cx + 9, table_y - 16), (cx - 9, table_y - 16)],
                    fill=suit)
        pen.polygon([(cx - 2, table_y - 16), (cx + 2, table_y - 16),
                     (cx, table_y - 8)], fill=WHT)
        pw = measure(name, plate_font) + 12
        pen.rectangle([cx - pw / 2, table_y + 9, cx + pw / 2, table_y + 24],
                      fill=(24, 24, 30))
        pen.text((cx - measure(name, plate_font) / 2, table_y + 11),
                 name, font=plate_font, fill=WHT)


def scene_gta(x, y, w, h):
    sunset = [(247, 127, 90), (244, 110, 120), (214, 84, 150),
              (150, 66, 150), (84, 52, 130)]
    band_h = h // len(sunset) + 1
    for idx, colour in enumerate(sunset):
        pen.rectangle([x, y + idx * band_h, x + w, y + (idx + 1) * band_h],
                      fill=colour)
    sun_x, sun_y = x + int(0.40 * w), y + int(0.52 * h)
    pen.ellipse([sun_x - 20, sun_y - 20, sun_x + 20, sun_y + 20],
                fill=(255, 214, 90))
    ground = y + int(0.78 * h)
    towers = [(0.00, 30), (0.07, 44), (0.14, 24), (0.52, 36), (0.60, 50),
              (0.68, 28), (0.90, 40), (0.96, 26)]
    for frac, th in towers:
        tx = x + int(frac * w)
        pen.rectangle([tx, ground - th, tx + int(0.06 * w) + 4, ground],
                      fill=(40, 26, 66))
    pen.rectangle([x, ground, x + w, y + h], fill=(40, 26, 66))
    pen.line([(x, ground), (x + w, ground)], fill=(0, 240, 220), width=2)
    palm_x = x + int(0.10 * w)
    top_x, top_y = palm_x + 5, ground - int(0.42 * h)
    pen.line([(palm_x, ground), (top_x, top_y)], fill=(20, 14, 34), width=4)
    for ddx, ddy in ((-18, -6), (-10, -13), (0, -16), (11, -13), (19, -6),
                     (-14, 3), (16, 3)):
        pen.line([(top_x, top_y), (top_x + ddx, top_y + ddy)],
                 fill=(20, 14, 34), width=2)
    car_y = y + h - 6
    pen.polygon([(x + 18, car_y), (x + 26, car_y - 9), (x + 40, car_y - 10),
                 (x + 50, car_y - 17), (x + 72, car_y - 17),
                 (x + 84, car_y - 10), (x + 96, car_y - 9),
                 (x + 104, car_y)], fill=(16, 12, 28))
    pen.rectangle([x + 53, car_y - 16, x + 69, car_y - 11],
                  fill=(0, 240, 220))
    for wheel_x in (x + 34, x + 88):
        pen.ellipse([wheel_x - 5, car_y - 7, wheel_x + 5, car_y + 3],
                    fill=(10, 8, 20), outline=(255, 90, 180))
    vi_font = load_font(SERIF_B, 62)
    pen.text((x + w - measure("VI", vi_font) - 14, y + 6), "VI",
             font=vi_font, fill=(255, 214, 90))


def scene_ant(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(24, 40, 78))
    for gx in range(x + 24, x + w - 8, 28):
        pen.line([(gx, y + 6), (gx, y + h - 6)], fill=(38, 58, 100),
                 width=1)
    pen.text((x + 38, y + 7), "ANT", font=load_font(SERIF_B, 30), fill=WHT)
    price_font = load_font(SANS_B, 16)
    pen.text((x + w - measure("$83", price_font) - 12, y + 10), "$83",
             font=price_font, fill=(255, 214, 90))
    base = y + h - 8
    heights = (14, 22, 32, 44, 58)
    tops = []
    for idx, bar_h in enumerate(heights):
        bx = x + 18 + idx * 40
        pen.rectangle([bx, base - bar_h, bx + 24, base], fill=(64, 199, 120))
        tops.append((bx + 12, base - bar_h))
    pen.line(tops, fill=(255, 120, 90), width=3)
    lx, ly = tops[-1]
    pen.polygon([(lx + 2, ly - 6), (lx + 14, ly - 4), (lx + 3, ly + 4)],
                fill=(255, 120, 90))


# ------------------------------------------------------------- card scenes
def scene_hague(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(203, 219, 231))
    dark = (50, 55, 68)
    pen.polygon([(x + 8, y + h * 0.36), (x + 52, y + h * 0.36),
                 (x + 30, y + h * 0.07)], fill=(246, 245, 241),
                outline=dark)
    for col_x in (x + 13, x + 24, x + 35, x + 46):
        pen.rectangle([col_x, y + h * 0.40, col_x + 4, y + h * 0.78],
                      fill=dark)
    pen.rectangle([x + 6, y + h * 0.78, x + 54, y + h * 0.90], fill=dark)
    cx = x + 82
    pen.rectangle([cx - 16, y + h * 0.21, cx + 16, y + h * 0.29],
                  fill=dark)
    pen.rectangle([cx - 1, y + h * 0.18, cx + 1, y + h * 0.71], fill=dark)
    for sx in (-1, 1):
        px = cx + sx * 16
        pen.line([(px, y + h * 0.29), (px - 4, y + h * 0.57)], fill=dark,
                 width=1)
        pen.line([(px, y + h * 0.29), (px + 4, y + h * 0.57)], fill=dark,
                 width=1)
        pen.polygon([(px - 5, y + h * 0.57), (px + 5, y + h * 0.57),
                     (px, y + h * 0.71)], fill=(212, 175, 55))
    pen.rectangle([cx - 6, y + h * 0.71, cx + 6, y + h * 0.79], fill=dark)
    vote_font = load_font(SERIF_B, max(13, min(21, h - 2)))
    pen.text((x + w - measure("9\u20136", vote_font) - 8, y + 2), "9\u20136",
             font=vote_font, fill=MARKC)


def scene_cop(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(250, 224, 178))
    pen.rectangle([x + 14, y + 3, x + 96, y + h - 3], fill=WHT,
                  outline=(120, 120, 120))
    for row in range(3):
        ly = y + 8 + row * 6
        if ly < y + h - 2:
            pen.line([(x + 20, ly), (x + 90, ly)], fill=(170, 170, 170),
                     width=1)
    ff_font = load_font(SANS_B, 11)
    pen.text((x + 20, y + 6), "FOSSIL FUELS", font=ff_font, fill=FG)
    pen.line([(x + 18, y + 12), (x + 92, y + 12)], fill=MARKC, width=2)
    draw_stamp(x + w - 58, y + 3, "CUT", size=11, angle=-12)


def scene_riyadh(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(24, 32, 64))
    pen.ellipse([x + 8, y + 3, x + 18, y + 13], fill=(240, 230, 180))
    pen.ellipse([x + 12, y + 2, x + 21, y + 12], fill=(24, 32, 64))
    for sx, ex in ((30, 90), (52, 128), (74, 158)):
        pen.line([(x + sx, y + h - 3), (x + (sx + ex) // 2, y + 1),
                  (x + ex, y + 4)], fill=(255, 170, 80), width=2)
        for ddx, ddy in ((-4, 0), (4, 0), (0, -4), (0, 4)):
            pen.line([(x + ex, y + 4), (x + ex + ddx, y + 4 + ddy)],
                     fill=(255, 214, 90), width=1)
    pen.rectangle([x, y + h - 3, x + w, y + h], fill=(12, 16, 34))


def scene_crimea(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(198, 214, 230))
    pen.rectangle([x, y + h - 9, x + w, y + h], fill=(60, 110, 150))
    dark = (40, 44, 54)
    mid = y + h - 8
    pen.rectangle([x + 34, y + 3, x + 37, mid], fill=dark)
    pen.rectangle([x + w - 37, y + 3, x + w - 34, mid], fill=dark)
    pen.line([(x + 35, y + 3), (x + w // 2, mid - 3)], fill=dark, width=1)
    pen.line([(x + w - 35, y + 3), (x + w // 2 + 6, mid - 2)], fill=dark,
             width=1)
    pen.line([(x + 3, mid - 3), (x + w // 2 - 3, mid - 3)], fill=dark, width=2)
    pen.line([(x + w // 2 + 7, mid - 2), (x + w - 3, mid)], fill=dark, width=2)
    fx, fy = x + w // 2 + 2, mid - 4
    pen.polygon([(fx, fy - 4), (fx + 1, fy), (fx + 5, fy),
                 (fx + 2, fy + 1), (fx + 3, fy + 5), (fx, fy + 3),
                 (fx - 3, fy + 5), (fx - 2, fy + 1), (fx - 5, fy),
                 (fx - 1, fy)], fill=(244, 140, 40))


def scene_akvan(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(96, 116, 134))
    pen.rectangle([x, y + h - 8, x + w, y + h], fill=(52, 84, 110))
    cx, cy = x + 34, y + h // 2
    for box, start, end in ((int(h * 0.9), 20, 200), (int(h * 0.62), 200, 380),
                            (int(h * 0.36), 40, 240)):
        pen.arc([cx - box, cy - box // 2, cx + box, cy + box // 2],
                start=start, end=end, fill=WHT, width=2)
    for idx in range(6):
        rx = x + 78 + idx * 16
        pen.line([(rx, y + h * 0.15), (rx - 4, y + h * 0.45)],
                 fill=(170, 195, 215), width=2)
        pen.line([(rx, y + h * 0.55), (rx - 4, y + h * 0.85)],
                 fill=(170, 195, 215), width=2)


def scene_seoul(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(232, 232, 226))
    cx = x + 44
    dark = (70, 72, 84)
    pen.polygon([(cx - 30, y + h * 0.31), (cx + 30, y + h * 0.31),
                 (cx, y + 1)], fill=dark)
    for col_x in (cx - 24, cx - 8, cx + 8, cx + 24):
        pen.rectangle([col_x - 3, y + h * 0.34, col_x + 3, y + h * 0.72],
                      fill=dark)
    pen.rectangle([cx - 34, y + h * 0.72, cx + 34, y + h * 0.86], fill=dark)
    draw_stamp(x + w - 108, y + 5, "OVERTURNED", size=10, angle=-10)


def scene_bogota(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    for bx, stripes in ((30, ((250, 200, 40), (40, 70, 160), (200, 40, 40))),
                        (96, ((250, 200, 40), (40, 70, 160), (200, 40, 40)))):
        pen.line([(x + bx + 9, y + h), (x + bx + 9, y + 5)],
                 fill=(90, 90, 90), width=2)
        for si, sc in enumerate(stripes):
            pen.rectangle([x + bx, y + 5 + si * 4, x + bx + 18,
                           y + 9 + si * 4], fill=sc)
    for row, ry in enumerate((y + h - 13, y + h - 8)):
        for idx in range(11):
            hx = x + 8 + idx * 16 + (8 if row else 0)
            pen.ellipse([hx, ry, hx + 6, ry + 6], fill=(50, 44, 40))


def scene_canberra(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    base = y + h - 3
    pen.rectangle([x + 16, base - int(h * 0.55), x + 44, base],
                  fill=(150, 150, 150))
    pen.rectangle([x + 56, base - int(h * 0.75), x + 84, base], fill=MARKC)
    lab_font = load_font(SANS_B, 9)
    pen.text((x + 22, y + 1), "4.7", font=lab_font, fill=MUTED)
    big_font = load_font(SERIF_B, max(13, min(19, h - 3)))
    pen.text((x + 96, y + 1), "4.9%", font=big_font, fill=MARKC)
    pen.line([(x + 8, base), (x + w - 8, base)], fill=FG, width=1)


def scene_greenland(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(210, 225, 235))
    fh = min(20, h - 8)
    for fx, kind in ((24, "dk"), (78, "gl")):
        pen.line([(x + fx, y + h - 3), (x + fx, y + 4)], fill=(70, 70, 70),
                 width=2)
        paint_flag(x + fx + 2, y + 4, int(fh * 1.5), fh, kind)
    vote_font = load_font(SERIF_B, max(13, min(19, h - 4)))
    pen.text((x + w - measure("109\u20130", vote_font) - 8, y + 2),
             "109\u20130", font=vote_font, fill=FG)


def scene_nairobi(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(178, 60, 40))
    pen.line([(x + 6, y + h - 6), (x + w - 6, y + h - 6)], fill=WHT, width=1)
    for cx in range(x + w - 34, x + w - 10, 6):
        for cy in range(y + 4, y + h - 8, 6):
            if ((cx + cy) // 6) % 2 == 0:
                pen.rectangle([cx, cy, cx + 6, cy + 6], fill=WHT)
    draw_stamp(x + 12, y + 5, "BANNED", size=11, angle=-10,
               colour=(255, 235, 220))


CARD_SCENES = {
    "hague": scene_hague, "cop": scene_cop, "riyadh": scene_riyadh,
    "crimea": scene_crimea, "akvan": scene_akvan, "seoul": scene_seoul,
    "bogota": scene_bogota, "canberra": scene_canberra,
    "greenland": scene_greenland, "nairobi": scene_nairobi,
}
HERO_SCENES = {"summit": scene_summit, "gta": scene_gta, "ant": scene_ant}


# ------------------------------------------------------------- the map
# Land as (first column, run length) spans per grid row, 81 x 18 grid.
LAND_RUNS = [
    [(3, 4), (11, 6), (26, 4), (47, 14), (64, 15)],
    [(1, 8), (10, 12), (25, 4), (37, 1), (43, 4), (48, 32)],
    [(9, 14), (39, 2), (41, 6), (47, 32)],
    [(8, 16), (38, 8), (47, 10), (57, 11), (71, 3)],
    [(8, 16), (38, 2), (42, 2), (44, 4), (48, 3), (51, 5), (58, 10),
     (68, 2), (70, 3)],
    [(9, 12), (13, 5), (37, 10), (47, 3), (50, 3), (53, 3), (56, 3),
     (59, 8)],
    [(12, 5), (36, 12), (48, 4), (56, 4), (60, 3), (63, 4), (67, 1),
     (68, 2)],
    [(14, 2), (36, 12), (48, 3), (56, 3), (59, 4), (67, 2)],
    [(23, 6), (36, 13), (49, 2), (57, 1), (59, 3), (62, 4)],
    [(23, 7), (37, 10), (60, 9)],
    [(23, 8), (37, 9), (62, 6), (69, 3)],
    [(24, 8), (38, 7), (66, 7)],
    [(24, 7), (38, 6), (46, 1), (64, 11)],
    [(25, 5), (38, 4), (63, 11)],
    [(25, 4), (38, 2), (67, 7)],
    [(25, 2), (78, 3)],
    [(25, 2), (77, 2)],
    [(25, 1)],
]

# (story number, grid column, grid row) for the 13 pictured stories.
MAP_MARKS = [
    (1, 67, 6), (2, 20, 5), (3, 23, 3), (4, 43, 2), (5, 50, 4),
    (6, 51, 6), (7, 48, 3), (8, 63, 8), (9, 68, 4), (10, 26, 10),
    (11, 73, 14), (12, 28, 1), (13, 49, 8),
]


def paint_map(x, y, w, h):
    pen.rectangle([x, y, x + w, y + 17], fill=RULEC)
    pen.text((x + 7, y + 3), "WHERE IT HAPPENED",
             font=load_font(SANS_B, 11), fill=WHT)
    pen.rectangle([x, y + 17, x + w, y + h], fill=MAPBG)
    grid_x = x + 9
    step_x = (w - 18) / 81
    step_y = min((h - 40) / 18, 7.5)
    grid_y = y + 22 + max(0, (h - 40 - 18 * step_y) / 2)
    r = min(step_x, step_y) * 0.40
    for row_idx, runs in enumerate(LAND_RUNS):
        for first_col, run_len in runs:
            for col in range(first_col, first_col + run_len):
                cx = grid_x + col * step_x
                cy = grid_y + row_idx * step_y
                pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LANDC)
    num_font = load_font(SANS_B, 8)
    for num, col, row in MAP_MARKS:
        cx = grid_x + col * step_x
        cy = grid_y + row * step_y
        pen.ellipse([cx - 6.5, cy - 6.5, cx + 6.5, cy + 6.5], fill=WHT)
        pen.ellipse([cx - 5.4, cy - 5.4, cx + 5.4, cy + 5.4], fill=MARKC)
        label = str(num)
        pen.text((cx - measure(label, num_font) / 2, cy - 4.5), label,
                 font=num_font, fill=WHT)
    pen.text((x + 8, y + h - 13),
             "Red numbers 1\u201313 mark the pictured stories",
             font=load_font(SANS, 9), fill=MUTED)


# ------------------------------------------------------------- layout maths
F_KICK = load_font(SANS_B, 11)
F_HERO_HEAD = load_font(SERIF_B, 30)
F_HERO_BODY = load_font(SANS, 14)
F_CARD_HEAD = load_font(SERIF_B, 16)
F_CARD_BODY = load_font(SANS, 13)
F_BRIEF = load_font(SANS, 12)
F_BRIEF_B = load_font(SANS_B, 12)
F_DC = load_font(SANS_B, 10)

HERO_W = (CONTENT_W - 2 * 12) // 3          # 317
HERO_TEXT_W = HERO_W - 16                   # 301
CARD_W = (CONTENT_W - 4 * 10) // 5          # 187
CARD_TEXT_W = CARD_W - 10                   # 177
BRIEF_AREA_W = CONTENT_W - 280 - 12         # 684, right of the map
BRIEF_COL_W = (BRIEF_AREA_W - 16) // 2      # 334
BRIEF_NUM_W = 24
MAP_W = 280


def hero_height(story, scene_h):
    head_lines = len(fold(story["headline"], F_HERO_HEAD, HERO_TEXT_W))
    body_lines = len(fold(story["summary"], F_HERO_BODY, HERO_TEXT_W))
    return (5 + 6 + scene_h + 5 + 13 + 2 + head_lines * 33 + 3
            + body_lines * 16.5 + 3 + 12 + 5)


def card_height(card, scene_h):
    head_lines = len(fold(card["headline"], F_CARD_HEAD, CARD_TEXT_W))
    body = card["summary"] + " \u2014 " + card["source"]
    body_lines = len(fold(body, F_CARD_BODY, CARD_TEXT_W))
    return (25 + scene_h + head_lines * 18 + body_lines * 15.5)


def brief_line_count(brief, col_w):
    place, what, source = brief[0], brief[1], brief[2]
    place_w = measure(place + " \u2014 ", F_BRIEF_B)
    text = what + " \u00b7 " + source
    lines = fold_first(text, F_BRIEF,
                       col_w - BRIEF_NUM_W - place_w, col_w)
    return len(lines)


def briefs_height(briefs):
    half = (len(briefs) + 1) // 2
    cols = (briefs[:half], briefs[half:])
    lines = max(sum(brief_line_count(b, BRIEF_COL_W) for b in col)
                for col in cols)
    return 17 + 3 + lines * 16 + 2, lines


def date_check_narrow_height():
    """The date-check box sits under the map in the left column."""
    inner_w = MAP_W - 20
    first_off = measure("DATE CHECK", F_DC) + 16
    lines = fold_first(DATE_CHECK_1, F_DC, inner_w - first_off, inner_w)
    lines += fold(DATE_CHECK_2, F_DC, inner_w)
    return 4 + len(lines) * 12 + 3, len(lines)


def compute_layout():
    """Pick the brief count and scene heights that fit the page.

    Priority: keep as many briefs as possible (cut from the bottom of
    the list, keeping at least 28 stories), then the largest hero
    scenes, then the largest card scenes. Typography never shrinks.
    The bottom section is as tall as the taller of its two columns:
    the briefs (right) and the map + date-check stack (left).
    Returns (briefs, scene_h, card_scene, heights dict)."""
    hero_top = 162
    date_h, date_lines = date_check_narrow_height()
    min_left = 100 + 6 + date_h
    for cut in range(0, len(BRIEFS) - 15 + 1):
        briefs = BRIEFS[:len(BRIEFS) - cut] if cut else list(BRIEFS)
        briefs_h, brief_lines = briefs_height(briefs)
        bottom_h = max(briefs_h, min_left)
        for card_floor in (18, 14):
            for scene_h in (108, 100, 92, 84, 80, 76, 72):
                hero_h = ceil(max(hero_height(s, scene_h) for s in HEROES))
                for card_scene in (30, 26, 22, 18, 14):
                    if card_scene < card_floor:
                        continue
                    row1 = ceil(max(card_height(c, card_scene)
                                    for c in CARDS[:5]))
                    row2 = ceil(max(card_height(c, card_scene)
                                    for c in CARDS[5:]))
                    cards_h = row1 + 7 + row2
                    end = (hero_top + hero_h + 5 + cards_h + 5 + bottom_h
                           + 3 + 12)
                    if end <= PAGE_H:
                        heights = dict(hero_h=hero_h, row1=row1, row2=row2,
                                       cards_h=cards_h, bottom_h=bottom_h,
                                       brief_lines=brief_lines,
                                       date_h=date_h,
                                       date_lines=date_lines, end=end)
                        return briefs, scene_h, card_scene, heights
    raise AssertionError("layout does not fit even fully flexed")


# ------------------------------------------------------------- the page
def build_page():
    briefs, scene_h, card_scene, lay = compute_layout()
    counts = region_counts(briefs)
    total = len(HEROES) + len(CARDS) + len(briefs)
    print("stories:", total, "| briefs used:", len(briefs),
          "| hero scene h:", scene_h, "| card scene h:", card_scene,
          "| layout:", lay)

    # ---- masthead
    pen.text((MARGIN, 5), "THE WORLD IN ONE DAY", font=load_font(SANS_B, 12),
             fill=MUTED)
    right = "%d STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY" % total
    pen.text((PAGE_W - MARGIN - measure(right, load_font(SANS_B, 12)), 5),
             right, font=load_font(SANS_B, 12), fill=MUTED)
    pen.line([(MARGIN, 22), (PAGE_W - MARGIN, 22)], fill=RULEC, width=2)
    centred("Thursday 19 November 2026", load_font(SERIF_B, 44), 26)
    centred("Trump, Xi and Putin share one table \u00b7 The World Court "
            "finds genocide in Myanmar \u00b7 GTA VI's record first day",
            load_font(SERIF_I, 15), 71, RED)
    pen.line([(MARGIN, 90), (PAGE_W - MARGIN, 90)], fill=RULEC, width=1)

    # ---- region tab strip
    tab_y, tab_h = 93, 17
    seg_w = CONTENT_W / len(REGION_ORDER)
    tab_font = load_font(SANS_B, 11)
    for idx, name in enumerate(REGION_ORDER):
        x0 = MARGIN + idx * seg_w
        pen.rectangle([x0 + 1, tab_y, x0 + seg_w - 1, tab_y + tab_h],
                      fill=REGION_COLOURS[name])
        label = "%s %d" % (name, counts[name])
        pen.text((x0 + (seg_w - measure(label, tab_font)) / 2, tab_y + 2),
                 label, font=tab_font, fill=WHT)

    # ---- numbers strip
    num_y, num_h = 114, 42
    pen.rectangle([MARGIN, num_y, PAGE_W - MARGIN, num_y + num_h],
                  fill=LEADBG)
    cell_w = CONTENT_W / len(NUMBERS)
    fig_font = load_font(SERIF_B, 20)
    lab_font = load_font(SANS, 9)
    for idx, (fig, lab) in enumerate(NUMBERS):
        cx = MARGIN + idx * cell_w + 8
        pen.text((cx, num_y + 1), fig, font=fig_font, fill=RED)
        text_lines(cx, num_y + 23, fold(lab, lab_font, cell_w - 14),
                   lab_font, 9.5, (45, 45, 45))

    # ---- hero panels
    hero_y = 162
    hero_h = lay["hero_h"]
    for idx, story in enumerate(HEROES):
        x0 = MARGIN + idx * (HERO_W + 12)
        pen.rectangle([x0, hero_y, x0 + HERO_W, hero_y + hero_h],
                      fill=LEADBG)
        pen.rectangle([x0, hero_y, x0 + HERO_W, hero_y + 5],
                      fill=story["colour"])
        HERO_SCENES[story["scene"]](x0 + 8, hero_y + 11, HERO_TEXT_W, scene_h)
        number_chip(x0 + 12, hero_y + 15, story["num"])
        tx = x0 + 8
        yy = hero_y + 11 + scene_h + 5
        pen.text((tx, yy), story["kicker"], font=F_KICK,
                 fill=story["colour"])
        yy += 15
        yy = text_lines(tx, yy, fold(story["headline"], F_HERO_HEAD,
                                     HERO_TEXT_W), F_HERO_HEAD, 33, FG)
        yy += 3
        yy = text_lines(tx, yy, fold(story["summary"], F_HERO_BODY,
                                     HERO_TEXT_W), F_HERO_BODY, 16.5,
                        (45, 45, 45))
        assert yy <= hero_y + hero_h - 14, (story["headline"], yy)
        pen.text((tx, hero_y + hero_h - 16), "\u2014 " + story["source"],
                 font=load_font(SANS_I, 11), fill=MUTED)

    # ---- pictured mid cards, two rows of five
    cards_y = hero_y + hero_h + 5
    row_heights = (lay["row1"], lay["row2"])
    for row_idx in range(2):
        row_y = cards_y + (row_heights[0] + 7 if row_idx else 0)
        row_h = row_heights[row_idx]
        for col_idx in range(5):
            card = CARDS[row_idx * 5 + col_idx]
            x0 = MARGIN + col_idx * (CARD_W + 10)
            pen.rectangle([x0, row_y, x0 + CARD_W, row_y + row_h],
                          fill=LEADBG)
            pen.rectangle([x0, row_y, x0 + CARD_W, row_y + 4],
                          fill=card["colour"])
            CARD_SCENES[card["scene"]](x0 + 5, row_y + 5, CARD_TEXT_W,
                                       card_scene)
            number_chip(x0 + 7, row_y + 7, card["num"])
            tx = x0 + 5
            yy = row_y + 5 + card_scene + 3
            pen.text((tx, yy), card["kicker"],
                     font=load_font(SANS_B, 10), fill=card["colour"])
            yy += 12
            yy = text_lines(tx, yy, fold(card["headline"], F_CARD_HEAD,
                                         CARD_TEXT_W), F_CARD_HEAD, 18, FG)
            yy += 1
            body = card["summary"] + " \u2014 " + card["source"]
            yy = text_lines(tx, yy, fold(body, F_CARD_BODY, CARD_TEXT_W),
                            F_CARD_BODY, 15.5, (45, 45, 45))
            assert yy <= row_y + row_h, (card["headline"], yy)

    # ---- bottom: map + date-check stack (left), briefs (right)
    bot_y = cards_y + lay["cards_h"] + 5
    bot_h = lay["bottom_h"]
    date_h = lay["date_h"]
    map_h = bot_h - 6 - date_h
    paint_map(MARGIN, bot_y, MAP_W, map_h)
    dc_y = bot_y + map_h + 6
    pen.rectangle([MARGIN, dc_y, MARGIN + MAP_W, dc_y + date_h],
                  outline=MARKC, width=2)
    ix = MARGIN + 10
    yy = dc_y + 4
    pen.text((ix, yy), "DATE CHECK", font=F_DC, fill=MARKC)
    chk_x = ix + measure("DATE CHECK", F_DC) + 5
    pen.line([(chk_x, yy + 5), (chk_x + 3, yy + 9), (chk_x + 9, yy + 1)],
             fill=MARKC, width=2)
    first_off = measure("DATE CHECK", F_DC) + 16
    lines = fold_first(DATE_CHECK_1, F_DC, MAP_W - 20 - first_off,
                       MAP_W - 20)
    pen.text((ix + first_off, yy), lines[0], font=F_DC, fill=FG)
    yy = text_lines(ix, yy + 12, lines[1:], F_DC, 12, FG)
    yy = text_lines(ix, yy, fold(DATE_CHECK_2, F_DC, MAP_W - 20),
                    F_DC, 12, FG)
    assert yy <= dc_y + date_h, (yy, dc_y + date_h)
    bx = MARGIN + MAP_W + 12
    pen.rectangle([bx, bot_y, bx + BRIEF_AREA_W, bot_y + 17], fill=RULEC)
    pen.text((bx + 7, bot_y + 2), "ALSO ON THURSDAY 19 NOVEMBER 2026",
             font=load_font(SANS_B, 12), fill=WHT)
    half = (len(briefs) + 1) // 2
    for col_idx, col in enumerate((briefs[:half], briefs[half:])):
        cx = bx + col_idx * (BRIEF_COL_W + 16)
        yy = bot_y + 22
        for off, brief in enumerate(col):
            num = 14 + col_idx * half + off
            place, what, source = brief[0], brief[1], brief[2]
            pen.text((cx, yy), str(num), font=F_BRIEF_B, fill=MARKC)
            place_txt = place + " \u2014 "
            pen.text((cx + BRIEF_NUM_W, yy), place_txt, font=F_BRIEF_B,
                     fill=FG)
            place_w = measure(place_txt, F_BRIEF_B)
            text = what + " \u00b7 " + source
            lines = fold_first(text, F_BRIEF,
                               BRIEF_COL_W - BRIEF_NUM_W - place_w,
                               BRIEF_COL_W)
            pen.text((cx + BRIEF_NUM_W + place_w, yy), lines[0],
                     font=F_BRIEF, fill=FG)
            for extra in lines[1:]:
                yy += 16
                pen.text((cx, yy), extra, font=F_BRIEF, fill=FG)
            yy += 16
        assert yy - 16 + 12 <= bot_y + bot_h, (col_idx, yy)

    # ---- footer
    foot_y = bot_y + bot_h + 3
    pen.line([(MARGIN, foot_y), (PAGE_W - MARGIN, foot_y)], fill=RULEC,
             width=1)
    centred(FOOTER, load_font(SANS_I, 10), foot_y + 3, MUTED)
    print("page end:", foot_y + 13, "of", PAGE_H)
    assert foot_y + 13 <= PAGE_H

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png")
    canvas.save(out_path, optimize=True)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build_page()
