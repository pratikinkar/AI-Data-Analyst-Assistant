
import streamlit as st
from core.data_profiler import generate_profile

st.title("📊 Data Profiling")
st.write("Understand your dataset's quality and statistical summary.")

df = st.session_state.get("original_df")

if df is None:
    st.warning("Please upload a dataset first from Data Import.")
    st.stop()

profile = generate_profile(df)

st.divider()

# Overall metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rows", profile["total_rows"])
col2.metric("Total Columns", profile["total_columns"])
col3.metric("Duplicate Rows", profile["duplicate_rows"])
col4.metric("Missing Values", profile["missing_values"])

st.divider()

# Column-level profiling
st.subheader("Column Quality Report")

column_data = []

for column, details in profile["columns"].items():
    column_data.append({
        "Column": column,
        "Data Type": details["data_type"],
        "Missing Values": details["missing_values"],
        "Missing %": details["missing_percentage"],
        "Unique Values": details["unique_values"]
    })

st.dataframe(column_data, use_container_width=True)

# Numerical statistics
st.divider()
st.subheader("Numerical Statistics")

for column, details in profile["columns"].items():

    if "statistics" in details:
        with st.expander(f"📈 {column}"):
            st.json(details["statistics"])
