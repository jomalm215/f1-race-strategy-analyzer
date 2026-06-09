# note that this notebook retains the original structure, but undergoes edits and suggestions from Copilot and GPT 5.5
# new export structure v1.1

import sys
from pathlib import Path

# Allows notebook/script to import from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from f1_strategy.analysis import (
    compare_drivers,
    estimate_stint_degradation,
    rank_drivers_by_clean_pace,
    summarize_stints,
)
from f1_strategy.cleaning import prepare_laps
from f1_strategy.data_loader import load_race_laps
from f1_strategy.plots import plot_driver_lap_times
from f1_strategy.report import generate_markdown_report, save_strategy_tables


def main() -> None:
    year = 2026
    race = "Monaco"
    session_type = "R"
    drivers = ["VER", "NOR", "PIA", "LEC", "SAI"]

    print(f"Loading {year} {race} {session_type} data...")
    raw_laps = load_race_laps(year, race, session_type)

    print("Cleaning lap data...")
    clean_laps = prepare_laps(raw_laps)

    print("Running strategy analysis...")
    stint_summary = summarize_stints(clean_laps)
    degradation = estimate_stint_degradation(clean_laps)
    comparison = compare_drivers(clean_laps, drivers[0], drivers[1])
    driver_ranking = rank_drivers_by_clean_pace(clean_laps)

    print("Plotting lap times...")
    plot_path = plot_driver_lap_times(
        clean_laps=clean_laps,
        drivers=drivers,
        title=f"{year} {race} Race Lap Times",
    )

    print("Saving strategy tables...")
    table_paths = save_strategy_tables(
        year=year,
        race=race,
        stint_summary=stint_summary[stint_summary["Driver"].isin(drivers)],
        degradation=degradation[degradation["Driver"].isin(drivers)],
        comparison=comparison,
    )

    ranking_path = Path("strategy_reports") / f"{year}_{race.lower()}_driver_ranking.csv"
    driver_ranking.to_csv(ranking_path, index=False)

    print("Generating Markdown report...")
    report_path = generate_markdown_report(
        year=year,
        race=race,
        session_type=session_type,
        drivers=drivers,
        plot_path=plot_path,
        stint_summary=stint_summary,
        degradation=degradation,
        comparison=comparison,
        driver_ranking=driver_ranking,
    )

    print("\nAnalysis complete.")
    print(f"Plot saved to: {plot_path}")
    print(f"Stint summary saved to: {table_paths['stint_summary']}")
    print(f"Degradation table saved to: {table_paths['degradation']}")
    print(f"Driver comparison saved to: {table_paths['driver_comparison']}")
    print(f"Driver ranking saved to: {ranking_path}")
    print(f"Markdown report saved to: {report_path}")


if __name__ == "__main__":
    main()