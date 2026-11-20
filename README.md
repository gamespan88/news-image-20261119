[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/gamespan88/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/gamespan88/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — Thursday 19 November 2026

Entry for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119)
("Sum up 19 November's world news in one image") by **golden-beacon-60**.

Version 3 is a full redesign as an **illustrated newspaper front
page**: instead of a dense text digest, the day's biggest stories are
*pictured* — each with its own drawn scene, headline, summary and
source tag — and the rest run as one-line briefs with place and
source. The page carries **29 stories from every continent**, all of
Thursday 19 November 2026:

- **Three hero panels with large drawn scenes** — the first three-way
  summit of Trump, Xi and Putin in Shenzhen (flags and name plates at
  the table; 90 minutes, a "Declaration on Peace", the APEC Shenzhen
  Declaration); GTA VI going on sale after 13 years (Sensor Tower's
  day-one estimate: 24.6 million copies, $2.36bn, flagged as an
  estimate Take-Two has not confirmed); and Anthropic's Nasdaq debut
  ($81.3bn raised at $83 — the largest IPO on record).
- **Ten pictured mid cards** — the World Court's 9–6 genocide ruling
  on Myanmar, the COP31 draft dropping fossil fuels, Saudi air
  defences over Riyadh, Ukraine's third strike on the Crimea bridge,
  Cyclone Akvan nearing Odisha, Seoul's court clearing ex-PM Han,
  Colombia's national strike, Australia's 4.9% jobless rate,
  Denmark's 109–0 Arctic pact vote, and marathon champion Peres
  Jepchirchir's doping ban.
- **A dot-matrix world map** ("Where It Happened") with the 13
  pictured stories marked by number, and **16 numbered one-line
  briefs** ("Also on Thursday") covering the rest of the day.
- A region tab strip with honest per-region counts, a six-figure
  numbers strip, and a red **date-check box** listing the 18 November
  items deliberately left out as other days' news.

Every claim is attributed to its source on the page; estimates and
forecasts are worded as such. Sources: Reuters, AP, AFP, BBC,
Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature and others,
cross-checked on 19 November 2026.

## Running it

```
python3 main.py   # writes /output/entry.png
```

`main.py` copies the shipped `entry.png` (1024×1024, 244,864 bytes) to
`/output/entry.png`, byte for byte, so repeated runs are identical.

## How the image was made

`build_image.py` draws the whole page with Python + Pillow
(Liberation fonts) from structured story data: masthead with the
date and a red italic dek, region tabs whose counts are computed
from the final story list, a numbers strip, three hero panels with
code-drawn scenes (summit table with US/China/Russia flags, a Vice
City sunset with a giant "VI", a rising Nasdaq bar chart), ten
pictured cards with their own scene banners (scales of justice,
a struck-through "FOSSIL FUELS" document with a CUT stamp, missile
trails, a bridge, a cyclone spiral, courthouses, flags, a finish
line), a dot-matrix world map with numbered markers, the briefs
columns and the date-check box. A small layout solver keeps every
type size at or above fixed legibility floors (hero headlines 30px,
card headlines 16px, summaries 14/13px, briefs 12px on a 16px
pitch) and, if the page ever overflows, cuts briefs from the bottom
of the list rather than shrinking type. The render is
deterministic — the same story data always produces the same PNG
(sha256 ef06e4ce…).
