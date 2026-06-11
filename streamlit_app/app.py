import sys
from pathlib import Path

import streamlit as st

# Allow Streamlit app to import from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from f1_strategy.pipeline import run_race_analysis


st.set_page_config(
    page_title="F1 Race Strategy Analyzer",
    layout="wide",
)

st.title("F1 Race Strategy Analyzer")
st.write(
    "Analyze Formula 1 race lap data using FastF1, then generate strategy tables, plots, and reports."
)

st.sidebar.header("Analysis Inputs")

year = st.sidebar.number_input(
    "Year",
    min_value=2018,
    max_value=2026,
    value=2024,
    step=1,

)

race = st.sidebar.text_input(

    "Race",
    value="Monza",
    help='Examples: "Monza", "Italian Grand Prix", "Monaco", "Silverstone"',
)

session_type = st.sidebar.selectbox(

    "Session",
    options=["R", "Q", "S", "FP1", "FP2", "FP3"],
    index=0,
)

drivers_text = st.sidebar.text_input(
    "Drivers",
    value="LEC SAI NOR PIA",
    help="Use three-letter driver codes separated by spaces.",
)

drivers = [driver.strip().upper() for driver in drivers_text.split() if driver.strip()]

run_button = st.sidebar.button("Run Analysis")

if not run_button:
    st.info("Choose inputs in the sidebar, then click **Run Analysis**.")
    st.stop()

if len(drivers) < 2:
    st.error("Please enter at least two drivers.")
    st.stop()

with st.spinner("Running race analysis... this may take a while the first time FastF1 downloads data."):
    try:
        results = run_race_analysis(
            year=int(year),
            race=race,
            session_type=session_type,
            drivers=drivers,
        )
    except Exception as error:
        st.error("Analysis failed.")
        st.exception(error)
        st.stop()

st.success("Analysis complete.")

st.subheader("Strategy Observations")

for observation in results["strategy_observations"]:
    st.write(f"- {observation}")
    
st.subheader("Run Summary")
st.write(f"**Race/session:** {year} {race} {session_type}")
st.write(f"**Drivers:** {', '.join(drivers)}")
st.write(f"**Markdown report:** `{results['report_path']}`")

st.subheader("Lap Time Plot")
if Path(results["plot_path"]).exists():
    st.image(str(results["plot_path"]))
else:
    st.warning(f"Plot file not found: {results['plot_path']}")

st.subheader("Compound Stint Plot")
if Path(results["compound_plot_path"]).exists():
    st.image(str(results["compound_plot_path"]))
else:
    st.warning(f"Compound plot file not found: {results['compound_plot_path']}")

st.subheader("Driver Ranking")
st.dataframe(results["driver_ranking"], use_container_width=True)

st.subheader("Stint Summary")
st.dataframe(results["stint_summary"], use_container_width=True)

st.subheader("Pit Stop Summary")
st.dataframe(results["pit_stop_summary"], use_container_width=True)

st.subheader("Pit Loss Summary")
st.dataframe(results["pit_loss_summary"], use_container_width=True)

st.subheader("Raw Pace Slope / Degradation Proxy")
st.dataframe(results["degradation"], use_container_width=True)

st.subheader("Head-to-Head Driver Comparison")
st.dataframe(results["comparison"], use_container_width=True)