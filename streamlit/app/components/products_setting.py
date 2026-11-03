import pandas as pd
import streamlit as st
from services.check_data import check_data_folder_exists
from services.read_data import read_tabular
from services.save_data import save_df
from utils.constants import *


PRODUCTS_STORAGE_COLUMNS = {
    column: column.lower().replace(' ', '_')
    for column in PRODUCTS_COLS
}


def render_products_button(container, products_df: pd.DataFrame):
    if container.button(
        MSG_SEND_INFO,
        width=COMPONENTS_WIDTH,
        key=f'{BUTTON_KEY_PREFIX}{ADLS_CATEGORY_PRODUCTS}',
    ):
        try:
            message = save_df(
                products_df.rename(columns=PRODUCTS_STORAGE_COLUMNS),
                layer=ADLS_LAYER_CONFIG,
                category=ADLS_CATEGORY_PRODUCTS,
            )
            container.success(message, icon=ICON_SUCCESS)
        except Exception as e:
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)


def render_products_inputs(container):
    products_path = f'{ADLS_LAYER_CONFIG}/{ADLS_CATEGORY_PRODUCTS}'

    if check_data_folder_exists(products_path):
        products_df = read_tabular(
            layer=ADLS_LAYER_CONFIG,
            category=ADLS_CATEGORY_PRODUCTS,
        )
        products_df = products_df.rename(
            columns={stored: display for display, stored in PRODUCTS_STORAGE_COLUMNS.items()}
        )
        products_df = products_df[PRODUCTS_COLS]
    else:
        products_df = pd.DataFrame(columns=PRODUCTS_COLS)
        products_df.loc[0] = None

    return container.data_editor(
        products_df,
        num_rows=PRODUCTS_DATA_EDITOR_NUM_ROWS,
        key=ADLS_CATEGORY_PRODUCTS,
        hide_index=True,
    )


def render_products_settings(container):
    settings_container = container.container()
    settings_container.header(PRODUCTS_SETTINGS_HEADER)
    products_df = render_products_inputs(settings_container)
    render_products_button(settings_container, products_df)
