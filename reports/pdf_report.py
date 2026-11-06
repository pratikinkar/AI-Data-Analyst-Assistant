
import io
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Image, KeepTogether
)


def generate_pdf_report(df, dataset_name="Analytics Report"):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=25,
        textColor=colors.HexColor("#243B64"),
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#243B64"),
        spaceBefore=12,
        spaceAfter=10
    )

    elements = []

    # 1. Cover page
    elements.append(Spacer(1, 65))
    elements.append(Paragraph("AI DATA ANALYST", title_style))
    elements.append(
        Paragraph("EXECUTIVE ANALYTICS REPORT", title_style)
    )
    elements.append(Spacer(1, 25))

    elements.append(Paragraph(
        f"<b>Dataset:</b> {dataset_name}",
        styles["Heading2"]
    ))
    elements.append(Paragraph(
        f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 25))
    elements.append(Paragraph(
        "A structured report covering dataset quality, "
        "statistical analysis, visual patterns and key findings.",
        styles["BodyText"]
    ))

    elements.append(PageBreak())

    # 2. Executive summary
    elements.append(Paragraph("1. Executive Summary", heading_style))

    numeric_df = df.select_dtypes(include="number")
    categorical_df = df.select_dtypes(exclude="number")

    summary_data = [
        ["Metric", "Result"],
        ["Total Records", f"{len(df):,}"],
        ["Total Columns", f"{len(df.columns):,}"],
        ["Numerical Columns", str(len(numeric_df.columns))],
        ["Categorical Columns", str(len(categorical_df.columns))],
        ["Missing Values", f"{df.isnull().sum().sum():,}"],
        ["Duplicate Rows", f"{df.duplicated().sum():,}"],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[230, 250]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    elements.append(summary_table)

    # 3. Data quality
    elements.append(Paragraph("2. Data Quality Analysis", heading_style))

    quality_data = [
        ["Column", "Data Type", "Missing", "Missing %", "Unique"]
    ]

    for col in df.columns:
        missing = int(df[col].isnull().sum())
        missing_pct = (missing / len(df) * 100) if len(df) else 0

        quality_data.append([
            str(col)[:30],
            str(df[col].dtype),
            str(missing),
            f"{missing_pct:.2f}%",
            str(df[col].nunique())
        ])

    quality_table = Table(
        quality_data,
        repeatRows=1,
        colWidths=[180, 100, 75, 85, 75]
    )

    quality_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(quality_table)

    # 4. Statistical analysis
    elements.append(PageBreak())
    elements.append(Paragraph("3. Statistical Analysis", heading_style))

    if not numeric_df.empty:
        stats = numeric_df.describe().T.round(2).reset_index()
        stats.rename(columns={"index": "Column"}, inplace=True)

        stats_data = [[str(c) for c in stats.columns]]
        stats_data += stats.astype(str).values.tolist()

        stats_table = Table(stats_data, repeatRows=1)

        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))

        elements.append(stats_table)
    else:
        elements.append(Paragraph(
            "No numerical columns are available.",
            styles["Normal"]
        ))

    # 5. Visual analytics
    elements.append(PageBreak())
    elements.append(Paragraph("4. Visual Analytics", heading_style))

    chart_columns = list(numeric_df.columns[:4])

    for col in chart_columns:
        values = numeric_df[col].dropna()

        if values.empty:
            continue

        fig, ax = plt.subplots(figsize=(7, 2.8))
        ax.hist(values, bins=25)
        ax.set_title(f"Distribution of {col}")
        ax.set_xlabel(str(col))
        ax.set_ylabel("Frequency")
        fig.tight_layout()

        chart_buffer = io.BytesIO()
        fig.savefig(chart_buffer, format="png", dpi=130)
        plt.close(fig)
        chart_buffer.seek(0)

        elements.append(KeepTogether([
            Paragraph(
                f"Distribution Analysis: {col}",
                styles["Heading3"]
            ),
            Image(chart_buffer, width=6.5*inch, height=2.6*inch),
            Spacer(1, 10)
        ]))

    # 6. Key findings
    elements.append(PageBreak())
    elements.append(Paragraph("5. Key Findings", heading_style))

    findings = [
        f"The dataset contains {len(df):,} records and {len(df.columns)} columns.",
        f"A total of {df.isnull().sum().sum():,} missing values were identified.",
        f"The dataset contains {df.duplicated().sum():,} duplicate rows."
    ]

    if not numeric_df.empty:
        for col in numeric_df.columns[:5]:
            findings.append(
                f"The average value of {col} is "
                f"{numeric_df[col].mean():,.2f}."
            )

    for finding in findings:
        elements.append(Paragraph(
            f"• {finding}",
            styles["BodyText"]
        ))
        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "<b>Note:</b> These findings are descriptive statistics. "
        "They do not establish causation or guarantee business outcomes.",
        styles["Italic"]
    ))

    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()
