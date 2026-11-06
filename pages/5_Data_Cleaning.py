
import streamlit as st
import plotly.express as px

from core.data_cleaner import clean_data
from core.cleaning_recommender import recommend_cleaning_methods


st.title("🧹 Intelligent Data Cleaning")
st.write("Analyze data quality, visualize distributions and choose suitable cleaning methods.")

df = st.session_state.get("original_df")

if df is None:
    st.warning("Please upload a dataset first from Data Import.")
    st.stop()

st.success(
    f"Current Dataset: {st.session_state.get('dataset_name', 'Dataset')}"
)

st.divider()

# Step 1: Dataset overview
st.subheader("1. Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rows", len(df))
col2.metric("Total Columns", len(df.columns))
col3.metric("Missing Values", int(df.isnull().sum().sum()))

# Step 2: Select zero-as-missing columns
st.divider()
st.subheader("2. Data Preparation")

numeric_columns = df.select_dtypes(include="number").columns.tolist()

zero_columns = st.multiselect(
    "Treat zero values as missing in these columns",
    options=numeric_columns,
    default=[]
)

st.caption(
    "Select only columns where zero represents an invalid or missing measurement."
)

# Step 3: Generate recommendations
analysis_df = df.copy()

for column in zero_columns:
    analysis_df[column] = analysis_df[column].replace(
        0, float("nan")
    )

recommendations = recommend_cleaning_methods(
    df,
    zero_as_missing=zero_columns
)

st.divider()
st.subheader("3. Intelligent Column Analysis")

column_methods = {}

for column, details in recommendations.items():

    with st.expander(f"📊 {column} — {details['type']}", expanded=False):

        st.write(f"**Missing values:** {details['missing_values']}")

        if details["type"] == "Numerical":

            valid_data = analysis_df[column].dropna()

            if len(valid_data) > 0:

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Skewness",
                    details["skewness"]
                    if details["skewness"] is not None else "N/A"
                )

                col2.metric("Distribution", details["skew_type"])
                col3.metric("Potential Outliers", details["outliers"])

                # Distribution histogram
                st.markdown("**Distribution Analysis**")

                fig_hist = px.histogram(
                    valid_data,
                    x=column,
                    nbins=30,
                    marginal="box",
                    title=f"Distribution of {column}",
                    labels={column: column}
                )

                st.plotly_chart(
                    fig_hist,
                    use_container_width=True
                )

                # Box plot
                st.markdown("**Outlier Detection — Box Plot**")

                fig_box = px.box(
                    valid_data,
                    y=column,
                    points="outliers",
                    title=f"Potential Outliers in {column}"
                )

                st.plotly_chart(
                    fig_box,
                    use_container_width=True
                )

            if details["missing_values"] > 0:

                st.info(
                    f"Recommended method: {details['recommended_method'].upper()}"
                )

                st.caption(details["reason"])

                column_methods[column] = st.selectbox(
                    f"Choose filling method for {column}",
                    options=["median", "mean"],
                    index=(
                        0
                        if details["recommended_method"] == "median"
                        else 1
                    ),
                    key=f"method_{column}"
                )

            else:
                st.success("No missing values. Analysis only.")

        else:

            if details["missing_values"] > 0:

                st.write(f"**Most frequent category (Mode):** {details['mode_value']}")

                if len(analysis_df[column].dropna()) > 0:

                    frequency = (
                        analysis_df[column]
                        .value_counts()
                        .reset_index()
                    )

                    frequency.columns = ["Category", "Count"]

                    fig_cat = px.bar(
                        frequency,
                        x="Category",
                        y="Count",
                        title=f"Category Frequency — {column}"
                    )

                    st.plotly_chart(
                        fig_cat,
                        use_container_width=True
                    )

                st.info("Recommended method: MODE")
                st.caption(details["reason"])

                column_methods[column] = "mode"

            else:
                st.success("No missing values. Analysis only.")

# Step 4: Apply cleaning
st.divider()
st.subheader("4. Apply Cleaning")

