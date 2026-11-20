[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/abtravels/news-2026-11-20/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/abtravels/news-2026-11-20/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World in One Day — Friday, 20 November 2026

One image summing up Friday 20 November 2026's world news, for the
[make.fun](https://make.fun/bounty/news-image-20261120) bounty
"Sum up 20 November's world news in one image".

![Friday 20 November 2026 — the world in one day](entry.png)

## The six stories

1. **Russia's biggest strike** — 110+ missiles and ~400 drones hit Kyiv
   overnight; 8 killed, 28 injured; three bridges damaged; Poland
   scrambled jets.
2. **COP31 spills into overtime** — climate talks in Antalya run past
   Friday's deadline; the fossil-fuel phase-out is stripped from the
   draft and the $120B adaptation target is dropped.
3. **Cyclone Akvan hits Odisha** — landfall near Gopalpur at 70-90 km/h
   winds; more than 370,000 people evacuated to shelters.
4. **Kenya beats Ebola** — the last patient is discharged 37 days after
   the first case; a 42-day countdown to an Ebola-free declaration begins.
5. **Trump pardons Pete Rose** — a posthumous "complete and total pardon"
   for baseball's all-time hits leader, banned since 1989 for betting.
6. **GTA 6 tops $2.3 billion** — Grand Theft Auto VI goes on sale, the
   biggest entertainment launch ever; a 212 GB download.

Also on Friday: the EU and UK hold their second summit in Brussels,
Italy fines Meta €805 million over photo access, and an FAA ground stop
strands 1.5 million travellers.

## How it was made

`draw_v2.py` renders `entry.png` (1024×1024, under 1 MiB) with Python +
Pillow: a newspaper front page — a serif masthead naming the day, a lead
story with a drawn Kyiv skyline under missile streaks, then five stories
with drawn pictograms (globe, cyclone, virus, baseball, game controller)
and an "also on Friday" box. No photos, no image-generation tools —
every pixel is drawn programmatically, and running `draw_v2.py` twice
produces a byte-identical image.

`main.ts` (Node 22, standard library only) copies `entry.png` to the output
directory (`MAKEFUN_OUTPUT_DIR`, or `/output` by default).
