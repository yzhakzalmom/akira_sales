from __future__ import annotations
from .general import render_date_input
from services.save_data import save_uploaded_df
from services.read_data import get_asset_dataframe, get_asset_text
from utils.constants import *

def render_uploader_button(container, costs_df: pd.DataFrame, cost_type: str, month: str, year: str):
    
    # On button click
    if container.button(MSG_SEND_INFO, width=COMPONENTS_WIDTH, key=f'{BUTTON_KEY_PREFIX}{cost_type}'):

        try: # to save costs dataframe

            # Get save message
            message = save_uploaded_df(costs_df, cost_type, month, year)

            # Render success message
            container.success(message, icon=ICON_SUCCESS)

        except Exception as e:
            # Render error message and description
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)


def render_costs_inputs(container, cost_type: str):

    # Create empty dataframetobe edited
    empty_costs_df = get_asset_dataframe(f'{cost_type}{PLACEHOLDER_SUFIX}')

    # Cast 'Descrição' to string
    empty_costs_df[COL_DESCRICAO] = empty_costs_df[COL_DESCRICAO].astype(str)

    # Render final costs editor
    final_costs_df = container.data_editor(empty_costs_df, num_rows=DATA_EDITOR_NUM_ROWS, key=cost_type)

    return final_costs_df

def render_costs_uploader(container, cost_type: str, header: str):

    # Create costs input container
    costs_container = container.container()

    # Render section header and text
    costs_container.header(header)
    costs_container.markdown(get_asset_text(cost_type))

    # Get date for the costs
    month, year = render_date_input(costs_container, key=cost_type)

    # Get costs inputs
    costs_container.caption(MSG_FILL_COSTS)
    costs_df = render_costs_inputs(costs_container, cost_type)

    # Update dataframe with month and year
    costs_df[COL_MES] = [month] * len(costs_df)
    costs_df[COL_ANO] = [year] * len(costs_df)

    # Render button only if 
    if (costs_df[COL_MES].notna().all()) and (costs_df[COL_ANO].notna().all()) and (costs_df[COL_CUSTO].notna().all()):
        render_uploader_button(costs_container, costs_df, cost_type, month, year)