import streamlit as st
from src.ui.player_view import player_view
from src.ui.coach_view import coach_view

import requests  # type: ignore

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Cricket Tracker", layout="wide")
st.title("Cricket Tracker")

if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
    st.stop()

if st.user.is_logged_in:
    st.sidebar.markdown(f"Welcome {st.user.name}")
    st.sidebar.button("Log Out", on_click=st.logout)

st.json(st.user)
# Role selection (placeholder for Auth0 integration)
role = st.sidebar.selectbox("Select your role", ["Player", "Coach"])

if role == "Player":
    player_view(API_URL)

if role == "Coach":
    coach_view()
