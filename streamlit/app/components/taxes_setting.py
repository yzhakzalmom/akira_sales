import pandas as pd
import streamlit as st
from .general import render_date_input
from services.read_data import get_asset_text, read_tabular
from services.save_data import save_df
from services.check_data import check_data_folder_exists
from utils.constants import *
from utils.helpers import get_months

def render_taxes_button(container, taxes_df: pd.DataFrame, year: str):

    if container.button(MSG_SEND_INFO, width=COMPONENTS_WIDTH, key=f'{BUTTON_KEY_PREFIX}{ADLS_CATEGORY_TAXES}'):
            
        try:
            message = save_df(
                taxes_df,
                layer=ADLS_LAYER_CONFIG,
                category=ADLS_CATEGORY_TAXES,
                year=year,
                month=None
            )

            # Render success message
            container.success(message, icon=ICON_SUCCESS)

        except Exception as e:
            # Render error message and exception details
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)


# Render data editor to input taxes information
def render_taxes_inputs(container, year: str):

    # Checks if taxes info already exists for the given year
    if not check_data_folder_exists(f'{ADLS_LAYER_CONFIG}/{ADLS_CATEGORY_TAXES}/{year}'):

        # Create taxes DataFrame with months name
        taxes_df = pd.DataFrame({
            TAXES_COL_MES: get_months().keys(),
            TAXES_COL_PCT: None,
            TAXES_COL_OBS: None
        })

    # If it does, read from ADLS
    else:
        taxes_df = read_tabular(layer=ADLS_LAYER_CONFIG, category=ADLS_CATEGORY_TAXES, month=None, year=year)

    # Cast columns types so that streamlit can validate
    taxes_df[TAXES_COL_PCT] = taxes_df[TAXES_COL_PCT].astype(float)
    taxes_df[TAXES_COL_OBS] = taxes_df[TAXES_COL_OBS].astype(str)

    # Define column config for percentage column
    column_config={
        TAXES_COL_PCT: st.column_config.NumberColumn(
            TAXES_COL_PCT,
            min_value=TAXES_PCT_COL_MIN,
            max_value=TAXES_PCT_COL_MAX,
            step=0.1,
            format="%.1f %%",
        )
    }

    # Render data editor
    taxes_df = container.data_editor(taxes_df, num_rows=TAXES_DATA_EDITOR_NUM_ROWS, disabled=[TAXES_COL_MES], key=TAXES_SETTINGS_FILE_NAME, hide_index=True, column_config=column_config)
    
    return taxes_df

def render_taxes_settings(container):

    # Define container for taxes settings
    settings_container = container.container()

    # Render header and guide text for the input
    settings_container.header(TAXES_SETTINGS_HEADER)
    settings_container.markdown(get_asset_text(TAXES_SETTINGS_FILE_NAME))

    # Get year from user selection
    year = render_date_input(settings_container, TAXES_SETTINGS_FILE_NAME, has_month=False)

    # Render taxes data editor
    settings_container.caption(MSG_FILL_TAXES)
    taxes_df = render_taxes_inputs(settings_container, year)

    # Render button that also saves the DataFrame
    render_taxes_button(settings_container, taxes_df=taxes_df, year=year)