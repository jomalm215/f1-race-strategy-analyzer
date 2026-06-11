# F1 Race Strategy Analyzer

This is my first formally documented solo Python project.

The goal is to analyze Formula 1 race lap data and generate basic race strategy insights using Python, FastF1, pandas, NumPy, matplotlib, and Streamlit.

## Current Features

* Load Formula 1 race data using FastF1
* Cache FastF1 data locally to avoid repeated downloads
* Clean raw lap timing data
* Convert lap times into seconds for analysis
* Identify pit-in, pit-out, and pit-affected laps
* Remove pit laps and extreme slow laps from clean race-pace calculations
* Plot lap times for selected drivers
* Generate compound-colored stint lap-time plots
* Summarize tyre stints by driver, compound, lap range, tyre life, and pace
* Estimate raw pace slope versus tyre life
* Compare two selected drivers head-to-head
* Rank selected drivers by clean median race pace
* Summarize pit stops by driver, pit lap, stint change, and compound change
* Estimate rough pit loss using pit lap time versus nearby clean pace
* Generate automatic strategy observations
* Export analysis tables as CSV files instead of relying on terminal output
* Generate a Markdown race strategy report
* Accept command-line inputs for year, race, session, and selected drivers
* Run analysis through a basic Streamlit dashboard

## Example Analysis

Current example:

* Year: 2024
* Race: Monza
* Session Type: Race
* Drivers: VER, NOR, PIA, LEC, SAI

Run the default analysis:

```powershell
python .\notebooks\01_first_lap_plot.py
```

Run a custom command-line analysis:

```powershell
python .\notebooks\01_first_lap_plot.py --year 2024 --race Monza --session R --drivers LEC SAI NOR PIA
```

Run the Streamlit dashboard:

```powershell
streamlit run .\streamlit_app\app.py
```

## Project Structure

```text
f1-strat-analysis/
├── data/
│   └── fastf1_cache/
├── notebooks/
│   └── 01_first_lap_plot.py
├── plots/
├── src/
│   └── f1_strategy/
│       ├── analysis.py
│       ├── cleaning.py
│       ├── data_loader.py
│       ├── pipeline.py
│       ├── plots.py
│       └── report.py
├── strategy_reports/
├── streamlit_app/
│   └── app.py
├── tests/
├── requirements.txt
└── README.md
```

## Outputs

Running the analysis script generates race-specific outputs.

```text
strategy_reports/
└── 2024_monza/
    ├── degradation.csv
    ├── driver_comparison.csv
    ├── driver_ranking.csv
    ├── pit_loss_summary.csv
    ├── pit_stop_summary.csv
    ├── stint_summary.csv
    ├── strategy_observations.txt
    └── strategy_report.md
```

Plots are saved separately:

```text
plots/
├── 2024_monza_race_lap_times.png
└── 2024_monza_compound_stint_lap_times.png
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the example analysis:

```powershell
python .\notebooks\01_first_lap_plot.py
```

Run the dashboard:

```powershell
streamlit run .\streamlit_app\app.py
```

## How the Analysis Works

The project follows this pipeline:

```text
Load race data
→ Clean lap data
→ Analyze stints, pace, pit stops, and pit loss
→ Generate lap-time plots
→ Export CSV tables
→ Generate automatic strategy observations
→ Generate Markdown report
→ Display results in Streamlit dashboard
```

The current version focuses on clean race-pace and basic strategy analysis. Pit laps and extreme slow laps are removed from main pace calculations so that results are not dominated by obvious non-representative laps.

## Output Files

### `stint_summary.csv`

Summarizes each selected driver's tyre stints, compounds, lap ranges, tyre-life range, stint length, and lap-time statistics.

### `degradation.csv`

Estimates a raw pace slope based on lap time versus tyre life.

This should be interpreted as a raw pace trend, not pure tyre degradation.

### `driver_comparison.csv`

Compares two selected drivers head-to-head using clean race laps.

### `driver_ranking.csv`

Ranks selected drivers by clean median race pace.

### `pit_stop_summary.csv`

Summarizes detected pit stops, including pit lap, stint change, and compound change.

### `pit_loss_summary.csv`

Estimates rough pit loss by comparing pit lap time against nearby clean racing pace.

### `strategy_observations.txt`

Stores automatic plain-English observations from the analysis, such as fastest selected-driver clean pace, longest stint, pit stop counts, and most stable raw pace slope.

### `strategy_report.md`

Generates a readable Markdown race strategy report with plots, tables, observations, and limitations.

### `.png` lap-time plots

Visualizes selected drivers' lap-time traces and compound-colored stint behavior.

## Streamlit Dashboard

The project includes a basic Streamlit dashboard for interactive race analysis.

Current dashboard features:

* Year input
* Race input
* Session selection
* Driver selection
* Run analysis button
* Strategy observations section
* Lap-time plot display
* Compound stint plot display
* Driver ranking table
* Stint summary table
* Pit stop summary table
* Pit loss summary table
* Raw pace slope/degradation proxy table
* Head-to-head driver comparison table

Run the dashboard with:

```powershell
streamlit run .\streamlit_app\app.py
```

## Important Limitations

The current degradation model is a simple linear fit of lap time versus tyre life. It should be interpreted as a raw pace slope, not pure tyre degradation.

The pit loss estimate is approximate. It compares a pit lap to nearby clean laps, but it does not yet fully account for out-lap behavior, in-lap behavior, traffic, safety car periods, tyre warmup, or exact pit-lane delta.

Lap time is affected by many factors, including:

* Fuel burn
* Traffic
* Safety car or virtual safety car periods
* Track evolution
* Tyre warmup
* Driver management
* Car damage
* Pit stop timing

Because of this, the current outputs should be treated as strategy indicators rather than final proof.

## Next Features

Planned improvements:

* Improve dashboard layout and visual polish
* Add dashboard metric cards
* Add downloadable CSV and report buttons
* Improve compound-colored stint plots
* Add lap classification
* Add safety car and virtual safety car filtering
* Rename raw degradation output to raw pace slope for clarity
* Add fuel-adjusted pace modeling
* Add tyre cliff detection
* Add pit window detection
* Add undercut and overcut analysis
* Add one-stop versus two-stop strategy comparison
* Add what-if pit strategy simulator

## Why I Built This

I built this project because I love Formula 1 and want to combine my interests in motorsport, data analysis, and engineering.