
import streamlit as st
from reports.export_engine import export_csv, export_excel
from reports.pdf_report import generate_pdf_report
from reports.html_report import generate_html_report

st.title("📑 Report Center")
st.caption("Generate and download professional analytics reports.")

df = st.session_state.get("working_df")
dataset_name = st.session_state.get("dataset_name", "Analytics Dataset")

if df is None or df.empty:
    st.warning("Please upload a dataset first from Data Import.")
    st.stop()

# Report Overview
st.subheader("📊 Report Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Records", f"{len(df):,}")
c2.metric("Total Columns", len(df.columns))
c3.metric("Missing Values", f"{df.isnull().sum().sum():,}")
c4.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

st.divider()

# CSV Report
st.subheader("📄 CSV Export")
st.write("Download the current working dataset in CSV format.")

st.download_button(
    "⬇️ Download CSV",
    data=export_csv(df),
    file_name="cleaned_dataset.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# Excel Report
st.subheader("📊 Excel Report")
st.write("Includes Dataset, Data Quality and Numerical Statistics sheets.")

st.download_button(
    "⬇️ Download Excel Report",
    data=export_excel(df),
    file_name="analytics_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.divider()

# PDF Report
st.subheader("📕 PDF Executive Report")
st.write("Download a structured summary with numerical statistics.")

if st.button("Generate PDF Report", use_container_width=True):
    try:
        pdf_data = generate_pdf_report(df, dataset_name)
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_data,
            file_name="executive_analytics_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as error:
        st.error(f"PDF generation failed: {error}")

st.divider()

# HTML Report
st.subheader("🌐 Interactive HTML Report")
st.write("Download an HTML report with an interactive Plotly chart.")

try:
    html_data = generate_html_report(df, dataset_name)

    st.download_button(
        "⬇️ Download HTML Report",
        data=html_data,
        file_name="interactive_analytics_report.html",
        mime="text/html",
        use_container_width=True
    )
except Exception as error:
    st.error(f"HTML generation failed: {error}")
