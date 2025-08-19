import streamlit as st

st.set_page_config(page_title="Cricket Tracker", layout="wide")

st.title("Cricket Tracker")

# Role selection (placeholder for Auth0 integration)
role = st.sidebar.selectbox("Select your role", ["Player", "Coach"])

if role == "Player":
    tab = st.sidebar.radio(
        "Player Menu", ["Workload Input", "Cycle Tracking", "Dashboard"]
    )
    if tab == "Workload Input":
        st.header("Workload Input")
        import pandas as pd

        # Initialize session state for entries
        if "workload_entries" not in st.session_state:
            st.session_state["workload_entries"] = [
                {
                    "Session Type": "Training",
                    "Date": pd.Timestamp.today().date(),
                    "Duration": 60,
                    "RPE": 5,
                    "Batting Minutes": 30,
                    "Bowling Overs": 5,
                    "Fielding Time": 20,
                },
                {
                    "Session Type": "Match",
                    "Date": pd.Timestamp.today().date() - pd.Timedelta(days=1),
                    "Duration": 120,
                    "RPE": 7,
                    "Batting Minutes": 60,
                    "Bowling Overs": 10,
                    "Fielding Time": 40,
                },
            ]
        # Form for new entry
        with st.form("workload_form"):
            session_type = st.selectbox(
                "Session Type", ["Training", "Match", "Other sport"]
            )
            date = st.date_input("Date")
            duration = st.slider(
                "Duration (minutes)", min_value=0, max_value=480, value=60, step=30
            )
            rpe = st.slider(
                "RPE (Rate of Perceived Exertion)", min_value=1, max_value=10, value=5
            )
            batting_minutes = st.number_input(
                "Batting Minutes", min_value=0, max_value=240, value=0
            )
            bowling_overs = st.number_input(
                "Bowling Overs", min_value=0, max_value=50, value=0
            )
            fielding_time = st.number_input(
                "Fielding Time (minutes)", min_value=0, max_value=240, value=0
            )
            comment = st.text_area("Comment (optional)")
            submitted = st.form_submit_button("Save")
        if submitted:
            st.session_state["workload_entries"].append(
                {
                    "Session Type": session_type,
                    "Date": date,
                    "Duration": duration,
                    "RPE": rpe,
                    "Batting Minutes": batting_minutes,
                    "Bowling Overs": bowling_overs,
                    "Fielding Time": fielding_time,
                    "Comment": comment,
                }
            )
            st.success("Workload entry saved (mock)")

        # Table of previous entries
        st.subheader("Previous Workload Entries")
        entries_df = pd.DataFrame(st.session_state["workload_entries"])
        # Add update/delete controls for each entry
        for idx, entry in enumerate(st.session_state["workload_entries"]):
            cols = st.columns([2, 2, 1, 1, 1, 1, 1, 2, 1, 1])
            cols[0].write(entry["Session Type"])
            cols[1].write(entry["Date"])
            cols[2].write(entry["Duration"])
            cols[3].write(entry["RPE"])
            cols[4].write(entry["Batting Minutes"])
            cols[5].write(entry["Bowling Overs"])
            cols[6].write(entry["Fielding Time"])
            cols[7].write(entry.get("Comment", ""))
            if cols[8].button("Update", key=f"update_{idx}"):
                # Simple update: repopulate form with entry values
                st.session_state["update_idx"] = idx
                st.session_state["update_mode"] = True
            if cols[7].button("Delete", key=f"delete_{idx}"):
                st.session_state["workload_entries"].pop(idx)
                st.experimental_rerun()
        # Update logic (mock)
        if st.session_state.get("update_mode", False):
            update_idx = st.session_state["update_idx"]
            entry = st.session_state["workload_entries"][update_idx]
            st.info(f"Update entry for {entry['Date']} ({entry['Session Type']})")
            with st.form("update_form"):
                session_type_u = st.selectbox(
                    "Session Type",
                    ["Training", "Match", "Other sport"],
                    index=["Training", "Match", "Other sport"].index(
                        entry["Session Type"]
                    ),
                )
                date_u = st.date_input("Date", value=entry["Date"])
                duration_u = st.slider(
                    "Duration (minutes)",
                    min_value=0,
                    max_value=480,
                    value=entry["Duration"],
                    step=30,
                )
                rpe_u = st.slider(
                    "RPE (Rate of Perceived Exertion)",
                    min_value=1,
                    max_value=10,
                    value=entry["RPE"],
                )
                batting_minutes_u = st.number_input(
                    "Batting Minutes",
                    min_value=0,
                    max_value=240,
                    value=entry["Batting Minutes"],
                )
                bowling_overs_u = st.number_input(
                    "Bowling Overs",
                    min_value=0,
                    max_value=50,
                    value=entry["Bowling Overs"],
                )
                fielding_time_u = st.number_input(
                    "Fielding Time (minutes)",
                    min_value=0,
                    max_value=240,
                    value=entry["Fielding Time"],
                )
                comment_u = st.text_area(
                    "Comment (optional)", value=entry.get("Comment", "")
                )
                updated = st.form_submit_button("Update Entry")
            if updated:
                st.session_state["workload_entries"][update_idx] = {
                    "Session Type": session_type_u,
                    "Date": date_u,
                    "Duration": duration_u,
                    "RPE": rpe_u,
                    "Batting Minutes": batting_minutes_u,
                    "Bowling Overs": bowling_overs_u,
                    "Fielding Time": fielding_time_u,
                    "Comment": comment_u,
                }
                st.session_state["update_mode"] = False
                st.success("Entry updated (mock)")
                st.experimental_rerun()
    elif tab == "Cycle Tracking":
        st.header("Menstrual Cycle Tracking")
        st.subheader("Log Period Start and Symptoms")
        with st.form("cycle_form"):
            period_start = st.date_input("Period Start Date")
            symptoms = st.multiselect(
                "Symptoms",
                [
                    "Fatigue",
                    "Cramps",
                    "Mood changes",
                    "Sleep quality",
                    "Headache",
                    "Bloating",
                    "Soreness",
                ],
            )
            wellness = st.slider("Wellness (1-5)", min_value=1, max_value=5, value=3)
            sleep = st.slider("Sleep Quality (1-5)", min_value=1, max_value=5, value=3)
            mood = st.slider("Mood (1-5)", min_value=1, max_value=5, value=3)
            soreness = st.slider("Soreness (1-5)", min_value=1, max_value=5, value=3)
            cycle_comment = st.text_area("Comment (optional)")
            submitted = st.form_submit_button("Save")
        if submitted:
            # Store cycle log with comment (mock)
            if "cycle_entries" not in st.session_state:
                st.session_state["cycle_entries"] = []
            st.session_state["cycle_entries"].append(
                {
                    "Period Start": period_start,
                    "Symptoms": symptoms,
                    "Wellness": wellness,
                    "Sleep": sleep,
                    "Mood": mood,
                    "Soreness": soreness,
                    "Comment": cycle_comment,
                }
            )
            st.success("Cycle log saved (mock)")
        st.subheader("Cycle Calendar")
        import pandas as pd
        import datetime
        from datetime import timedelta

        # Use the last logged period_start or today if not submitted
        today = datetime.date.today()
        cycle_start = period_start if submitted else today - timedelta(days=5)
        cycle_length = 28
        period_length = 5

        # Generate mock cycle days for the next 2 cycles
        dates = [cycle_start + timedelta(days=i) for i in range(cycle_length * 2)]
        phases = []
        for i in range(len(dates)):
            day_in_cycle = i % cycle_length
            if day_in_cycle < period_length:
                phases.append("Menstrual")
            elif day_in_cycle < 14:
                phases.append("Follicular")
            elif day_in_cycle < 16:
                phases.append("Ovulatory")
            else:
                phases.append("Luteal")

        df = pd.DataFrame({"Date": dates, "Phase": phases})
        phase_colors = {
            "Menstrual": "#ffb6c1",
            "Follicular": "#add8e6",
            "Ovulatory": "#ffd700",
            "Luteal": "#90ee90",
        }

        # Show calendar as a colored table
        st.write("### Projected Cycle Days")

        def color_row(row):
            color = phase_colors.get(row["Phase"], "white")
            return [f"background-color: {color}" for _ in row]

        st.dataframe(df.style.apply(color_row, axis=1), use_container_width=True)
    elif tab == "Dashboard":
        st.header("Player Dashboard")
        st.subheader("Weekly Workload Chart")
        import numpy as np
        import pandas as pd

        # Mock workload data
        weeks = pd.date_range(end=pd.Timestamp.today(), periods=8, freq="W-MON")
        acute = np.random.randint(100, 300, size=8)
        chronic = np.random.randint(80, 250, size=8)
        acwr = acute / np.maximum(chronic, 50)
        df = pd.DataFrame(
            {"Week": weeks, "Acute": acute, "Chronic": chronic, "ACWR": acwr}
        )
        st.line_chart(df.set_index("Week")[["Acute", "Chronic"]])
        st.subheader("Training Load Summary")
        st.metric("Acute Load", f"{acute[-1]}")
        st.metric("Chronic Load", f"{chronic[-1]}")
        st.metric("A:C Ratio", f"{acwr[-1]:.2f}")
        st.subheader("AI Insights")
        risk = "moderate" if acwr[-1] > 1.2 else "low"
        st.info(f"You are at {risk} injury risk this week.")
        st.success("Suggested: Take a recovery day after high load.")
