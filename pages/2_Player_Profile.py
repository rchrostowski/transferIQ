import streamlit as st
import pandas as pd

df = pd.read_csv("data/transfers.csv")
player = st.selectbox("Player", df["player"])

row = df[df["player"] == player].iloc[0]

st.metric("Expected Snaps", row["year1_snaps"])
st.metric("Scheme Fit", row["scheme_match"])
st.metric("NIL Tier", row["nil_bucket"])


