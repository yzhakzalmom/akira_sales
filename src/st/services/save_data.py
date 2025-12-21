from __future__ import annotations
from .check_data import check_data_folder_exists
from .ADLSClient import ADLSClient
from io import BytesIO
from utils.constants import *
import pandas as pd
import openpyxl

# ========================
# GENERAL
# ========================

# Create ADLS connection object
adls_client = ADLSClient()

# Generate message to be return when a file is saved
def generate_save_return_message(folder_path: str, month: str, year: str, save_type: str) -> str:
    # Create file already exist message
    file_exists_message = MSG_FILE_EXISTS_TEMPLATE.format(save_type=save_type, month=month, year=year)

    # Create return message
    return_message = 'Upload bem sucedido!'

    # Update return message if file already exists
    return_message = (file_exists_message + return_message) if check_data_folder_exists(folder_path) else return_message

    # Return the final message
    return return_message

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

# ========================
# TO BRONZE
# ========================

# Save user's uploaded sheet
def save_uploaded_sheet(sales_sheet, month: str, year: str) -> str:

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_SALES}/{year}/{month}/{RAW_FILE_PREFIX}{SALES_FILE_PREFIX}{year}_{month}{BRONZE_SALES_FILE_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_VENDAS)

    # Get excel sheet bytes
    excel_bytes = sales_sheet.getvalue()

    # Save excel in ADLS
    adls_client.upload(file_path, excel_bytes)

    # Return the save message
    return message

# Save user's uploaded DataFrame to Bronze layer
def save_uploaded_df(df: pd.DataFrame, cost_type:str, month: str, year: str) -> str:

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{cost_type}/{year}/{month}/{RAW_FILE_PREFIX}{COSTS_FILE_PREFIX}{year}_{month}{TABULAR_STD_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_CUSTOS)

    # Get df bytes
    df_bytes = get_df_bytes(df)

    # Save dataframe in ADLS
    adls_client.upload(file_path, df_bytes)
    
    # Return the save message
    return message

# ========================
# TO LAYERS
# ========================

# Save sheet in ADLS as parquet
# Excel bytes -> DataFrame -> Parquet bytes -> ADLS
def save_sheet(wb: openpyxl.workbook.workbook.Workbook, month: str, year: str):

    # Create path
    path = f'{ADLS_LAYER_SILVER}/{ADLS_CATEGORY_SALES}/{year}/{month}/{TREATED_FILE_PREFIX}{SALES_FILE_PREFIX}{year}_{month}{TABULAR_STD_EXTENSION}'

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
def save_df(df: pd.DataFrame, layer: str, category: str, year: str, month: str):

    path = f'{layer}/{category}/{year}/{month}/{category}_{year}_{month}{TABULAR_STD_EXTENSION}'

    # Get df parquet bytes
    parquet_bytes = get_df_bytes(df)

    # Upload parquet bytes to adls
    adls_client.upload(path, parquet_bytes)  