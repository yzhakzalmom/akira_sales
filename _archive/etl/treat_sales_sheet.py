from services.read_data import read_sheet
from services.save_data import save_sheet
from utils.constants import *

# Load sales workbook
sales_wb = read_sheet(ADLS_LAYER_BRONZE, year, month)

# Read sales worksheet
sales_ws = sales_wb.active

# Remove initial rows that prevent correct reading
# Delete from bottom to top to avoid index issues
for row_num in SALES_SHEET_ROWS_DELETE_RANGE:
    sales_ws.delete_rows(row_num)

# Change column names by adding their header
# Find the last column with data in row 2 (was row 1 in 0-indexed)
max_col = sales_ws.max_column

current_header = None

for col in range(1, max_col + 1):

    column_header_value = sales_ws.cell(1, col).value

    if (column_header_value is not None) and (column_header_value != ''):
        current_header = column_header_value

    sales_ws.cell(2, col).value = sales_ws.cell(2, col).value.replace(' ', '_') + f'_{current_header}' 

# Delete the headers (row 1 in 1-indexed, was row 0 in 0-indexed)
sales_ws.delete_rows(1)

# Save sheet in ADLS
save_sheet(sales_wb, month, year)