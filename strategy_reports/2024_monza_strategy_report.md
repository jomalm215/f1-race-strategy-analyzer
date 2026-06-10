# 2024 Monza Strategy Analysis

## Session

- Year: 2024
- Race: Monza
- Session: R
- Drivers analyzed: LEC, SAI

## Lap Time Plot

![Lap time plot](../../plots/2024_monza_race_lap_times.png)

## Compound Stint Plot

This plot shows selected drivers' clean lap times with points colored by tyre compound. It helps connect lap-time trends to stint strategy.

![Compound stint plot](../../plots/2024_monza_compound_stint_lap_times.png)

## Clean Pace Ranking

This ranks drivers by median clean lap time after removing pit laps and extreme slow laps. It is useful for a quick race-pace comparison, but it does not fully normalize for compound, fuel, traffic, or strategy.

| Driver   |   CleanLapCount |   MeanLapTime |   MedianLapTime |   BestLapTime |   DeltaToFastestMedian |
|:---------|----------------:|--------------:|----------------:|--------------:|-----------------------:|
| LEC      |              51 |       84.0323 |          83.718 |        83.226 |                  0.238 |
| SAI      |              51 |       84.3363 |          83.931 |        83.219 |                  0.451 |

## Pit Stop Summary

This table summarizes detected pit stops using pit-in laps. It shows the lap where each driver pitted and the compound change before and after the stop.

| Driver   |   PitLap |   StintBefore |   StintAfter | CompoundBefore   | CompoundAfter   |
|:---------|---------:|--------------:|-------------:|:-----------------|:----------------|
| LEC      |       15 |             1 |            2 | MEDIUM           | HARD            |
| SAI      |       19 |             1 |            2 | MEDIUM           | HARD            |

## Pit Loss Estimate

This table estimates rough pit loss by comparing each pit-in lap time against nearby clean racing laps. It is an approximation and can be affected by traffic, out-lap behavior, tyre warmup, and race conditions.

| Driver   |   PitLap |   PitLapTime |   ReferenceLapTime |   EstimatedPitLoss |
|:---------|---------:|-------------:|-------------------:|-------------------:|
| LEC      |       15 |       90.192 |             84.916 |              5.276 |
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
| SAI      |       1 | MEDIUM     |          1 |       18 |         18 |               1 |            18 |       85.3788 |         85.2085 |        84.642 |            18 |
| SAI      |       2 | HARD       |         21 |       53 |         33 |               2 |            34 |       83.7676 |         83.722  |        83.219 |            33 |

## Estimated Pace Slope / Degradation Proxy

The slope below is a simple linear fit of lap time versus tyre life. Positive values mean laps got slower as tyre life increased. Negative values mean laps got faster as the stint progressed, which can happen because of fuel burn, track evolution, clean air, or race management.

| Driver   |   Stint | Compound   |   LapCountUsed |   StartLap |   EndLap |   StartTyreLife |   EndTyreLife |   DegradationSecondsPerLap |   EstimatedBaseLapTime |   MeanLapTime |   MedianLapTime |
|:---------|--------:|:-----------|---------------:|-----------:|---------:|----------------:|--------------:|---------------------------:|-----------------------:|--------------:|----------------:|
| LEC      |       1 | MEDIUM     |             14 |          1 |       14 |               1 |            14 |                -0.0785143  |                85.6977 |       85.1089 |         84.828  |
| LEC      |       2 | HARD       |             37 |         17 |       53 |               2 |            38 |                -0.00832029 |                83.7914 |       83.6249 |         83.624  |
| SAI      |       1 | MEDIUM     |             18 |          1 |       18 |               1 |            18 |                -0.0573075  |                85.9233 |       85.3788 |         85.2085 |
| SAI      |       2 | HARD       |             33 |         21 |       53 |               2 |            34 |                 0.00394552 |                83.6966 |       83.7676 |         83.722  |

## Notes and Limitations

This report uses cleaned lap-time data from FastF1. The analysis removes pit laps and extreme slow laps, but it does not yet fully model fuel burn, traffic, safety car periods, tyre warmup, driver management, car damage, or exact pit-loss time. Therefore, the results should be treated as strategy indicators rather than final proof.
