from __future__ import annotations

from .check_data import check_data_folder_exists
from utils.constants import *
from .ADLSClient import ADLSClient
from io import BytesIO

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

    return return_message

# Return df bytes by saving in memory without saving in disk
def get_df_bytes(df: pd.DataFrame) -> bytes:

    # Save df to buffer to get df bytes
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    df_bytes = buffer.getvalue()

    return df_bytes

def get_sheet_bytes(wb: openpyxl.workbook.workbook.Workbook) -> bytes:

    # Save sheet to buffer to get sheet bytes
    buffer = BytesIO()
    wb.save(buffer)
    sheet_bytes = buffer.getvalue()
    wb.close() # after using the workbook, it is necessaty to close it

    return sheet_bytes

# ========================
# BRONZE
# ========================

# Save user's uploaded sheet
def save_uploaded_sheet(sales_sheet, month: str, year: str) -> str:

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_SALES}/{year}/{month}/{RAW_FILE_PREFIX}{SALES_FILE_PREFIX}{year}_{month}{SALES_FILE_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_VENDAS)

    # Get excel sheet bytes
    excel_bytes = sales_sheet.getvalue()

    # Save excel in ADLS
    adls_client.upload(file_path, excel_bytes)

    return message

def save_uploaded_df(df: pd.DataFrame, cost_type:str, month: str, year: str) -> str:

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{cost_type}/{year}/{month}/{RAW_FILE_PREFIX}{COSTS_FILE_PREFIX}{year}_{month}{COSTS_FILE_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_CUSTOS)

    # Get df bytes
    df_bytes = get_df_bytes(df)

    # Save dataframe in ADLS
    adls_client.upload(file_path, df_bytes)
    
    return message

# ========================
# SILVER
# ========================

def save_sheet(wb: openpyxl.workbook.workbook.Workbook, month: str, year: str):

    # Create path
    path = f'{ADLS_LAYER_SILVER}/{ADLS_CATEGORY_SALES}/{year}/{month}/{TREATED_FILE_PREFIX}{SALES_FILE_PREFIX}{year}_{month}{SALES_FILE_EXTENSION}'

    # Get sheet bytes
    sheet_bytes = get_sheet_bytes(wb)

    # Upload file to adls
    adls_client.upload(path, sheet_bytes)