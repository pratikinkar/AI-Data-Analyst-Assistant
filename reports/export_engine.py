
import pandas as pd
import io


def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def export_excel(df):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Dataset", index=False)

        quality = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        quality.to_excel(
            writer,
            sheet_name="Data Quality",
            index=False
        )

        numeric = df.describe().T.reset_index()
        numeric.rename(columns={"index": "Column"}, inplace=True)
        numeric.to_excel(
            writer,
            sheet_name="Statistics",
            index=False
        )

    return output.getvalue()

