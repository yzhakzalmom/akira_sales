from __future__ import annotations

import os
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from .ADLSClient import ADLSClient
from src.utils.helpers import get_asset_file_path
from src.utils.constants import *

# Create ADLS connection object
adls_client = ADLSClient()

# ===== FROM ST_WEB =====
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

# Get the name of a folder's only file
def get_filename_from_folder(path:str) -> str:

    # # Return the first file name in the folder
    # for file_info in dbutils.fs.ls(path):
    #     return file_info.name
    pass

# Return df bytes by saving in memory without saving in disk
def get_df_bytes(df: pd.DataFrame) -> bytes:

    # Save df to buffer to get df bytes
    buffer = BytesIO()
    # Convert DataFrame to parquet format in memory
    df.to_parquet(buffer, index=False)
    # Get bytes from buffer
    df_bytes = buffer.getvalue()

    # Return the bytes
    return BytesIO(df_bytes)

# Convert openpyxl workbook to BytesIO object
def get_sheet_bytes(wb: openpyxl.workbook.workbook.Workbook) -> bytes:

    # Save sheet to buffer to get sheet bytes
    buffer = BytesIO()
    # Save workbook to buffer
    wb.save(buffer)
    # Get bytes from buffer
    sheet_bytes = buffer.getvalue()
    # After using the workbook, it is necessary to close it
    wb.close()

    # Return BytesIO object with sheet bytes
    return BytesIO(sheet_bytes)

# ===== FROM ST_WEB =====
# Read Excel sheet from ADLS layer and return as openpyxl workbook
def read_sheet(layer: str, year: str, month: str):

    # Construct the file path using layer, year, and month
    path = f'{layer}/{ADLS_CATEGORY_SALES}/{year}/{month}'

    # Read the Excel file from ADLS as bytes
    sheet_bytes = adls_client.read_folder(path)

    # Return the openpyxl workbook
    return load_workbook(sheet_bytes)

# ===== FROM ST_WEB =====
# Read tabular file from ADLS layer and return as DataFrame
def read_tabular(layer: str, category: str, year: str, month: str):

    # Construct the file path using layer, category, year, and month
    print(f'{layer}/{category}/{year}/{month}')
    path = f'{layer}/{category}/{year}/{month}'

    # Read the parquet file from ADLS as bytes
    parquet_bytes = adls_client.read_folder(path)

    # Return the parquet DataFrame
    return pd.read_parquet(parquet_bytes)