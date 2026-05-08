
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

from analysis import (
    get_tyre_degradation,
    get_lap_comparison,
    get_speed_telemetry,
    get_pit_strategy,
    get_theoretical_fastest_lap,
    get_driver_improvements,
    get_sector_analysis,
    get_gear_map,
    get_race_pace_evolution,
)

from utils import TRACK_LIST, DRIVER_CODES, load_session_cached

st.set_page_config(page_title="F1 Telemetry Analyzer", page_icon="🏎️", layout="wide")

st.title("🏎️ F1 Telemetry Analyzer")

with st.sidebar:
    st.header("Session Config")
    year = st.selectbox("Season", [2024, 2023, 2022])
    track = st.selectbox("Track", TRACK_LIST)
    session_type = st.selectbox("Session", ["R", "Q", "FP1"])
    driver1 = st.selectbox("Primary Driver", DRIVER_CODES)
    driver2 = st.selectbox("Compare Driver", DRIVER_CODES)

    if st.button("Load Session"):
        session, drivers = load_session_cached(year, track, session_type)
        st.session_state["session"] = session
        st.success("Session Loaded")

if "session" not in st.session_state:
    st.info("Load a session from the sidebar.")
    st.stop()

session = st.session_state["session"]

tabs = st.tabs([
    "Overview",
    "Lap Times",
    "Tyre Deg",
    "Telemetry",
    "Pit Strategy",
    "AI Coach"
])

with tabs[0]:
    st.subheader("Session Overview")
    laps = session.laps
    fastest = laps.pick_fastest()
    st.metric("Fastest Driver", fastest["Driver"])
    st.metric("Fastest Lap", str(fastest["LapTime"]))

with tabs[1]:
    result = get_lap_comparison(session, driver1, driver2)
    st.plotly_chart(result["fig_line"], use_container_width=True)
    st.plotly_chart(result["fig_delta"], use_container_width=True)

with tabs[2]:
    result = get_tyre_degradation(session, driver1)
    st.plotly_chart(result["fig_deg"], use_container_width=True)
    st.plotly_chart(result["fig_stints"], use_container_width=True)

with tabs[3]:
    result = get_speed_telemetry(session, driver1, driver2, 1)
    st.plotly_chart(result["fig_speed"], use_container_width=True)
    st.plotly_chart(result["fig_throttle"], use_container_width=True)
    st.plotly_chart(result["fig_brake"], use_container_width=True)

with tabs[4]:
    result = get_pit_strategy(session)
    st.plotly_chart(result["fig_strategy"], use_container_width=True)

with tabs[5]:
    if st.button("Generate AI Insights"):
        result = get_driver_improvements(session, driver1)
        tf = get_theoretical_fastest_lap(session)

        st.metric("Theoretical Fastest", tf["theoretical_time"])

        for insight in result["insights"]:
            st.info(f"{insight['corner']} → {insight['text']}")
