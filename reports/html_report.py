
import plotly.express as px


def generate_html_report(df, dataset_name="Analytics Report"):
    numeric_df = df.select_dtypes(include="number")

    charts = ""

    if not numeric_df.empty:
        column = numeric_df.columns[0]

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}",
            template="plotly_white"
        )

        charts = fig.to_html(
            full_html=False,
            include_plotlyjs="cdn"
        )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Data Analyst Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f5f7fb;
                color: #24324a;
            }}
            .card {{
                background: white;
                padding: 22px;
                margin-bottom: 20px;
                border-radius: 10px;
            }}
            h1 {{ color: #243B64; }}
        </style>
    </head>
    <body>
        <h1>AI Data Analyst - Analytics Report</h1>

        <div class="card">
            <h2>Dataset Overview</h2>
            <p>Dataset: {dataset_name}</p>
            <p>Total Records: {len(df):,}</p>
            <p>Total Columns: {len(df.columns):,}</p>
            <p>Missing Values: {df.isnull().sum().sum():,}</p>
            <p>Duplicate Rows: {df.duplicated().sum():,}</p>
        </div>

        <div class="card">
            <h2>Column Information</h2>
            {df.dtypes.astype(str).to_frame("Data Type").to_html()}
        </div>

        <div class="card">
            <h2>Data Visualization</h2>
            {charts}
        </div>
    </body>
    </html>
    """

    return html.encode("utf-8")
