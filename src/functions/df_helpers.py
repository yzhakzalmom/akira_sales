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


# Une os dataframes de vendas em bronze/vendas
def sales_union():
    from pathlib import Path

    # Define diretório de vendas
    diretorio_vendas = '../data/silver/separate_sales'

    # Define uma variável que armazenará o dataframe final
    vendas_df = None

    # Itera pelos arquivos do diretório de vendas como objetos
    for item in Path(diretorio_vendas).iterdir():

        # Garante que o item seja um arquivo
        if item.is_file():

            # Lê o arquivo como DataFrame
            df = pd.read_excel(item)

            # Une o dataframe com o dataframe final
            vendas_df = pd.concat([vendas_df, df])

    # Salva o dataframe final como CSV
    vendas_df.to_csv('../data/silver/union_sales/sales.csv', index=False)