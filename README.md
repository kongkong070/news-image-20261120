# The World in One Day — Friday 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kongkong070/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kongkong070/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up the world's news of
Friday 20 November 2026, drawn offline with Pillow
(`draw_frontpage.py`) and committed as `entry.png`. `main.ts`
(Node 22, stdlib only) copies it to `/output/entry.png`
(or `$MAKEFUN_OUTPUT_DIR`).

## Stories

1. **Three leaders, one table** — Trump, Xi and Putin hold a historic
   trilateral summit in Shenzhen and issue a four-point declaration.
2. **Genocide, the court rules** — the ICJ finds Myanmar committed
   genocide against the Rohingya, a first for a state.
3. **Missile over Riyadh** — a Houthi missile strikes the PIF Tower.
4. **Cyclone Akvan** — the storm bears down on Odisha.
5. **$81.3bn debut** — Anthropic starts trading after its IPO,
   shares up 34% on the first day.
6. **One light-day out** — Voyager 1 reaches a full light-day
   from the Sun.

Sources: Reuters, BBC, The Times, Qazinform — see the image.

## Run

```sh
python3 draw_frontpage.py   # regenerate entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
