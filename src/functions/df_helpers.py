from __future__ import annotations

# Change '.' for ',' in float columns
def replace_decimal_character(df: pyspark.pandas.DataFrame) -> pyspark.pandas.DataFrame:

    # For each column
    for column in df.columns:

        # If column type is float64
        if df[column].dtype == 'float64':

            # Replace '.' for ','
            df[column] = df[column].fillna(0).astype(str).str.replace('.', ',', regex=False)

    return df