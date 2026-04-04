from __future__ import annotations

import os
import pandas as pd
from utils.constants import *
from utils.helpers import generate_save_return_message
from services.read_data import get_df_bytes, get_sheet_bytes
from .ADLSClient import ADLSClient

# Create ADLS connection object
adls_client = ADLSClient()

# Get env variable
ADLS_CONTAINER = os.getenv('ADLS_CONTAINER')

# ========================
# TO BRONZE
# ========================

# Save user's uploaded sheet
def save_uploaded_sheet(sales_sheet, month: str, year: str) -> str:

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_SALES}/{year}/{month}/{RAW_FILE_PREFIX}_{SALES_FILE_PREFIX}_{year}_{month}{BRONZE_SALES_FILE_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_VENDAS)

    # Get excel sheet bytes
    excel_bytes = sales_sheet.getvalue()

    # Save excel in ADLS
    adls_client.upload(file_path, excel_bytes)

    # Return the save message
    return message

# Save user's uploaded DataFrame to Bronze layer
# def save_uploaded_df(df: pd.DataFrame, cost_type:str, month: str, year: str) -> str:

#     # Create file subpath
#     file_path = f'{ADLS_LAYER_BRONZE}/{cost_type}/{year}/{month}/{RAW_FILE_PREFIX}{COSTS_FILE_PREFIX}{year}_{month}{TABULAR_STD_EXTENSION}'

#     # Create return message
#     message = generate_save_return_message(file_path, month, year, SAVE_TYPE_CUSTOS)

#     # Get df bytes
#     df_bytes = get_df_bytes(df)

#     # Save dataframe in ADLS
#     adls_client.upload(file_path, df_bytes)
    
#     # Return the save message
#     return message

# ========================
# TO LAYERS
# ========================

# Save sheet in ADLS as parquet
# Excel bytes -> DataFrame -> Parquet bytes -> ADLS
def save_sheet(wb: openpyxl.workbook.workbook.Workbook, month: str, year: str):

    # Create path
    path = f'{ADLS_LAYER_SILVER}/{ADLS_CATEGORY_SALES}/{year}/{month}/{TREATED_FILE_PREFIX}_{SALES_FILE_PREFIX}_{year}_{month}{TABULAR_STD_EXTENSION}'

    # Get sheet bytes
    sheet_bytes = get_sheet_bytes(wb)

    # Read sheet as df
    sheet_df = pd.read_excel(sheet_bytes)

    # Get df parquet bytes
    parquet_bytes = get_df_bytes(sheet_df)

    # Upload parquet bytes to adls
    adls_client.upload(path, parquet_bytes)

# Save df in ADLS as parquet
# DataFrame -> Parquet bytes -> ADLS
# save_uploaded_df(df: pd.DataFrame, cost_type:str, month: str, year: str)
def save_df(df: pd.DataFrame, layer: str, category: str, year: str, month: str, file_prefix: str = None):
    
    # Define file prefix if None
    file_prefix = category if not file_prefix else file_prefix

    # Define path according to the month parameter
    path_month = f'{layer}/{category}/{year}/{month}/{file_prefix}_{year}_{month}{TABULAR_STD_EXTENSION}'
    path_monthless = f'{layer}/{category}/{year}/{file_prefix}_{year}{TABULAR_STD_EXTENSION}'
    path = path_monthless if not month else path_month

    # Get df parquet bytes
    parquet_bytes = get_df_bytes(df)

    # Generate message concerning the upload
    message = generate_save_return_message(path, month, year, category.replace('_', ' ').title())

    # Upload parquet bytes to adls
    adls_client.upload(path, parquet_bytes)

    return message