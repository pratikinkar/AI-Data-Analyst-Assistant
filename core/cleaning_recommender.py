
import pandas as pd


def recommend_cleaning_methods(df, zero_as_missing=None):
    """
    Analyze numerical distributions, skewness and potential outliers.
    Recommend Mean, Median or Mode for columns with missing values.
    """

    analyzed_df = df.copy()
    zero_as_missing = zero_as_missing or []

    # Apply selected zero-as-missing rules before analysis
    for column in zero_as_missing:
        if column in analyzed_df.columns:
            analyzed_df[column] = analyzed_df[column].replace(
                0, float("nan")
            )

    recommendations = {}

    for column in analyzed_df.columns:

        series = analyzed_df[column]
        missing_count = int(series.isnull().sum())

        # Numerical column analysis
        if pd.api.types.is_numeric_dtype(series):

            valid_data = series.dropna()

            if len(valid_data) < 3:
                skewness = None
                skew_type = "Insufficient data"
                outlier_count = 0
                outlier_percentage = 0.0
                method = "median" if missing_count else None
                reason = (
                    "Limited valid observations. Median is a fallback."
                    if missing_count else
                    "Not enough valid observations for reliable analysis."
                )

            else:
                skewness = float(valid_data.skew())

                if skewness > 0.5:
                    skew_type = "Right-skewed"
                elif skewness < -0.5:
                    skew_type = "Left-skewed"
                else:
                    skew_type = "Approximately symmetrical"

                q1 = valid_data.quantile(0.25)
                q3 = valid_data.quantile(0.75)
                iqr = q3 - q1

                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outlier_mask = (
                    (valid_data < lower_bound) |
                    (valid_data > upper_bound)
                )

                outlier_count = int(outlier_mask.sum())
                outlier_percentage = round(
                    outlier_count / len(valid_data) * 100, 2
                )

                # Recommend a method only when missing values exist
                if missing_count:
                    if abs(skewness) > 0.5 or outlier_count > 0:
                        method = "median"
                        reason = (
                            "Skewness or potential outliers detected. "
                            "Median is more robust."
                        )
                    else:
                        method = "mean"
                        reason = (
                            "Distribution is approximately symmetrical "
                            "with no IQR outliers."
                        )
                else:
                    method = None
                    reason = "No missing values. Distribution analyzed only."

            recommendations[column] = {
                "type": "Numerical",
                "missing_values": missing_count,
                "skewness": (
                    round(skewness, 3)
                    if skewness is not None else None
                ),
                "skew_type": skew_type,
                "outliers": outlier_count,
                "outlier_percentage": outlier_percentage,
                "recommended_method": method,
                "reason": reason
            }

        # Categorical column analysis
        else:

            mode_values = series.mode(dropna=True)

            mode_value = (
                mode_values.iloc[0]
                if not mode_values.empty else None
            )

            method = (
                "mode"
                if missing_count > 0 and mode_value is not None
                else None
            )

            recommendations[column] = {
                "type": "Categorical",
                "missing_values": missing_count,
                "mode_value": mode_value,
                "recommended_method": method,
                "reason": (
                    "Most frequent category recommended for missing values."
                    if method else
                    "No missing values or no valid category available."
                )
            }

    return recommendations
