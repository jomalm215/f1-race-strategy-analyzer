# note that this notebook retains the original structure, but undergoes edits and suggestions from Copilot and GPT 5.5
## new export structure v1.0
## adding terminal command line inputs, instead of hardcoding test case v1.1

import argparse
import sys
from pathlib import Path

# Allows notebook/script to import from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from f1_strategy.analysis import (
    compare_drivers,
    estimate_pit_loss,
    estimate_stint_degradation,
    rank_drivers_by_clean_pace,
    summarize_pit_stops,
    summarize_stints,
)
from f1_strategy.cleaning import prepare_laps
from f1_strategy.data_loader import load_race_laps
from f1_strategy.plots import plot_driver_lap_times, plot_compound_stint_lap_times
from f1_strategy.report import (
    generate_markdown_report,
    make_safe_filename,
    save_strategy_tables,
)


# handles parsing of cmd line inputs
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze F1 race strategy using FastF1 data."
    )

## worth noting an error i made, initially wanted "Year:", "Race:", that format
## the capital letters and colons will cause trouble

### keep default race as 2024 Monza GP
### python .\notebooks\01_first_lap_plot.py --year 2024 --race Monza --session R --drivers LEC SAI

    parser.add_argument(
        "--year",
        type=int,
        default=2024,
        help="F1 season year, ex: 2024.",
    )

    parser.add_argument(
        "--race",
        type=str,
        default="Monza",
        help='Race name/location, ex: "Monza" or "Italian Grand Prix".',
    )

    parser.add_argument(
        "--session",
        type=str,
        default="R",
        help='Session type, ex: "R", "Q", "FP1", "FP2", "FP3", or "S".',
    )

    parser.add_argument(
        "--drivers",
        nargs="+",
        default=["LEC", "SAI"],
        help="Driver abbreviations, ex: VER NOR PIA LEC SAI.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    year = args.year
    race = args.race
    session_type = args.session
    drivers = args.drivers

    if len(drivers) < 2:
        raise ValueError("Please provide at least two drivers for comparison.")

    print(f"Loading {year} {race} {session_type} data...")
    raw_laps = load_race_laps(year, race, session_type)

    print("Cleaning lap data...")
    clean_laps = prepare_laps(raw_laps)

    available_drivers = sorted(clean_laps["Driver"].dropna().unique())
    missing_drivers = [driver for driver in drivers if driver not in available_drivers]

    if missing_drivers:
        raise ValueError(
            f"These drivers were not found in the session data: {missing_drivers}. "
            f"Available drivers are: {available_drivers}"
        )

    print("Running strategy analysis...")
    stint_summary = summarize_stints(clean_laps)
    degradation = estimate_stint_degradation(clean_laps)
    comparison = compare_drivers(clean_laps, drivers[0], drivers[1])
    driver_ranking = rank_drivers_by_clean_pace(clean_laps)
    pit_stop_summary = summarize_pit_stops(clean_laps)
    pit_loss_summary = estimate_pit_loss(clean_laps)

    print("Plotting lap times...")
    plot_path = plot_driver_lap_times(
        clean_laps=clean_laps,
        drivers=drivers,
        title=f"{year} {race} Race Lap Times",
    )

    compound_plot_path = plot_compound_stint_lap_times(
        clean_laps=clean_laps,
        drivers=drivers,
        title=f"{year} {race} Compound Stint Lap Times",
    )

    print(f"DEBUG compound_plot_path: {compound_plot_path}")

    print("Saving strategy tables...")
    table_paths = save_strategy_tables(
        year=year,
        race=race,
        stint_summary=stint_summary[stint_summary["Driver"].isin(drivers)],
        degradation=degradation[degradation["Driver"].isin(drivers)],
        comparison=comparison,
    )

    report_folder = Path("strategy_reports") / make_safe_filename(f"{year}_{race}")
    report_folder.mkdir(parents=True, exist_ok=True)

    ranking_path = report_folder / "driver_ranking.csv"
    driver_ranking[driver_ranking["Driver"].isin(drivers)].to_csv(
        ranking_path,
        index=False,
    )

    pit_stop_path = report_folder / "pit_stop_summary.csv"
    pit_stop_summary[pit_stop_summary["Driver"].isin(drivers)].to_csv(
        pit_stop_path,
        index = False

    )

    pit_loss_path = report_folder / "pit_loss_summary.csv"
    pit_loss_summary[pit_loss_summary["Driver"].isin(drivers)].to_csv(
        pit_loss_path,
        index=False,
    )

    print("Generating Markdown report...")
    report_path = generate_markdown_report(
        year=year,
        race=race,
        session_type=session_type,
        drivers=drivers,
        plot_path=plot_path,
        compound_plot_path=compound_plot_path,
        stint_summary=stint_summary,
        degradation=degradation,
        comparison=comparison,
        driver_ranking=driver_ranking,
        pit_stop_summary=pit_stop_summary,
        pit_loss_summary=pit_loss_summary,
    )

    print("\nAnalysis complete.")
    print(f"Race/session: {year} {race} {session_type}")
    print(f"Drivers: {', '.join(drivers)}")
    print(f"Plot saved to: {plot_path}")
    print(f"Compound stint plot saved to: {compound_plot_path}")
    print(f"Stint summary saved to: {table_paths['stint_summary']}")
    print(f"Degradation table saved to: {table_paths['degradation']}")
    print(f"Driver comparison saved to: {table_paths['driver_comparison']}")
    print(f"Driver ranking saved to: {ranking_path}")
    print(f"Pit Stop summary saved to: {pit_stop_path}")
    print(f"Pit loss summary saved to: {pit_loss_path}")
    print(f"Markdown report saved to: {report_path}")


if __name__ == "__main__":
    main()