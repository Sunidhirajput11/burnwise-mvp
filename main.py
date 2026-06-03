import streamlit as st
import pandas as pd

st.title("💸 BurnWise")
st.subheader("BurnWise shows where your business is losing money and how to stop it.")

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

        st.metric("Total Spending", f"€{total_spend:.2f}")
        st.metric("Average Expense", f"€{avg_spend:.2f}")
        st.metric("Highest Expense", f"€{max_spend:.2f}")

        st.subheader("📂 Category Breakdown")

        if "category" in df.columns:
            category_summary = df.groupby("category")[amount_col].sum()
            st.write(category_summary)

        st.subheader("🔝 Top 5 Expenses")
        st.write(df.nlargest(5, amount_col))

        st.subheader("⚠️ Waste Signals")
        st.write(df[df.duplicated()])
