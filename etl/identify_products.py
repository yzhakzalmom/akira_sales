# %% [markdown]
# # Config

# %% [markdown]
# Import libraries and functions

# %%
from functions.df_helpers import replace_decimal_character
from services.read_data import read_tabular
from services.save_data import save_df
from services.treat_data import identify_sale_products
from unidecode import unidecode
from utils.constants import *

# %% [markdown]
# Get year and month parameters

# %%
year, month =  ('2026', '01')

# %% [markdown]
# # Identify products contained in each sale

# %% [markdown]
# Read sales and costs DataFrames

# %%
sales_df = read_tabular(ADLS_LAYER_GOLD, ADLS_CATEGORY_SALES, year, month)
products_costs_df = read_tabular(ADLS_LAYER_BRONZE, ADLS_CATEGORY_PRODUCTS_COSTS, year, month)
other_costs_df = read_tabular(ADLS_LAYER_BRONZE, ADLS_CATEGORY_OTHER_COSTS, year, month)

# %%
# # Create normalized column names
# normalized_columns_names = [unidecode(col_name.lower()) for col_name in PRODUCTS_COSTS_COLS]

# Normalize and lower costs columns names
products_costs_df.columns = [unidecode(col_name.lower()) for col_name in PRODUCTS_COSTS_COLS]
other_costs_df.columns = [unidecode(col_name.lower()) for col_name in OTHER_COSTS_COLS]

# %%
# Create dictionary with values per product
product_costs_dict = dict(zip(products_costs_df['descricao'].to_list(), products_costs_df['custo'].to_list()))

# %% [markdown]
# # Identify products in each sale

# %% [markdown]
# Select columns and filter rows of interest in sales df

# %%
# Define list of columns to select
columns_to_select = ['id_venda', 'unidades_vendidas', 'titulo_anuncio', 'count_produto']

# Select columns and filter
sales_df = sales_df[columns_to_select]
sales_df = sales_df[sales_df['count_produto']==True]

# Remove count_produto column, which will no longer be needed
columns_to_select.remove('count_produto')
sales_df = sales_df[columns_to_select]

# %% [markdown]
# Iterate through sales DataFrame to identify products in each sale

# %%
# Create products per sale dataframe
products_per_sale_df = identify_sale_products(sales_df, product_costs_dict)

# %% [markdown]
# Save DataFrames

# %%
# Apply decimal character correction to each dataframe
other_costs_df = replace_decimal_character(other_costs_df)
products_per_sale_df = replace_decimal_character(products_per_sale_df)

# Replace null for false in other costs df 'Incluir no Lucro' column
other_costs_df[COL_INCLUIR_LUCRO.lower()] = other_costs_df[COL_INCLUIR_LUCRO.lower()].fillna(False)

# Save dataframes
save_df(other_costs_df, ADLS_LAYER_GOLD, ADLS_CATEGORY_OTHER_COSTS, year, month)
save_df(products_per_sale_df, ADLS_LAYER_GOLD, ADLS_CATEGORY_PRODUCTS_PER_SALE, year, month)


