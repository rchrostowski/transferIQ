import streamlit as st
import pandas as pd

teams = pd.read_csv("data/teams.csv")
team = st.selectbox("Team", teams["team"])
st.json(teams[teams["team"] == team].to_dict("records")[0])

