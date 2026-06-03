import streamlit as st
import pandas as pd

st.set_page_config(page_title="BurnWise", layout="wide")

st.title("💸 BurnWise")
st.subheader("AI-powered spending intelligence for startups")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) == 0:
        st.error("No numeric columns found.")
    else:
        amount_col = numeric_cols[0]

        total_spend = df[amount_col].sum()
        avg_spend = df[amount_col].mean()
        max_spend = df[amount_col].max()
        waste_estimate = total_spend * 0.1

        # HEADER INSIGHT (important)
        st.info(
            f"Your total spending is €{total_spend:.2f}. "
            f"Estimated avoidable waste is around €{waste_estimate:.2f}."
        )

        # METRICS
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Spend", f"€{total_spend:.2f}")
        col2.metric("Average", f"€{avg_spend:.2f}")
        col3.metric("Highest", f"€{max_spend:.2f}")
        col4.metric("Waste", f"€{waste_estimate:.2f}")

        st.divider()

        # CATEGORY INSIGHT
        if "category" in df.columns:
            top_category = df.groupby("category")[amount_col].sum().idxmax()
            st.warning(f"Highest spending category: {top_category}")

        st.divider()

        # DATA
        st.subheader("📊 Top Expenses")
        st.dataframe(df.nlargest(5, amount_col), use_container_width=True)

        st.subheader("⚠️ Duplicate Transactions")
        st.dataframe(df[df.duplicated()], use_container_width=True)

        if "category" in df.columns:
            st.subheader("📂 Category Breakdown")
            st.bar_chart(df.groupby("category")[amount_col].sum())
