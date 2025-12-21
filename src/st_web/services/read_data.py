from __future__ import annotations

import pandas as pd
from openpyxl import load_workbook
from .ADLSClient import ADLSClient
from utils.constants import *
from st_web.utils.helpers import get_asset_file_path

# Create ADLS connection object
adls_client = ADLSClient()

# =======================
# FROM ASSETS
# =======================

# Read text file from assets folder
def get_asset_text(text_file_name: str) -> str:
    
    # Find text path
    text_path = get_asset_file_path(ASSET_TYPE_TEXTS, f'{text_file_name}{TEXT_FILE_EXTENSION}')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        # Read file content into text variable
        text = f.read()

    # Return the text content
    return text

# Read CSV file from assets folder and return as DataFrame
def get_asset_dataframe(df_name: str) -> pd.DataFrame:

    # Find df path
    df_path = get_asset_file_path(ASSET_TYPE_DATAFRAMES, f'{df_name}{CSV_FILE_EXTENSION}')

    # Read and return placeholder csv
    return pd.read_csv(df_path, sep=CSV_SEP)

# =======================
# FROM LAYERS
# =======================

# Read Excel sheet from ADLS layer and return as openpyxl workbook
def read_sheet(layer: str, year: str, month: str):

    # Construct the file path using layer, year, and month
    path = f'{layer}/{ADLS_CATEGORY_SALES}/{year}/{month}'

    # Read the Excel file from ADLS as bytes
    sheet_bytes = adls_client.read_folder(path)

    # Return the openpyxl workbook
    return load_workbook(sheet_bytes)


# Read tabular file from ADLS layer and return as DataFrame
def read_tabular(layer: str, category: str, year: str, month: str):

    # Construct the file path using layer, category, year, and month
    path = f'{layer}/{category}/{year}/{month}'

    # Read the parquet file from ADLS as bytes
    parquet_bytes = adls_client.read_folder(path)

    # Return the parquet DataFrame
    return pd.read_parquet(parquet_bytes)