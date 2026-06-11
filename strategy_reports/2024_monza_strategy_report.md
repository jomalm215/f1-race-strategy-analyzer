# 2024 Monza Strategy Analysis

## Session

- Year: 2024
- Race: Monza
- Session: R
- Drivers analyzed: LEC, SAI, NOR, PIA

## Lap Time Plot

![Lap time plot](../../plots/2024_monza_race_lap_times.png)

## Compound Stint Plot

This plot shows selected drivers' clean lap times with points colored by tyre compound. It helps connect lap-time trends to stint strategy.

![Compound stint plot](../../plots/2024_monza_compound_stint_lap_times.png)

## Clean Pace Ranking

This ranks drivers by median clean lap time after removing pit laps and extreme slow laps. It is useful for a quick race-pace comparison, but it does not fully normalize for compound, fuel, traffic, or strategy.

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   DeltaToFastestMedian |
|:---------|----------------:|--------------:|----------------:|--------------:|-----------------------:|
| PIA      |              49 |       83.6253 |          83.48  |        81.943 |                  0     |
| NOR      |              49 |       83.7171 |          83.601 |        81.432 |                  0.121 |
| LEC      |              51 |       84.0323 |          83.718 |        83.226 |                  0.238 |
| SAI      |              51 |       84.3363 |          83.931 |        83.219 |                  0.451 |

## Pit Stop Summary

This table summarizes detected pit stops using pit-in laps. It shows the lap where each driver pitted and the compound change before and after the stop.

| Driver   |   PitLap |   StintBefore |   StintAfter | CompoundBefore   | CompoundAfter   |
|:---------|---------:|--------------:|-------------:|:-----------------|:----------------|
| LEC      |       15 |             1 |            2 | MEDIUM           | HARD            |
| NOR      |       14 |             1 |            2 | MEDIUM           | HARD            |
| NOR      |       32 |             2 |            3 | HARD             | HARD            |
| PIA      |       16 |             1 |            2 | MEDIUM           | HARD            |
| PIA      |       38 |             2 |            3 | HARD             | HARD            |
| SAI      |       19 |             1 |            2 | MEDIUM           | HARD            |

## Pit Loss Estimate

This table estimates rough pit loss by comparing each pit-in lap time against nearby clean racing laps. It is an approximation and can be affected by traffic, out-lap behavior, tyre warmup, and race conditions.

| Driver   |   PitLap |   PitLapTime |   ReferenceLapTime |   EstimatedPitLoss |
|:---------|---------:|-------------:|-------------------:|-------------------:|
| LEC      |       15 |       90.192 |             84.916 |              5.276 |
| NOR      |       14 |       89.417 |             84.655 |              4.762 |
| NOR      |       32 |       87.414 |             83.3   |              4.114 |
| PIA      |       16 |       89.939 |             84.67  |              5.269 |
| PIA      |       38 |       88.125 |             83.409 |              4.716 |
| SAI      |       19 |       90.388 |             85.341 |              5.047 |

## Head-to-Head Driver Comparison

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   MedianDeltaToOther |
|:---------|----------------:|--------------:|----------------:|--------------:|---------------------:|
| LEC      |              51 |       84.0323 |          83.718 |        83.226 |               -0.213 |
| SAI      |              51 |       84.3363 |          83.931 |        83.219 |                0.213 |

## Stint Summary

