def save_sales_sheet(sales_sheet, file_month = None, file_year = None) -> None:
    from utils.helpers import get_data_path
    import streamlit as st

    # Create new file in data folder
    with open(get_data_path() / 'test.xlsx', 'wb') as f:

        # Write the file with the sales sheet content
        f.write(sales_sheet.getbuffer())