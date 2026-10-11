# Stage B - behavioural state discovery

engine_stage_b v1.0 | engine_core v1.0 | declaration e3c6bd173874970a | 2026-10-12 00:33 | stocks HDFCBANK, ICICIBANK, SBIN, INFY, TCS, RELIANCE, BHARTIARTL, LT, MARUTI, SUNPHARMA (list ba1c73b77e553bc5) | development 2021-10-01..2024-12-31; nothing later is read

## VERDICT: STATES INFORMATIVE

Learned states carry out-of-sample information about which way the price goes next, beyond each stock's own time-of-day behaviour, and they are stable. This earns Stage C (confidence and evidence) for the representations marked below. It is NOT evidence of a profitable trade.

Preferred representation (the simplest informative and stable one not significantly worse than the best): **grid12**.

In plain words: 'Brier skill' is how much better the state predicts which barrier (+0.3 ATR or -0.3 ATR) is hit first than the stock's own time-of-day rate does (0 = no better; 0.01 = 1% lower squared error). 'IC' is the rank correlation, across the stocks at the same decision time, between the predicted and the actual next-hour return (both relative to the stock's time-of-day baseline), averaged per session. 'Magnitude' is the same skill for how far the price ranges in the next hour. All are pooled over the 5 test windows, which the models never saw; [ ] = 95% block-bootstrap interval over test sessions; Holm p corrects for the 16 direction tests.

| representation | states | Brier skill | Holm p | IC | Holm p | magnitude skill | seed ARI | refit ARI | PSI | persist (chance) | ECE | gross bp, n | fit s | informative | stable |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grid12 | 12 | -0.0021 [-0.0056, +0.0013] | 1.000 | +0.013 [+0.005, +0.022] | 0.016 | +0.071 [+0.057, +0.084] | 1.00 | 1.00 | 0.014 | 0.76 (0.13) | 0.036 | +1.2, 46,925 | 0.0 | YES | YES |
| kmeans4 | 4 | -0.0003 [-0.0029, +0.0023] | 1.000 | +0.008 [-0.000, +0.017] | 0.390 | +0.018 [+0.013, +0.022] | 0.73 | 0.78 | 0.028 | 0.86 (0.36) | 0.032 | +1.5, 47,989 | 2.6 | no | YES |
| kmeans8 | 8 | -0.0039 [-0.0078, -0.0003] | 1.000 | +0.009 [-0.002, +0.019] | 0.825 | +0.030 [+0.021, +0.040] | 0.76 | 0.79 | 0.089 | 0.84 (0.15) | 0.039 | +1.2, 47,489 | 6.4 | no | YES |
| gmm4 | 4 | -0.0007 [-0.0029, +0.0016] | 1.000 | +0.014 [+0.004, +0.023] | 0.030 | +0.031 [+0.025, +0.038] | 0.77 | 0.75 | 0.012 | 0.84 (0.32) | 0.035 | +1.2, 45,658 | 3.7 | YES | YES |
| gmm8 | 8 | -0.0028 [-0.0055, -0.0000] | 1.000 | +0.005 [-0.004, +0.014] | 1.000 | +0.053 [+0.044, +0.061] | 0.75 | 0.68 | 0.084 | 0.76 (0.16) | 0.034 | +1.1, 47,275 | 9.3 | no | YES |
| hmm4 | 4 | -0.0024 [-0.0049, +0.0003] | 1.000 | +0.012 [+0.003, +0.021] | 0.035 | +0.030 [+0.023, +0.037] | 0.93 | 0.69 | 0.015 | 0.90 (0.29) | 0.037 | +0.9, 46,969 | 4.9 | YES | YES |
| hmm8 | 8 | -0.0062 [-0.0097, -0.0029] | 1.000 | +0.006 [-0.005, +0.016] | 1.000 | +0.039 [+0.030, +0.049] | 0.91 | 0.71 | 0.107 | 0.90 (0.14) | 0.042 | +0.4, 45,076 | 10.3 | no | YES |
| knn100 | - | -0.0006 [-0.0030, +0.0017] | 1.000 | +0.013 [+0.003, +0.023] | 0.097 | +0.045 [+0.039, +0.052] | - | - | - | - (-) | 0.028 | +0.9, 45,017 | 5.2 | no | n/a |

