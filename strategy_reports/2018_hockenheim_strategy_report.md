# 2018 Hockenheim Strategy Analysis

## Session

- Year: 2018
- Race: Hockenheim
- Session: R
- Drivers analyzed: VET, RAI, BOT, HAM

## Lap Time Plot

![Lap time plot](../../plots/2018_hockenheim_race_lap_times.png)

## Compound Stint Plot

This plot shows selected drivers' clean lap times with points colored by tyre compound. It helps connect lap-time trends to stint strategy.

![Compound stint plot](../../plots/2018_hockenheim_compound_stint_lap_times.png)

## Clean Pace Ranking

This ranks drivers by median clean lap time after removing pit laps and extreme slow laps. It is useful for a quick race-pace comparison, but it does not fully normalize for compound, fuel, traffic, or strategy.

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   DeltaToFastestMedian |
|:---------|----------------:|--------------:|----------------:|--------------:|-----------------------:|
| HAM      |              59 |       78.5164 |          78.07  |        75.545 |                  0     |
| RAI      |              59 |       78.5523 |          78.2   |        75.99  |                  0.13  |
| BOT      |              59 |       78.4615 |          78.355 |        75.721 |                  0.285 |
| VET      |              49 |       78.7511 |          78.377 |        77.29  |                  0.307 |

## Pit Stop Summary

This table summarizes detected pit stops using pit-in laps. It shows the lap where each driver pitted and the compound change before and after the stop.

| Driver   |   PitLap |   StintBefore |   StintAfter | CompoundBefore   | CompoundAfter   |
|:---------|---------:|--------------:|-------------:|:-----------------|:----------------|
| BOT      |       28 |             1 |            2 | ULTRASOFT        | SOFT            |
| BOT      |       52 |             2 |            3 | SOFT             | ULTRASOFT       |
| HAM      |       42 |             1 |            2 | SOFT             | ULTRASOFT       |
| RAI      |       14 |             1 |            2 | ULTRASOFT        | SOFT            |
| RAI      |       53 |             2 |            3 | SOFT             | ULTRASOFT       |
| VET      |       25 |             1 |            2 | ULTRASOFT        | SOFT            |

## Pit Loss Estimate

This table estimates rough pit loss by comparing each pit-in lap time against nearby clean racing laps. It is an approximation and can be affected by traffic, out-lap behavior, tyre warmup, and race conditions.

| Driver   |   PitLap |   PitLapTime |   ReferenceLapTime |   EstimatedPitLoss |
|:---------|---------:|-------------:|-------------------:|-------------------:|
| BOT      |       28 |       83.547 |            78.899  |             4.648  |
| BOT      |       52 |      102.191 |            82.063  |            20.128  |
| HAM      |       42 |       81.893 |            77.87   |             4.023  |
| RAI      |       14 |       81.741 |            78.472  |             3.269  |
| RAI      |       53 |      131.483 |            88.0645 |            43.4185 |
| VET      |       25 |       82.849 |            78.649  |             4.2    |

## Head-to-Head Driver Comparison

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   MedianDeltaToOther |
|:---------|----------------:|--------------:|----------------:|--------------:|---------------------:|
| RAI      |              59 |       78.5523 |          78.2   |         75.99 |               -0.177 |
| VET      |              49 |       78.7511 |          78.377 |         77.29 |                0.177 |

## Stint Summary

