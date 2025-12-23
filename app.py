import streamlit as st

st.set_page_config(
    page_title="TransferIQ — NCAA Football",
    layout="wide"
)

st.title("🏈 TransferIQ — NCAA Football")
st.markdown("""
**Decision-support analytics for transfer portal recruiting & NIL efficiency.**

This tool ranks transfer candidates by **expected Year-1 contribution**, **scheme fit**, and **cost efficiency**.
""")

st.info("Use the sidebar to explore rankings, player profiles, and methodology.")

