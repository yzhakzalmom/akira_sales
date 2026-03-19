# %% [markdown]
# # Config

# %% [markdown]
# Import libraries and functions

# %%
from services.read_data import read_sheet
from services.save_data import save_sheet
from utils.constants import *
# from utils.helpers import get_year_month_params

# %% [markdown]
# Get year and month parameters

# %%
# year, month =  get_year_month_params()
year, month = ('2026', '01')

# %% [markdown]
# # Sales sheet processing

# %% [markdown]
# Read sales sheet from Data Lake

# %%
# Load sales workbook
sales_wb = read_sheet(ADLS_LAYER_BRONZE, year, month)

# Read sales worksheet
sales_ws = sales_wb.active

# %% [markdown]
# Normalize sheet: delete useless rows, update columns names with their headers to make them unique and  delete headers row

# %%
# Remove initial rows that prevent correct reading
# Delete from bottom to top to avoid index issues
for row_num in SALES_SHEET_ROWS_DELETE_RANGE:
    sales_ws.delete_rows(row_num)

# %%
# Change column names by adding their header
# Find the last column with data in row 2 (was row 1 in 0-indexed)
max_col = sales_ws.max_column

current_header = None

for col in range(1, max_col + 1):

    column_header_value = sales_ws.cell(1, col).value

    if (column_header_value is not None) and (column_header_value != ''):
        current_header = column_header_value

    sales_ws.cell(2, col).value = sales_ws.cell(2, col).value.replace(' ', '_') + f'_{current_header}' 

# %%
# Delete the headers (row 1 in 1-indexed, was row 0 in 0-indexed)
sales_ws.delete_rows(1)

# %% [markdown]
# Save sheet in ADLS

# %%
save_sheet(sales_wb, month, year)


