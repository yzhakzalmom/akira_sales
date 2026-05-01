"""
Component module for rendering cost data uploader interface.
Handles UI components for uploading products costs and other costs data.
"""

from __future__ import annotations
import pandas as pd
import streamlit as st
from .general import render_date_input
from services.save_data import save_df
from services.read_data import get_asset_text, read_tabular
from utils.constants import *
from utils.helpers import create_placeholder_df

def render_uploader_button(container, costs_df: pd.DataFrame, cost_type: str, month: str, year: str):
    """
    Render a button to upload the costs dataframe to ADLS.
    
    Args:
        container: Streamlit container object for rendering UI components.
        costs_df: DataFrame containing the costs data to be uploaded.
        cost_type: Type of cost ('products_costs' or 'other_costs').
        month: Month string for the costs data.
        year: Year string for the costs data.
    """
    # On button click, attempt to save the costs dataframe
    if container.button(MSG_SEND_INFO, width=COMPONENTS_WIDTH, key=f'{BUTTON_KEY_PREFIX}{cost_type}'):

        try: # to save costs dataframe
            # Get save message from save operation
            message = save_df(
                costs_df,
                layer=ADLS_LAYER_BRONZE,
                category=cost_type,
                year=year,
                month=month,
                file_prefix= f'{RAW_FILE_PREFIX}_{COSTS_FILE_PREFIX}'
            )

            # Render success message
            container.success(message, icon=ICON_SUCCESS)

        except Exception as e:
            # Render error message and exception details
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)


def render_costs_inputs(container, cost_type: str, month: str, year: str):
    """
    Render an editable dataframe for users to input costs data.
    
    Args:
        container: Streamlit container object for rendering UI components.
        cost_type: Type of cost ('products_costs' or 'other_costs').
    
    Returns:
        pd.DataFrame: The edited dataframe with user input.
    """

    try:

        if month == '01':
            month = '12'
            year = str(int(year) - 1)

        base_costs_df = read_tabular(
            layer=ADLS_LAYER_BRONZE,
            category=cost_type,
            year=year,
            month = f'0{str(int(month) - 1)}'[-2:]
        )

        column_config={
            COL_CUSTO: st.column_config.NumberColumn(
                "Custo",
                format="%.2f"
            ),
            COL_MES: None,
            COL_ANO: None
        }

    except:
        # Create empty dataframe template to be edited by user
        base_costs_df = create_placeholder_df(PLACEHOLDER_COLS[cost_type])

        # Cast 'Descrição' column to string type
        base_costs_df[COL_DESCRICAO] = base_costs_df[COL_DESCRICAO].astype(str)

        # Guarantee execution only for other costs
        if (cost_type == ADLS_CATEGORY_OTHER_COSTS):
            # Cast 'Incluir no Lucro' column to bool type
            base_costs_df[COL_INCLUIR_LUCRO] = base_costs_df[COL_INCLUIR_LUCRO].astype(bool)

        column_config={
            COL_DESCRICAO: st.column_config.SelectboxColumn(
                "Descrição",
                options=COSTS_SELECTBOX_DICT[cost_type]
            ),
            COL_CUSTO: st.column_config.NumberColumn(
                "Custo",
                format="%.2f"
            ),
            COL_MES: None,
            COL_ANO: None
        }

    # Render data editor and get the edited dataframe
    final_costs_df = container.data_editor(base_costs_df, num_rows=COSTS_DATA_EDITOR_NUM_ROWS, key=cost_type, hide_index=True, column_config=column_config)

    return final_costs_df

def render_costs_uploader(container, cost_type: str, header: str):
    """
    Main function to render the complete costs uploader interface.
    Includes header, instructions, date input, data editor, and upload button.
    
    Args:
        container: Streamlit container object for rendering UI components.
        cost_type: Type of cost ('products_costs' or 'other_costs').
        header: Header text to display for this uploader section.
    """
    # Create costs input container
    costs_container = container.container()

    # Render section header and instructions text
    costs_container.header(header)
    costs_container.markdown(get_asset_text(cost_type))

    # Get date input for the costs (month and year)
    month, year = render_date_input(costs_container, key=cost_type)

    # Render costs data input editor
    costs_container.caption(MSG_FILL_COSTS)
    costs_df = render_costs_inputs(costs_container, cost_type, month, year)

    # Update dataframe with selected month and year for all rows
    costs_df[COL_MES] = [month] * len(costs_df)
    costs_df[COL_ANO] = [year] * len(costs_df)

    # Render upload button only if all required fields are filled
    # (month, year, description, and cost values must not be null)
    if (costs_df[COL_MES].notna().all()) and (costs_df[COL_ANO].notna().all()) and (costs_df[COL_CUSTO].notna().all()) and (costs_df[COL_DESCRICAO].notna().all()):
        render_uploader_button(costs_container, costs_df, cost_type, month, year)