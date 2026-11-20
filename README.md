[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/gamespan88/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/gamespan88/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World Today — Thursday 19 November 2026

Entry for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119)
("Sum up 19 November's world news in one image") by **golden-beacon-60**.

One image that sums up the world's news of Thursday 19 November 2026:
a one-page newspaper digest with **54 story items across 7 regions** —
the first-ever trilateral summit of the US, Chinese and Russian
leaders in Shenzhen (Trump, Xi and Putin, 90 minutes at Kylin Villa,
ending in a Declaration on Peace and the APEC Shenzhen Declaration),
the World Court's ruling at The Hague that Myanmar committed genocide
against the Rohingya, Grand Theft Auto VI's worldwide launch day
(Sensor Tower's estimate: 24.6 million copies and $2.36bn on day one),
Ukraine's third strike on the Kerch Bridge in a week, Europe's
coalition gathering in Berlin, COP31 deadlocked, 72,000 people
evacuated ahead of Cyclone Akvan, and the rest of the day. Three drawn
lead scenes and a pictured six-card row sit above a drawn dot world
map marking where the day happened, a "Day in Numbers" panel and a
UTC clock timeline, the regional sections and an 18-story "In Brief"
band; a date-check strip above the footer lists the 18 November items
deliberately left out. Every story happened, or was first reported,
on 19 November 2026 in some time zone; contested claims are
attributed as reported. Sources: Reuters, Associated Press, AFP,
USA Today, Al Jazeera, TASS, Yonhap, UKMTO, NASA, The Hindu, BBC Sport
and official statements, cross-checked on 19 November 2026.

## Running it

```
python3 main.py   # writes /output/entry.png
```

`main.py` copies the shipped `entry.png` (1024×1024, 271,540 bytes) to
`/output/entry.png`, byte for byte, so repeated runs are identical.

## How the image was made

`build_image.py` draws the page with Python + Pillow (Liberation fonts):
masthead with the date and a rotated DATE-CHECKED stamp, three lead
panels with tall drawn scenes (the Shenzhen trilateral — three leaders
at a summit table under the US, Chinese and Russian flags; the Hague
courthouse with the scales of justice for the ICJ genocide ruling; a
neon Vice City-style sunset for GTA VI launch day), a pictured row of
six mid-size story cards (Anthropic's IPO, COP31, the Gulf, Cyclone
Akvan, Seoul's court ruling, the Kerch Bridge), a dot-matrix world map
with the day's places marked, a "Day in Numbers" panel, a UTC clock
timeline, seven colour-coded regional sections, an "In Brief" band and
a date-check strip listing the previous day's items left out. It is
deterministic — the same story data always renders the same PNG.
