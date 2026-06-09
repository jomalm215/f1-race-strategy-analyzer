import numpy as np
import pandas as pd

# tire stint summaries

def summarize_stints(clean_laps : pd.DataFrame) -> pd.DataFrame:

    required_columns = [
        "Driver",
        "Stint",
        "Compound",
        "LapNumber",
        "LapTimeSeconds",
        "TyreLife",
        "IsPitLap",
        "IsExtremeSlowLap",
    ]

    missing_columns = [col for col in required_columns if col not in clean_laps.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    racing_laps = clean_laps[
        (~clean_laps["IsPitLap"])
        & (~clean_laps["IsExtremeSlowLap"])
        & (clean_laps["LapTimeSeconds"].notna())
    ].copy()

    grouped = (
        racing_laps
        .groupby(["Driver", "Stint", "Compound"], dropna=False)
        .agg(
            StartLap=("LapNumber", "min"),
            EndLap=("LapNumber", "max"),
            LapCount=("LapNumber", "count"),
            StartTyreLife=("TyreLife", "min"),
            EndTyreLife=("TyreLife", "max"),
            MeanLapTime=("LapTimeSeconds", "mean"),
            MedianLapTime=("LapTimeSeconds", "median"),
            BestLapTime=("LapTimeSeconds", "min"),
        )
        .reset_index()
    )

    grouped["StintLength"] = grouped["EndLap"] - grouped["StartLap"] + 1

    return grouped.sort_values(["Driver", "Stint"]).reset_index(drop=True)

# 1st order estimate of tire deg
def estimate_stint_degradation(clean_laps: pd.DataFrame, min_laps: int = 5) -> pd.DataFrame:
 
    required_columns = [
        "Driver",
        "Stint",
        "Compound",
        "LapNumber",
        "LapTimeSeconds",
        "TyreLife",
        "IsPitLap",
        "IsExtremeSlowLap",
    ]

    missing_columns = [col for col in required_columns if col not in clean_laps.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    racing_laps = clean_laps[
        (~clean_laps["IsPitLap"])
        & (~clean_laps["IsExtremeSlowLap"])
        & (clean_laps["LapTimeSeconds"].notna())
        & (clean_laps["TyreLife"].notna())
    ].copy()

    rows = []

    for (driver, stint, compound), group in racing_laps.groupby(
        ["Driver", "Stint", "Compound"], dropna=False
    ):
        group = group.sort_values("TyreLife").copy()

        if len(group) < min_laps:
            continue

        x = group["TyreLife"].astype(float).to_numpy()
        y = group["LapTimeSeconds"].astype(float).to_numpy()

        # Need at least two unique tyre-life values to fit a line.
        if len(np.unique(x)) < 2:
            continue

        slope, intercept = np.polyfit(x, y, 1)

        rows.append(
            {
                "Driver": driver,
                "Stint": stint,
                "Compound": compound,
                "LapCountUsed": len(group),
                "StartLap": group["LapNumber"].min(),
                "EndLap": group["LapNumber"].max(),
                "StartTyreLife": group["TyreLife"].min(),
                "EndTyreLife": group["TyreLife"].max(),
                "DegradationSecondsPerLap": slope,
                "EstimatedBaseLapTime": intercept,
                "MeanLapTime": group["LapTimeSeconds"].mean(),
                "MedianLapTime": group["LapTimeSeconds"].median(),
            }
        )

    return pd.DataFrame(rows).sort_values(["Driver", "Stint"]).reset_index(drop=True)

# driver comparison (in clean air)
def compare_drivers(clean_laps: pd.DataFrame, driver_1: str, driver_2: str) -> pd.DataFrame:

    racing_laps = clean_laps[
        (~clean_laps["IsPitLap"])
        & (~clean_laps["IsExtremeSlowLap"])
        & (clean_laps["LapTimeSeconds"].notna())
    ].copy()

    selected = racing_laps[racing_laps["Driver"].isin([driver_1, driver_2])].copy()

    if selected.empty:
        raise ValueError("No laps found for the selected drivers.")

    summary = (
        selected
        .groupby("Driver")
        .agg(
            CleanLapCount=("LapNumber", "count"),
            MeanLapTime=("LapTimeSeconds", "mean"),
            MedianLapTime=("LapTimeSeconds", "median"),
            BestLapTime=("LapTimeSeconds", "min"),
        )
        .reset_index()
    )

    if len(summary) == 2:
        d1_median = summary.loc[summary["Driver"] == driver_1, "MedianLapTime"].iloc[0]
        d2_median = summary.loc[summary["Driver"] == driver_2, "MedianLapTime"].iloc[0]

        summary["MedianDeltaToOther"] = summary["Driver"].map(
            {
                driver_1: d1_median - d2_median,
                driver_2: d2_median - d1_median,
            }
        )
    else:
        summary["MedianDeltaToOther"] = np.nan

    return summary.sort_values("MedianLapTime").reset_index(drop=True)

def rank_drivers_by_clean_pace(clean_laps: pd.DataFrame) -> pd.DataFrame:

    required_columns = [
        "Driver",
        "LapNumber",
        "LapTimeSeconds",
        "IsPitLap",
        "IsExtremeSlowLap",
    ]

    missing_columns = [col for col in required_columns if col not in clean_laps.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    racing_laps = clean_laps[
        (~clean_laps["IsPitLap"])
        & (~clean_laps["IsExtremeSlowLap"])
        & (clean_laps["LapTimeSeconds"].notna())
    ].copy()

    ranking = (
        racing_laps
        .groupby("Driver")
        .agg(
            CleanLapCount=("LapNumber", "count"),
            MeanLapTime=("LapTimeSeconds", "mean"),
            MedianLapTime=("LapTimeSeconds", "median"),
            BestLapTime=("LapTimeSeconds", "min"),
        )
        .reset_index()
        .sort_values("MedianLapTime")
        .reset_index(drop=True)
    )

    fastest_median = ranking["MedianLapTime"].min()
    ranking["DeltaToFastestMedian"] = ranking["MedianLapTime"] - fastest_median

    return ranking