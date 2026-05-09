
import fastf1
import pandas as pd
import streamlit as st
import os

os.makedirs("cache", exist_ok=True)

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
    "VER","PER","HAM","RUS","LEC","SAI",
    "NOR","PIA","ALO","STR","TSU","RIC"
]

@st.cache_data
def load_session_cached(year, track, session_type):
    session = fastf1.get_session(year, track, session_type)
    session.load()
    drivers = session.laps['Driver'].unique().tolist()
    return session, drivers
