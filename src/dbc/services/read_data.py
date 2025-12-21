from __future__ import annotations

import pyspark.pandas as ps
from io import BytesIO
from databricks.sdk.runtime import dbutils
from utils.constants import *
from dbc.utils.helpers import get_filename_from_folder

# =======================
# FROM LAYERS
# =======================

# Get the name of a folder's only file
def get_filename_from_folder(path:str) -> str:

    # Return the first file name in the folder
    for file_info in dbutils.fs.ls(path):
        return file_info.name


# Read Excel sheet from ADLS layer and return as openpyxl workbook
def read_sheet(layer: str, year: str, month: str):
    from openpyxl import load_workbook
    
    # Construct the file path using layer, year, and month
    path = f'{ADLS_CONTAINER}{layer}/{ADLS_CATEGORY_SALES}/{year}/{month}'

    # Get desired sheet's name
    file_name = get_filename_from_folder(path)

    # Copy sheet to tmp folder
    dbutils.fs.cp(
        f'{path}/{file_name}',
        DBFS_TMP_PATH
    )

    tmp_sheet_path = f'../tmp/{file_name}'

    # Return the openpyxl workbook
    return load_workbook(tmp_sheet_path)


# Read tabular file from ADLS layer and return as DataFrame
def read_tabular(layer: str, category: str, year: str, month: str) -> ps.DataFrame:

    # Construct the file path using layer, category, year, and monthy
    path = f'{ADLS_CONTAINER}{layer}/{category}/{year}/{month}'

    # Return the parquet DataFrame
    return ps.read_parquet(path)