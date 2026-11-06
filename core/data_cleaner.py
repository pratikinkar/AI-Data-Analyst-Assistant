
import pandas as pd


def clean_data(
    df,
    zero_as_missing=None,
    fill_method="median",
    column_methods=None
):
    """
    Clean a copy of the dataset using selected methods per column.
    The original DataFrame remains unchanged.
    """

    cleaned_df = df.copy()

    zero_as_missing = zero_as_missing or []
    column_methods = column_methods or {}

    # Step 1: Treat selected zero values as missing
    for column in zero_as_missing:
        if column in cleaned_df.columns:
            cleaned_df[column] = cleaned_df[column].replace(0, float("nan"))

    # Step 2: Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Step 3: Fill missing values column by column
    for column in cleaned_df.columns:

        if not cleaned_df[column].isnull().any():
            continue

        method = column_methods.get(column)

        # Numerical columns
        if pd.api.types.is_numeric_dtype(cleaned_df[column]):

            if method is None:
                method = fill_method

            if method == "mean":
                fill_value = cleaned_df[column].mean()

            elif method == "median":
                fill_value = cleaned_df[column].median()

            else:
                continue

            if pd.notna(fill_value):
                cleaned_df[column] = cleaned_df[column].fillna(fill_value)

        # Categorical columns
        else:
            if method is None:
                method = "mode"

            if method == "mode":
                mode_values = cleaned_df[column].mode(dropna=True)

                if not mode_values.empty:
                    cleaned_df[column] = cleaned_df[column].fillna(
                        mode_values.iloc[0]
                    )

    return cleaned_df
