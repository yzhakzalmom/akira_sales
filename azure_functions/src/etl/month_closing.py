from src.functions.df_helpers import replace_decimal_character
from src.services.read_data import read_tabular, read_sheet
from src.services.save_data import save_df, save_sheet
from src.services.treat_data import identify_sale_products
from src.utils.helpers import get_months
from src.utils.constants import *
from unidecode import unidecode
import pandas as pd

def treat_sales_sheet(year:str, month: str):

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

def clean_sales(year:str, month:str):

    # Read excel and transform to DataFrame
    sales_df = read_tabular(ADLS_LAYER_SILVER, ADLS_CATEGORY_SALES, year, month)

    # Create tuple of required column suffixes
    required_suffixes = tuple(SALES_SHEET_REQUIRED_SUFFIXES)

    # Define list of dataframe columns and remove 'Reclamação_encerrada_Reclamações' from the list as it is an exception to the defined rule and will be needed
    df_columns = list(sales_df.columns)
    df_columns.remove('Reclamação_encerrada_Reclamações')

    # Remove unnecessary columns by suffix
    for col in df_columns:
        if not col.endswith(required_suffixes):
            sales_df = sales_df.drop(col, axis=1)

    # Drop more unnecessary columns
    columns_to_drop = ['Descrição_do_status_Vendas', 'Pacote_de_diversos_produtos_Vendas', 'Pertence_a_um_kit_Vendas', 'SKU_Anúncios', '#_de_anúncio_Anúncios', 'Canal_de_venda_Anúncios', 'Receita_por_acréscimo_no_preço_(pago_pelo_comprador)_Vendas', 'Taxa_de_parcelamento_equivalente_ao_acréscimo_Vendas', 'Depósito_Vendas', 'Custo_de_envio_com_base_nas_medidas_e_peso_declarados_Vendas', 'Descontos_e_bônus_Vendas']
    sales_df = sales_df.drop(columns_to_drop, axis=1)

    # Rename columns
    new_names = ['id_venda', 'data_venda', 'status_venda', 'unidades_vendidas', 'receita_por_produto', 'tarifas_impostos_venda', 'receita_envio', 'tarifa_envio', 'custo_envio', 'diff_custo_envio', 'cancelamentos_reembolsos', 'total_vendas', 'mes_faturamento_tarifas', 'venda_publicidade', 'titulo_anuncio', 'variacao_anuncio', 'preco_unitario_anuncio', 'tipo_anuncio', 'reclamacao_encerrada']
    sales_df.columns = new_names

    # Fill na in column total_vendas and cancelamentos_reembolsos
    sales_df['total_vendas'] = sales_df['total_vendas'].fillna(0)
    sales_df['cancelamentos_reembolsos'] = sales_df['cancelamentos_reembolsos'].fillna(0)

    # Create auxiliary list that will create count_produto column
    count_product = []

    # For each row in the df, check if there is a condition that should nullify the product count
    # As all rows are necessary for analysis, create a 'count_produto' column and mark with False in these cases
    for row in sales_df.itertuples():

        # Create conditions to the filter below
        is_canceled = (row.cancelamentos_reembolsos != 0 or ('cancel' in row.status_venda.lower()))
        is_devolution = (('devol' in row.status_venda.lower()) and row.total_vendas == 0)
        is_multiple_products = ('pacote de' in row.status_venda.lower())

        # Tag each row as True or False for product count
        if is_canceled or is_devolution or is_multiple_products:
            count_product.append(False)
        else:
            count_product.append(True)

    # Create count_produto column
    sales_df['count_produto'] = count_product

    # Convert id from int to string
    sales_df['id_venda'] = sales_df['id_venda'].astype(str)

    # Remove time from date column
    sales_df['data_venda'] = sales_df['data_venda'].str.slice(0, -9)

    # Change column types to int
    sales_df[['unidades_vendidas', 'reclamacao_encerrada']] = sales_df[['unidades_vendidas', 'reclamacao_encerrada']].fillna(0).astype(int)

    # Replace period with comma in decimal columns
    sales_df = replace_decimal_character(sales_df)

    # Remove empty spaces from ad variation column and the keys 'color' and 'size'
    sales_df['variacao_anuncio'] = sales_df['variacao_anuncio'] \
                                        .str.replace(' ', '', regex=False) \
                                        .str.replace('Cor:', '', regex=False) \
                                        .str.replace('Tamanho:', '', regex=False)

    # Create kimono color and kimono size columns from ad variation column
    sales_df[['cor_kimono', 'tamanho_kimono']] = sales_df['variacao_anuncio'].str.split('|', n=1, expand=True)

    # Save DataFrame
    save_df(sales_df, ADLS_LAYER_GOLD, ADLS_CATEGORY_SALES, year, month)

