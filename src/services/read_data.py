from __future__ import annotations

def get_text(text_file_name: str) -> str:
    from utils.helpers import get_asset_file_path

    # Find text path
    text_path = get_asset_file_path('texts', f'{text_file_name}.md')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

def get_dataframe(df_name: str) -> pd.DataFrame:
    import pandas as pd
    from utils.helpers import get_asset_file_path

    # Find df path
    df_path = get_asset_file_path('dataframes', f'{df_name}.csv')

    # Read and return placeholder csv
    return pd.read_csv(df_path, sep=';')