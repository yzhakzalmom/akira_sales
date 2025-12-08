def get_sales_uploader_text() -> str:
    from utils.helpers import get_asset_file_path, get_months
    # Find text path
    text_path = get_asset_file_path('texts', 'sales_uploader.md')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

def save_sales_sheet(sales_sheet, file_month = None, file_year = None) -> None:
    from utils.helpers import get_data_path
    import streamlit as st

    # Create new file in data folder
    with open(get_data_path() / 'test.xlsx', 'wb') as f:

        # Write the file with the sales sheet content
        f.write(sales_sheet.getbuffer())