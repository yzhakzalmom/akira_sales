import pyspark.pandas as ps

def identify_sale_products(sales_df: ps.DataFrame, product_costs_dict: ps.DataFrame) -> ps.DataFrame:
    
    # Create list to store the rows of products_per_sale_df
    rows = []

    for row in sales_df.itertuples():
        # Define auxiliary list to store sale products and ad title
        product_list = []
        ad_title = row.titulo_anuncio.lower()

        # According to products found in ad title, add product to product list
        if ('akai' in ad_title):
            product_list.append('AKAI')
        elif ('feminin' in ad_title):
            product_list.append('FEM')
        elif ('ronin' in ad_title):
            product_list.append('RON')
        else:
            product_list.append('STR')
        
        # Each product may or not have a belt with it
        if 'faixa' in ad_title:
            product_list.append('FX')

        # For each product, create a row in products per sale df
        for product in product_list:
            rows.append({
                'id_venda': row.id_venda,
                'unidades_vendidas': row.unidades_vendidas,
                'categoria_produto': product,
                'custo_producao': row.unidades_vendidas * product_costs_dict[product]
            })

    # Return products per sale dataframe
    return ps.DataFrame(rows)