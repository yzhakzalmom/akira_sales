from __future__ import annotations

import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from services.ADLSClient import ADLSClient
from utils.constants import *
from utils.helpers import get_asset_file_path

# Create ADLS connection object
adls_client = ADLSClient()

# =======================
# ASSETS
# =======================

def get_asset_text(text_file_name: str) -> str:
    
    # Find text path
    text_path = get_asset_file_path(ASSET_TYPE_TEXTS, f'{text_file_name}{TEXT_FILE_EXTENSION}')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

def get_asset_dataframe(df_name: str) -> pd.DataFrame:

    # Find df path
    df_path = get_asset_file_path(ASSET_TYPE_DATAFRAMES, f'{df_name}{CSV_FILE_EXTENSION}')

    # Read and return placeholder csv
    return pd.read_csv(df_path, sep=CSV_SEP)

# =======================
# LAYERS
# =======================

def read_sheet(layer: str, year: str, month: str):

    # Construct the file path using layer, year, and month
    path = f'{layer}/{ADLS_CATEGORY_SALES}/{year}/{month}'

    # Read the Excel file from ADLS as bytes
    sheet_bytes = BytesIO(adls_client.read_folder(path))

    # Return the Excel bytes
    return load_workbook(sheet_bytes)