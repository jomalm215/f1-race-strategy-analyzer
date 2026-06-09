import pandas as pd

## goal here is process and clean the raw data from FastF1

# 1.) convert lap times to seconds
# 2.) keep only the valid times
# 3.) remove non-racing laps / obvious outliers
# 4.) booleans for pit-in and pit-out flags


def prepare_laps(laps: pd.DataFrame) -> pd.DataFrame:

    df = laps.copy()

    if "LapTime" not in df.columns:
        raise ValueError("Expected column 'LapTime' not found in lap data.")

    df["LapTimeSeconds"] = df["LapTime"].dt.total_seconds()

    df = df[df["LapTimeSeconds"].notna()].copy()

    if "PitInTime" in df.columns:
        df["IsPitInLap"] = df["PitInTime"].notna()
    else:
        df["IsPitInLap"] = False

    if "PitOutTime" in df.columns:
        df["IsPitOutLap"] = df["PitOutTime"].notna()
    else:
        df["IsPitOutLap"] = False

    df["IsPitLap"] = df["IsPitInLap"] | df["IsPitOutLap"]

    # These could be safety car laps, traffic, incidents, cooldown laps, etc.
    median_lap = df["LapTimeSeconds"].median()
    df["IsExtremeSlowLap"] = df["LapTimeSeconds"] > median_lap * 1.2

    return df

# for filtering the now-clean data per driver
def get_driver_laps(
    clean_laps: pd.DataFrame,
    driver: str,
    remove_pit_laps: bool = True,
    remove_extreme_slow_laps: bool = True,
) -> pd.DataFrame:

    df = clean_laps[clean_laps["Driver"] == driver].copy()

    if remove_pit_laps:
        df = df[~df["IsPitLap"]].copy()

    if remove_extreme_slow_laps:
        df = df[~df["IsExtremeSlowLap"]].copy()

    return df