Reading the columns: seed ARI = agreement of two fits with different random starts (1 = the same states); refit ARI = agreement of the previous window's model with this window's on the same test data; PSI = how much the states' shares move from training to test (under 0.25 is stable); persist = how often the state at one decision is the same 15 minutes later (vs chance); ECE = calibration error of the predicted barrier probability; gross bp = average gross return per observation of going with the prediction when it is in the training top fifth and against it in the bottom fifth, 60-minute exit, NO costs - compare with 12.49 bp per trade. It is context, not a strategy and not a gate.

## State confidence is not trade confidence (grid12)

Brier skill of the barrier prediction by state-confidence tercile (top state probability; training cut-offs), and on observations unlike the training data (novel: beyond its 1st percentile of likelihood / distance).

| representation | low-confidence skill (n) | mid | high | novel share | novel skill |
|---|---|---|---|---|---|
| kmeans4 | hard states: no probability to grade | | | 0.019 | +0.0027 |
| kmeans8 | hard states: no probability to grade | | | 0.019 | -0.0034 |
| gmm4 | -0.0017 (23,349) | -0.0039 (20,705) | +0.0034 (21,540) | 0.018 | -0.0062 |
| gmm8 | -0.0011 (22,953) | -0.0021 (21,260) | -0.0053 (21,381) | 0.019 | -0.0061 |
| hmm4 | -0.0017 (24,598) | -0.0048 (20,006) | -0.0009 (20,990) | 0.019 | -0.0088 |
| hmm8 | -0.0055 (25,150) | -0.0073 (20,741) | -0.0059 (19,703) | 0.018 | -0.0087 |

## Calibration of the predicted barrier probability (grid12, all test windows)

| predicted | n | mean predicted | observed |
|---|---|---|---|
| 0.2-0.3 | 119 | 0.282 | 0.345 |
| 0.3-0.4 | 4,559 | 0.371 | 0.454 |
| 0.4-0.5 | 34,456 | 0.459 | 0.494 |
| 0.5-0.6 | 25,386 | 0.532 | 0.505 |
| 0.6-0.7 | 1,074 | 0.621 | 0.532 |

Brier 0.2516 vs R0 0.2511; log loss 0.6965 vs R0 0.6954; ECE 0.036. These probabilities are the state's average outcome on past data, shrunk; they are NOT yet calibrated probabilities (that is Stage C, on a separate slice).

## State cards (grid12, last fold's model, training window)

Each state's share of training decisions and the 4 features furthest from typical (robust z, + = above usual). Outcome columns: the pooled shrunk deviation from the time-of-day baseline (barrier probability in points, next-hour return in ATR).