| Driver   |   Stint | Compound   |   StartLap |   EndLap |   LapCount |   StartTyreLife |   EndTyreLife |   MeanLapTime |   MedianLapTime |   BestLapTime |   StintLength |
|:---------|--------:|:-----------|-----------:|---------:|-----------:|----------------:|--------------:|--------------:|----------------:|--------------:|--------------:|
| BOT      |       1 | ULTRASOFT  |          2 |       27 |         26 |               4 |            29 |       78.6515 |         78.592  |        78.092 |            26 |
| BOT      |       2 | SOFT       |         30 |       51 |         22 |               2 |            23 |       79.0265 |         77.757  |        76.956 |            22 |
| BOT      |       3 | ULTRASOFT  |         58 |       67 |         10 |               6 |            15 |       76.3737 |         76.345  |        75.721 |            10 |
| BOT      |     nan | nan        |          1 |        1 |          1 |             nan |           nan |       81.972  |         81.972  |        81.972 |             1 |
| HAM      |       1 | SOFT       |          2 |       41 |         40 |               1 |            40 |       78.6165 |         78.2075 |        77.523 |            40 |
| HAM      |       2 | ULTRASOFT  |         44 |       67 |         18 |               2 |            25 |       77.6529 |         76.485  |        75.545 |            24 |
| HAM      |     nan | nan        |          1 |        1 |          1 |             nan |           nan |       90.059  |         90.059  |        90.059 |             1 |
| RAI      |       1 | ULTRASOFT  |          2 |       13 |         12 |               4 |            15 |       78.6286 |         78.6885 |        78.2   |            12 |
| RAI      |       2 | SOFT       |         16 |       51 |         36 |               2 |            37 |       78.9613 |         78.1215 |        77.152 |            36 |
| RAI      |       3 | ULTRASOFT  |         58 |       67 |         10 |               5 |            14 |       76.5121 |         76.412  |        75.99  |            10 |
| RAI      |     nan | nan        |          1 |        1 |          1 |             nan |           nan |       83.317  |         83.317  |        83.317 |             1 |
| VET      |       1 | ULTRASOFT  |          3 |       24 |         22 |               4 |            25 |       78.4488 |         78.5035 |        77.777 |            22 |
| VET      |       2 | SOFT       |         27 |       51 |         25 |               2 |            26 |       78.9668 |         78.204  |        77.29  |            25 |
| VET      |     nan | nan        |          1 |        2 |          2 |             nan |           nan |       79.3815 |         79.3815 |        77.942 |             2 |

## Estimated Pace Slope / Degradation Proxy

The slope below is a simple linear fit of lap time versus tyre life. Positive values mean laps got slower as tyre life increased. Negative values mean laps got faster as the stint progressed, which can happen because of fuel burn, track evolution, clean air, or race management.

| Driver   |   Stint | Compound   |   LapCountUsed |   StartLap |   EndLap |   StartTyreLife |   EndTyreLife |   DegradationSecondsPerLap |   EstimatedBaseLapTime |   MeanLapTime |   MedianLapTime |
|:---------|--------:|:-----------|---------------:|-----------:|---------:|----------------:|--------------:|---------------------------:|-----------------------:|--------------:|----------------:|
| BOT      |       1 | ULTRASOFT  |             26 |          2 |       27 |               4 |            29 |                  0.0245795 |                78.2459 |       78.6515 |         78.592  |
| BOT      |       2 | SOFT       |             22 |         30 |       51 |               2 |            23 |                  0.304799  |                75.2165 |       79.0265 |         77.757  |
| BOT      |       3 | ULTRASOFT  |             10 |         58 |       67 |               6 |            15 |                 -0.13243   |                77.7642 |       76.3737 |         76.345  |
| HAM      |       1 | SOFT       |             40 |          2 |       41 |               1 |            40 |                 -0.0520435 |                79.6833 |       78.6165 |         78.2075 |
| HAM      |       2 | ULTRASOFT  |             18 |         44 |       67 |               2 |            25 |                 -0.186164  |                80.2282 |       77.6529 |         76.485  |
| RAI      |       1 | ULTRASOFT  |             12 |          2 |       13 |               4 |            15 |                  0.0384021 |                78.2638 |       78.6286 |         78.6885 |
| RAI      |       2 | SOFT       |             36 |         16 |       51 |               2 |            37 |                  0.140933  |                76.2131 |       78.9613 |         78.1215 |
| RAI      |       3 | ULTRASOFT  |             10 |         58 |       67 |               5 |            14 |                 -0.120273  |                77.6547 |       76.5121 |         76.412  |
| VET      |       1 | ULTRASOFT  |             22 |          3 |       24 |               4 |            25 |                  0.026188  |                78.069  |       78.4488 |         78.5035 |
| VET      |       2 | SOFT       |             25 |         27 |       51 |               2 |            26 |                  0.199778  |                76.1699 |       78.9668 |         78.204  |

## Notes and Limitations

This report uses cleaned lap-time data from FastF1. The analysis removes pit laps and extreme slow laps, but it does not yet fully model fuel burn, traffic, safety car periods, tyre warmup, driver management, car damage, or exact pit-loss time. Therefore, the results should be treated as strategy indicators rather than final proof.
