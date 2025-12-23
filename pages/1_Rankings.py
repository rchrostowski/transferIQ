import streamlit as st
import pandas as pd
from models.regression import train, predict
from utils.scheme_fit import compute_scheme_fit
from utils.scoring import total_score

teams = pd.read_csv("data/teams.csv")
df = pd.read_csv("data/transfers.csv")

team = st.selectbox("Select Team", teams["team"])
team_row = teams[teams["team"] == team].iloc[0]

df["scheme_match"] = df["position"].apply(
    lambda p: compute_scheme_fit(p, team_row["offense"])
)

model = train(df)
df = predict(df, model)

df["Total Score"] = df.apply(total_score, axis=1)
df = df.sort_values("Total Score", ascending=False)

st.dataframe(df[[
    "player",
    "position",
    "expected_snaps",
    "scheme_match",
    "nil_bucket",
    "Total Score"
]], use_container_width=True)