| state | share | what it looks like | barrier prob. dev. | next-hour ret dev. (ATR) |
|---|---|---|---|---|
| 0 | 0.115 | i_or -4.2, i_ret -1.2, i_vwap -1.1, i_eff +1.0 | -0.0480 | -0.0091 |
| 1 | 0.105 | i_or -3.5, i_ret -1.7, i_vwap -1.4, i_pdh -1.4 | -0.0152 | -0.0032 |
| 2 | 0.007 | i_or -1.7, i_ret -0.9, rs_n -0.9, al_w -0.7 | +0.0074 | -0.0057 |
| 3 | 0.017 | i_rv +1.4, i_rng +1.3, i_ret -1.2, rs_n -1.1 | +0.0115 | -0.0100 |
| 4 | 0.194 | i_or -1.0, i_rv -0.8, i_vx +0.6, i_rng -0.6 | -0.0211 | -0.0041 |
| 5 | 0.079 | i_rv +0.9, i_or -0.8, i_vwap -0.8, d_rng1 +0.6 | -0.0329 | -0.0073 |
| 6 | 0.182 | i_or +1.0, i_rv -0.7, i_vx +0.6, i_rng -0.6 | +0.0261 | +0.0041 |
| 7 | 0.077 | i_or +1.0, i_rv +0.9, i_vwap +0.8, d_rng1 +0.7 | +0.0321 | +0.0073 |
| 8 | 0.005 | i_or +2.0, i_ret +1.0, rs_n +1.0, al_w +0.9 | +0.0159 | +0.0044 |
| 9 | 0.019 | i_rng +1.4, i_rv +1.4, rs_n +1.3, i_ret +1.3 | +0.0107 | +0.0021 |
| 10 | 0.093 | i_or +4.3, i_ret +1.3, i_vwap +1.2, rs_n +1.1 | +0.0346 | +0.0096 |
| 11 | 0.107 | i_or +3.7, i_ret +1.8, rs_n +1.7, i_rng +1.5 | +0.0230 | +0.0065 |

## Per fold

| fold | train | test | representation | test rows | seed ARI | refit ARI | PSI | fit s |
|---|---|---|---|---|---|---|---|---|
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | grid12 | 25,746 | 1.00 | - | 0.024 | 0.0 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | kmeans4 | 25,746 | 0.52 | - | 0.013 | 1.8 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | kmeans8 | 25,746 | 0.60 | - | 0.029 | 3.3 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | gmm4 | 25,746 | 0.64 | - | 0.012 | 2.2 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | gmm8 | 25,746 | 0.67 | - | 0.029 | 5.7 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | hmm4 | 25,746 | 1.00 | - | 0.015 | 4.8 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | hmm8 | 25,746 | 0.57 | - | 0.021 | 5.5 |
| 1 | 2021-10-01..2022-09-30 | 2022-10-01..2023-03-31 | knn100 | 25,746 | - | - | - | 3.2 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | grid12 | 25,704 | 1.00 | 1.00 | 0.011 | 0.0 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | kmeans4 | 25,704 | 0.69 | 0.68 | 0.042 | 1.9 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | kmeans8 | 25,704 | 0.64 | 0.67 | 0.149 | 4.2 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | gmm4 | 25,704 | 0.77 | 0.71 | 0.028 | 2.1 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | gmm8 | 25,704 | 0.56 | 0.46 | 0.084 | 5.8 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | hmm4 | 25,704 | 1.00 | 0.54 | 0.044 | 3.0 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | hmm8 | 25,704 | 1.00 | 0.56 | 0.169 | 8.4 |
| 2 | 2021-10-01..2023-03-31 | 2023-04-01..2023-09-30 | knn100 | 25,704 | - | - | - | 4.5 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | grid12 | 25,179 | 1.00 | 1.00 | 0.014 | 0.0 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | kmeans4 | 25,179 | 0.68 | 0.94 | 0.033 | 2.3 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | kmeans8 | 25,179 | 1.00 | 0.69 | 0.089 | 6.9 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | gmm4 | 25,179 | 0.71 | 0.89 | 0.048 | 3.3 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | gmm8 | 25,179 | 1.00 | 0.56 | 0.131 | 12.0 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | hmm4 | 25,179 | 1.00 | 0.91 | 0.055 | 4.1 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | hmm8 | 25,179 | 1.00 | 0.75 | 0.115 | 10.9 |
| 3 | 2021-10-01..2023-09-30 | 2023-10-01..2024-03-31 | knn100 | 25,179 | - | - | - | 6.0 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | grid12 | 26,040 | 1.00 | 1.00 | 0.007 | 0.0 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | kmeans4 | 26,040 | 0.76 | 0.74 | 0.001 | 2.9 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | kmeans8 | 26,040 | 0.58 | 0.86 | 0.012 | 7.0 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | gmm4 | 26,040 | 0.71 | 0.72 | 0.001 | 3.6 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | gmm8 | 26,040 | 0.51 | 0.81 | 0.010 | 9.6 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | hmm4 | 26,040 | 0.67 | 0.67 | 0.001 | 4.7 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | hmm8 | 26,040 | 1.00 | 0.62 | 0.013 | 13.1 |
| 4 | 2021-10-01..2024-03-31 | 2024-04-01..2024-09-30 | knn100 | 26,040 | - | - | - | 8.0 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | grid12 | 12,768 | 1.00 | 1.00 | 0.019 | 0.0 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | kmeans4 | 12,768 | 1.00 | 0.77 | 0.028 | 4.0 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | kmeans8 | 12,768 | 1.00 | 0.94 | 0.116 | 10.4 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | gmm4 | 12,768 | 1.00 | 0.68 | 0.002 | 7.1 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | gmm8 | 12,768 | 1.00 | 0.91 | 0.096 | 13.6 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | hmm4 | 12,768 | 1.00 | 0.64 | 0.004 | 8.0 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | hmm8 | 12,768 | 1.00 | 0.92 | 0.107 | 13.2 |
| 5 | 2021-10-01..2024-09-30 | 2024-10-01..2024-12-31 | knn100 | 12,768 | - | - | - | 4.3 |

