# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ilham270207/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ilham270207/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

`main.py` draws a newspaper front page — **"The World in One Page"** — summing up Tuesday 24 November 2026's world news as a single 1024×1024 PNG. The page is dense and busy, like a morning paper: a lead story, two right-column stories, three middle stories, a sports strip and a BY THE NUMBERS band. Text, layout and every illustration are drawn in code with Pillow (vector shapes only — factory fire, cargo ship, globe, protest crowd, cracked earth, telephone); no photographs, no network, no likenesses of real people. No random numbers, no timestamps. Running it twice writes byte-identical PNGs.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $OUTPUT_PATH; falls back to ./output/entry.png)
```

---

Entered on [make.fun](https://make.fun/?ref=vs40zhzs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards

## The stories (all verified from multiple outlets)

1. **INDONESIA — Fire kills 24 at Java candy factory.** Blaze rips through a plant in Banten province; around 30 workers still missing as rescuers search the charred factory. (Reuters, AP, The Guardian, NDTV)
2. **UKRAINE WAR — Kyiv hit as war spills to the sea.** Russian drones strike the Kyiv region; cargo ship Sparta II ablaze off Finland after a drone attack; a Russian corvette burns in Libya's Benghazi port. (Reuters, CNN, The Guardian, Naval News)
3. **CLIMATE — COP31 ends with no fossil-fuel deal.** Talks in Antalya close divided over fossil fuels; critics call the outcome a setback for the planet. (NDTV, AP)
4. **LISBON — Thousands march on living costs.** Protesters fill the streets of Portugal's capital over rising prices. (The Guardian)
5. **GAZA — Land, air and water 'poisoned'.** Oxfam and CEOBS: heavy metals, asbestos and explosive residues threaten life across the Strip for decades. (Oxfam, CEOBS)
6. **WASHINGTON — Kim ignores Trump's calls.** Pyongyang rebuffs US bids to revive talks as it expands its nuclear arsenal. (Wall Street Journal)
7. **SPORT —** Verstappen wins the Las Vegas Grand Prix; Alcaraz takes his first ATP Finals title; Pant hits 128 in the Wellington Test draw; Gukesh defends the chess crown against Sindarov in Geneva.
8. **BY THE NUMBERS —** 24 killed in the Banten fire; ~30 missing; $1tn Nvidia gain as Huang returns; 1,484 points lost by India's Sensex.

## Verification (local, 24 Nov 2026)

- `python3 main.py` twice → identical SHA-256 (`f25b30f5d323814d08da1ef3bc3e6420f039056c594d8112501edbff5adfd07b`)
- Output: 1024×1024 PNG, 164,410 bytes (limit 1 MiB)
- Visual check: masthead, lead story, right column, three middle stories, sports strip and numbers band all render; every headline and deck complete, no overlaps, all text readable
- No network access in the program; all artwork is drawn in code.

## License

MIT. Fonts: DejaVu Sans / DejaVu Serif (see `fonts/`).