if st.button("🧹 Clean Dataset", type="primary"):

    cleaned_df = clean_data(
        df,
        zero_as_missing=zero_columns,
        column_methods=column_methods
    )

    st.session_state["working_df"] = cleaned_df
    st.session_state["cleaning_applied"] = True

    st.success("Cleaning process completed!")

# Step 5: Before and after comparison
if st.session_state.get("cleaning_applied", False):

    cleaned_df = st.session_state["working_df"]

    st.divider()
    st.subheader("5. Before vs After Cleaning")

    col1, col2, col3 = st.columns(3)

    col1.metric("Original Rows", len(df))
    col2.metric("Cleaned Rows", len(cleaned_df))
    col3.metric(
        "Duplicates Removed",
        int(df.duplicated().sum())
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Original Missing Values",
        int(df.isnull().sum().sum())
    )

    col2.metric(
        "Cleaned Missing Values",
        int(cleaned_df.isnull().sum().sum())
    )

    st.subheader("Cleaned Dataset Preview")
    st.dataframe(cleaned_df.head(20), use_container_width=True)

    csv_data = cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )


    
# Step 6: Interactive Chart Customizer
st.divider()
st.title("🎨 Interactive Chart Customizer")
st.write("Create and customize charts using your own dataset columns.")

chart_df = st.session_state.get("working_df", df)

chart_type = st.selectbox(
    "Choose Chart Type",
    ["Histogram", "Box Plot", "Scatter Plot", "Bar Chart"]
)

all_columns = chart_df.columns.tolist()
numeric_columns = chart_df.select_dtypes(include="number").columns.tolist()

if chart_type in ["Histogram", "Box Plot"]:
    x_options = numeric_columns
else:
    x_options = all_columns

if not x_options:
    st.warning("No suitable columns available for this chart.")
    st.stop()

x_column = st.selectbox("Select X-axis", x_options)

y_column = None

if chart_type in ["Scatter Plot", "Bar Chart"]:
    y_options = [
        column for column in numeric_columns
        if column != x_column
    ]

    if y_options:
        y_column = st.selectbox("Select Y-axis", y_options)
    elif chart_type == "Scatter Plot":
        st.warning("Scatter Plot requires two numerical columns.")
        st.stop()

# Chart-specific controls
if chart_type == "Histogram":
    bins = st.slider("Number of Bins", 5, 100, 30)

if chart_type == "Box Plot":
    show_outliers = st.checkbox("Show potential outliers", value=True)

# Build chart
if chart_type == "Histogram":
    fig = px.histogram(
        chart_df,
        x=x_column,
        nbins=bins,
        title=f"Histogram of {x_column}"
    )

elif chart_type == "Box Plot":
    fig = px.box(
        chart_df,
        y=x_column,
        points="outliers" if show_outliers else False,
        title=f"Box Plot of {x_column}"
    )

elif chart_type == "Scatter Plot":
    fig = px.scatter(
        chart_df,
        x=x_column,
        y=y_column,
        title=f"{y_column} vs {x_column}"
    )

else:
    if y_column:
        fig = px.bar(
            chart_df,
            x=x_column,
            y=y_column,
            title=f"{y_column} by {x_column}"
        )
    else:
        counts = chart_df[x_column].value_counts().reset_index()
        counts.columns = [x_column, "Count"]

        fig = px.bar(
            counts,
            x=x_column,
            y="Count",
            title=f"Frequency of {x_column}"
        )

fig.update_layout(
    template="plotly_white",
    height=550,
    title_x=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": True, "displaylogo": False}
)

# PNG download
try:
    png_data = fig.to_image(format="png", scale=2)

    st.download_button(
        "⬇️ Download Chart as PNG",
        data=png_data,
        file_name="custom_chart.png",
        mime="image/png"
    )

except Exception as error:
    st.warning(
        "PNG export is not ready. Check the Kaleido installation. "
        f"Details: {error}"
    )

