# Stage 0 - persistent stock-specific intraday behaviour

stage0_persistence v1.0 | declaration 93f908bfe9c52af9 | 2026-10-11 21:15 | costs 4.49 bp round trip at Rs 500,000 + slippage 5 bp entry, 3 bp time exit = 12.49 bp a trade

## VERDICT: no persistent stock-specific behaviour

No setup-side passed both legs (Holm-corrected permutation p <= 0.05 AND the H1 top decile's H2 interval above zero). Persistent on leg 1 alone: ORC_L, ORC_S, FHM_S, CMP_L, PDB_S. Stop here.

## Persistence per setup-side

Excess = a stock's mean net per trade minus its own plain open-to-15:03 trade in the same direction (same half). rho = Spearman of H1 vs H2 excess across stocks with >= 30 trades in each half; p = one-sided permutation (stock labels shuffled, 10,000 times); Holm over 20 setup-sides. Top decile = best 10% of stocks by H1 excess; their H2 net (after costs) per trade-day with a 95% block-bootstrap interval. rho vs ATR: how much the H1 excess just tracks volatility.

| setup-side | stocks | rho | perm p | Holm p | top-decile stocks | H2 trades | H2 win | H2 net bp/trade | H2 bp/trade-day [95%] | rho vs ATR | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORC_L | 299 | +0.211 | 0.0003 | 0.0054 | 32 | 4,817 | 41% | -6.5 | -18.0 [-26.7, -9.0] | -0.03 | leg 1 only |
| ORC_S | 319 | +0.205 | 0.0004 | 0.0068 | 33 | 5,367 | 51% | +3.7 | -13.0 [-20.6, -4.9] | +0.20 | leg 1 only |
| ORF_L | 303 | +0.111 | 0.0273 | 0.3549 | 32 | 4,586 | 42% | -13.8 | -8.9 [-14.3, -3.4] | -0.17 | - |
| ORF_S | 288 | +0.101 | 0.0408 | 0.4896 | 31 | 3,097 | 50% | -5.5 | +3.0 [-6.2, +12.1] | -0.07 | - |
| GAPC_L | 106 | +0.144 | 0.0668 | 0.6679 | 14 | 549 | 42% | -12.4 | -17.1 [-33.9, +2.3] | +0.05 | - |
| GAPC_S | 4 | n/a | 1.0000 | 1.0000 | 0 | 0 | n/a | n/a | n/a [n/a, n/a] | n/a | - |
| GAPF_L | 14 | n/a | 1.0000 | 1.0000 | 6 | 137 | 45% | -11.1 | -8.8 [-28.0, +13.5] | n/a | - |
| GAPF_S | 191 | +0.021 | 0.3945 | 1.0000 | 20 | 1,111 | 51% | -5.6 | +5.2 [-8.6, +19.4] | -0.11 | - |
| VWR_L | 229 | +0.149 | 0.0128 | 0.1920 | 24 | 1,720 | 46% | -9.7 | +4.3 [-5.4, +14.0] | +0.03 | - |
| VWR_S | 215 | +0.023 | 0.3687 | 1.0000 | 22 | 1,407 | 46% | -19.4 | -6.5 [-15.5, +2.7] | -0.10 | - |
| FHM_L | 241 | +0.104 | 0.0541 | 0.5950 | 25 | 1,802 | 41% | -14.9 | -14.7 [-24.3, -5.4] | +0.07 | - |
| FHM_S | 258 | +0.242 | 0.0001 | 0.0020 | 27 | 2,239 | 52% | +5.3 | -5.0 [-14.0, +4.1] | +0.08 | leg 1 only |
| CMP_L | 215 | +0.202 | 0.0019 | 0.0304 | 22 | 1,319 | 39% | -9.7 | -14.5 [-22.6, -6.0] | +0.12 | leg 1 only |
| CMP_S | 236 | +0.135 | 0.0208 | 0.2912 | 25 | 1,800 | 46% | -7.4 | -13.3 [-18.4, -8.1] | -0.01 | - |
| PDB_L | 266 | +0.069 | 0.1308 | 1.0000 | 28 | 2,846 | 40% | -16.5 | -29.0 [-40.9, -17.8] | +0.07 | - |
| PDB_S | 281 | +0.290 | 0.0001 | 0.0020 | 29 | 2,690 | 51% | +6.5 | -16.7 [-26.9, -7.5] | +0.23 | leg 1 only |
| PDR_L | 267 | +0.029 | 0.3179 | 1.0000 | 28 | 2,632 | 42% | -14.8 | -8.8 [-17.6, +0.5] | -0.08 | - |
| PDR_S | 259 | -0.003 | 0.5111 | 1.0000 | 27 | 2,604 | 49% | -13.4 | -7.4 [-17.2, +3.4] | -0.11 | - |
| VSF_L | 314 | +0.063 | 0.1375 | 1.0000 | 33 | 6,893 | 41% | -9.7 | -8.7 [-14.4, -3.0] | +0.01 | - |
| VSF_S | 312 | +0.057 | 0.1564 | 1.0000 | 33 | 5,545 | 50% | -5.0 | -7.6 [-13.1, -2.0] | +0.05 | - |

## All stocks pooled (context, not a rule)

| setup-side | H1 trades | H1 win | H1 net bp/trade | H2 trades | H2 win | H2 net bp/trade |
|---|---|---|---|---|---|---|
| ORC_L | 49,526 | 41% | -21.0 | 74,555 | 41% | -14.7 |
| ORC_S | 57,291 | 49% | +1.2 | 89,436 | 47% | -7.6 |
| ORF_L | 45,477 | 39% | -25.8 | 72,003 | 40% | -18.0 |
| ORF_S | 40,312 | 48% | -5.7 | 59,964 | 49% | -9.8 |
| GAPC_L | 8,576 | 41% | -23.5 | 12,476 | 41% | -20.5 |
| GAPC_S | 4,648 | 51% | +10.1 | 4,122 | 43% | -20.7 |
| GAPF_L | 6,375 | 43% | -22.9 | 6,867 | 47% | +1.8 |
| GAPF_S | 12,599 | 52% | +5.8 | 20,055 | 51% | -4.2 |
| VWR_L | 18,655 | 44% | -21.0 | 29,940 | 45% | -14.9 |
| VWR_S | 14,890 | 49% | -5.9 | 26,193 | 48% | -15.9 |
| FHM_L | 20,693 | 41% | -19.0 | 31,195 | 41% | -14.2 |
| FHM_S | 24,845 | 50% | +3.4 | 39,835 | 48% | -7.0 |
| CMP_L | 16,079 | 39% | -16.4 | 23,547 | 39% | -8.2 |
| CMP_S | 19,235 | 44% | -4.0 | 28,639 | 45% | -6.6 |
| PDB_L | 28,415 | 40% | -23.8 | 44,564 | 40% | -17.6 |
| PDB_S | 30,684 | 48% | -2.0 | 50,036 | 47% | -7.0 |
| PDR_L | 26,966 | 41% | -21.0 | 42,532 | 42% | -15.3 |
| PDR_S | 28,949 | 50% | -1.6 | 43,692 | 50% | -5.9 |
| VSF_L | 62,047 | 40% | -22.5 | 98,131 | 41% | -12.8 |
| VSF_S | 61,319 | 48% | -2.0 | 96,584 | 47% | -10.8 |

## Context

- Plain open-to-15:03 long trade, H1 vs H2 per-stock Spearman: +0.070 over 347 stocks (how much intraday drift persists on its own; the excess removes it).
- Stocks with usable sessions: 794 of 815 liquid equity stocks (16 liquid stock(s) without a 3-minute file).
- Liquid stock-days with a usable session (after reconciliation and the 80% rule): H1 98.1% of 98,505; H2 98.1% of 151,852.
- Data checks in H1-H2: 584,418 sessions with bars, 16,924 failed reconciliation, 1,508 without a first bar or under 80% of bars, 0 unreadable files, 1 stock-days dropped by the 20% gap guard.
- Nothing after 2024-12-31 was read into any number.

## Caveats

- In-sample screen only: H1 and H2 are both inside 2021-10 to 2024-12; a PASS earns a Stage 1 build, not money. 2025 onward stays untouched for later confirmation
- A setup that enters later in the day keeps a small part of the stock's drift in its excess (it skips the morning part of the plain trade); with about 60 trades per stock per half this is small next to the noise, and the H2 leg judges net money, not the excess
- Costs are assumed (slippage not measured); the time exit is fixed at 15:03 for every setup
- One permutation per setup-side; the shuffles are not shared across setup-sides, so the Holm correction does not use their correlation (conservative)
