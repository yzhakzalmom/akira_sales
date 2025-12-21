from databricks.sdk.runtime import dbutils
from utils.constants import *
import os

DBFS_TMP_PATH = os.getenv('DBFS_TMP_PATH')

# Get year and month parameters passed to a notebook
def get_year_month_params():

    year = dbutils.widgets.get("year")
    month = dbutils.widgets.get("month")

    return year, month

# Get the name of a folder's only file
def get_filename_from_folder(path:str) -> str:

    # Return the first file name in the folder
    for file_info in dbutils.fs.ls(path):
        return file_info.name
    
# Clear tmp folder after used
def clear_tmp_folder():
    
    for file_info in dbutils.fs.ls(DBFS_TMP_PATH):
        dbutils.fs.rm(file_info.path)

    dbutils.fs.rm(DBFS_TMP_PATH)