
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

def get_lap_comparison(session, driver1, driver2=None, compare_mode="Single Driver"):
    laps = session.laps

    drv1 = laps.pick_drivers(driver1)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=drv1['LapNumber'],
        y=drv1['LapTime'].dt.total_seconds(),
        name=driver1
    ))

    fig_delta = go.Figure()

    if driver2:
        drv2 = laps.pick_drivers(driver2)

        fig_line.add_trace(go.Scatter(
            x=drv2['LapNumber'],
            y=drv2['LapTime'].dt.total_seconds(),
            name=driver2
        ))

    return {
        "fig_line": fig_line,
        "fig_delta": fig_delta
    }

def get_tyre_degradation(session, driver):
    laps = session.laps.pick_drivers(driver)

    fig_deg = px.scatter(
        laps,
        x='TyreLife',
        y=laps['LapTime'].dt.total_seconds(),
        color='Compound'
    )

    fig_stints = px.histogram(laps, x="Compound")

    return {
        "fig_deg": fig_deg,
        "fig_stints": fig_stints
    }

def get_speed_telemetry(session, driver1, driver2=None, lap_num=1):
    lap = session.laps.pick_drivers(driver1).pick_laps(lap_num).iloc[0]
    tel = lap.get_car_data().add_distance()

    fig_speed = go.Figure()
    fig_speed.add_trace(go.Scatter(x=tel['Distance'], y=tel['Speed']))

    fig_throttle = go.Figure()
    fig_throttle.add_trace(go.Scatter(x=tel['Distance'], y=tel['Throttle']))

    fig_brake = go.Figure()
    fig_brake.add_trace(go.Scatter(x=tel['Distance'], y=tel['Brake']))

    return {
        "fig_speed": fig_speed,
        "fig_throttle": fig_throttle,
        "fig_brake": fig_brake
    }

def get_pit_strategy(session):
    laps = session.laps
    pit_table = laps.groupby('Driver')['Stint'].max().reset_index()

    fig = px.bar(pit_table, x='Driver', y='Stint')

    return {
        "fig_strategy": fig
    }

def get_theoretical_fastest_lap(session):
    fastest = session.laps.pick_fastest()

    return {
        "theoretical_time": str(fastest['LapTime'])
    }

def get_driver_improvements(session, driver):
    return {
        "insights": [
            {
                "corner": "Turn 1",
                "text": "Brake slightly later for improved entry speed."
            },
            {
                "corner": "Turn 7",
                "text": "Apply throttle progressively on exit."
            }
        ]
    }

def get_sector_analysis(session, driver1, driver2=None):
    return {}

def get_gear_map(session, driver):
    fig, ax = plt.subplots()
    ax.plot([1,2,3], [3,4,5])
    return fig

def get_race_pace_evolution(session, driver1, driver2=None, compare_mode="Single Driver"):
    return {}
