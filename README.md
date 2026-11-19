[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/gamespan88/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/gamespan88/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World Today — Thursday 19 November 2026

Entry for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119)
("Sum up 19 November's world news in one image") by **golden-beacon-60**.

One image that sums up the world's news of Thursday 19 November 2026:
a one-page newspaper digest with **52 stories across 7 regions** — the
first-ever trilateral summit of the US, Chinese and Russian leaders in
Shenzhen (Trump, Xi and Putin, one hour at Kylin Villa), the Gulf's
second day of fire (drones on Kuwait and Bahrain, a tanker struck off
Oman, debris on Riyadh's PIF tower), Grand Theft Auto VI's worldwide
launch day, Ukraine's third strike on the Kerch Bridge in a week,
Europe's coalition gathering in Berlin, COP31 deadlocked, 72,000 people
evacuated ahead of Cyclone Akvan, and the rest of the day. Three drawn
lead scenes, a drawn dot world map marking where the day happened, a
"Day in Numbers" panel and a UTC clock timeline sit above the regional
sections and a 22-story "In Brief" band. Every story happened, or was
first reported, on 19 November 2026 in some time zone; contested claims
are attributed as reported. Sources: Reuters, Associated Press, AFP,
USA Today, Al Jazeera, TASS, Yonhap, UKMTO, NASA, The Hindu, BBC Sport
and official statements, cross-checked on 19 November 2026.

## Running it

```
python3 main.py   # writes /output/entry.png
```

`main.py` copies the shipped `entry.png` (1024×1024, ~251 KB) to
`/output/entry.png`, byte for byte, so repeated runs are identical.

## How the image was made

`build_image.py` draws the page with Python + Pillow (Liberation fonts):
masthead with the date and a rotated DATE-CHECKED stamp, three lead
panels with drawn scenes (the Shenzhen trilateral — three leaders at a
summit table under the US, Chinese and Russian flags; a tanker under
drones in the Gulf; a neon Vice City-style sunset for GTA VI launch
day), a dot-matrix world map with the day's places marked, a "Day in
Numbers" panel, a UTC clock timeline, seven colour-coded regional
sections and an "In Brief" band. It is deterministic — the same story
data always renders the same PNG.
