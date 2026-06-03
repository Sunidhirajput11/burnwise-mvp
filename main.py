import streamlit as st
import pandas as pd

st.title("BurnWise MVP - Expense Analyzer")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.write(df)

    st.subheader("Basic Summary")
    st.write(df.describe(include="all"))
