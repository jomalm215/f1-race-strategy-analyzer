# F1 Race Strategy Analyzer

This is technically my first formally-documented solo Python project!

Goal here is to analyze Formula 1 race laps and give basic race strategy insights.

## Current Features (v1.1) 

- Load F1 race data from FastF1
- Clean lap timing data
- Removes pit laps and very slow laps
- Plot lap times for selected drivers
- Tire stint summary (or as I learned the hard way "tyre")
- Raw pace estimate given tire life
- Driver H2H comparison
- Driver ranking by median laps of race pace
- All tables exported as .csv files (not in terminal!)
- Generate a "markdown report"

## Example Analysis

Current example: 

- Year: 2024
- Race: Monza
- Session Type: Race
- Drivers: VER, NOR, PIA, LEC, SAI

Outputs are saved to:

plots/
strategy_reports/

Example generated outputs:

strategy_reports/
├── 2024_monza/
│   ├── degradation.csv
│   ├── driver_comparison.csv
│   ├── driver_ranking.csv
│   ├── stint_summary.csv
│   └── strategy_report.md

Project Structure

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
│       ├── plots.py
│       └── report.py
├── strategy_reports/
├── tests/
├── requirements.txt
└── README.md

Setup

Create and activate a virtual environment:

python -m venv .venv
.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install --upgrade pip
pip install -r requirements.txt

Run the example analysis:

python .\notebooks\01_first_lap_plot.py

How the Analysis Works

The project follows a simple analysis pipeline:

Load race data
- Clean lap data
- Analyze stints and pace
- Plot lap times
- Export CSV tables
- Generate Markdown report

The current version focuses on clean race-pace analysis. 

Pit laps and extreme slow laps are removed from the main pace calculations so that the results are not dominated by obvious non-representative laps.

Output Files

The script generates:

stint_summary.csv
Summary of each driver's tyre stints, compounds, lap ranges, and median lap times.

degradation.csv
A simple raw pace-slope estimate based on lap time versus tyre life.

driver_comparison.csv
Head-to-head comparison between two selected drivers.

driver_ranking.csv
Ranking of drivers by clean median race pace.

strategy_report.md
A readable Markdown summary of the analysis.

.png lap-time plot
A visual comparison of selected drivers' lap times.

Important Limitations

The current degradation model is a simple linear fit of lap time versus tyre life. It should be interpreted as a raw pace slope, not pure tyre degradation.

Lap time is affected by many factors, including:

Fuel burn
Traffic
Safety car or virtual safety car periods
Track evolution
Tyre warmup
Driver management
Car damage
Pit stop timing

Because of this, the current outputs should be treated as strategy indicators rather than final proof.

Next Features

Planned improvements:

Compound-colored stint plots
Pit stop loss estimate
Undercut and overcut analysis
Safety car and virtual safety car filtering
Fuel-adjusted pace model
Streamlit dashboard
Command-line arguments for year, race, session, and drivers

Why I Built This

I built this project because I love Formula 1! I want to combine my interests in motorsport, data analysis, and engineering. 

The project helped me practice Python project structure, data cleaning, visualization, statistical thinking, and technical communication using real Formula 1 race data.