def identify_products(year:str, month:str):

    # Read sales and costs DataFrames
    sales_df = read_tabular(ADLS_LAYER_GOLD, ADLS_CATEGORY_SALES, year, month)
    products_costs_df = read_tabular(ADLS_LAYER_BRONZE, ADLS_CATEGORY_PRODUCTS_COSTS, year, month)
    other_costs_df = read_tabular(ADLS_LAYER_BRONZE, ADLS_CATEGORY_OTHER_COSTS, year, month)

    # # Create normalized column names
    # normalized_columns_names = [unidecode(col_name.lower()) for col_name in PRODUCTS_COSTS_COLS]

    # Normalize and lower costs columns names
    products_costs_df.columns = [unidecode(col_name.lower()) for col_name in PRODUCTS_COSTS_COLS]
    other_costs_df.columns = [unidecode(col_name.lower()) for col_name in OTHER_COSTS_COLS]

    # Create dictionary with values per product
    product_costs_dict = dict(zip(products_costs_df['descricao'].to_list(), products_costs_df['custo'].to_list()))

    # # Identify products in each sale
    # Select columns and filter rows of interest in sales df

    # Define list of columns to select
    columns_to_select = ['id_venda', 'unidades_vendidas', 'titulo_anuncio', 'count_produto']

    # Select columns and filter
    sales_df = sales_df[columns_to_select]
    sales_df = sales_df[sales_df['count_produto']==True]

    # Remove count_produto column, which will no longer be needed
    columns_to_select.remove('count_produto')
    sales_df = sales_df[columns_to_select]

    # Iterate through sales DataFrame to identify products in each sale
    # Create products per sale dataframe
    products_per_sale_df = identify_sale_products(sales_df, product_costs_dict)

    # Save DataFrames
    # Apply decimal character correction to each dataframe
    other_costs_df = replace_decimal_character(other_costs_df)
    products_per_sale_df = replace_decimal_character(products_per_sale_df)

    # Replace null for false in other costs df 'Incluir no Lucro' column
    other_costs_df[COL_INCLUIR_LUCRO.lower()] = other_costs_df[COL_INCLUIR_LUCRO.lower()].fillna(False)

    # Save dataframes
    save_df(other_costs_df, ADLS_LAYER_GOLD, ADLS_CATEGORY_OTHER_COSTS, year, month)
    save_df(products_per_sale_df, ADLS_LAYER_GOLD, ADLS_CATEGORY_PRODUCTS_PER_SALE, year, month)

def calculate_taxes(year:str, month:str):

    # Read sales DataFrame, select and rename columns, and fill na
    sales_df = read_tabular(layer=ADLS_LAYER_SILVER, category=ADLS_CATEGORY_SALES, year=year, month=month)
    sales_df = sales_df[['Data_da_venda_Vendas', 'Receita_por_produtos_(BRL)_Vendas', 'Cancelamentos_e_reembolsos_(BRL)_Vendas']]
    sales_df.columns = ['data_venda', 'receita_por_produtos', 'cancelamentos_reembolsos']
    sales_df = sales_df.fillna(0)

    # Remove hour from date info and split date into day, month and year to convert month name to number and then convert to datetime format
    sales_df['data_venda'] = sales_df['data_venda'].str[:-10]
    date_series = sales_df['data_venda'].str.split(r'\bde\b')

    # Get month dictionary
    month_dict = get_months()

    # Convert date to datetime format
    for i in range(len(date_series)):
        date_series[i] = date_series[i][0].strip() + '-' + month_dict[date_series[i][1].strip()] + '-' + date_series[i][2].strip()

    # Assign converted date back to dataframe and convert to datetime
    sales_df['data_venda'] = date_series
    sales_df['data_venda'] = pd.to_datetime(sales_df['data_venda'], format='%d-%m-%Y')

    # Create year-month column to be able to merge with taxes dataframe
    sales_df['ano_mes'] = sales_df['data_venda'].dt.year * 100 + sales_df['data_venda'].dt.month

    # Calculate gross revenue of the invoice by adding revenue by products and cancellations/reimbursements (as they are negative values)
    sales_df['fat_bruto_nf'] = sales_df['receita_por_produtos'] + sales_df['cancelamentos_reembolsos']

    # Read taxes dataframe
    taxes_df = read_tabular(layer=ADLS_LAYER_CONFIG, category=ADLS_CATEGORY_TAXES, year='2026', month=None)

    # Create year-month column to be able to merge with sales dataframe
    taxes_df['ano_mes'] = (taxes_df['ano'].astype(int) * 100) + taxes_df['num_mes'].astype(int)

    # Rename columns
    taxes_df = taxes_df.rename(columns={
        'Imposto (%)': 'valor_imposto',
        'Mês': 'mes',
        'Observação': 'observacao'
    })

    # Convert tax percentage to decimal
    taxes_df['valor_imposto'] = taxes_df['valor_imposto'] / 100

    # Merge sales and taxes dataframes and calculate estimated tax by multiplying gross revenue of the invoice by the tax percentage
    sales_taxes_df = sales_df.merge(taxes_df[['ano_mes', 'valor_imposto']], on='ano_mes', how='left').fillna(0)
    sales_taxes_df['imposto_estimado'] = sales_taxes_df['fat_bruto_nf'] * sales_taxes_df['valor_imposto']

    # Save dataframe with estimated tax per sale
    save_df(sales_taxes_df, layer=ADLS_LAYER_GOLD, category=ADLS_CATEGORY_TAX_PER_SALE, year=year, month=month)