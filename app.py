import streamlit as st
import pandas as pd

from analyzer import analyze_csv
from llm import ask_llm


st.title("🤖 AI Data Analyst")

st.write(
    "Upload a CSV file and analyze your data using AI."
)

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)


if uploaded_file:

    st.success("CSV uploaded successfully!")

    # -------------------------
    # Run analysis
    # -------------------------

    df, results = analyze_csv(uploaded_file)

    # -------------------------
    # Dataset Preview
    # -------------------------

    st.subheader("📊 Dataset Preview")

    st.dataframe(df.head())

    # -------------------------
    # Dataset Information
    # -------------------------

    st.subheader("📋 Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric(
            "Missing Values",
            df.isnull().sum().sum()
        )

    # -------------------------
    # Data Types
    # -------------------------

    st.subheader("🔤 Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(dtype_df)

    # -------------------------
    # Statistical Summary
    # -------------------------

    st.subheader("📈 Statistical Summary")

    st.dataframe(df.describe())

    # -------------------------
    # Missing Values
    # -------------------------

    st.subheader("⚠️ Missing Values")

    missing = df.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values
    })

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if len(missing_df) > 0:
        st.dataframe(missing_df)
    else:
        st.success("No missing values found!")

    # -------------------------
    # Ask AI
    # -------------------------

    st.subheader("🤖 Ask AI About Your Data")

    question = st.text_input(
        "Ask a question about your dataset:"
    )

    if question:

        with st.spinner("AI is analyzing your data..."):

            answer = ask_llm(
                question,
                results
            )

        st.subheader("💡 AI Analysis")

        st.write(answer)