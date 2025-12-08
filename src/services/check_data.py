# Checks if the sales sheet pattern is correct and return sheet preview
def check_sales_sheet_format(container, sales_sheet) -> None:
    import pandas as pd

    # Read sales sheet into a dataframe
    sales_df = pd.read_excel(sales_sheet)

    # Variable to hold headers index. It will be incresed below
    headers_idx = 0

    # Loop over the rows to find headers row
    for idx, row in sales_df.iterrows():

        # Search for 'Vendas', sheet's first header
        if row[sales_df.columns[0]] == 'Vendas':
            # Update header index with headers row index
            headers_idx += idx + 1
            break

    # If this header was not found, the file has a wrong pattern
    if headers_idx == 0:
        raise Exception('Arquivo não está no formato padrão da planilha de vendas')

    # Create current columns list based on the headers
    current_columns = sales_df.iloc[headers_idx].tolist()

    # Create new columns list
    new_columns = [f'{i+1}_{current_columns[i]}' for i in range(len(current_columns))]

    # Update column names
    sales_df.columns = new_columns

    # Create preview dataframe that will be rendered
    preview_df = sales_df.iloc[5:15]

    return preview_df