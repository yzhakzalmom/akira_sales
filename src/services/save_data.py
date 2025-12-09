from __future__ import annotations

def save_sales_sheet(sales_sheet, month: str, year: str):
    from utils.helpers import get_data_path, generate_save_return_message

    # Create file subpath
    file_subpath = f'bronze/sales/sales_{year}_{month}.xlsx'

    # Create file path
    file_path = get_data_path() / file_subpath

    # Create return message
    message = generate_save_return_message(file_subpath, month, year, 'vendas')

    # Create new file in data folder
    with open(file_path, 'wb') as f:

        # Write the file with the sales sheet content
        f.write(sales_sheet.getbuffer())

    return message

def save_costs_df(costs_df: pd.DataFrame, cost_type:str, month: str, year: str):
    from utils.helpers import get_data_path, generate_save_return_message

    # Create file subpath
    file_subpath = f'bronze/costs/{cost_type}/costs_{year}_{month}.csv'

    # Create file path
    file_path = get_data_path() / file_subpath

    # Create return message
    message = generate_save_return_message(file_subpath, month, year, 'custos')

    # Save dataframe and return message
    costs_df.to_csv(file_path, index=False)
    
    return message