---
MVP Status: All core screens implemented and interactive (Player/Coach workload, cycle tracking, dashboards, model retraining, entry management).

1. Login & Role-based Home

Login: Auth0 integration (email/password or federated login).

Roles: Player / Coach.

After login, show dashboard based on role.

2. Player Screens
(a) Workload Input Screen

Simple form for Session Type (Training / Match / Other sport).

Date & Duration.

Self-reported RPE (Rate of Perceived Exertion) scale slider (1–10).

Batting minutes / Bowling overs / Fielding time.

Save button → writes to Cosmos DB.
(Streamlit widgets: st.date_input, st.slider, st.number_input, st.form)

(b) Menstrual Cycle Tracking

Calendar view (current + projected cycle days).

Option to log: Period start, symptoms (fatigue, cramps, mood, sleep quality).

Auto-predict next cycle phase & risk windows.
(Streamlit: st.date_input, st.radio, st.multiselect)

(c) Player Dashboard

Weekly workload chart (line chart with acute:chronic ratio).

Training load summary cards:

Acute Load

Chronic Load

A:C Ratio

AI Insights (“You are at moderate injury risk this week”, “Suggested recovery day”).
(Streamlit: st.metric, st.line_chart)

3. Coach Screens
(a) Team Dashboard

Player table (Name, Role, Last 7-day load, A:C Ratio, Risk status).

Filters (batters, bowlers, all-rounders).

Team summary: average loads, red/yellow flag players.
(Streamlit: st.dataframe, st.bar_chart)

(b) Player Profile View

Select player → detailed dashboard:

Workload trends (batting, bowling, overall).

Menstrual cycle overlay (highlighting high-risk phases).

AI recommendations (rest, reduced overs, match readiness).

(c) Model Retraining Screen

Button: “Retrain Model” → triggers batch job (fetch Cosmos DB → train TensorFlow model → save model in Blob Storage).

Status indicator (last trained date, accuracy).
(Streamlit: st.button, st.progress, st.success)

4. Admin/Coach Extra

Export Data → CSV or Excel download.

Notifications → “Player X is in high-risk zone this week”.

Settings → Manage roles, teams, competitions.
Manual Entry → Capture player workload details.

⚡ Flow

Players log workloads & cycles → Data stored in Cosmos DB.

Coaches see dashboards + AI insights → Use ML-driven workload balancing.

Coach can trigger retrain weekly to improve predictions.