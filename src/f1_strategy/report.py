# mostly GPT 5.5-gen, b/c who wants all this info in the terminal
## also this is report work...

from pathlib import Path

import pandas as pd


REPORTS_DIR = Path("strategy_reports")


def make_safe_filename(text: str) -> str:
    """
    Convert text into a safe lowercase filename.
    """
    return (
        text.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def save_strategy_tables(
    year: int,
    race: str,
    stint_summary: pd.DataFrame,
    degradation: pd.DataFrame,
    comparison: pd.DataFrame,
) -> dict[str, Path]:
    """
    Save strategy analysis tables as CSV files.

    Returns a dictionary containing the saved file paths.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    prefix = make_safe_filename(f"{year}_{race}")

    paths = {
        "stint_summary": REPORTS_DIR / f"{prefix}_stint_summary.csv",
        "degradation": REPORTS_DIR / f"{prefix}_degradation.csv",
        "driver_comparison": REPORTS_DIR / f"{prefix}_driver_comparison.csv",
    }

    stint_summary.to_csv(paths["stint_summary"], index=False)
    degradation.to_csv(paths["degradation"], index=False)
    comparison.to_csv(paths["driver_comparison"], index=False)

    return paths


def generate_markdown_report(
    year: int,
    race: str,
    session_type: str,
    drivers: list[str],
    plot_path: Path,
    compound_plot_path: Path,
    stint_summary: pd.DataFrame,
    degradation: pd.DataFrame,
    comparison: pd.DataFrame,
    driver_ranking: pd.DataFrame,
    pit_stop_summary: pd.DataFrame,
    pit_loss_summary: pd.DataFrame,
) -> Path:
    """
    Generate a clean Markdown strategy report.

    This is easier to read than the terminal and works well for GitHub.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    prefix = make_safe_filename(f"{year}_{race}")
    report_path = REPORTS_DIR / f"{prefix}_strategy_report.md"

    lap_plot_relative_path = Path("../../") / plot_path
    compound_plot_relative_path = Path("../../") / compound_plot_path

    lap_plot_markdown_path = lap_plot_relative_path.as_posix()
    compound_plot_markdown_path = compound_plot_relative_path.as_posix()

    selected_stints = stint_summary[stint_summary["Driver"].isin(drivers)].copy()
    selected_degradation = degradation[degradation["Driver"].isin(drivers)].copy()
    selected_ranking = driver_ranking[driver_ranking["Driver"].isin(drivers)].copy()
    selected_pit_stops = pit_stop_summary[pit_stop_summary["Driver"].isin(drivers)].copy()
    selected_pit_loss = pit_loss_summary[pit_loss_summary["Driver"].isin(drivers)].copy()
    
    with report_path.open("w", encoding="utf-8") as file:
        file.write(f"# {year} {race} Strategy Analysis\n\n")

        file.write("## Session\n\n")
        file.write(f"- Year: {year}\n")
        file.write(f"- Race: {race}\n")
        file.write(f"- Session: {session_type}\n")
        file.write(f"- Drivers analyzed: {', '.join(drivers)}\n\n")

        file.write("## Lap Time Plot\n\n")
        file.write(f"![Lap time plot](../../{plot_path.as_posix()})\n\n")

        file.write("## Compound Stint Plot\n\n")
        file.write(
            "This plot shows selected drivers' clean lap times with points colored by tyre compound. "
            "It helps connect lap-time trends to stint strategy.\n\n"
        )
        file.write(f"![Compound stint plot](../../{compound_plot_path.as_posix()})\n\n")
       
        file.write("## Clean Pace Ranking\n\n")
        file.write(
            "This ranks drivers by median clean lap time after removing pit laps "
            "and extreme slow laps. It is useful for a quick race-pace comparison, "
            "but it does not fully normalize for compound, fuel, traffic, or strategy.\n\n"
        )

        selected_ranking = driver_ranking[driver_ranking["Driver"].isin(drivers)].copy()

        if selected_ranking.empty:
            file.write("No driver ranking data available.\n\n")
        else:
            file.write(selected_ranking.to_markdown(index=False))
            file.write("\n\n")

        file.write("## Pit Stop Summary\n\n")
        file.write(
            "This table summarizes detected pit stops using pit-in laps. "
            "It shows the lap where each driver pitted and the compound change before and after the stop.\n\n"
        )

        if selected_pit_stops.empty:
            file.write("No pit stop data available for selected drivers.\n\n")
        else:
            file.write(selected_pit_stops.to_markdown(index=False))
            file.write("\n\n")
        
        file.write("## Pit Loss Estimate\n\n")
        file.write(
            "This table estimates rough pit loss by comparing each pit-in lap time "
            "against nearby clean racing laps. It is an approximation and can be affected "
            "by traffic, out-lap behavior, tyre warmup, and race conditions.\n\n"
        )

        if selected_pit_loss.empty:
            file.write("No pit loss data available for selected drivers.\n\n")
        else:
            file.write(selected_pit_loss.to_markdown(index=False))
            file.write("\n\n")

        file.write("## Head-to-Head Driver Comparison\n\n")
        if comparison.empty:
            file.write("No driver comparison data available.\n\n")
        else:
            file.write(comparison.to_markdown(index=False))
            file.write("\n\n")

        file.write("## Stint Summary\n\n")
        if selected_stints.empty:
            file.write("No stint summary data available for selected drivers.\n\n")
        else:
            file.write(selected_stints.to_markdown(index=False))
            file.write("\n\n")

        file.write("## Estimated Pace Slope / Degradation Proxy\n\n")
        file.write(
            "The slope below is a simple linear fit of lap time versus tyre life. "
            "Positive values mean laps got slower as tyre life increased. "
            "Negative values mean laps got faster as the stint progressed, which can happen "
            "because of fuel burn, track evolution, clean air, or race management.\n\n"
        )

        if selected_degradation.empty:
            file.write("No degradation estimates available for selected drivers.\n\n")
        else:
            file.write(selected_degradation.to_markdown(index=False))
            file.write("\n\n")

        file.write("## Notes and Limitations\n\n")
        file.write(
            "This report uses cleaned lap-time data from FastF1. The analysis removes pit laps "
            "and extreme slow laps, but it does not yet fully model fuel burn, traffic, safety car "
            "periods, tyre warmup, driver management, car damage, or exact pit-loss time. "
            "Therefore, the results should be treated as strategy indicators rather than final proof.\n"
        )

    return report_path