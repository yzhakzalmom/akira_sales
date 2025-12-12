from __future__ import annotations

from .check_data import check_data_folder_exists
from utils.constants import *
from .ADLSClient import ADLSClient
from io import BytesIO

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
def df_buffer_save(df: pd.DataFrame):

    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    df_bytes = buffer.getvalue()

    return df_bytes

def save_sales_sheet(sales_sheet, month: str, year: str):

    # Create ADLS connection object
    adls_client = ADLSClient()

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_SALES}/{year}/{month}/sales_{year}_{month}{SALES_FILE_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_VENDAS)

    # Get excel sheet bytes
    excel_bytes = sales_sheet.getvalue()

    # Save excel in ADLS
    adls_client.upload(file_path, excel_bytes)

    return message

def save_costs_df(costs_df: pd.DataFrame, cost_type:str, month: str, year: str):

    # Create ADLS connection object
    adls_client = ADLSClient()

    # Create file subpath
    file_path = f'{ADLS_LAYER_BRONZE}/{cost_type}/{year}/{month}/{COSTS_FILE_PREFIX}{year}_{month}{COSTS_FILE_EXTENSION}'

    # Create return message
    message = generate_save_return_message(file_path, month, year, SAVE_TYPE_CUSTOS)

    # Get costs_df bytes
    costs_df_bytes = df_buffer_save(costs_df)

    # Save dataframe in ADLS
    adls_client.upload(file_path, costs_df_bytes)
    
    return message