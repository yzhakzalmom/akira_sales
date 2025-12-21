from __future__ import annotations
from io import BytesIO
from databricks.sdk.runtime import dbutils
from utils.constants import *
from dbc.utils.helpers import clear_tmp_folder
import pyspark.pandas as ps

# ========================
# GENERAL
# ========================

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
# TO LAYERS
# ========================

# Save sheet in ADLS as parquet
# Excel bytes -> DataFrame -> Parquet bytes -> ADLS
def save_sheet(wb, year: str, month: str):

    # Create path
    path = f'{ADLS_CONTAINER}{ADLS_LAYER_SILVER}/{ADLS_CATEGORY_SALES}/{year}/{month}'

    # Get sheet bytes
    sheet_bytes = get_sheet_bytes(wb)

    # Read sheet as df
    sheet_df = ps.read_excel(sheet_bytes)

    # Save df
    sheet_df.to_parquet(path, index=False)

    # Clear tmp folder after used
    clear_tmp_folder()

# Save df in ADLS as parquet
# DataFrame -> Parquet bytes -> ADLS
def save_df(df: ps.DataFrame, layer: str, category: str, year: str, month: str):

    path = f'{ADLS_CONTAINER}{layer}/{category}/{year}/{month}'

    # Save in ADLS
    df.to_parquet(path, index=False)