import streamlit as st
import pandas as pd

st.set_page_config(page_title="BurnWise", layout="wide")

# HEADER
st.title("💸 BurnWise")
st.subheader("Find where your business is losing money and how to stop it.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # detect numeric column
    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) == 0:
        st.error("No numeric columns found.")
    else:
        amount_col = numeric_cols[0]

        total_spend = df[amount_col].sum()
        avg_spend = df[amount_col].mean()
        max_spend = df[amount_col].max()
        waste_estimate = total_spend * 0.1

        # DASHBOARD METRICS (clean UI)
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Spend", f"€{total_spend:.2f}")
        col2.metric("Average", f"€{avg_spend:.2f}")
        col3.metric("Highest", f"€{max_spend:.2f}")
        col4.metric("Waste Estimate", f"€{waste_estimate:.2f}")

        st.divider()

        # INSIGHTS SECTION
        st.subheader("📊 Insights")

        st.write("Top 5 Expenses")
        st.dataframe(df.nlargest(5, amount_col), use_container_width=True)

        st.write("Duplicate Transactions")
        st.dataframe(df[df.duplicated()], use_container_width=True)

        # CATEGORY BREAKDOWN
        if "category" in df.columns:
            st.subheader("📂 Spending by Category")
            category_summary = df.groupby("category")[amount_col].sum()
            st.bar_chart(category_summary)
