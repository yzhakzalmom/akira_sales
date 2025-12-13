import pandas as pd

# Troca ponto por vírgula nas colunas float64 em um dataframe
def replace_decimal_character(df: pd.DataFrame) -> pd.DataFrame:

    # Para cada coluna
    for column in df.columns:

        # Caso a coluna seja float64
        if df[column].dtype == 'float64':

            # Realiza o replace
            df[column] = df[column].fillna(0).astype(str).str.replace('.', ',', regex=False)

    return df