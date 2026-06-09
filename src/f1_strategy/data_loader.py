# v1 dataloader
from pathlib import Path

import fastf1
import pandas as pd

CACHE_DIR = Path("data") / "fastf1_cache"

# dont want to keep reloading same data
def setup_fastf1_cache() -> None: 
    
    CACHE_DIR.mkdir(parents=True, exist_ok = True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))

# loads lap data given year, race, and session type
def load_race_laps(year:int, race:str, session_type:str = "R") -> pd.DataFrame:

    setup_fastf1_cache()

    session = fastf1.get_session(year, race, session_type)
    session.load(laps=True, telemetry=False, weather=True, messages=True)

    laps = session.laps.copy()

    return pd.DataFrame(laps)

