import pandas as pd
import streamlit as st
from .general import render_date_input
from services.read_data import get_asset_text, read_tabular
from services.save_data import save_df
from services.check_data import check_data_folder_exists
from utils.constants import *

def render_products_settings_button(container, products_sett_df: pd.DataFrame):

    if container.button(MSG_SEND_INFO, width=COMPONENTS_WIDTH, key=f'{BUTTON_KEY_PREFIX}{ADLS_CATEGORY_SETT_PRODUCTS}'):
            
        try:
            message = save_df(
                products_sett_df,
                layer=ADLS_LAYER_CONFIG,
                category=ADLS_CATEGORY_SETT_PRODUCTS,
                month=None
            )

            # Render success message
            container.success(message, icon=ICON_SUCCESS)

        except Exception as e:
            # Render error message and exception details
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)

def render_products_inputs(container: st.container):
    
    
    if not check_data_folder_exists(f'{ADLS_LAYER_CONFIG}/{ADLS_CATEGORY_SETT_PRODUCTS}'):
        
        products_sett_df = pd.DataFrame({
            PROD_SETT_COL_NAME: [None]
        })

    # If it does, read from ADLS
    else:
        products_sett_df = read_tabular(layer=ADLS_LAYER_CONFIG, category=ADLS_CATEGORY_SETT_PRODUCTS)

    column_config={
        PROD_SETT_COL_NAME: st.column_config.TextColumn(
            required=True
        )
    }

    products_sett_df = container.data_editor(
        products_sett_df, 
        num_rows=PRODUCTS_SETT_DATA_EDITOR_NUM_ROWS, 
        key='x', 
        hide_index=True,
        column_config=column_config
    )

    return products_sett_df

def render_products_settings(container: st.container):

    prod_settings_container = container.container()

    # Header
    prod_settings_container.header(PRODUCTS_SETT_HEADER)
    prod_settings_container.markdown(get_asset_text(PRODUCTS_SETT_FILE_NAME))

    products_sett_df = render_products_inputs(prod_settings_container)

    