| Driver   |   Stint | Compound   |   StartLap |   EndLap |   LapCount |   StartTyreLife |   EndTyreLife |   MeanLapTime |   MedianLapTime |   BestLapTime |   StintLength |
|:---------|--------:|:-----------|-----------:|---------:|-----------:|----------------:|--------------:|--------------:|----------------:|--------------:|--------------:|
| LEC      |       1 | MEDIUM     |          1 |       14 |         14 |               1 |            14 |       85.1089 |         84.828  |        84.362 |            14 |
| LEC      |       2 | HARD       |         17 |       53 |         37 |               2 |            38 |       83.6249 |         83.624  |        83.226 |            37 |
| NOR      |       1 | MEDIUM     |          1 |       13 |         13 |               1 |            13 |       85.1439 |         84.674  |        84.391 |            13 |
| NOR      |       2 | HARD       |         16 |       31 |         16 |               2 |            17 |       83.8286 |         83.633  |        83.067 |            16 |
| NOR      |       3 | HARD       |         34 |       53 |         20 |               2 |            21 |       82.7004 |         82.557  |        81.432 |            20 |
| PIA      |       1 | MEDIUM     |          1 |       15 |         15 |               1 |            15 |       84.8851 |         84.67   |        84.077 |            15 |
| PIA      |       2 | HARD       |         18 |       37 |         20 |               2 |            21 |       83.4972 |         83.4325 |        82.968 |            20 |
| PIA      |       3 | HARD       |         40 |       53 |         14 |               2 |            15 |       82.4584 |         82.3775 |        81.943 |            14 |
| SAI      |       1 | MEDIUM     |          1 |       18 |         18 |               1 |            18 |       85.3788 |         85.2085 |        84.642 |            18 |
| SAI      |       2 | HARD       |         21 |       53 |         33 |               2 |            34 |       83.7676 |         83.722  |        83.219 |            33 |

## Estimated Pace Slope / Degradation Proxy

The slope below is a simple linear fit of lap time versus tyre life. Positive values mean laps got slower as tyre life increased. Negative values mean laps got faster as the stint progressed, which can happen because of fuel burn, track evolution, clean air, or race management.

| Driver   |   Stint | Compound   |   LapCountUsed |   StartLap |   EndLap |   StartTyreLife |   EndTyreLife |   DegradationSecondsPerLap |   EstimatedBaseLapTime |   MeanLapTime |   MedianLapTime |
|:---------|--------:|:-----------|---------------:|-----------:|---------:|----------------:|--------------:|---------------------------:|-----------------------:|--------------:|----------------:|
| LEC      |       1 | MEDIUM     |             14 |          1 |       14 |               1 |            14 |                -0.0785143  |                85.6977 |       85.1089 |         84.828  |
| LEC      |       2 | HARD       |             37 |         17 |       53 |               2 |            38 |                -0.00832029 |                83.7914 |       83.6249 |         83.624  |
| NOR      |       1 | MEDIUM     |             13 |          1 |       13 |               1 |            13 |                -0.169121   |                86.3278 |       85.1439 |         84.674  |
| NOR      |       2 | HARD       |             16 |         16 |       31 |               2 |            17 |                -0.0545824  |                84.3472 |       83.8286 |         83.633  |
| NOR      |       3 | HARD       |             20 |         34 |       53 |               2 |            21 |                -0.0564233  |                83.3492 |       82.7003 |         82.557  |
| PIA      |       1 | MEDIUM     |             15 |          1 |       15 |               1 |            15 |                -0.0810143  |                85.5332 |       84.8851 |         84.67   |
| PIA      |       2 | HARD       |             20 |         18 |       37 |               2 |            21 |                -0.0335481  |                83.8831 |       83.4973 |         83.4325 |
| PIA      |       3 | HARD       |             14 |         40 |       53 |               2 |            15 |                -0.00598901 |                82.5093 |       82.4584 |         82.3775 |
| SAI      |       1 | MEDIUM     |             18 |          1 |       18 |               1 |            18 |                -0.0573075  |                85.9233 |       85.3788 |         85.2085 |
| SAI      |       2 | HARD       |             33 |         21 |       53 |               2 |            34 |                 0.00394552 |                83.6966 |       83.7676 |         83.722  |

## Notes and Limitations

This report uses cleaned lap-time data from FastF1. The analysis removes pit laps and extreme slow laps, but it does not yet fully model fuel burn, traffic, safety car periods, tyre warmup, driver management, car damage, or exact pit-loss time. Therefore, the results should be treated as strategy indicators rather than final proof.
