[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/soedirman566-stack/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/soedirman566-stack/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The Daily Globe — Friday, 20 November 2026

A one-page newspaper front page that sums up the world news of **Friday,
20 November 2026** in a single 1024×1024 image (`entry.png`).

## The four stories

1. **Trump, Xi and Putin hold their first three-way summit in Shenzhen and
   sign a peace declaration** (lead story). The US, Chinese and Russian
   leaders met in Shenzhen and pledged UN reform, reduced nuclear risk and
   stable energy supplies — the day's defining diplomatic event, made
   sharper by the heavy Russian missile strike on Kyiv that followed hours
   later.
2. **World Court rules Myanmar committed genocide against the Rohingya.**
   The International Court of Justice in The Hague ruled 9–6 that Myanmar's
   2017 crackdown was genocide — the first time the court has held a state
   responsible for genocide.
3. **AI doubts spark a global stock sell-off.** Anthropic's record
   stock-market debut failed to calm nerves about AI valuations: the S&P 500
   fell about 2% for a fifth straight loss, Japan's Nikkei plunged 4.8% and
   gold slid 4.2%.
4. **COP31 draft drops the call to phase out fossil fuels.** Negotiators in
   Antalya, Turkey deleted every mention of ending fossil fuel use from the
   slimmed-down draft deal as the UN climate talks reached their final day.

Together they span diplomacy, international justice, the world economy and
the climate talks, across Asia, Europe, the Americas and the Middle East.

## Photo credits

- Summit (Shenzhen skyline over the Buji River): Dinkun Chen, CC BY-SA 4.0,
  via Wikimedia Commons / One Turn —
  https://oneturn.news/media/stories/2026-11-20/shenzhen-summit.jpg
- World Court (Peace Palace, The Hague): International Court of Justice,
  public domain, via Wikimedia Commons —
  https://upload.wikimedia.org/wikipedia/commons/a/a0/International_Court_of_Justice_HQ_2006.jpg
- Markets (Wall Street): Vlad Lazarenko, CC BY-SA 3.0, via Wikimedia
  Commons / One Turn —
  https://oneturn.news/media/stories/2026-11-20/wall-street-selloff.jpg
- COP31 (venue signage, Antalya): IISD / Earth Negotiations Bulletin,
  photo by Mike Muzurakis —
  https://enb.iisd.org/sites/default/files/styles/max_650x650/public/2026-11/UNFCCC-COP31-8167.jpg?itok=4m5cP0Xy

News reporting drawn from One Turn's 20 November 2026 edition, CNN and
The Times.

## How it is built and run

- `compose.py` (Python + Pillow) lays out the front page from the photos in
  `assets/` and writes `entry.png`. It is deterministic — no randomness, no
  clock — and fits every headline and caption with an adaptive font-size
  ladder, so it always produces the same bytes.
- `main.ts` (Node, standard library only) is the submitted program: it
  copies the repository's `entry.png` to
  `join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png')`,
  creating the output directory if needed.