## Data

- HDFCBANK (NIFTY BANK): 793 clean of 799 development sessions; 16,653 decision points; barrier resolved 57.6% (1 hit both barriers inside one bar - order unknown, left out)
- ICICIBANK (NIFTY BANK): 796 clean of 799 development sessions; 16,716 decision points; barrier resolved 61.7% (1 hit both barriers inside one bar - order unknown, left out)
- SBIN (NIFTY BANK): 799 clean of 799 development sessions; 16,779 decision points; barrier resolved 59.0% (1 hit both barriers inside one bar - order unknown, left out)
- INFY (NIFTY IT): 796 clean of 799 development sessions; 16,716 decision points; barrier resolved 51.9% (0 hit both barriers inside one bar - order unknown, left out)
- TCS (NIFTY IT): 799 clean of 799 development sessions; 16,779 decision points; barrier resolved 55.0% (0 hit both barriers inside one bar - order unknown, left out)
- RELIANCE: 795 clean of 799 development sessions; 16,695 decision points; barrier resolved 58.8% (1 hit both barriers inside one bar - order unknown, left out)
- BHARTIARTL: 793 clean of 799 development sessions; 16,653 decision points; barrier resolved 57.3% (0 hit both barriers inside one bar - order unknown, left out)
- LT: 797 clean of 799 development sessions; 16,737 decision points; barrier resolved 56.4% (1 hit both barriers inside one bar - order unknown, left out)
- MARUTI: 796 clean of 799 development sessions; 16,716 decision points; barrier resolved 55.3% (3 hit both barriers inside one bar - order unknown, left out)
- SUNPHARMA: 798 clean of 799 development sessions; 16,758 decision points; barrier resolved 59.1% (1 hit both barriers inside one bar - order unknown, left out)

## Limitations (stated before the run)

- In-sample to the project: 2021-10..2024-12 was already searched by BIGMOVE discovery and Stage 0. The walk-forward test windows are out of sample for these models only.
- Decision points 15 minutes apart with 60-minute outcomes overlap; the bootstrap resamples whole sessions in blocks of 10, which keeps that overlap inside each resample.
- Information is not money: a state can predict direction a little and still lose after 12.49 bp a trade. Stage B prices nothing.
- Experiments: this run adds 8 representations to experiments.jsonl (cumulative count 8); prior research before the engine: at least 84 + 6 + 80 + 20 = 190 declared cells before this engine, plus their gate and exit variants; the engine's own experiments are added in experiments.jsonl.
