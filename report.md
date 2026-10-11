# Stage C1 - the cost check

engine_stage_c v1.0 | engine_core v1.0 | Stage C declaration 8db702a0889366cd | engine declaration e3c6bd173874970a | 2026-10-12 01:19 | stocks HDFCBANK, ICICIBANK, SBIN, INFY, TCS, RELIANCE, BHARTIARTL, LT, MARUTI, SUNPHARMA (list ba1c73b77e553bc5) | Stage B run B_20261012_001 | development 2021-10-01..2024-12-31; nothing later is read

## VERDICT: BELOW COST

No state representation, honestly calibrated, picks trades that pay for themselves after the 12.49 bp a trade costs. The direction these states know about is real but smaller than the cost of acting on it. For these stocks with these states the engine's answer is NO TRADE, and the direction track stops here. The rules are not changed to get a pass.

Tested on the test windows of folds 2-5 (2023-04-03 .. 2024-12-31, 428 sessions). A trade = the first decision point of a stock's session whose calibrated expected move is at least 12.49 bp, in the direction of that move; net = gross - 12.49 bp. [ ] = 95% block-bootstrap interval over sessions; Holm p corrects for the 6 tests; a pass needs 100+ trades, a lower bound above 0 and Holm p <= 0.05.

| representation | exit | trades | expected move bp (mean) | gross bp / trade | net bp / trade | Holm p | hit rate | net at 1.5x costs | PASS |
|---|---|---|---|---|---|---|---|---|---|
| grid12 | H60 | 0 | - | - | - | - | - | - | no (no decision point expects 12.49 bp) |
| grid12 | EOD | 0 | - | - | - | - | - | - | no (no decision point expects 12.49 bp) |
| gmm4 | H60 | 0 | - | - | - | - | - | - | no (no decision point expects 12.49 bp) |
| gmm4 | EOD | 0 | - | - | - | - | - | - | no (no decision point expects 12.49 bp) |
| hmm4 | H60 | 0 | - | - | - | - | - | - | no (no decision point expects 12.49 bp) |
| hmm4 | EOD | 0 | - | - | - | - | - | - | no (no decision point expects 12.49 bp) |

## How close do the states come to the cost?

The expected move of every decision point in the test windows, in bp. 'Calibrated' is what the trade rule uses; 'raw' takes the state tables at face value (no calibration). The cost is 12.49 bp.

| representation | exit | calibrated: share >= cost | median | 99th pct | max | raw: share >= cost | median | 99th pct | max |
|---|---|---|---|---|---|---|---|---|---|
| grid12 | H60 | 0.00% | 0.5 | 2.2 | 4.9 | 0.00% | 1.7 | 7.1 | 14.4 |
| grid12 | EOD | 0.00% | 1.0 | 4.9 | 12.1 | 3.89% | 3.8 | 17.1 | 42.3 |
| gmm4 | H60 | 0.00% | 0.6 | 3.1 | 5.8 | 0.00% | 1.4 | 5.9 | 8.9 |
| gmm4 | EOD | 0.00% | 0.8 | 5.8 | 10.0 | 1.07% | 2.8 | 12.6 | 19.8 |
| hmm4 | H60 | 0.00% | 0.4 | 2.4 | 4.1 | 0.00% | 1.5 | 6.1 | 9.3 |
| hmm4 | EOD | 0.00% | 0.8 | 4.7 | 7.7 | 1.79% | 3.0 | 13.7 | 21.9 |

## Do bigger expected moves come true? (realised gross bp going with the expected direction, by decile of the expected move)

| representation | exit | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| grid12 | H60 | +0.3 | -0.1 | +0.1 | +1.7 | -0.1 | +0.6 | +1.0 | +1.6 | +1.9 | +1.3 |
| grid12 | EOD | +0.3 | +0.2 | +1.3 | +1.2 | -1.4 | -1.3 | +0.1 | +1.4 | +4.8 | -1.0 |
| gmm4 | H60 | +0.1 | -0.4 | -0.5 | -0.7 | +1.1 | +0.6 | +0.1 | +0.6 | +1.3 | +1.6 |
| gmm4 | EOD | +0.5 | -0.5 | +3.4 | -0.3 | +1.7 | -0.0 | +0.0 | +3.3 | -0.1 | +0.2 |
| hmm4 | H60 | +1.2 | +0.1 | +0.0 | -0.2 | -0.2 | -0.2 | +1.1 | -0.6 | +2.8 | +0.2 |
| hmm4 | EOD | +1.6 | +2.2 | +1.6 | +3.4 | +0.5 | -2.3 | +3.9 | -0.8 | -2.0 | +1.5 |

D1 = the smallest tenth of expected moves, D10 = the largest. A usable signal rises from D1 to D10 and ends well above 12.49 bp.

## Calibration (fitted on earlier test windows only)

How much of each prediction came true before: c = the share of the state's predicted deviation that was realised (1 = all of it, 0 = none); a = the same for the stock's time-of-day baseline.

| representation | target | fold 2 | fold 3 | fold 4 | fold 5 |
|---|---|---|---|---|---|
| grid12 | H60 | a 0.27, c 0.23 | a 0.25, c 0.34 | a 0.19, c 0.41 | a 0.26, c 0.41 |
| grid12 | EOD | a 0.37, c 0.17 | a 0.00, c 0.30 | a 0.06, c 0.34 | a 0.24, c 0.26 |
| grid12 | barrier | c 0.36 | c 0.32 | c 0.41 | c 0.36 |
| gmm4 | H60 | a 0.26, c 0.90 | a 0.25, c 0.61 | a 0.18, c 0.62 | a 0.26, c 0.66 |
| gmm4 | EOD | a 0.36, c 0.56 | a 0.00, c 0.36 | a 0.05, c 0.41 | a 0.24, c 0.37 |
| gmm4 | barrier | c 0.59 | c 0.33 | c 0.36 | c 0.39 |
| hmm4 | H60 | a 0.26, c 0.60 | a 0.25, c 0.38 | a 0.18, c 0.40 | a 0.26, c 0.44 |
| hmm4 | EOD | a 0.35, c 0.42 | a 0.00, c 0.28 | a 0.05, c 0.34 | a 0.23, c 0.29 |
| hmm4 | barrier | c 0.32 | c 0.18 | c 0.21 | c 0.25 |

| representation | calibrated barrier-probability Brier skill vs the time-of-day baseline |
|---|---|
| grid12 | +0.0011 [-0.0004, +0.0025] |
| gmm4 | +0.0001 [-0.0010, +0.0012] |
| hmm4 | +0.0001 [-0.0006, +0.0008] |

## Limitations (stated before the run)

- In-sample to the project: 2021-10..2024-12 was searched by BIGMOVE discovery, Stage 0 and Stage B; folds 2-5 are out of sample for these models and calibrators only.
- The trade rule is a feasibility probe, not a strategy: one fixed entry, two fixed exits, no stop. A pass earns the next stage, never money.
- Costs are the engine's declared 12.49 bp a trade; a pass that does not survive 1.5x costs is flagged in the report but not failed here (Stage F applies the stress).
- Experiments: this run adds 6 tests to experiments.jsonl (cumulative count 14).
