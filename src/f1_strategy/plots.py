from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PLOTS_DIR = Path("plots")

# plotting lapt imes for selected drivers
# parameters: clean_laps, drivers, title

def plot_driver_lap_times(clean_laps : pd.DataFrame, drivers : list[str], title : str) -> Path:

    PLOTS_DIR.mkdir(parents = True, exist_ok = True)

    fig, ax = plt.subplots(figsize = (12,6))

    for driver in drivers : 
        driver_laps = clean_laps[(clean_laps["Driver"] == driver)
                                 & (~clean_laps["IsPitLap"])
                                 & (~clean_laps["IsExtremeSlowLap"])
        ].copy()
        
        ax.plot(
            
            driver_laps["LapNumber"],
            driver_laps["LapTimeSeconds"],
            marker = "o",
            linewidth = 1.25,
            label = driver,
        )   

    ax.set_title(title)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (seconds)")
    ax.legend()
    ax.grid(True, alpha = 0.3)

    safe_title = "_".join(title.lower().replace("/", "_").split())
    output_path = PLOTS_DIR / f"{safe_title}.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi = 150)
    plt.close(fig)

    return output_path

# plotting lap times but by TIRE COMPOUND

def plot_compound_stint_lap_times(
        clean_laps: pd.DataFrame,
        drivers: list[str],
        title: str,
    ) -> Path:

    PLOTS_DIR.mkdir(parents = True, exist_ok = True)

    required_columns = [
        "Driver",
        "LapNumber",
        "LapTimeSeconds",
        "Compound",
        "IsPitLap",
        "IsExtremeSlowLap",
    ]

    missing_columns = [col for col in required_columns if col not in clean_laps.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    compound_colors = {
        "SOFT": "red",
        "MEDIUM": "gold",
        "HARD": "gray",
        "INTERMEDIATE": "green",
        "WET": "blue",
        "UNKNOWN": "black",
    }

    fig, ax = plt.subplots(figsize=(13, 7))

    selected_laps = clean_laps[

        (clean_laps["Driver"].isin(drivers))
        & (~clean_laps["IsPitLap"])
        & (~clean_laps["IsExtremeSlowLap"])
        & (clean_laps["LapTimeSeconds"].notna())
    ].copy()

    for driver in drivers:
        driver_laps = selected_laps[selected_laps["Driver"] == driver].copy()

        if driver_laps.empty:
            continue

        # Thin line for driver trend
        ax.plot(
            driver_laps["LapNumber"],
            driver_laps["LapTimeSeconds"],
            linewidth=1,
            alpha=0.45,
            label=f"{driver} trend",
        )

        # Compound-colored points
        for compound, compound_laps in driver_laps.groupby("Compound"):
            color = compound_colors.get(str(compound), compound_colors["UNKNOWN"])

            ax.scatter(
                compound_laps["LapNumber"],
                compound_laps["LapTimeSeconds"],
                s=28,
                color=color,
                edgecolors="black",
                linewidths=1.25,
                label=f"{driver} {compound}",
            )

    ax.set_title(title)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time, seconds")
    ax.grid(True, alpha=0.3)

    # Remove duplicate legend entries.
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(
        unique.values(),
        unique.keys(),
        fontsize=8,
        loc="best",
        ncols=2,
    )

    safe_title = "_".join(title.lower().replace("/", "_").split())
    output_path = PLOTS_DIR / f"{safe_title}.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path                            