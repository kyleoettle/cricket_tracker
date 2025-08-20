import streamlit as st
import requests  # type: ignore

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Cricket Tracker", layout="wide")
st.title("Cricket Tracker (API Demo)")

# Role selection (placeholder for Auth0 integration)
role = st.sidebar.selectbox("Select your role", ["Player", "Coach"])

if role == "Player":
    tab = st.sidebar.radio(
        "Player Menu", ["Workload Input", "Cycle Tracking", "Dashboard"]
    )
    if tab == "Workload Input":
        st.header("Workload Input")
        sessions = requests.get(f"{API_URL}/sessions").json()
        st.table(sessions)
        with st.form("workload_form"):
            player_id = st.text_input("Player ID")
            date = st.date_input("Date")
            session_type = st.text_input("Session Type")
            duration = st.number_input("Duration (min)", min_value=0)
            rpe = st.number_input("RPE", min_value=0)
            batting_minutes = st.number_input("Batting Minutes", min_value=0)
            bowling_overs = st.number_input("Bowling Overs", min_value=0)
            fielding_time = st.number_input("Fielding Time", min_value=0)
            comment = st.text_area("Comment")
            submitted = st.form_submit_button("Add Session")
            if submitted:
                payload = {
                    "player_id": player_id,
                    "date": str(date),
                    "session_type": session_type,
                    "duration": duration,
                    "rpe": rpe,
                    "batting_minutes": batting_minutes,
                    "bowling_overs": bowling_overs,
                    "fielding_time": fielding_time,
                    "comment": comment,
                }
                resp = requests.post(f"{API_URL}/sessions", json=payload)
                st.success(f"Session added: {resp.json()}")
    elif tab == "Cycle Tracking":
        st.header("Cycle Logs (API Demo)")
        cyclelogs = requests.get(f"{API_URL}/cyclelogs").json()
        st.table(cyclelogs)
        with st.form("cyclelog_form"):
            player_id = st.text_input("Player ID (CycleLog)")
            period_start = st.date_input("Period Start")
            symptoms = st.text_input("Symptoms (comma separated)")
            wellness = st.number_input("Wellness", min_value=0)
            sleep = st.number_input("Sleep", min_value=0)
            mood = st.number_input("Mood", min_value=0)
            soreness = st.number_input("Soreness", min_value=0)
            comment = st.text_area("Comment (CycleLog)")
            submitted = st.form_submit_button("Add CycleLog")
            if submitted:
                payload = {
                    "player_id": player_id,
                    "period_start": str(period_start),
                    "symptoms": [s.strip() for s in symptoms.split(",") if s.strip()],
                    "wellness": wellness,
                    "sleep": sleep,
                    "mood": mood,
                    "soreness": soreness,
                    "comment": comment,
                }
                resp = requests.post(f"{API_URL}/cyclelogs", json=payload)
                st.success(f"CycleLog added: {resp.json()}")
    elif tab == "Dashboard":
        st.header("Player Dashboard (API Demo)")
        sessions = requests.get(f"{API_URL}/sessions").json()
        metrics = requests.get(f"{API_URL}/metrics").json()
        injuries = requests.get(f"{API_URL}/injuries").json()
        cyclelogs = requests.get(f"{API_URL}/cyclelogs").json()
        st.subheader("Sessions")
        st.table(sessions)
        st.subheader("Metrics")
        st.table(metrics)
        st.subheader("Injuries")
        st.table(injuries)
        st.subheader("Cycle Logs")
        st.table(cyclelogs)

