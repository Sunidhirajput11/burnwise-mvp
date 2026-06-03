import streamlit as st
import pandas as pd

st.title("💸 BurnWise MVP - Expense Intelligence")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data")
    st.write(df)

    st.subheader("📌 Insights")

    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) == 0:
        st.error("No numeric columns found.")
    else:
        amount_col = numeric_cols[0]

        total_spend = df[amount_col].sum()
        avg_spend = df[amount_col].mean()
        max_spend = df[amount_col].max()

        waste_estimate = total_spend * 0.1

        st.metric("Total Spending", f"€{total_spend:.2f}")
        st.metric("Average Expense", f"€{avg_spend:.2f}")
        st.metric("Highest Expense", f"€{max_spend:.2f}")
        st.metric("Estimated Waste", f"€{waste_estimate:.2f}")

        st.subheader("⚠️ Waste Signals")

        st.write("Duplicate transactions:")
        st.write(df[df.duplicated()])

        st.write("Top 5 expenses:")
        st.write(df.nlargest(5, amount_col))
