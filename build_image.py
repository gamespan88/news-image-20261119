#!/usr/bin/env python3
"""Generator for the make.fun news-image-20261119 entry image.

Draws a one-page newspaper digest of Thursday 19 November 2026 with
Pillow: stories in 7 regional sections, three drawn lead scenes
(the Shenzhen trilateral, the Hague genocide ruling, GTA VI launch
night), a pictured mid-card row, a dot-matrix world map, a Day in
Numbers panel, a UTC timeline, a date-check stamp and strip.
Deterministic: same data, same PNG, every run.
"""
import os
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
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_I = FONT_DIR + "LiberationSans-Italic.ttf"

MARGIN = 26
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


def centred(txt, font, top, colour=FG):
    pen.text(((PAGE_W - measure(txt, font)) / 2, top), txt, font=font, fill=colour)


# ------------------------------------------------------------- the day's news
LEAD_STORIES = [
    ("SHENZHEN · A FIRST IN HISTORY", (29, 78, 137),
     "Trump, Xi & Putin sit down together",
     "The US, Chinese and Russian leaders met for 90 minutes at Kylin "
     "Villa — the first three-way summit ever held. They issued a "
     "'Declaration on Peace' on nuclear risk and UN reform; APEC "
     "leaders adopted the Shenzhen Declaration. (AP/AFP)"),
    ("THE HAGUE · WORLD COURT RULING", (0, 110, 100),
     "World Court rules Myanmar committed genocide",
     "The International Court of Justice ruled 9–6 that Myanmar "
     "committed genocide against the Rohingya and ordered "
     "reparations. (Al Jazeera/UN News)"),
    ("GTA VI · LAUNCH DAY", (150, 20, 90),
     "The world's biggest game lands",
     "Rockstar's Grand Theft Auto VI went on sale worldwide on "
     "Thursday — and by evening Sensor Tower estimated day one at "
     "24.6 million copies and $2.36bn including pre-orders: the "
     "biggest entertainment launch ever, about three times GTA V's "
     "first day. Take-Two has not confirmed the figures. "
     "(Sensor Tower)"),
]

