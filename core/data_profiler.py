
import pandas as pd


def generate_profile(df):
    """Generate basic data quality and statistical profile."""

    profile = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum()),
        "columns": {}
    }

    for column in df.columns:
        col = df[column]

        profile["columns"][column] = {
            "data_type": str(col.dtype),
            "missing_values": int(col.isnull().sum()),
            "unique_values": int(col.nunique()),
            "missing_percentage": round(
                col.isnull().mean() * 100, 2
            )
        }

        if pd.api.types.is_numeric_dtype(col):
            profile["columns"][column]["statistics"] = {
                "mean": round(float(col.mean()), 2) if col.notna().any() else None,
                "median": round(float(col.median()), 2) if col.notna().any() else None,
                "minimum": float(col.min()) if col.notna().any() else None,
                "maximum": float(col.max()) if col.notna().any() else None
            }

    return profile
