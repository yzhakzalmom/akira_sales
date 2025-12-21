"""
Component module for rendering cost data uploader interface.
Handles UI components for uploading products costs and other costs data.
"""

from __future__ import annotations
import pandas as pd
from .general import render_date_input
from st_web.services.save_data import save_uploaded_df
from st_web.services.read_data import get_asset_dataframe, get_asset_text
from utils.constants import *

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
            message = save_uploaded_df(costs_df, cost_type, month, year)

            # Render success message
            container.success(message, icon=ICON_SUCCESS)

        except Exception as e:
            # Render error message and exception details
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)


def render_costs_inputs(container, cost_type: str):
    """
    Render an editable dataframe for users to input costs data.
    
    Args:
        container: Streamlit container object for rendering UI components.
        cost_type: Type of cost ('products_costs' or 'other_costs').
    
    Returns:
        pd.DataFrame: The edited dataframe with user input.
    """
    # Create empty dataframe template to be edited by user
    empty_costs_df = get_asset_dataframe(f'{cost_type}{PLACEHOLDER_SUFIX}')

    # Cast 'Descrição' column to string type
    empty_costs_df[COL_DESCRICAO] = empty_costs_df[COL_DESCRICAO].astype(str)

    # Render data editor and get the edited dataframe
    final_costs_df = container.data_editor(empty_costs_df, num_rows=DATA_EDITOR_NUM_ROWS, key=cost_type)

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
    costs_df = render_costs_inputs(costs_container, cost_type)

    # Update dataframe with selected month and year for all rows
    costs_df[COL_MES] = [month] * len(costs_df)
    costs_df[COL_ANO] = [year] * len(costs_df)

    # Render upload button only if all required fields are filled
    # (month, year, and cost values must not be null)
    if (costs_df[COL_MES].notna().all()) and (costs_df[COL_ANO].notna().all()) and (costs_df[COL_CUSTO].notna().all()):
        render_uploader_button(costs_container, costs_df, cost_type, month, year)