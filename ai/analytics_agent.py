
import pandas as pd
from ai.llm_client import generate_ai_response


def get_dataset_summary(df):
    """Generate factual dataset statistics using Pandas."""

    numeric_df = df.select_dtypes(include="number")

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_summary": (
            numeric_df.describe().round(2).to_dict()
            if not numeric_df.empty else {}
        )
    }

    return summary


def answer_dataset_question(df, question):
    """Answer questions using actual dataset calculations."""

    if df is None or df.empty:
        return "Please upload a dataset first."

    summary = get_dataset_summary(df)

    context = f"""
    DATASET INFORMATION:
    Rows: {summary['rows']}
    Columns: {summary['columns']}
    Column names: {summary['column_names']}
    Missing values: {summary['missing_values']}
    Duplicate rows: {summary['duplicate_rows']}

    NUMERICAL STATISTICS:
    {summary['numeric_summary']}
    """

    messages = [
        {
            "role": "system",
            "content": """
            You are an expert Data Analyst AI Assistant.

            Answer questions using only the supplied dataset information.
            Never invent statistics or values.
            If the information is unavailable, clearly say so.
            Explain results in simple professional English.
            Give useful analytical insights when relevant.
            """
        },
        {
            "role": "user",
            "content": f"""
            {context}

            USER QUESTION:
            {question}

            Analyze the available information and answer accurately.
            """
        }
    ]

    try:
        return generate_ai_response(messages)
    except Exception as error:
        return f"AI Assistant Error: {str(error)}"
