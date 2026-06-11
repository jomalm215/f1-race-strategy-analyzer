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

# pit stop summary

def summarize_pit_stops(clean_laps : pd.DataFrame) -> pd.DataFrame:

    required_columns = [

        "Driver",
        "LapNumber",
        "Stint",
        "Compound",
        "IsPitInLap",

    ]

    missing_columns = [col for col in required_columns if col not in clean_laps.columns]
   
    if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    rows = []

    for driver, driver_laps in clean_laps.groupby("Driver"):
        driver_laps = driver_laps.sort_values("LapNumber").copy()

        pit_in_laps = driver_laps[driver_laps["IsPitInLap"]].copy()

        for _, pit_lap_row in pit_in_laps.iterrows():
            pit_lap_number =  pit_lap_row["LapNumber"]

            before_laps = driver_laps[driver_laps["LapNumber"] < pit_lap_number]
            after_laps = driver_laps[driver_laps["LapNumber"] > pit_lap_number]

            if before_laps.empty or after_laps.empty:
                continue

            lap_before = before_laps.iloc[-1]
            lap_after = after_laps.iloc[0]

            rows.append(
                {
                    "Driver": driver,
                    "PitLap": pit_lap_number,
                    "StintBefore": lap_before["Stint"],
                    "StintAfter": lap_after["Stint"],
                    "CompoundBefore": lap_before["Compound"],
                    "CompoundAfter": lap_after["Compound"],
                }
            )

    if not rows:
        return pd.DataFrame(

            columns=[

                "Driver",
                "PitLap",
                "StintBefore",
                "StintAfter",
                "CompoundBefore",
                "CompoundAfter",

            ]
        )

    return pd.DataFrame(rows).sort_values(["Driver", "PitLap"]).reset_index(drop=True)

