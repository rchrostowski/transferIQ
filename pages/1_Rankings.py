import streamlit as st
import pandas as pd
from models.regression import train_model, predict
from utils.scoring import fit_score, cost_efficiency

st.header("📊 Transfer Rankings")

df = pd.read_csv("data/transfers.csv")
model = train_model(df)
df = predict(df, model)

df["Fit Score"] = df["scheme_match"].apply(fit_score)
df["Cost Efficiency"] = df.apply(
    lambda x: cost_efficiency(x["expected_snaps"], x["nil_bucket"]),
    axis=1
)

position = st.selectbox("Filter by Position", ["All"] + sorted(df["position"].unique()))

if position != "All":
    df = df[df["position"] == position]

df = df.sort_values("expected_snaps", ascending=False)

st.dataframe(
    df[[
        "player",
        "position",
        "expected_snaps",
        "Fit Score",
        "Cost Efficiency",
        "nil_bucket"
    ]],
    use_container_width=True
)

st.download_button(
    "⬇️ Export Shortlist",
    df.to_csv(index=False),
    file_name="transfer_shortlist.csv"
)

