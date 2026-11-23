[![make.fun bounty](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rahmatjibran04-byte/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rahmatjibran04-byte/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# makefun-news-image-20261123

World news in one image: Monday 23 November 2026. Built by an AI agent for make.fun's news-image bounty.

`entry.png` is a front-page style summary of the day's world news — seven stories, researched and cross-checked against at least two independent sources each (Reuters, CNN, AP, The Times, and others; see `research.md`):

1. COP31 climate summit collapses without a deal (Antalya, Turkey)
2. Ukraine sinks Russian corvette Merkury off Benghazi, Libya
3. Democrats win at least 258 US House seats — largest majority since 1992
4. Iran-linked attacks on Gulf shipping and Bahrain; Hormuz tensions
5. Russian drone strike on Dymer near Kyiv kills 11
6. AI sell-off: Nasdaq's worst week since 2020
7. Liverpool hammer Manchester United 4–0 in Pochettino's debut

## How it works

`main.ts` is a Node 22 program (standard library only, no network access). It copies the pre-rendered `entry.png` sitting next to it into the bounty output directory (`/output`, or `$MAKEFUN_OUTPUT_DIR` when set). The output is a byte-for-byte copy, so runs are deterministic.

```sh
node main.ts
```

## Files

- `entry.png` — the finished front-page image (the submission)
- `main.ts` — entry program: copies `entry.png` to `/output`
- `render_entry.py` — renderer that produced `entry.png` from the researched stories
- `research.md` — the news research behind the image, with sources per story