SECTIONS = [
    ("ASIA-PACIFIC", (29, 111, 184), [
        ("Xi opens the APEC plenary",
         "China pledged $20m for APEC cooperation and a new Asia-Pacific studies centre in Shenzhen. (AP)"),
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
    ("EUROPE & UKRAINE", (68, 86, 168), [
        ("Kerch Bridge hit for a third time in a week",
         "Night strike on the railway section halted traffic; a 227-metre span fell on 17 Nov. (Reuters)"),
        ("Russian strikes kill four in central Odesa",
         "Three strikes on the centre; a market hit in Zlatopol injured 11; Naftogaz sites attacked."),
        ("Europe's coalition gathers in Berlin",
         "30+ leaders with Zelensky as the €45bn loan plan targeted Kyiv's €70bn funding gap."),
        ("Britain pledges 1,000 cruise missiles",
         "Reported as the allies met in Berlin to close Kyiv's funding and air-defence gaps."),
    ]),
    ("MIDDLE EAST", (179, 84, 30), [
        ("Tanker struck off Oman at Hormuz",
         "A projectile hit the engine room 6 nautical miles north of Khasab, Oman (UKMTO 212)."),
        ("Debris damages Saudi PIF tower",
         "Debris from an intercepted Houthi rocket struck Riyadh's PIF tower; the all-clear followed."),
        ("Israeli tanks push west of Gaza's Yellow Line",
         "First ground push since the ceasefire, near Nuseirat and Bureij; medics reported 3 killed."),
        ("IEA: Hormuz is the gravest energy threat ever seen",
         "The agency called the crisis the biggest energy-security threat it has ever recorded."),
    ]),
    ("AMERICAS", (46, 125, 50), [
        ("Trump tells Americans to 'relax'",
         "He called the bank, Microsoft and air-traffic failures unrelated; Rubio saw no link. (AP)"),
        ("218 signatures force an Epstein files vote",
         "The discharge petition hit 218 as the FAA lifted a nationwide ground stop."),
        ("US & Venezuela restore military ties",
         "Announced by Defense Secretary Hegseth on a visit to Caracas."),
        ("Lula courts investors for Brazil's rare earths",
         "US trade is now just 9.2% of Brazil's total; Canada pledged $400m for forests."),
        ("Pastor convicted over Haiti president's killing",
         "A Miami court convicted him over the 2021 assassination of President Jovenel Moïse."),
    ]),
    ("AFRICA", (166, 124, 0), [
        ("Nigeria's Senate demands answers for 37 dead miners",
         "Lawmakers sought accountability over artisanal miners who died in custody in Minna. (AFP)"),
        ("Dangote refinery IPO upsized to $2.1bn",
         "Demand near $4.5bn lifted the offer from $1.62bn — among Africa's largest listings."),
    ]),
    ("OCEANIA", (0, 131, 143), [
        ("England take the ODI series in Hobart",
         "A 97-run win in the decider sealed the one-day series 2–1 over Australia. (BBC Sport)"),
        ("Canberra holds the line to a silent Voyager",
         "Confirmed by carrier signal alone: no data since 14 Nov; commands take a day each way."),
    ]),
    ("CLIMATE · TECH · SPORT · CULTURE", (106, 27, 154), [
        ("COP31 deadlocked: 21 issues still open",
         "Ministers launched the second Global Stocktake; finance and fossil fuels unresolved. (Reuters)"),
        ("Anthropic's $81.3bn IPO is history's largest",
         "Priced at $83 (ticker ANT), the raise values the AI firm at $1.5 trillion."),
        ("Markets slide; gold sinks to a 14-month low",
         "S&P fell a fifth day; gold lost 3.6% to $3,726, Brent near $92, Bitcoin $63,479."),
        ("Vinícius hat-trick as Brazil rout Singapore 7–0",
         "Three first-half goals from Vinícius headlined the friendly rout."),
    ]),
]
LEFT_COL = [s[0] for s in SECTIONS[:3]]
RIGHT_COL = [s[0] for s in SECTIONS[3:]]
SECTION_BY_NAME = {name: (colour, stories) for name, colour, stories in SECTIONS}

BRIEF_ITEMS = [
    ("SHENZHEN", "Putin backs the draft Shenzhen Declaration"),
    ("APEC", "CEO Summit issues its first-ever Shenzhen Initiative"),
    ("SEOUL", "Lee & Putin chat 10 minutes at the welcome banquet"),
    ("HONG KONG", "John Lee hails five APEC outcomes; Chile deal signed"),
    ("MANILA", "Envoy: 'biggest trade deal' unsigned; 12.5% tariff stands"),
    ("APEC", "Trump champions US economy, opposes global AI rules"),
    ("BRUSSELS", "EU–UK draft drops the words 'trusted partnership'"),
    ("NUCLEAR", "New START's expiry hangs over the Shenzhen talks"),
    ("COP31", "Adaptation Fund pledges total just $50.2m"),
    ("COP31", "75 countries back the '35x35' electrification push"),
    ("COP31", "Four nations unveil fossil-fuel phaseout roadmaps"),
    ("US", "Emergency Supreme Court filing over Venezuelan TPS"),
    ("TECH", "IEA: datacentre emissions to rise 70% by 2030"),
    ("FOOTBALL", "Chelsea edge PSG 1–0 in Women's Champions League"),
    ("FOOTBALL", "City, Real Madrid & Juventus also reach knockouts"),
    ("SPORT", "Marathon champion Jepchirchir banned over doping"),
    ("AUCTION", "A Van Gogh sells for a record $190.4 million"),
    ("UGANDA", "Landslide survivors seek justice at the UN"),
]

NUMBER_ITEMS = [
    ("$2.36bn", "GTA VI's estimated first-day sales (Sensor Tower)"),
    ("1st", "first US–China–Russia summit ever — 90 min in Shenzhen"),
    ("$81.3bn", "raised by Anthropic's IPO, the largest ever recorded"),
    ("72,000", "people evacuated in Odisha as Cyclone Akvan nears landfall"),
    ("1,000", "long-range cruise missiles pledged by Britain to Ukraine"),
    ("$190.4m", "record auction price for a Van Gogh, set on Thursday"),
]

# Pictured mid cards: (colour, headline, summary, source tag, scene key).
MID_CARDS = [
    ((106, 27, 154),
     "Anthropic raises $81.3bn in a record IPO",
     "Priced at $83 a share; Nasdaq debut on Thursday",
     "(AP)", "ipo"),
    ((46, 125, 50),
     "COP31 draft drops fossil-fuel phase-out",
     "Antalya text sets a $120bn adaptation goal",
     "(Reuters/AFP)", "cop"),
    ((179, 84, 30),
     "Houthi missiles downed over Riyadh",
     "Debris fell on the capital, the Saudi-led coalition said",
     "(Reuters)", "gulf"),
    ((29, 111, 184),
     "Cyclone Akvan forces mass evacuations",
     "72,000 moved in Odisha; landfall due Friday",
     "(IMD)", "cyclone"),
    ((29, 111, 184),
     "Court overturns ex-PM Han's conviction",
     "Seoul court quashes Han Duck-soo's martial-law case",
     "(AP)", "seoul"),
    ((68, 86, 168),
     "Kerch Bridge hit third time in a week",
     "Rail traffic halted after the Crimea strike",
     "(Euronews)", "bridge"),
]

DATE_CHECK_LINES = [
    "LEFT OUT AS OTHER DAYS' NEWS — 18 NOV: EU's €45bn Ukraine loan "
    "plan · Iran fires on Kuwait & Bahrain · Nvidia results",
    "Jeffries named for US speaker · Anthropic's $83 IPO pricing · "
    "Voyager 1 one light-day out",
]

STORY_TOTAL = (len(LEAD_STORIES)
               + sum(len(stories) for _, _, stories in SECTIONS)
               + len(BRIEF_ITEMS)
               + len(MID_CARDS))
print("story count:", STORY_TOTAL)
assert STORY_TOTAL == 54, STORY_TOTAL


# ------------------------------------------------------------- lead scenes
def paint_flag(fx, fy, fw, fh, kind):
    if kind == "cn":
        pen.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
        pen.rectangle([fx + 3, fy + 3, fx + 6, fy + 6], fill=(255, 222, 0))
    elif kind == "ru":
        third = fh // 3
        pen.rectangle([fx, fy, fx + fw, fy + third], fill=WHT)
        pen.rectangle([fx, fy + third, fx + fw, fy + 2 * third], fill=(0, 57, 166))
        pen.rectangle([fx, fy + 2 * third, fx + fw, fy + fh], fill=(213, 43, 30))
    else:  # us: five stripes and a blue canton
        for stripe in range(5):
            y0 = fy + stripe * fh // 5
            pen.rectangle([fx, y0, fx + fw, fy + (stripe + 1) * fh // 5],
                          fill=(178, 34, 52) if stripe % 2 == 0 else WHT)
        pen.rectangle([fx, fy, fx + fw // 2, fy + fh // 2], fill=(60, 59, 110))


def paint_summit(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(38, 62, 110))
    pen.rectangle([x + 4, y + 6, x + w - 4, y + 21], fill=(212, 175, 55))
    pen.rectangle([x + 4, y + 9, x + w - 4, y + 11], fill=(38, 62, 110))
    table_y = y + h - 46
    pen.rectangle([x + 4, table_y + 10, x + w - 4, y + h - 4],
                  fill=(140, 32, 44))
    flag_spots = [(0.16, "us"), (0.47, "cn"), (0.78, "ru")]
    for frac, kind in flag_spots:
        pole_x = x + int(frac * w)
        pen.line([(pole_x, table_y), (pole_x, y + 27)], fill=(220, 220, 225),
                 width=2)
        paint_flag(pole_x + 2, y + 27, 26, 19, kind)
    pen.rectangle([x + 5, table_y, x + w - 5, table_y + 9], fill=(96, 62, 38))
    pen.rectangle([x + 9, table_y + 9, x + 13, table_y + 14], fill=(70, 45, 28))
    pen.rectangle([x + w - 13, table_y + 9, x + w - 9, table_y + 14],
                  fill=(70, 45, 28))
    leaders = [(0.17, (30, 30, 34)), (0.48, (24, 24, 40)), (0.79, (34, 30, 30))]
    for frac, suit in leaders:
        cx = x + int(frac * w)
        pen.ellipse([cx - 7, table_y - 26, cx + 7, table_y - 12],
                    fill=(232, 190, 150))
        pen.polygon([(cx - 11, table_y), (cx + 11, table_y),
                     (cx + 7, table_y - 12), (cx - 7, table_y - 12)],
                    fill=suit)
        pen.polygon([(cx - 2, table_y - 12), (cx + 2, table_y - 12),
                     (cx, table_y - 5)], fill=WHT)


def paint_hague(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(203, 219, 231))
    pen.ellipse([x + w - 30, y + 10, x + w - 12, y + 28], fill=(244, 164, 40))
    pen.rectangle([x + 8, y + 62, x + w - 8, y + h - 28],
                  fill=(246, 245, 241), outline=(70, 74, 84), width=2)
    pen.polygon([(x + 4, y + 62), (x + w - 4, y + 62), (x + w // 2, y + 36)],
                fill=(246, 245, 241), outline=(70, 74, 84))
    for col_x in (x + 16, x + 34, x + w - 41, x + w - 23):
        pen.rectangle([col_x, y + 66, col_x + 7, y + h - 30],
                      fill=(214, 212, 205))
    cx = x + w // 2
    dark = (50, 55, 68)
    pen.rectangle([cx - 32, y + 74, cx + 32, y + 77], fill=dark)
    pen.rectangle([cx - 2, y + 72, cx + 2, y + 128], fill=dark)
    pen.ellipse([cx - 3, y + 66, cx + 3, y + 72], fill=dark)
    for sx in (-1, 1):
        px = cx + sx * 32
        pen.line([(px, y + 77), (px - 6, y + 92)], fill=dark, width=2)
        pen.line([(px, y + 77), (px + 6, y + 92)], fill=dark, width=2)
        pen.polygon([(px - 8, y + 92), (px + 8, y + 92), (px, y + 99)],
                    fill=(212, 175, 55))
    pen.rectangle([cx - 10, y + 128, cx + 10, y + 131], fill=dark)
    pen.rectangle([x + 4, y + h - 28, x + w - 4, y + h - 21],
                  fill=(196, 194, 186))
    pen.rectangle([x + 2, y + h - 21, x + w - 2, y + h - 14],
                  fill=(196, 194, 186))
    pen.rectangle([x, y + h - 14, x + w, y + h - 6], fill=(196, 194, 186))
    pen.rectangle([x, y + h - 6, x + w, y + h], fill=(150, 158, 148))


def paint_vice_city(x, y, w, h):
    sunset = [(247, 127, 90), (244, 110, 120), (214, 84, 150),
              (150, 66, 150), (84, 52, 130)]
    band_h = h // len(sunset) + 1
    for idx, colour in enumerate(sunset):
        pen.rectangle([x, y + idx * band_h, x + w, y + (idx + 1) * band_h],
                      fill=colour)
    sun_x, sun_y = x + int(0.60 * w), y + int(0.50 * h)
    pen.ellipse([sun_x - 19, sun_y - 19, sun_x + 19, sun_y + 19],
                fill=(255, 214, 90))
    shore = y + int(0.74 * h)
    pen.rectangle([x, shore, x + w, y + h], fill=(40, 26, 66))
    pen.line([(x, shore), (x + w, shore)], fill=(0, 240, 220), width=2)
    fronds = [(-16, -6), (-9, -12), (0, -15), (10, -12), (18, -6),
              (-13, 3), (15, 3)]
    for frac in (0.15, 0.85):
        palm_x = x + int(frac * w)
        top_x, top_y = palm_x + 4, shore - int(0.36 * h)
        pen.line([(palm_x, shore), (top_x, top_y)], fill=(20, 14, 34), width=3)
        for ddx, ddy in fronds:
            pen.line([(top_x, top_y), (top_x + ddx, top_y + ddy)],
                     fill=(20, 14, 34), width=2)
    car_y = y + h - 10
    pen.polygon([(x + 12, car_y), (x + 19, car_y - 8), (x + 31, car_y - 9),
                 (x + 40, car_y - 15), (x + 58, car_y - 15),
                 (x + 68, car_y - 9), (x + 78, car_y - 8), (x + 84, car_y)],
                fill=(16, 12, 28))
    pen.rectangle([x + 42, car_y - 14, x + 56, car_y - 10],
                  fill=(0, 240, 220))
    for wheel_x in (x + 26, x + 70):
        pen.ellipse([wheel_x - 5, car_y - 7, wheel_x + 5, car_y + 3],
                    fill=(10, 8, 20), outline=(255, 90, 180))


# ------------------------------------------------------------- card banners
def banner_ipo(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(26, 44, 84))
    for idx, bar_h in enumerate((6, 10, 14, 18)):
        bx = x + 10 + idx * 16
        pen.rectangle([bx, y + h - 3 - bar_h, bx + 10, y + h - 3],
                      fill=(64, 199, 120))
    pen.line([(x + 8, y + h - 6), (x + w - 14, y + 4)],
             fill=(255, 120, 90), width=2)
    pen.polygon([(x + w - 14, y + 4), (x + w - 22, y + 5), (x + w - 15, y + 11)],
                fill=(255, 120, 90))


def banner_cop(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(250, 224, 178))
    pen.rectangle([x, y + 13, x + w, y + h], fill=(38, 110, 138))
    pen.ellipse([x + 16, y + 3, x + 28, y + 15], fill=(244, 164, 40))
    palm_x = x + w - 24
    pen.line([(palm_x, y + 13), (palm_x + 4, y + 4)], fill=(20, 40, 30),
             width=2)
    for ddx, ddy in ((-8, -2), (-3, -4), (3, -4), (8, -2)):
        pen.line([(palm_x + 4, y + 4), (palm_x + 4 + ddx, y + 4 + ddy)],
                 fill=(20, 40, 30), width=1)


def banner_gulf(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(250, 224, 178))
    pen.rectangle([x, y + 10, x + w, y + h], fill=(38, 110, 138))
    pen.ellipse([x + 8, y + 2, x + 18, y + 12], fill=(244, 164, 40))
    pen.polygon([(x + 40, y + 15), (x + 110, y + 15), (x + 102, y + 20),
                 (x + 48, y + 20)], fill=(35, 35, 40))
    pen.rectangle([x + 48, y + 12, x + 102, y + 15], fill=(90, 90, 96))
    pen.rectangle([x + 94, y + 7, x + 100, y + 12], fill=(60, 60, 66))
    pen.rectangle([x + 94, y + 5, x + 100, y + 7], fill=(178, 34, 52))
    dx, dy = x + 124, y + 5
    pen.line([(dx - 4, dy - 2), (dx + 4, dy + 2)], fill=(30, 30, 30), width=2)
    pen.line([(dx - 4, dy + 2), (dx + 4, dy - 2)], fill=(30, 30, 30), width=2)


def banner_cyclone(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(96, 116, 134))
    pen.rectangle([x, y + 16, x + w, y + h], fill=(52, 84, 110))
    for box, start, end in ((18, 20, 200), (12, 200, 380), (6, 40, 240)):
        pen.arc([x + 30 - box // 2, y + 11 - box // 2,
                 x + 30 + box // 2, y + 11 + box // 2],
                start=start, end=end, fill=WHT, width=2)
    for idx in range(5):
        rx = x + 62 + idx * 16
        pen.line([(rx, y + 4), (rx - 4, y + 12)], fill=(170, 195, 215),
                 width=1)


def banner_seoul(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(232, 232, 226))
    cx = x + w // 2
    dark = (70, 72, 84)
    pen.polygon([(cx - 22, y + 9), (cx + 22, y + 9), (cx, y + 2)], fill=dark)
    for col_x in (cx - 18, cx - 3, cx + 13):
        pen.rectangle([col_x, y + 10, col_x + 5, y + 19], fill=dark)
    pen.rectangle([cx - 24, y + 19, cx + 24, y + 21], fill=dark)


def banner_bridge(x, y, w, h):
    pen.rectangle([x, y, x + w, y + h], fill=(198, 214, 230))
    pen.rectangle([x, y + 15, x + w, y + h], fill=(60, 110, 150))
    dark = (40, 44, 54)
    pen.rectangle([x + 30, y + 4, x + 33, y + 15], fill=dark)
    pen.rectangle([x + w - 33, y + 4, x + w - 30, y + 15], fill=dark)
    pen.line([(x + 31, y + 4), (x + w // 2, y + 12)], fill=dark, width=1)
    pen.line([(x + w - 31, y + 4), (x + w // 2 + 8, y + 13)], fill=dark,
             width=1)
    pen.line([(x + 4, y + 12), (x + w // 2 - 2, y + 12)], fill=dark, width=2)
    pen.line([(x + w // 2 + 6, y + 13), (x + w - 4, y + 15)], fill=dark,
             width=2)
    fx, fy = x + w // 2 + 2, y + 8
    pen.polygon([(fx, fy - 6), (fx + 2, fy - 1), (fx + 7, fy - 1),
                 (fx + 3, fy + 2), (fx + 5, fy + 7), (fx, fy + 4),
                 (fx - 5, fy + 7), (fx - 3, fy + 2), (fx - 7, fy - 1),
                 (fx - 2, fy - 1)], fill=(244, 140, 40))


BANNER_PAINTERS = {
    "ipo": banner_ipo, "cop": banner_cop, "gulf": banner_gulf,
    "cyclone": banner_cyclone, "seoul": banner_seoul, "bridge": banner_bridge,
}


def paint_card(x, y, w, h, card):
    colour, head, summary, tag, scene = card
    pen.rectangle([x, y, x + w, y + h], fill=LEADBG)
    pen.rectangle([x, y, x + w, y + 4], fill=colour)
    BANNER_PAINTERS[scene](x + 6, y + 7, w - 12, 22)
    head_font = load_font(SERIF_B, 11)
    yy = y + 32
    for line in fold(head, head_font, w - 12):
        pen.text((x + 6, yy), line, font=head_font, fill=FG)
        yy += 12
    body_font = load_font(SANS, 9)
    for line in fold(summary, body_font, w - 12):
        pen.text((x + 6, yy + 1), line, font=body_font, fill=(45, 45, 45))
        yy += 9.75
    pen.text((x + 6, y + h - 13), tag, font=load_font(SANS_B, 9), fill=colour)


SCENE_PAINTERS = [paint_summit, paint_hague, paint_vice_city]


def build_page():
    # ---- masthead
    centred("THE WHOLE DAY'S WORLD NEWS IN A SINGLE IMAGE",
            load_font(SANS_B, 11), 4, MUTED)
    centred("THE WORLD TODAY", load_font(SERIF_B, 44), 13)
    pen.line([(MARGIN, 59), (PAGE_W - MARGIN, 59)], fill=RULEC, width=3)
    centred("Thursday 19 November 2026", load_font(SERIF_B, 32), 64, RED)
    centred("%d stories  ·  7 regions  ·  drawn map & scenes  ·  "
            "every story reported on the day itself, date-checked"
            % STORY_TOTAL,
            load_font(SANS, 13), 98, MUTED)
    pen.line([(MARGIN, 114), (PAGE_W - MARGIN, 114)], fill=RULEC, width=1)

    # ---- rotated date-check stamp, drawn on its own layer
    stamp = Image.new("RGBA", (176, 48), (0, 0, 0, 0))
    sp = ImageDraw.Draw(stamp)
    sp.rectangle([2, 2, 173, 45], outline=(178, 34, 52, 255), width=3)
    big = load_font(SANS_B, 16)
    small = load_font(SANS_B, 11)
    sp.text((88 - sp.textlength("DATE-CHECKED", font=big) / 2, 5),
            "DATE-CHECKED", font=big, fill=(178, 34, 52, 255))
    sp.text((88 - sp.textlength("THU 19 NOV 2026", font=small) / 2, 27),
            "THU 19 NOV 2026", font=small, fill=(178, 34, 52, 255))
    tilted = stamp.rotate(8, expand=True, resample=Image.BILINEAR)
    canvas.paste(tilted, (836, 8), tilted)

    # ---- three lead panels with tall scenes
    lead_y, lead_h = 120, 184
    lead_w = (CONTENT_W - 2 * 12) // 3
    head_font = load_font(SERIF_B, 15)
    body_font = load_font(SANS, 10)
    kick_font = load_font(SANS_B, 11)
    for idx, (kick, colour, head, body) in enumerate(LEAD_STORIES):
        x0 = MARGIN + idx * (lead_w + 12)
        pen.rectangle([x0, lead_y, x0 + lead_w, lead_y + lead_h], fill=LEADBG)
        pen.rectangle([x0, lead_y, x0 + lead_w, lead_y + 5], fill=colour)
        SCENE_PAINTERS[idx](x0 + 8, lead_y + 8, 104, lead_h - 16)
        tx = x0 + 120
        pen.text((tx, lead_y + 8), kick, font=kick_font, fill=colour)
        yy = lead_y + 23
        for line in fold(head, head_font, lead_w - 126):
            pen.text((tx, yy), line, font=head_font, fill=FG)
            yy += 17
        yy += 2
        for line in fold(body, body_font, lead_w - 126):
            pen.text((tx, yy), line, font=body_font, fill=(45, 45, 45))
            yy += 11.5
        assert yy <= lead_y + lead_h - 2, (head, yy)

    # ---- pictured mid-card row
    card_y, card_h = lead_y + lead_h + 6, 90
    card_w = (CONTENT_W - 5 * 8) // 6
    for idx, card in enumerate(MID_CARDS):
        paint_card(MARGIN + idx * (card_w + 8), card_y, card_w, card_h, card)

    # ---- map (left) and numbers (right)
    map_y = card_y + card_h + 6
    map_h = 104
    map_w = 470
    pen.rectangle([MARGIN, map_y, MARGIN + map_w, map_y + 16], fill=RULEC)
    pen.text((MARGIN + 8, map_y + 2), "THE DAY ON THE MAP — WHERE THURSDAY HAPPENED",
             font=load_font(SANS_B, 12), fill=WHT)
    pen.rectangle([MARGIN, map_y + 16, MARGIN + map_w, map_y + map_h], fill=MAPBG)
    paint_map(map_y)

    num_x = MARGIN + map_w + 12
    num_w = PAGE_W - MARGIN - num_x
    pen.rectangle([num_x, map_y, num_x + num_w, map_y + 16], fill=RULEC)
    pen.text((num_x + 8, map_y + 2), "THE DAY IN NUMBERS",
             font=load_font(SANS_B, 12), fill=WHT)
    pen.rectangle([num_x, map_y + 16, num_x + num_w, map_y + map_h], fill=LEADBG)
    paint_numbers(num_x, num_w, map_y)

    # ---- UTC timeline strip
    tl_y = map_y + map_h + 6
    pen.rectangle([MARGIN, tl_y, PAGE_W - MARGIN, tl_y + 24], fill=FG)
    clock_line = ("BY THE CLOCK (UTC)  »  before dawn: Bahrain & Kuwait intercept "
                  "fresh barrages  »  04:45: Trump–Xi bilateral  »  07:30: three "
                  "leaders sit down together — a first  »  all day: APEC plenary, "
                  "COP31 deadlocked  »  by nightfall: GTA VI on sale")
    tl_font = load_font(SANS_B, 10)
    while measure(clock_line, tl_font) > CONTENT_W - 20:
        tl_font = load_font(SANS_B, tl_font.size - 1)
    pen.text((MARGIN + 10, tl_y + 5), clock_line, font=tl_font, fill=WHT)

    # ---- regional sections in two columns
    col_w = (CONTENT_W - 20) // 2
    top = tl_y + 26
    left_h = sum(section_height(name) for name in LEFT_COL)
    right_h = sum(section_height(name) for name in RIGHT_COL)
    print("left col height:", left_h, "right col height:", right_h,
          "sections top:", top)
    yy = top
    for name in LEFT_COL:
        yy = paint_section(name, MARGIN, yy, col_w)
    left_end = yy
    yy = top
    for name in RIGHT_COL:
        yy = paint_section(name, MARGIN + col_w + 20, yy, col_w)
    sections_end = max(left_end, yy)

    # ---- In Brief band
    brief_y = sections_end + 5
    pen.rectangle([MARGIN, brief_y, PAGE_W - MARGIN, brief_y + 17], fill=RULEC)
    pen.text((MARGIN + 8, brief_y + 2),
             "IN BRIEF — %d MORE STORIES FROM THE DAY" % len(BRIEF_ITEMS),
             font=load_font(SANS_B, 12), fill=WHT)
    brief_col_w = (CONTENT_W - 2 * 14) // 3
    brief_font = load_font(SANS_B, 9)
    yy = brief_y + 23
    for row_start in range(0, len(BRIEF_ITEMS), 3):
        for col_idx, (tag, txt) in enumerate(BRIEF_ITEMS[row_start:row_start + 3]):
            x0 = MARGIN + col_idx * (brief_col_w + 14)
            pen.rectangle([x0 + 1, yy + 3, x0 + 5, yy + 9], fill=RULEC)
            line = tag + " · " + txt
            assert measure(line, brief_font) <= brief_col_w - 10, line
            pen.text((x0 + 10, yy), line, font=brief_font, fill=FG)
        yy += 10.75

    # ---- date-check strip: what was left out as other days' news
    strip_y = yy + 1
    pen.rectangle([MARGIN, strip_y, PAGE_W - MARGIN, strip_y + 23], fill=RULEC)
    strip_font = load_font(SANS_B, 9)
    for idx, line in enumerate(DATE_CHECK_LINES):
        assert measure(line, strip_font) <= CONTENT_W - 20, line
        pen.text((MARGIN + 10, strip_y + 2 + idx * 10.5), line,
                 font=strip_font, fill=WHT)

    # ---- footer
    foot_y = strip_y + 26
    pen.line([(MARGIN, foot_y), (PAGE_W - MARGIN, foot_y)], fill=RULEC, width=2)
    centred("Every story happened, or was first reported, on Thursday 19 November "
            "2026 in some time zone. Contested claims are attributed as reported.",
            load_font(SANS_I, 10), foot_y + 3, MUTED)
    centred("Sources: Reuters · Associated Press · AFP · USA Today · Al Jazeera · "
            "TASS · Yonhap · UKMTO · NASA · The Hindu · BBC Sport · official statements",
            load_font(SANS, 9), foot_y + 15, MUTED)
    print("footer text ends:", foot_y + 24, "of", PAGE_H)
    assert foot_y + 24 <= PAGE_H

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    canvas.save(out_path, optimize=True)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


# Land as (first column, run length) spans per grid row, 81 x 18 grid.
LAND_RUNS = [
    [(3, 4), (11, 6), (26, 4), (47, 14), (64, 15)],
    [(1, 8), (10, 12), (25, 4), (37, 1), (43, 4), (48, 32)],
    [(9, 14), (39, 2), (41, 6), (47, 32)],
    [(8, 16), (38, 8), (47, 10), (57, 11), (71, 3)],
    [(8, 16), (38, 2), (42, 2), (44, 4), (48, 3), (51, 5), (58, 10), (68, 2), (70, 3)],
    [(9, 12), (13, 5), (37, 10), (47, 3), (50, 3), (53, 3), (56, 3), (59, 8)],
    [(12, 5), (36, 12), (48, 4), (56, 4), (60, 3), (63, 4), (67, 1), (68, 2)],
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

MAP_MARKS = [
    {"c": 66, "r": 6, "label": "SHENZHEN", "side": "l", "dy": 0},
    {"c": 68, "r": 7, "label": "MANILA", "side": "r", "dy": 0},
    {"c": 63, "r": 8, "label": "ODISHA", "side": "r", "dy": 12},
    {"c": 47, "r": 3, "label": "KYIV", "side": "l", "dy": 3},
    {"c": 45, "r": 2, "label": "BERLIN", "side": "l", "dy": -3},
    {"c": 46, "r": 4},
    {"c": 53, "r": 6, "label": "HORMUZ", "side": "r", "dy": 11},
    {"c": 50, "r": 6},
    {"c": 48, "r": 5},
    {"c": 23, "r": 4, "label": "WASHINGTON", "side": "l", "dy": 0},
    {"c": 25, "r": 8},
    {"c": 48, "r": 9},
    {"c": 44, "r": 8},
    {"c": 74, "r": 15},
    {"c": 71, "r": 4},
]


def paint_map(map_y):
    grid_x = MARGIN + 24
    grid_y = map_y + 21
    step_x, step_y = 5.2, 4.7
    for row_idx, runs in enumerate(LAND_RUNS):
        for first_col, run_len in runs:
            for col in range(first_col, first_col + run_len):
                cx = grid_x + col * step_x
                cy = grid_y + row_idx * step_y
                pen.ellipse([cx - 2.2, cy - 2.2, cx + 2.2, cy + 2.2], fill=LANDC)
    label_font = load_font(SANS_B, 9)
    for mark in MAP_MARKS:
        cx = grid_x + mark["c"] * step_x
        cy = grid_y + mark["r"] * step_y
        pen.ellipse([cx - 4.5, cy - 4.5, cx + 4.5, cy + 4.5], fill=WHT)
        pen.ellipse([cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2], fill=MARKC)
        if "label" in mark:
            label = mark["label"]
            if mark["side"] == "r":
                lx = cx + 7
            else:
                lx = cx - 7 - measure(label, label_font)
            pen.text((lx, cy - 5 + mark["dy"]), label, font=label_font,
                     fill=FG, stroke_width=2, stroke_fill=MAPBG)


def paint_numbers(num_x, num_w, map_y):
    big_font = load_font(SERIF_B, 19)
    lab_font = load_font(SANS, 9)
    cell_w = (num_w - 24) // 3
    for idx, (num, lab) in enumerate(NUMBER_ITEMS):
        cx = num_x + 10 + (idx % 3) * (cell_w + 8)
        cy = map_y + 21 + (idx // 3) * 40
        pen.text((cx, cy), num, font=big_font, fill=RED)
        yy = cy + 22
        for line in fold(lab, lab_font, cell_w - 4):
            pen.text((cx, yy), line, font=lab_font, fill=(45, 45, 45))
            yy += 9.5


def section_height(name):
    _, stories = SECTION_BY_NAME[name]
    body_font = load_font(SANS, 9)
    col_w = (CONTENT_W - 20) // 2
    height = 18
    for _, body in stories:
        height += 10.5 + len(fold(body, body_font, col_w - 10)) * 9.5
    return height + 0.5


def paint_section(name, x, y, col_w):
    colour, stories = SECTION_BY_NAME[name]
    pen.rectangle([x, y, x + col_w, y + 17], fill=colour)
    pen.text((x + 8, y + 2), name, font=load_font(SANS_B, 12), fill=WHT)
    head_font = load_font(SANS_B, 11)
    body_font = load_font(SANS, 9)
    yy = y + 18
    for head, body in stories:
        pen.rectangle([x + 1, yy + 3, x + 5, yy + 9], fill=colour)
        pen.text((x + 10, yy), head, font=head_font, fill=FG)
        yy += 10.5
        for line in fold(body, body_font, col_w - 10):
            pen.text((x + 10, yy), line, font=body_font, fill=(60, 60, 60))
            yy += 9.5
    return yy + 0.5


if __name__ == "__main__":
    build_page()
