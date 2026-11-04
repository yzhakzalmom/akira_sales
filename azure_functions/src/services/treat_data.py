import pandas as pd
from src.utils.constants import (
    PRODUCT_COL_ABBREVIATION,
    PRODUCT_COL_KEYWORD,
    PRODUCT_COL_NAME,
)


def _as_text(value) -> str:
    return '' if pd.isna(value) else str(value).strip()


def _title_key(value) -> tuple[bool, str]:
    return (True, '') if pd.isna(value) else (False, str(value))


def identify_sale_products(
    sales_df: pd.DataFrame,
    product_costs_dict: dict[str, float],
    products_df: pd.DataFrame,
) -> pd.DataFrame:
    output_columns = [
        'id_venda',
        'unidades_vendidas',
        'categoria_produto',
        'custo_producao',
    ]
    if sales_df.empty:
        return pd.DataFrame(columns=output_columns)

    configured_products = [
        {
            'name': _as_text(row[PRODUCT_COL_NAME]).lower(),
            'abbreviation': _as_text(row[PRODUCT_COL_ABBREVIATION]).upper(),
            'keyword': _as_text(row[PRODUCT_COL_KEYWORD]).lower(),
        }
        for _, row in products_df.iterrows()
    ]

    def configured_code(marker: str, fallback: str) -> str:
        for product in configured_products:
            searchable_text = f"{product['name']} {product['keyword']}"
            if marker in searchable_text and product['abbreviation']:
                return product['abbreviation']
        return fallback

    feminine_code = configured_code('feminin', 'FEM')
    start_code = configured_code('start', 'STR')
    belt_code = configured_code('faixa', 'FX')

    # Classify each distinct ad title once, using its aggregated sold quantity.
    title_sales_df = sales_df.groupby(
        'titulo_anuncio', as_index=False, dropna=False
    ).agg(unidades_vendidas=('unidades_vendidas', 'sum'))
    products_by_title = {}

    for row in title_sales_df.itertuples(index=False):
        ad_title = _as_text(row.titulo_anuncio).lower()

        if 'feminin' in ad_title and 'sakura' not in ad_title:
            main_product = feminine_code
        else:
            main_product = start_code
            for product in configured_products:
                keyword = product['keyword']
                abbreviation = product['abbreviation']
                special_product = any(
                    marker in f"{product['name']} {keyword}"
                    for marker in ('feminin', 'start', 'faixa')
                )
                if keyword and abbreviation and not special_product and keyword in ad_title:
                    main_product = abbreviation
                    break

        product_codes = [main_product]
        if 'faixa' in ad_title:
            product_codes.append(belt_code)
        products_by_title[_title_key(row.titulo_anuncio)] = product_codes

    sales_by_order_and_title = sales_df.groupby(
        ['id_venda', 'titulo_anuncio'], as_index=False, dropna=False
    ).agg(unidades_vendidas=('unidades_vendidas', 'sum'))
    normalized_costs = {
        _as_text(product).upper(): cost
        for product, cost in product_costs_dict.items()
    }
    rows = []

    for row in sales_by_order_and_title.itertuples(index=False):
        for product in products_by_title[_title_key(row.titulo_anuncio)]:
            if product not in normalized_costs:
                raise KeyError(f'No production cost configured for product code {product!r}')
            rows.append({
                'id_venda': row.id_venda,
                'unidades_vendidas': row.unidades_vendidas,
                'categoria_produto': product,
                'custo_producao': row.unidades_vendidas * normalized_costs[product],
            })

    return pd.DataFrame(rows, columns=output_columns)