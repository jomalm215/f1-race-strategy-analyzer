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

    safe_title = title.lower().replace(" ", " _ ").replace("/", "_")
    output_path = PLOTS_DIR / f"{safe_title}.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi = 150)
    plt.close(fig)

    return output_path
                                                 