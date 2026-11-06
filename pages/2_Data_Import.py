
import streamlit as st
from core.file_loader import load_uploaded_file

st.title("📂 Data Import")
st.write("Upload your dataset to start analysing it.")

st.divider()

uploaded_file = st.file_uploader(
    "Choose a dataset",
    type=["csv", "xlsx", "xls", "json"]
)

if uploaded_file is not None:

    df = load_uploaded_file(uploaded_file)

    if df is not None:
        st.session_state["original_df"] = df.copy()
        st.session_state["working_df"] = df.copy()
        st.session_state["dataset_name"] = uploaded_file.name

        st.success(f"Successfully loaded: {uploaded_file.name}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isnull().sum().sum()))

        st.subheader("Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)

        with st.expander("Column Information"):
            st.write(df.dtypes.astype(str))

else:
    st.info("Upload a CSV, Excel, or JSON file to see your dataset preview.")
