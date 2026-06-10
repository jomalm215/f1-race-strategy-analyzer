from pathlib import Path

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
from f1_strategy.plots import plot_compound_stint_lap_times, plot_driver_lap_times
from f1_strategy.report import (
    generate_markdown_report,
    make_safe_filename,
    save_strategy_tables,
)

## goal is to have a Streamlit dashboard, so i want it to call one clean function
## build a pipeline, similar stuff to the 01 notebook

def run_race_analysis(
    year: int,
    race: str,
    session_type: str,
    drivers: list[str],
) -> dict:

    if len(drivers) < 2:
        raise ValueError("Please provide at least two drivers for comparison.")

    raw_laps = load_race_laps(year, race, session_type)
    clean_laps = prepare_laps(raw_laps)

    available_drivers = sorted(clean_laps["Driver"].dropna().unique())
    missing_drivers = [driver for driver in drivers if driver not in available_drivers]

    if missing_drivers:
        raise ValueError(
            f"These drivers were not found in the session data: {missing_drivers}. "
            f"Available drivers are: {available_drivers}"
        )

    stint_summary = summarize_stints(clean_laps)
    degradation = estimate_stint_degradation(clean_laps)
    comparison = compare_drivers(clean_laps, drivers[0], drivers[1])
    driver_ranking = rank_drivers_by_clean_pace(clean_laps)
    pit_stop_summary = summarize_pit_stops(clean_laps)
    pit_loss_summary = estimate_pit_loss(clean_laps)

    selected_stints = stint_summary[stint_summary["Driver"].isin(drivers)]
    selected_degradation = degradation[degradation["Driver"].isin(drivers)]
    selected_ranking = driver_ranking[driver_ranking["Driver"].isin(drivers)]
    selected_pit_stops = pit_stop_summary[pit_stop_summary["Driver"].isin(drivers)]
    selected_pit_loss = pit_loss_summary[pit_loss_summary["Driver"].isin(drivers)]

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

    table_paths = save_strategy_tables(
        year=year,
        race=race,
        stint_summary=selected_stints,
        degradation=selected_degradation,
        comparison=comparison,
    )

    report_folder = Path("strategy_reports") / make_safe_filename(f"{year}_{race}")
    report_folder.mkdir(parents=True, exist_ok=True)

    ranking_path = report_folder / "driver_ranking.csv"
    selected_ranking.to_csv(ranking_path, index=False)

    pit_stop_path = report_folder / "pit_stop_summary.csv"
    selected_pit_stops.to_csv(pit_stop_path, index=False)

    pit_loss_path = report_folder / "pit_loss_summary.csv"
    selected_pit_loss.to_csv(pit_loss_path, index=False)

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

    return {
        "raw_laps": raw_laps,
        "clean_laps": clean_laps,
        "stint_summary": selected_stints,
        "degradation": selected_degradation,
        "comparison": comparison,
        "driver_ranking": selected_ranking,
        "pit_stop_summary": selected_pit_stops,
        "pit_loss_summary": selected_pit_loss,
        "plot_path": plot_path,
        "compound_plot_path": compound_plot_path,
        "table_paths": table_paths,
        "ranking_path": ranking_path,
        "pit_stop_path": pit_stop_path,
        "pit_loss_path": pit_loss_path,
        "report_path": report_path,
    }