def estimate_pit_loss(clean_laps: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate pit stop loss for each detected pit-in lap.

    Method:
    - Find each pit-in lap.
    - Compare that pit lap time against the driver's nearby clean racing pace.
    - Nearby pace is estimated using the median of clean laps within +/- 3 laps.

    This is a rough estimate, not an official pit loss calculation.
    """

    required_columns = [
        "Driver",
        "LapNumber",
        "LapTimeSeconds",
        "IsPitInLap",
        "IsPitLap",
        "IsExtremeSlowLap",
    ]

    missing_columns = [col for col in required_columns if col not in clean_laps.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    rows = []

    for driver, driver_laps in clean_laps.groupby("Driver"):
        driver_laps = driver_laps.sort_values("LapNumber").copy()
        pit_laps = driver_laps[driver_laps["IsPitInLap"]].copy()

        for _, pit_row in pit_laps.iterrows():
            pit_lap_number = pit_row["LapNumber"]
            pit_lap_time = pit_row["LapTimeSeconds"]

            nearby_clean_laps = driver_laps[
                (driver_laps["LapNumber"] >= pit_lap_number - 3)
                & (driver_laps["LapNumber"] <= pit_lap_number + 3)
                & (~driver_laps["IsPitLap"])
                & (~driver_laps["IsExtremeSlowLap"])
                & (driver_laps["LapTimeSeconds"].notna())
            ].copy()

            if nearby_clean_laps.empty:
                reference_lap_time = driver_laps[
                    (~driver_laps["IsPitLap"])
                    & (~driver_laps["IsExtremeSlowLap"])
                    & (driver_laps["LapTimeSeconds"].notna())
                ]["LapTimeSeconds"].median()
            else:
                reference_lap_time = nearby_clean_laps["LapTimeSeconds"].median()

            estimated_pit_loss = pit_lap_time - reference_lap_time

            rows.append(
                {
                    "Driver": driver,
                    "PitLap": pit_lap_number,
                    "PitLapTime": pit_lap_time,
                    "ReferenceLapTime": reference_lap_time,
                    "EstimatedPitLoss": estimated_pit_loss,
                }
            )

    if not rows:
        return pd.DataFrame(
            columns=[
                "Driver",
                "PitLap",
                "PitLapTime",
                "ReferenceLapTime",
                "EstimatedPitLoss",
            ]
        )

    return pd.DataFrame(rows).sort_values(["Driver", "PitLap"]).reset_index(drop=True)


# improve readability, summary of analysis for the streamlit dashboad and insights
def generate_strategy_observations(
        
    stint_summary: pd.DataFrame,
    degradation : pd.DataFrame,
    driver_ranking: pd.DataFrame,
    pit_stop_summary: pd.DataFrame,
    pit_loss_summary: pd.DataFrame,
    drivers : list[str],
) -> list[str]:
    
    observations: list[str] = []
    selected_stints = stint_summary[stint_summary["Driver"].isin(drivers)].copy()
    selected_degradation = degradation[degradation["Driver"].isin(drivers)].copy()
    selected_ranking = driver_ranking[driver_ranking["Driver"].isin(drivers)].copy()
    selected_pit_stops = pit_stop_summary[pit_stop_summary["Driver"].isin(drivers)].copy()
    selected_pit_loss = pit_loss_summary[pit_loss_summary["Driver"].isin(drivers)].copy()

    # 1. Fastest clean median pace among selected drivers.
    if not selected_ranking.empty and "MedianLapTime" in selected_ranking.columns:
        fastest_row = selected_ranking.sort_values("MedianLapTime").iloc[0]
        observations.append(
            f"{fastest_row['Driver']} had the fastest selected-driver clean median race pace "
            f"at {fastest_row['MedianLapTime']:.3f} seconds."
        )

    # 2. Longest stint among selected drivers.
    if not selected_stints.empty and "StintLength" in selected_stints.columns:
        longest_stint = selected_stints.sort_values("StintLength", ascending=False).iloc[0]
        observations.append(
            f"{longest_stint['Driver']} completed the longest selected-driver stint: "
            f"{int(longest_stint['StintLength'])} laps on {longest_stint['Compound']} "
            f"from lap {int(longest_stint['StartLap'])} to lap {int(longest_stint['EndLap'])}."
        )

    # 3. Pit stop count by driver.
    if not selected_pit_stops.empty:
        pit_counts = (
            selected_pit_stops.groupby("Driver")
            .size()
            .reset_index(name="PitStopCount")
            .sort_values("PitStopCount", ascending=False)
        )

        max_stops = pit_counts["PitStopCount"].max()
        most_stops = pit_counts[pit_counts["PitStopCount"] == max_stops]["Driver"].tolist()

        observations.append(
            f"Most detected pit stops among selected drivers: {', '.join(most_stops)} "
            f"with {int(max_stops)} stop(s)."
        )

        one_stop_drivers = pit_counts[pit_counts["PitStopCount"] == 1]["Driver"].tolist()
        if one_stop_drivers:
            observations.append(
                f"Detected one-stop drivers among the selected group: {', '.join(one_stop_drivers)}."
            )

    # 4. Lowest estimated pit loss.
    if not selected_pit_loss.empty and "EstimatedPitLoss" in selected_pit_loss.columns:
        valid_pit_loss = selected_pit_loss[selected_pit_loss["EstimatedPitLoss"].notna()].copy()

        if not valid_pit_loss.empty:
            lowest_loss = valid_pit_loss.sort_values("EstimatedPitLoss").iloc[0]
            observations.append(
                f"Lowest rough pit-loss estimate among selected drivers: {lowest_loss['Driver']} "
                f"on lap {int(lowest_loss['PitLap'])}, approximately "
                f"{lowest_loss['EstimatedPitLoss']:.3f} seconds."
            )

    # 5. Most stable stint by raw pace slope.
    if (
        not selected_degradation.empty
        and "DegradationSecondsPerLap" in selected_degradation.columns
    ):
        stable = selected_degradation.copy()
        stable["AbsSlope"] = stable["DegradationSecondsPerLap"].abs()
        stable = stable.sort_values("AbsSlope")

        most_stable = stable.iloc[0]
        observations.append(
            f"Most stable raw pace slope among selected stints: {most_stable['Driver']} "
            f"stint {int(most_stable['Stint'])} on {most_stable['Compound']} "
            f"at {most_stable['DegradationSecondsPerLap']:.4f} sec/lap."
        )

    # Fallback if no observations were generated.
    if not observations:
        observations.append(
            "No automatic observations were generated. Check the input drivers and available race data."
        )

    observations.append(
        "Note: these observations are based on cleaned lap-time data and should be treated as strategy indicators, not final proof."
    )

    return observations
