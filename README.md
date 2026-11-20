# makefun-news-1119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/firhanaf/makefun-news-1119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/firhanaf/makefun-news-1119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-image front page for Thursday 19 November 2026. The lead is the International Court of Justice ruling that
Myanmar committed genocide against the Rohingya. Below it are six stories from Asia, Europe, the Middle East and
Africa: the first Trump–Xi–Putin meeting at APEC in Shenzhen, Ukraine's third strike on the Kerch Strait bridge that
week, Houthi missiles hitting Riyadh's financial district, the Mongolian president's resignation, Somalia expelling
the UAE's ambassador, and Serbia's interim president. Five short briefs fill the bottom. `render.py` draws the page
from scratch with Pillow. `main.ts` checks that `entry.png` is a PNG within the bounty's limits, then copies it to
`/output`.

![entry](entry.png)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# re-render the image (needs Pillow and Arial/Georgia fonts): python render.py
```

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
