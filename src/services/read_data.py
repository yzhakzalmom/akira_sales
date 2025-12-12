from __future__ import annotations

import pandas as pd
from utils.constants import *
from utils.helpers import get_asset_file_path

def get_text(text_file_name: str) -> str:
    
    # Find text path
    text_path = get_asset_file_path(ASSET_TYPE_TEXTS, f'{text_file_name}{TEXT_FILE_EXTENSION}')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

def get_dataframe(df_name: str) -> pd.DataFrame:

    # Find df path
    df_path = get_asset_file_path(ASSET_TYPE_DATAFRAMES, f'{df_name}{CSV_FILE_EXTENSION}')

    # Read and return placeholder csv
    return pd.read_csv(df_path, sep=CSV_SEP)