import fastf1
import pandas as pd
import streamlit as st
import os

# Create cache folder automatically
os.makedirs("cache", exist_ok=True)

# Enable FastF1 cache
fastf1.Cache.enable_cache("cache")

TRACK_LIST = [
    "Bahrain",
    "Saudi Arabia",
    "Australia",
    "Japan",
    "Miami",
    "Monaco",
    "Silverstone",
    "Monza",
    "Singapore",
    "Abu Dhabi"
]

DRIVER_CODES = [
    "VER", "PER", "HAM", "RUS", "LEC", "SAI",
    "NOR", "PIA", "ALO", "STR", "TSU", "RIC"
]

@st.cache_data
def load_session_cached(year, track, session_type):

    session = fastf1.get_session(year, track, session_type)

    try:
        session.load()

        laps = session.laps

        if laps is None or laps.empty:
            raise Exception("No lap data loaded")

        drivers = laps['Driver'].dropna().unique().tolist()

        return session, drivers

    except Exception as e:
        raise Exception(f"FastF1 failed to load session: {e}")