elif role == "Coach":
    tab = st.sidebar.radio(
        "Coach Menu", ["Team Dashboard", "Player Profile", "Model Retraining"]
    )
    if tab == "Team Dashboard":
        st.header("Team Dashboard")
        st.subheader("Player Table")
        import pandas as pd
        import numpy as np

        # Mock player data
        roles = ["Batter", "Bowler", "All-rounder"]
        player_names = [f"Player {i+1}" for i in range(12)]
        player_roles = np.random.choice(roles, size=12)
        last7_load = np.random.randint(80, 300, size=12)
        acwr = np.round(np.random.uniform(0.8, 1.6, size=12), 2)
        risk_status = [
            "Red" if x > 1.4 else "Yellow" if x > 1.2 else "Green" for x in acwr
        ]
        df = pd.DataFrame(
            {
                "Name": player_names,
                "Role": player_roles,
                "Last 7d Load": last7_load,
                "A:C Ratio": acwr,
                "Risk": risk_status,
            }
        )
        filter_role = st.selectbox("Filter by Role", ["All"] + roles)
        if filter_role != "All":
            df = df[df["Role"] == filter_role]
        st.dataframe(df, use_container_width=True)
        st.subheader("Team Summary")
        st.bar_chart(df.set_index("Name")["Last 7d Load"])
        avg_load = df["Last 7d Load"].mean()
        red_flags = (df["Risk"] == "Red").sum()
        yellow_flags = (df["Risk"] == "Yellow").sum()
        st.metric("Average Load", f"{avg_load:.0f}")
        st.metric("Red Flags", red_flags)
        st.metric("Yellow Flags", yellow_flags)

        # --- Coach workload entry for players ---
        st.markdown("---")
        st.subheader("Add/Manage Workload Entries for Players")
        # Initialize session state for coach entries
        if "coach_workload_entries" not in st.session_state:
            st.session_state["coach_workload_entries"] = {
                name: [] for name in player_names
            }
        selected_player_c = st.selectbox("Select Player to Add Entry", player_names)
        with st.form("coach_workload_form"):
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
            st.session_state["coach_workload_entries"][selected_player_c].append(
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
            st.success(f"Entry added for {selected_player_c} (mock)")

        # Table of previous entries for selected player
        st.subheader(f"Previous Entries for {selected_player_c}")
        entries_c_df = pd.DataFrame(
            st.session_state["coach_workload_entries"][selected_player_c]
        )
        if not entries_c_df.empty:
            for idx, entry in enumerate(
                st.session_state["coach_workload_entries"][selected_player_c]
            ):
                cols = st.columns([2, 2, 1, 1, 1, 1, 1, 2, 1, 1])
                cols[0].write(entry["Session Type"])
                cols[1].write(entry["Date"])
                cols[2].write(entry["Duration"])
                cols[3].write(entry["RPE"])
                cols[4].write(entry["Batting Minutes"])
                cols[5].write(entry["Bowling Overs"])
                cols[6].write(entry["Fielding Time"])
                cols[7].write(entry.get("Comment", ""))
                if cols[8].button(
                    "Update", key=f"coach_update_{selected_player_c}_{idx}"
                ):
                    st.session_state["coach_update_idx"] = idx
                    st.session_state["coach_update_player"] = selected_player_c
                    st.session_state["coach_update_mode"] = True
                if cols[7].button(
                    "Delete", key=f"coach_delete_{selected_player_c}_{idx}"
                ):
                    st.session_state["coach_workload_entries"][selected_player_c].pop(
                        idx
                    )
                    st.experimental_rerun()
        # Update logic (mock)
        if (
            st.session_state.get("coach_update_mode", False)
            and st.session_state.get("coach_update_player") == selected_player_c
        ):
            update_idx_c = st.session_state["coach_update_idx"]
            entry_c = st.session_state["coach_workload_entries"][selected_player_c][
                update_idx_c
            ]
            st.info(
                f"Update entry for {selected_player_c} on {entry_c['Date']} ({entry_c['Session Type']})"
            )
            with st.form("coach_update_form"):
                session_type_uc = st.selectbox(
                    "Session Type",
                    ["Training", "Match", "Other sport"],
                    index=["Training", "Match", "Other sport"].index(
                        entry_c["Session Type"]
                    ),
                )
                date_uc = st.date_input("Date", value=entry_c["Date"])
                duration_uc = st.slider(
                    "Duration (minutes)",
                    min_value=0,
                    max_value=480,
                    value=entry_c["Duration"],
                    step=30,
                )
                rpe_uc = st.slider(
                    "RPE (Rate of Perceived Exertion)",
                    min_value=1,
                    max_value=10,
                    value=entry_c["RPE"],
                )
                batting_minutes_uc = st.number_input(
                    "Batting Minutes",
                    min_value=0,
                    max_value=240,
                    value=entry_c["Batting Minutes"],
                )
                bowling_overs_uc = st.number_input(
                    "Bowling Overs",
                    min_value=0,
                    max_value=50,
                    value=entry_c["Bowling Overs"],
                )
                fielding_time_uc = st.number_input(
                    "Fielding Time (minutes)",
                    min_value=0,
                    max_value=240,
                    value=entry_c["Fielding Time"],
                )
                comment_uc = st.text_area(
                    "Comment (optional)", value=entry_c.get("Comment", "")
                )
                updated_c = st.form_submit_button("Update Entry")
            if updated_c:
                st.session_state["coach_workload_entries"][selected_player_c][
                    update_idx_c
                ] = {
                    "Session Type": session_type_uc,
                    "Date": date_uc,
                    "Duration": duration_uc,
                    "RPE": rpe_uc,
                    "Batting Minutes": batting_minutes_uc,
                    "Bowling Overs": bowling_overs_uc,
                    "Fielding Time": fielding_time_uc,
                    "Comment": comment_uc,
                }
                st.session_state["coach_update_mode"] = False
                st.success("Entry updated (mock)")
                st.experimental_rerun()
    elif tab == "Player Profile":
        st.header("Player Profile View")
        # Select player
        player_names = [f"Player {i+1}" for i in range(12)]
        selected_player = st.selectbox("Select Player", player_names)
        import numpy as np
        import pandas as pd

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
