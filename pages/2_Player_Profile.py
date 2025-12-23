import streamlit as st
import pandas as pd
from models.regression import train_model, predict

st.header("🧑‍🏫 Player Profile")

df = pd.read_csv("data/transfers.csv")
model = train_model(df)
df = predict(df, model)

player = st.selectbox("Select Player", df["player"].unique())
row = df[df["player"] == player].iloc[0]

st.subheader(player)

col1, col2 = st.columns(2)

with col1:
    st.metric("Expected Year-1 Snaps", round(row["expected_snaps"], 1))
    st.metric("Previous Snaps", row["prev_snaps"])
    st.metric("Years Experience", row["years_exp"])

with col2:
    st.metric("Scheme Match", round(row["scheme_match"] * 100, 1))
    st.metric("NIL Cost Tier", row["nil_bucket"])
    st.metric("Starter Previously", "Yes" if row["starter_prev"] else "No")

st.markdown("### Model Explanation")
st.markdown("""
This estimate is driven primarily by:
- Prior playing time
- Experience level
- Role continuity
- Scheme alignment
- Relative NIL cost
""")

