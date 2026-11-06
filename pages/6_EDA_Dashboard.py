
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# CREDIT CARD CUSTOMER ANALYTICS DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Credit Card Analytics",
    page_icon="💳",
    layout="wide"
)

# ---------------- THEME ----------------

theme = st.session_state.get("theme", "Light")
template = "plotly_dark" if theme == "Dark" else "plotly_white"

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}
.dashboard-header {
    padding: 25px 28px;
    border-radius: 12px;
    background: linear-gradient(110deg, #14243A, #234B70);
    color: white;
    margin-bottom: 22px;
}
.dashboard-header h1 {
    color: white;
    font-size: 29px;
    margin: 0;
}
.dashboard-header p {
    color: #D5E3F0;
    margin: 7px 0 0 0;
    font-size: 14px;
}
.kpi-card {
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 10px;
    padding: 17px 18px;
    min-height: 112px;
    background: rgba(128,128,128,0.045);
}
.kpi-label {
    font-size: 12px;
    color: #8795A5;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .6px;
}
.kpi-value {
    font-size: 25px;
    font-weight: 700;
    margin-top: 12px;
}
.section-heading {
    font-size: 19px;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 4px;
}
.section-subtitle {
    font-size: 12px;
    color: #8995A3;
    margin-bottom: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATASET ----------------

if st.session_state.get("cleaning_applied", False):
    df = st.session_state.get("working_df")
else:
    df = st.session_state.get("original_df")

if df is None or df.empty:
    st.warning("Please upload your credit card dataset first.")
    st.stop()

df = df.copy()

required_columns = [
    "BALANCE",
    "BALANCE_FREQUENCY",
    "PURCHASES",
    "ONEOFF_PURCHASES",
    "INSTALLMENTS_PURCHASES",
    "CASH_ADVANCE",
    "PURCHASES_FREQUENCY",
    "ONEOFF_PURCHASES_FREQUENCY",
    "PURCHASES_INSTALLMENTS_FREQUENCY",
    "CASH_ADVANCE_FREQUENCY",
    "CASH_ADVANCE_TRX",
    "PURCHASES_TRX",
    "CREDIT_LIMIT",
    "PAYMENTS",
    "MINIMUM_PAYMENTS",
    "PRC_FULL_PAYMENT",
    "TENURE"
]

available = [c for c in required_columns if c in df.columns]

for column in available:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# ---------------- HEADER ----------------

dataset_name = st.session_state.get(
    "dataset_name", "Credit Card Dataset"
)

st.markdown(f"""
<div class="dashboard-header">
    <h1>💳 Credit Card Customer Analytics</h1>
    <p>Portfolio Intelligence | Spending Behaviour | Payment Analysis | Customer Insights</p>
    <p>Dataset: {dataset_name} &nbsp; | &nbsp;
    {len(df):,} customer records &nbsp; | &nbsp;
    {len(df.columns)} attributes</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FILTERS ----------------

st.markdown('<div class="section-heading">Dashboard Filters</div>',
            unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])

filtered_df = df.copy()

if "TENURE" in df.columns:
    tenure_values = df["TENURE"].dropna()

    if not tenure_values.empty:
        min_tenure = int(tenure_values.min())
        max_tenure = int(tenure_values.max())

        with filter_col1:
            tenure_range = st.slider(
                "Customer Tenure",
                min_value=min_tenure,
                max_value=max_tenure,
                value=(min_tenure, max_tenure)
            )

        filtered_df = filtered_df[
            filtered_df["TENURE"].between(*tenure_range)
        ]

with filter_col2:
    metric_choice = st.selectbox(
        "Analysis Metric",
        [
            "PURCHASES",
            "BALANCE",
            "CASH_ADVANCE",
            "CREDIT_LIMIT",
            "PAYMENTS"
        ]
    )

with filter_col3:
    st.caption("All KPIs and charts respond to the selected tenure filter.")

if filtered_df.empty:
    st.warning("No records available for the selected filters.")
    st.stop()

# ---------------- KPI CARDS ----------------

def format_number(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"

def kpi_card(label, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-heading">Portfolio Overview</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Key metrics for the selected customer records</div>',
    unsafe_allow_html=True
)

kpis = [
    ("CUSTOMER RECORDS", f"{len(filtered_df):,}"),
    ("AVG. BALANCE", format_number(filtered_df["BALANCE"].mean())
     if "BALANCE" in filtered_df else "N/A"),
    ("AVG. PURCHASES", format_number(filtered_df["PURCHASES"].mean())
     if "PURCHASES" in filtered_df else "N/A"),
    ("AVG. CREDIT LIMIT", format_number(filtered_df["CREDIT_LIMIT"].mean())
     if "CREDIT_LIMIT" in filtered_df else "N/A"),
    ("AVG. PAYMENTS", format_number(filtered_df["PAYMENTS"].mean())
     if "PAYMENTS" in filtered_df else "N/A")
]

kpi_cols = st.columns(5)

for col, (label, value) in zip(kpi_cols, kpis):
    with col:
        kpi_card(label, value)

# ---------------- CHART HELPER ----------------

def style_chart(fig, height=350):
    fig.update_layout(
        template=template,
        height=height,
        margin=dict(l=20, r=20, t=55, b=25),
        font=dict(size=11),
        title_font=dict(size=15),
        legend_title_text=""
    )
    return fig

def has_columns(columns):
    return all(c in filtered_df.columns for c in columns)

# ---------------- SPENDING ANALYSIS ----------------

st.markdown('<div class="section-heading">Spending Behaviour Analysis</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Understand how customers use their credit cards for purchases</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("**Purchase Type Contribution**")

        purchase_types = {
            "One-off Purchases": "ONEOFF_PURCHASES",
            "Installment Purchases": "INSTALLMENTS_PURCHASES"
        }

        purchase_data = []

        for label, column in purchase_types.items():
            if column in filtered_df:
                amount = filtered_df[column].clip(lower=0).sum()
                purchase_data.append({
                    "Purchase Type": label,
                    "Amount": amount
                })

        if purchase_data and sum(x["Amount"] for x in purchase_data) > 0:
            fig = px.pie(
                pd.DataFrame(purchase_data),
                names="Purchase Type",
                values="Amount",
                hole=0.58
            )
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True,
                key="purchase_contribution"
            )
        else:
            st.info("Purchase data is unavailable.")

with right:
    with st.container(border=True):
        st.markdown("**Purchase Amount Distribution**")

        if "PURCHASES" in filtered_df:
            fig = px.histogram(
                filtered_df,
                x="PURCHASES",
                nbins=35,
                marginal="box",
                color_discrete_sequence=["#3984B8"]
            )
            fig.update_xaxes(title="Purchase Amount")
            fig.update_yaxes(title="Customer Count")
            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True,
                key="purchase_distribution"
            )
        else:
            st.info("Purchase data is unavailable.")

# ---------------- CREDIT ANALYSIS ----------------

st.markdown('<div class="section-heading">Credit & Cash Advance Analysis</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Explore credit limits, balances and cash advance patterns</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("**Balance vs Credit Limit**")

        if has_columns(["BALANCE", "CREDIT_LIMIT"]):
            fig = px.scatter(
                filtered_df,
                x="CREDIT_LIMIT",
                y="BALANCE",
                opacity=0.55,
                color="CASH_ADVANCE" if "CASH_ADVANCE" in filtered_df else None,
                color_continuous_scale="Blues"
            )
            fig.update_xaxes(title="Credit Limit")
            fig.update_yaxes(title="Customer Balance")

            st.plotly_chart(
                style_chart(fig, 370),
                use_container_width=True,
                key="balance_credit_scatter"
            )
        else:
            st.info("Required credit columns are unavailable.")

with right:
    with st.container(border=True):
        st.markdown("**Cash Advance Distribution**")

        if "CASH_ADVANCE" in filtered_df:
            fig = px.histogram(
                filtered_df,
                x="CASH_ADVANCE",
                nbins=35,
                color_discrete_sequence=["#D18B45"]
            )
            fig.update_xaxes(title="Cash Advance Amount")
            fig.update_yaxes(title="Customer Count")

            st.plotly_chart(
                style_chart(fig, 370),
                use_container_width=True,
                key="cash_advance_distribution"
            )
        else:
            st.info("Cash advance data is unavailable.")

# ---------------- CUSTOMER ACTIVITY ----------------

st.markdown('<div class="section-heading">Customer Activity & Transactions</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Transaction frequency and customer engagement patterns</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("**Purchase Frequency vs Purchase Amount**")

        if has_columns(["PURCHASES_FREQUENCY", "PURCHASES"]):
            fig = px.scatter(
                filtered_df,
                x="PURCHASES_FREQUENCY",
                y="PURCHASES",
                size="PURCHASES_TRX" if "PURCHASES_TRX" in filtered_df else None,
                opacity=0.6
            )
            fig.update_xaxes(title="Purchase Frequency")
            fig.update_yaxes(title="Purchase Amount")

            st.plotly_chart(
                style_chart(fig, 370),
                use_container_width=True,
                key="purchase_frequency_scatter"
            )
        else:
            st.info("Required purchase columns are unavailable.")

with right:
    with st.container(border=True):
        st.markdown("**Customer Tenure Distribution**")

        if "TENURE" in filtered_df:
            tenure_counts = (
                filtered_df["TENURE"]
                .value_counts()
                .sort_index()
                .rename_axis("Tenure")
                .reset_index(name="Customers")
            )

            fig = px.bar(
                tenure_counts,
                x="Tenure",
                y="Customers",
                text="Customers"
            )

            st.plotly_chart(
                style_chart(fig, 370),
                use_container_width=True,
                key="tenure_distribution"
            )
        else:
            st.info("Tenure data is unavailable.")

# ---------------- PAYMENT ANALYSIS ----------------

st.markdown('<div class="section-heading">Payment Behaviour Analysis</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Evaluate customer payments and full-payment behaviour</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("**Payments vs Minimum Payments**")

        if has_columns(["PAYMENTS", "MINIMUM_PAYMENTS"]):
            fig = px.scatter(
                filtered_df,
                x="MINIMUM_PAYMENTS",
                y="PAYMENTS",
                opacity=0.55
            )
            fig.update_xaxes(title="Minimum Payments")
            fig.update_yaxes(title="Payments")

            st.plotly_chart(
                style_chart(fig, 370),
                use_container_width=True,
                key="payment_comparison"
            )
        else:
            st.info("Payment columns are unavailable.")

with right:
    with st.container(border=True):
        st.markdown("**Full Payment Ratio Distribution**")

        if "PRC_FULL_PAYMENT" in filtered_df:
            fig = px.histogram(
                filtered_df,
                x="PRC_FULL_PAYMENT",
                nbins=25,
                color_discrete_sequence=["#3B9B83"]
            )
            fig.update_xaxes(title="Full Payment Ratio")
            fig.update_yaxes(title="Customer Count")

            st.plotly_chart(
                style_chart(fig, 370),
                use_container_width=True,
                key="full_payment_distribution"
            )
        else:
            st.info("Full payment data is unavailable.")

# ---------------- CORRELATION ANALYSIS ----------------

st.markdown('<div class="section-heading">Portfolio Correlation Analysis</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Identify relationships between credit card behaviour variables</div>',
    unsafe_allow_html=True
)

correlation_columns = [
    c for c in [
        "BALANCE",
        "PURCHASES",
        "ONEOFF_PURCHASES",
        "INSTALLMENTS_PURCHASES",
        "CASH_ADVANCE",
        "CREDIT_LIMIT",
        "PAYMENTS",
        "PURCHASES_TRX",
        "CASH_ADVANCE_TRX",
        "PRC_FULL_PAYMENT"
    ]
    if c in filtered_df.columns
]

if len(correlation_columns) >= 2:
    correlation = filtered_df[correlation_columns].corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto"
    )

    st.plotly_chart(
        style_chart(fig, 520),
        use_container_width=True,
        key="portfolio_correlation"
    )
else:
    st.info("Not enough numerical columns for correlation analysis.")

# ---------------- CUSTOMER SEGMENTS ----------------

st.markdown('<div class="section-heading">Customer Behaviour Segments</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Exploratory rule-based grouping using purchase and cash advance behaviour</div>',
    unsafe_allow_html=True
)

if has_columns(["PURCHASES", "CASH_ADVANCE"]):
    segment_df = filtered_df[
        ["PURCHASES", "CASH_ADVANCE"]
    ].copy()

    purchase_median = segment_df["PURCHASES"].median()
    cash_median = segment_df["CASH_ADVANCE"].median()

    segment_df["Customer Segment"] = np.select(
        [
            (segment_df["PURCHASES"] >= purchase_median) &
            (segment_df["CASH_ADVANCE"] < cash_median),

            (segment_df["PURCHASES"] < purchase_median) &
            (segment_df["CASH_ADVANCE"] >= cash_median),

            (segment_df["PURCHASES"] >= purchase_median) &
            (segment_df["CASH_ADVANCE"] >= cash_median)
        ],
        [
            "Purchase Focused",
            "Cash Advance Focused",
            "High Activity"
        ],
        default="Low Activity"
    )

    segment_counts = (
        segment_df["Customer Segment"]
        .value_counts()
        .rename_axis("Segment")
        .reset_index(name="Customers")
    )

    left, right = st.columns([1, 1])

    with left:
        with st.container(border=True):
            st.markdown("**Customer Segment Distribution**")

            fig = px.bar(
                segment_counts,
                x="Segment",
                y="Customers",
                color="Segment",
                text="Customers"
            )

            st.plotly_chart(
                style_chart(fig, 360),
                use_container_width=True,
                key="customer_segments"
            )

    with right:
        with st.container(border=True):
            st.markdown("**Segment Summary**")

            st.dataframe(
                segment_counts,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "These are exploratory groups based on median thresholds, "
                "not trained machine-learning clusters."
            )
else:
    st.info("Purchase and cash advance columns are required for segmentation.")

# ---------------- AUTOMATIC INSIGHTS ----------------

st.markdown('<div class="section-heading">Executive Insights</div>',
            unsafe_allow_html=True)

insights = []

if "PURCHASES" in filtered_df:
    insights.append(
        f"Average purchase amount is {format_number(filtered_df['PURCHASES'].mean())}."
    )

if "BALANCE" in filtered_df:
    insights.append(
        f"Average customer balance is {format_number(filtered_df['BALANCE'].mean())}."
    )

if "CASH_ADVANCE" in filtered_df:
    insights.append(
        f"Average cash advance amount is {format_number(filtered_df['CASH_ADVANCE'].mean())}."
    )

if "PRC_FULL_PAYMENT" in filtered_df:
    full_payment_avg = filtered_df["PRC_FULL_PAYMENT"].mean()
    insights.append(
        f"Average full payment ratio is {full_payment_avg:.2%}."
    )

if "PURCHASES_FREQUENCY" in filtered_df:
    frequency_avg = filtered_df["PURCHASES_FREQUENCY"].mean()
    insights.append(
        f"Average purchase frequency is {frequency_avg:.2%}."
    )

with st.container(border=True):
    for insight in insights:
        st.markdown(f"• {insight}")

# ---------------- DATA EXPORT ----------------

st.markdown('<div class="section-heading">Download Dashboard Data</div>',
            unsafe_allow_html=True)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="credit_card_analytics_data.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "Credit Card Customer Analytics | AI Data Analyst Assistant"
)
