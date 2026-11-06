
import runpy
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Data Analyst Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME SETTINGS ----------------

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

with st.sidebar:
    st.title("📊 Data Analyst AI")
    st.caption("Intelligent Analytics Platform")

    st.divider()

    selected_theme = st.radio(
        "Choose Theme",
        ["Light", "Dark"],
        horizontal=True,
        index=0 if st.session_state.theme == "Light" else 1
    )

    st.session_state.theme = selected_theme

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "📂 Data Import",
            "🔍 Data Explorer",
            "📊 Data Profiling",
            "🧹 Data Cleaning",
            "📈 EDA Dashboard",
            "🤖 AI Assistant",
            "📑 Report Center",
            "⚙️ Settings"
        ],
        label_visibility="visible"
    )

# ---------------- THEME COLORS ----------------

if st.session_state.theme == "Dark":

    bg = "#101827"
    card = "#1E293B"
    text = "#F1F5F9"
    muted = "#CBD5E1"
    border = "#334155"
    accent = "#38BDF8"

else:

    bg = "#F5F7FB"
    card = "#FFFFFF"
    text = "#172033"
    muted = "#64748B"
    border = "#CBD5E1"
    accent = "#2563EB"

# ---------------- CUSTOM STYLING ----------------

st.markdown(
    f"""
    <style>

    /* Main application background */

    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    /* Main content width and spacing */

    .block-container {{
        max-width: 100%;
        padding-top: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 2rem;
    }}

    /* Header */

    [data-testid="stHeader"] {{
        background: {bg};
    }}

    [data-testid="stToolbar"] {{
        right: 1rem;
    }}

    /* Sidebar */

    [data-testid="stSidebar"] {{
        background-color: {card};
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {{
        color: {text} !important;
    }}

    /* Main headings and text */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp p,
    .stApp label {{
        color: {text};
    }}

    /* Captions */

    .stApp [data-testid="stCaptionContainer"] p {{
        color: {muted} !important;
    }}

    /* Metric cards */

    [data-testid="stMetric"] {{
        background-color: {card};
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {border};
    }}

    [data-testid="stMetricLabel"] p {{
        color: {muted} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {text} !important;
    }}

    /* File uploader */

    [data-testid="stFileUploader"] {{
        background-color: {card};
        border-radius: 12px;
    }}

    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {{
        color: {text} !important;
    }}

    [data-testid="stFileUploader"] section {{
        background-color: {card};
        border: 1px dashed {border};
        border-radius: 12px;
    }}

    /* Buttons */

    .stButton button,
    .stDownloadButton button {{
        border-radius: 8px;
        font-weight: 600;
    }}

    /* Dataframes */

    [data-testid="stDataFrame"] {{
        border: 1px solid {border};
        border-radius: 10px;
    }}

    /* Expanders */

    [data-testid="stExpander"] {{
        border: 1px solid {border};
        border-radius: 10px;
    }}

    /* Dividers */

    hr {{
        border-color: {border};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HOME PAGE ----------------

if page == "🏠 Home":

    st.markdown(
        f"""
        <h1 style="color:{text};">
            Welcome to AI Data Analyst Assistant 👋
        </h1>

        <p style="color:{muted}; font-size:18px;">
            Your intelligent workspace for data analysis.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    df = st.session_state.get("original_df")

    if df is not None:
        total_rows = len(df)
        total_columns = len(df.columns)
        missing_values = int(df.isnull().sum().sum())
        dataset_count = 1
    else:
        total_rows = 0
        total_columns = 0
        missing_values = 0
        dataset_count = 0

    col1.metric("Datasets Loaded", dataset_count)
    col2.metric("Total Records", total_rows)
    col3.metric("Total Columns", total_columns)
    col4.metric("Missing Values", missing_values)

    st.divider()

    st.subheader("🚀 Quick Start")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📂 Import Dataset")
        st.write(
            "Upload CSV, Excel or JSON files "
            "to begin your analysis."
        )

    with col2:
        st.markdown("### 🤖 AI Data Assistant")
        st.write(
            "Ask questions and discover meaningful "
            "insights from your data."
        )

    st.divider()

    st.subheader("Platform Features")

    features = [
        ("📊", "Data Analysis", "Automatic EDA and statistics"),
        ("🧹", "Data Cleaning", "Handle missing values and duplicates"),
        ("📈", "Visualizations", "Interactive charts and dashboards"),
        ("🤖", "AI Assistant", "Ask questions about your dataset"),
        ("📑", "Reports", "Export PDF, Excel and HTML reports"),
        ("🔗", "SQL Connection", "Connect MySQL and PostgreSQL")
    ]

    feature_cols = st.columns(3)

    for i, (icon, title, description) in enumerate(features):

        with feature_cols[i % 3]:
            st.markdown(f"### {icon} {title}")
            st.caption(description)

# ---------------- DATA IMPORT ----------------

elif page == "📂 Data Import":

    runpy.run_path("pages/2_Data_Import.py")

# ---------------- DATA PROFILING ----------------

elif page == "📊 Data Profiling":

    runpy.run_path("pages/4_Data_Profiling.py")

# ---------------- DATA CLEANING ----------------

elif page == "🧹 Data Cleaning":

    runpy.run_path("pages/5_Data_Cleaning.py")

# ---------------- EDA DASHBOARD ----------------

elif page == "📈 EDA Dashboard":

    runpy.run_path("pages/6_EDA_Dashboard.py")

elif page == "🤖 AI Assistant":

    runpy.run_path("pages/7_AI_Assistant.py")

elif page == "📑 Report Center":

    runpy.run_path("pages/8_Report_Center.py")

    
# ---------------- OTHER MODULES ----------------

else:

    st.title(page)

    st.info(
        "This module will be developed in an upcoming milestone."
    )
