from functions.df_helpers import replace_decimal_character
from services.read_data import read_tabular
from services.save_data import save_df
from utils.constants import *

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
columns_to_drop = ['Descrição_do_status_Vendas', 'Pacote_de_diversos_produtos_Vendas', 'Pertence_a_um_kit_Vendas', 'SKU_Anúncios', '#_de_anúncio_Anúncios', 'Canal_de_venda_Anúncios', 'Receita_por_acréscimo_no_preço_(pago_pelo_comprador)_Vendas', 'Taxa_de_parcelamento_equivalente_ao_acréscimo_Vendas']
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