if role == "Coach":
    import pandas as pd
    import numpy as np

    roles = ["Batter", "Bowler", "All-rounder"]
    player_names = [f"Player {i+1}" for i in range(12)]
    player_roles = np.random.choice(roles, size=12)
    last7_load = np.random.randint(80, 300, size=12)
    acwr = np.round(np.random.uniform(0.8, 1.6, size=12), 2)
    risk_status = ["Red" if x > 1.4 else "Yellow" if x > 1.2 else "Green" for x in acwr]
    df = pd.DataFrame(
        {
            "Name": player_names,
            "Role": player_roles,
            "Last 7d Load": last7_load,
            "A:C Ratio": acwr,
            "Risk": risk_status,
        }
    )
    tab = st.sidebar.radio(
        "Coach Menu", ["Team Dashboard", "Player Profile", "Model Retraining"]
    )
    if tab == "Team Dashboard":
        st.header("Team Dashboard")
        st.subheader("Player Table")
        filter_role = st.selectbox("Filter by Role", ["All"] + roles)
        df_filtered = df.copy()
        if filter_role != "All":
            df_filtered = df_filtered[df_filtered["Role"] == filter_role]
        st.dataframe(df_filtered, use_container_width=True)
        st.subheader("Team Summary")
        st.bar_chart(df_filtered.set_index("Name")["Last 7d Load"])
        avg_load = df_filtered["Last 7d Load"].mean()
        red_flags = (df_filtered["Risk"] == "Red").sum()
        yellow_flags = (df_filtered["Risk"] == "Yellow").sum()
        st.metric("Average Load", f"{avg_load:.0f}")
        st.metric("Red Flags", red_flags)
        st.metric("Yellow Flags", yellow_flags)
    elif tab == "Player Profile":
        st.header("Player Profile View")
        # Select player
        selected_player = st.selectbox("Select Player", player_names)
        weeks = pd.date_range(end=pd.Timestamp.today(), periods=8, freq="W-MON")
        # Mock player data
        batting = np.random.randint(20, 120, size=8)
        bowling = np.random.randint(10, 80, size=8)
        overall = batting + bowling + np.random.randint(10, 40, size=8)
        player_rpe = np.random.randint(3, 9, size=8)
        # Mock team data (average)
        team_batting = np.random.randint(30, 100, size=8)
        team_bowling = np.random.randint(20, 70, size=8)
        team_overall = team_batting + team_bowling + np.random.randint(20, 50, size=8)
        team_rpe = np.random.randint(4, 8, size=8)
        df_player = pd.DataFrame(
            {
                "Week": weeks,
                "Batting": batting,
                "Bowling": bowling,
                "Overall": overall,
                "RPE": player_rpe,
            }
        )
        df_team = pd.DataFrame(
            {
                "Week": weeks,
                "Batting": team_batting,
                "Bowling": team_bowling,
                "Overall": team_overall,
                "RPE": team_rpe,
            }
        )

        # --- Player-specific info (restored) ---
        st.subheader(f"{selected_player} Workload Trends")
        st.line_chart(df_player.set_index("Week")[["Batting", "Bowling", "Overall"]])
        st.subheader(f"{selected_player} RPE Trend")
        st.line_chart(df_player.set_index("Week")[["RPE"]])
        st.write("#### Player Summary Metrics")
        st.metric(f"{selected_player} Last Week RPE", f"{player_rpe[-1]}")
        st.metric(f"{selected_player} Last Week Workload", f"{overall[-1]}")

        # --- Manual workload entry for coach ---
        st.markdown("---")
        st.subheader(f"Add Manual Workload Entry for {selected_player}")
        if "coach_workload_entries" not in st.session_state:
            st.session_state["coach_workload_entries"] = {
                name: [] for name in player_names
            }
        with st.form("coach_workload_form_profile"):
            session_type_c = st.selectbox(
                "Session Type", ["Training", "Match", "Other sport"]
            )
            date_c = st.date_input("Date")
            duration_c = st.slider(
                "Duration (minutes)", min_value=0, max_value=480, value=60, step=30
            )
            rpe_c = st.slider(
                "RPE (Rate of Perceived Exertion)", min_value=1, max_value=10, value=5
            )
            batting_minutes_c = st.number_input(
                "Batting Minutes", min_value=0, max_value=240, value=0
            )
            bowling_overs_c = st.number_input(
                "Bowling Overs", min_value=0, max_value=50, value=0
            )
            fielding_time_c = st.number_input(
                "Fielding Time (minutes)", min_value=0, max_value=240, value=0
            )
            comment_c = st.text_area("Comment (optional)")
            submitted_c = st.form_submit_button("Add Entry")
        if submitted_c:
            st.session_state["coach_workload_entries"][selected_player].append(
                {
                    "Session Type": session_type_c,
                    "Date": date_c,
                    "Duration": duration_c,
                    "RPE": rpe_c,
                    "Batting Minutes": batting_minutes_c,
                    "Bowling Overs": bowling_overs_c,
                    "Fielding Time": fielding_time_c,
                    "Comment": comment_c,
                }
            )
            st.success(f"Entry added for {selected_player} (mock)")

        # Table of previous entries for selected player
        st.subheader(f"Previous Entries for {selected_player}")
        entries_c_df = pd.DataFrame(
            st.session_state["coach_workload_entries"][selected_player]
        )
        if not entries_c_df.empty:
            st.dataframe(entries_c_df, use_container_width=True)

        # --- Team comparison section ---
        st.markdown("---")
        st.subheader("Team Comparison")
        st.write("#### Workload Comparison")
        # Generate mock weekly data for all players
        num_players = 12
        player_names_all = [f"Player {i+1}" for i in range(num_players)]
        # Each player gets a random workload and RPE for each week
        all_workloads = np.random.randint(80, 300, size=(num_players, len(weeks)))
        all_rpes = np.random.randint(3, 9, size=(num_players, len(weeks)))
        # Calculate team averages for each week
        team_avg_workload = np.mean(all_workloads, axis=0)
        team_avg_rpe = np.mean(all_rpes, axis=0)
        # Use selected player's data for comparison
        selected_idx = player_names_all.index(selected_player)
        selected_workload = all_workloads[selected_idx]
        selected_rpe = all_rpes[selected_idx]
        # Workload comparison chart
        workload_compare = pd.DataFrame(
            {
                f"{selected_player} Overall": selected_workload,
                "Team Avg Overall": team_avg_workload,
            },
            index=weeks,
        )
        st.line_chart(workload_compare)
        st.write("#### RPE Comparison")
        rpe_compare = pd.DataFrame(
            {f"{selected_player} RPE": selected_rpe, "Team Avg RPE": team_avg_rpe},
            index=weeks,
        )
        st.line_chart(rpe_compare)
        st.write("#### Team Comparison Metrics")
        st.metric("Team Avg Last Week RPE", f"{team_rpe[-1]}")
        st.metric("Team Avg Last Week Workload", f"{team_overall[-1]}")

        st.subheader("Menstrual Cycle Overlay (mock)")
        cycle_overlay = ["Menstrual" if i % 4 == 0 else "Low risk" for i in range(8)]
        overlay_df = pd.DataFrame({"Week": weeks, "Cycle Phase": cycle_overlay})
        st.dataframe(overlay_df, use_container_width=True)
        st.subheader("AI Recommendations")
        st.info(
            "Rest recommended during menstrual phase. Reduce overs if high load detected."
        )
        st.success("Player is match ready.")
    elif tab == "Model Retraining":
        st.header("Model Retraining")
        st.write("Trigger a model retraining job and view status.")
        import time

        # Mock retraining state
        if "retrain_status" not in st.session_state:
            st.session_state["retrain_status"] = "Idle"
            st.session_state["last_retrained"] = "Never"
            st.session_state["retrain_log"] = []
        # Button to trigger retraining
        if st.button("Start Model Retraining"):
            st.session_state["retrain_status"] = "Running"
            st.session_state["last_retrained"] = time.strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["retrain_log"] = ["Retraining started..."]
        # Simulate progress (mock)
        if st.session_state["retrain_status"] == "Running":
            st.progress(70)
            st.session_state["retrain_log"].append("Epoch 1/3: Loss=0.45")
            st.session_state["retrain_log"].append("Epoch 2/3: Loss=0.39")
            st.session_state["retrain_log"].append("Epoch 3/3: Loss=0.33")
            st.session_state["retrain_log"].append("Model retraining complete.")
            st.session_state["retrain_status"] = "Complete"
        st.write(f"**Status:** {st.session_state['retrain_status']}")
        st.write(f"**Last Retrained:** {st.session_state['last_retrained']}")
        st.write("**Retraining Log:**")
        for log_entry in st.session_state["retrain_log"]:
            st.write(log_entry)
