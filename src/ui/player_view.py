import streamlit as st
import requests  # type: ignore
import pandas as pd


def player_view(api_url: str) -> None:
    """Render the Player UI: workload input, cycle tracking and dashboard."""
    tab = st.sidebar.radio(
        "Player Menu", ["Workload Tracking", "Cycle Tracking", "Dashboard"]
    )

    if tab == "Workload Tracking":
        st.header("Training Sessions")
        with st.form("workload_form"):
            date = st.date_input("Date")
            session_type = st.selectbox(
                "Session Type", ["Training", "Match", "Other sport"]
            )
            duration = st.slider(
                "Duration (minutes)", min_value=0, max_value=480, value=60, step=30
            )
            rpe = st.slider(
                "RPE (Rate of Perceived Exertion)", min_value=1, max_value=10, value=5
            )
            batting_minutes = st.number_input(
                "Batting Minutes", min_value=0, max_value=240, value=0, step=15
            )
            bowling_overs = st.number_input(
                "Bowling Overs", min_value=0, max_value=50, value=0
            )
            fielding_time = st.number_input(
                "Fielding Time (minutes)", min_value=0, max_value=240, value=0, step=15
            )
            comment = st.text_area("Comment")
            submitted = st.form_submit_button("Add Session")
            if submitted:
                payload = {
                    "player_id": st.user.name,
                    "date": str(date),
                    "session_type": session_type,
                    "duration": duration,
                    "rpe": rpe,
                    "batting_minutes": batting_minutes,
                    "bowling_overs": bowling_overs,
                    "fielding_time": fielding_time,
                    "comment": comment,
                }
                resp = requests.post(f"{api_url}/sessions", json=payload)
                st.success(f"Session added: {resp.json()}")
        st.header("Previous sessions")
        sessions = requests.get(f"{api_url}/sessions").json()
        # Convert to DataFrame, drop player_id column, and show
        if sessions:
            df = pd.DataFrame(sessions)
            df = CleanupPlayerData(df)
            st.table(df)
        else:
            st.info("No sessions available.")

    elif tab == "Cycle Tracking":
        st.header("Cycle tracking")
        with st.form("cyclelog_form"):
            period_start = st.date_input("Period Start")
            symptoms = st.text_input("Symptoms (comma separated)")
            wellness = st.slider(
                "Overall Perceived Wellness", min_value=1, max_value=10, value=5
            )
            sleep = st.slider(
                "Overall Perceived Sleep Quality", min_value=1, max_value=10, value=5
            )
            soreness = st.slider(
                "Overall Perceived soreness", min_value=1, max_value=10, value=5
            )
            mood = st.slider(
                "Overall Perceived Mood", min_value=1, max_value=10, value=5
            )
            comment = st.text_area("Comment")
            submitted = st.form_submit_button("Add Cycle")
            if submitted:
                payload = {
                    "player_id": st.user.name,
                    "period_start": str(period_start),
                    "symptoms": [s.strip() for s in symptoms.split(",") if s.strip()],
                    "wellness": wellness,
                    "sleep": sleep,
                    "mood": mood,
                    "soreness": soreness,
                    "comment": comment,
                }
                resp = requests.post(f"{api_url}/cyclelogs", json=payload)
                st.success(f"CycleLog added: {resp.json()}")
        st.header("Previous cycle logs")

        cyclelogs = requests.get(f"{api_url}/cyclelogs").json()
        if cyclelogs:
            df = pd.DataFrame(cyclelogs)
            df = CleanupPlayerData(df)
            st.table(df)
        else:
            st.info("No cycle logs available.")

    elif tab == "Dashboard":
        st.header("Player Dashboard")
        sessions = requests.get(f"{api_url}/sessions").json()
        metrics = requests.get(f"{api_url}/metrics").json()
        injuries = requests.get(f"{api_url}/injuries").json()
        cyclelogs = requests.get(f"{api_url}/cyclelogs").json()
        st.subheader("Sessions")
        if sessions:
            df = pd.DataFrame(sessions)
            df = CleanupPlayerData(df)
            st.table(df)
        else:
            st.info("No sessions available.")
        st.subheader("Metrics")
        if metrics:
            df = pd.DataFrame(metrics)
            df = CleanupPlayerData(df)
            st.table(df)
        else:
            st.info("No metrics available.")
        st.subheader("Injuries")
        if injuries:
            df = pd.DataFrame(injuries)
            df = CleanupPlayerData(df)
            st.table(df)
        else:
            st.info("No injuries available.")
        st.subheader("Cycle Logs")
        if cyclelogs:
            df = pd.DataFrame(cyclelogs)
            df = CleanupPlayerData(df)
            st.table(df)
        else:
            st.info("No cycle logs available.")


def CleanupPlayerData(df: pd.DataFrame) -> pd.DataFrame:
    if "id" in df.columns:
        df = df.drop(columns=["id"])
    if "player_id" in df.columns:
        df = df.drop(columns=["player_id"])
    return df
