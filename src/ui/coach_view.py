import streamlit as st
import pandas as pd
import numpy as np


def coach_view() -> None:
    """Render the Coach UI: team dashboard, player profile and model retraining."""
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
        st.dataframe(df_filtered, width="stretch")
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
        selected_player = st.selectbox("Select Player", player_names)
        weeks = pd.date_range(end=pd.Timestamp.today(), periods=8, freq="W-MON")
        batting = np.random.randint(20, 120, size=8)
        bowling = np.random.randint(10, 80, size=8)
        overall = batting + bowling + np.random.randint(10, 40, size=8)
        player_rpe = np.random.randint(3, 9, size=8)
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

        st.subheader(f"{selected_player} Workload Trends")
        st.line_chart(df_player.set_index("Week")[["Batting", "Bowling", "Overall"]])
        st.subheader(f"{selected_player} RPE Trend")
        st.line_chart(df_player.set_index("Week")[["RPE"]])
        st.write("#### Player Summary Metrics")
        st.metric(f"{selected_player} Last Week RPE", f"{player_rpe[-1]}")
        st.metric(f"{selected_player} Last Week Workload", f"{overall[-1]}")

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
                "Batting Minutes", min_value=0, max_value=240, value=0, step=15
            )
            bowling_overs_c = st.number_input(
                "Bowling Overs", min_value=0, max_value=50, value=0
            )
            fielding_time_c = st.number_input(
                "Fielding Time (minutes)", min_value=0, max_value=240, value=0, step=15
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

        st.subheader(f"Previous Entries for {selected_player}")
        entries_c_df = pd.DataFrame(
            st.session_state["coach_workload_entries"][selected_player]
        )
        if not entries_c_df.empty:
            st.dataframe(entries_c_df, width="stretch")

    elif tab == "Model Retraining":
        st.header("Model Retraining")
        st.write("Trigger a model retraining job and view status.")
        import time

        if "retrain_status" not in st.session_state:
            st.session_state["retrain_status"] = "Idle"
            st.session_state["last_retrained"] = "Never"
            st.session_state["retrain_log"] = []
        if st.button("Start Model Retraining"):
            st.session_state["retrain_status"] = "Running"
            st.session_state["last_retrained"] = time.strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["retrain_log"] = ["Retraining started..."]
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
