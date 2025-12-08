def save_sales_sheet(sales_sheet, file_month: str, file_year: str) -> None:
    from utils.helpers import get_data_path

    # Create file name
    file_name = f'sales_{file_year}_{file_month}.xlsx'

    # Create new file in data folder
    with open(get_data_path() / file_name, 'wb') as f:

        # Write the file with the sales sheet content
        f.write(sales_sheet.getbuffer())