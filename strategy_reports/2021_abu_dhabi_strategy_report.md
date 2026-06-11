# 2021 Abu Dhabi Strategy Analysis

## Session

- Year: 2021
- Race: Abu Dhabi
- Session: R
- Drivers analyzed: HAM, VER, STR

## Lap Time Plot

![Lap time plot](../../plots/2021_abu_dhabi_race_lap_times.png)

## Compound Stint Plot

This plot shows selected drivers' clean lap times with points colored by tyre compound. It helps connect lap-time trends to stint strategy.

![Compound stint plot](../../plots/2021_abu_dhabi_compound_stint_lap_times.png)

## Clean Pace Ranking

This ranks drivers by median clean lap time after removing pit laps and extreme slow laps. It is useful for a quick race-pace comparison, but it does not fully normalize for compound, fuel, traffic, or strategy.

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   DeltaToFastestMedian |
|:---------|----------------:|--------------:|----------------:|--------------:|-----------------------:|
| HAM      |              51 |       88.5351 |          87.889 |        86.615 |                  0     |
| VER      |              49 |       87.9626 |          88.041 |        86.103 |                  0.152 |
| STR      |              49 |       90.6857 |          90.369 |        88.567 |                  2.48  |

## Pit Stop Summary

This table summarizes detected pit stops using pit-in laps. It shows the lap where each driver pitted and the compound change before and after the stop.

| Driver   |   PitLap |   StintBefore |   StintAfter | CompoundBefore   | CompoundAfter   |
|:---------|---------:|--------------:|-------------:|:-----------------|:----------------|
| HAM      |       14 |             1 |            2 | MEDIUM           | HARD            |
| STR      |       21 |             1 |            2 | MEDIUM           | HARD            |
| STR      |       52 |             2 |            3 | HARD             | SOFT            |
| VER      |       13 |             1 |            2 | SOFT             | HARD            |
| VER      |       36 |             2 |            3 | HARD             | HARD            |
| VER      |       53 |             3 |            4 | HARD             | SOFT            |

## Pit Loss Estimate

This table estimates rough pit loss by comparing each pit-in lap time against nearby clean racing laps. It is an approximation and can be affected by traffic, out-lap behavior, tyre warmup, and race conditions.

| Driver   |   PitLap |   PitLapTime |   ReferenceLapTime |   EstimatedPitLoss |
|:---------|---------:|-------------:|-------------------:|-------------------:|
| HAM      |       14 |       90.253 |             88.134 |              2.119 |
| STR      |       21 |       92.575 |             90.283 |              2.292 |
| STR      |       52 |      105.169 |             88.709 |             16.46  |
| VER      |       13 |       91.515 |             89.006 |              2.509 |
| VER      |       36 |      103.598 |             87.581 |             16.017 |
| VER      |       53 |      102.072 |             87.048 |             15.024 |

## Head-to-Head Driver Comparison

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   MedianDeltaToOther |
|:---------|----------------:|--------------:|----------------:|--------------:|---------------------:|
| HAM      |              51 |       88.5351 |          87.889 |        86.615 |               -0.152 |
| VER      |              49 |       87.9626 |          88.041 |        86.103 |                0.152 |

## Stint Summary

| Driver   |   Stint | Compound   |   StartLap |   EndLap |   LapCount |   StartTyreLife |   EndTyreLife |   MeanLapTime |   MedianLapTime |   BestLapTime |   StintLength |
|:---------|--------:|:-----------|-----------:|---------:|-----------:|----------------:|--------------:|--------------:|----------------:|--------------:|--------------:|
| HAM      |       1 | MEDIUM     |          1 |       13 |         13 |               4 |            16 |       88.7493 |         88.585  |        88.134 |            13 |
| HAM      |       2 | HARD       |         16 |       58 |         38 |               3 |            45 |       88.4618 |         87.627  |        86.615 |            43 |
| STR      |       1 | MEDIUM     |          1 |       20 |         20 |               1 |            20 |       91.6154 |         90.9325 |        90.283 |            20 |
| STR      |       2 | HARD       |         23 |       51 |         28 |               2 |            30 |       89.9607 |         89.355  |        88.567 |            29 |
| STR      |       3 | SOFT       |         57 |       57 |          1 |               5 |             5 |       92.389  |         92.389  |        92.389 |             1 |
| VER      |       1 | SOFT       |          1 |       12 |         12 |               4 |            15 |       89.2178 |         88.8585 |        88.636 |            12 |
| VER      |       2 | HARD       |         15 |       35 |         21 |               2 |            22 |       88.234  |         88.179  |        87.581 |            21 |
| VER      |       3 | HARD       |         38 |       52 |         15 |               2 |            16 |       86.6682 |         86.656  |        86.103 |            15 |
| VER      |       4 | SOFT       |         58 |       58 |          1 |               8 |             8 |       86.618  |         86.618  |        86.618 |             1 |

## Estimated Pace Slope / Degradation Proxy

The slope below is a simple linear fit of lap time versus tyre life. Positive values mean laps got slower as tyre life increased. Negative values mean laps got faster as the stint progressed, which can happen because of fuel burn, track evolution, clean air, or race management.

| Driver   |   Stint | Compound   |   LapCountUsed |   StartLap |   EndLap |   StartTyreLife |   EndTyreLife |   DegradationSecondsPerLap |   EstimatedBaseLapTime |   MeanLapTime |   MedianLapTime |
|:---------|--------:|:-----------|---------------:|-----------:|---------:|----------------:|--------------:|---------------------------:|-----------------------:|--------------:|----------------:|
| HAM      |       1 | MEDIUM     |             13 |          1 |       13 |               4 |            16 |               -0.141648    |                90.1658 |       88.7493 |         88.585  |
| HAM      |       2 | HARD       |             38 |         16 |       58 |               3 |            45 |                7.17718e-05 |                88.4603 |       88.4618 |         87.627  |
| STR      |       1 | MEDIUM     |             20 |          1 |       20 |               1 |            20 |               -0.235819    |                94.0915 |       91.6154 |         90.9325 |
| STR      |       2 | HARD       |             28 |         23 |       51 |               2 |            30 |               -0.0583242   |                90.896  |       89.9607 |         89.355  |
| VER      |       1 | SOFT       |             12 |          1 |       12 |               4 |            15 |               -0.138112    |                90.5299 |       89.2178 |         88.8585 |
| VER      |       2 | HARD       |             21 |         15 |       35 |               2 |            22 |               -0.0597805   |                88.9514 |       88.234  |         88.179  |
| VER      |       3 | HARD       |             15 |         38 |       52 |               2 |            16 |                0.0631821   |                86.0996 |       86.6682 |         86.656  |

## Notes and Limitations

This report uses cleaned lap-time data from FastF1. The analysis removes pit laps and extreme slow laps, but it does not yet fully model fuel burn, traffic, safety car periods, tyre warmup, driver management, car damage, or exact pit-loss time. Therefore, the results should be treated as strategy indicators rather than final proof.
