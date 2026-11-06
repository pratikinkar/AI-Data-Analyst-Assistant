
import pandas as pd
import streamlit as st


def load_uploaded_file(uploaded_file):
    """Load CSV, Excel, or JSON files into a DataFrame."""

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        elif file_name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)

        elif file_name.endswith(".json"):
            return pd.read_json(uploaded_file)

        else:
            st.error("Unsupported file format. Please upload CSV, Excel, or JSON.")
            return None

    except Exception as error:
        st.error(f"Unable to load file: {error}")
        return None
