from __future__ import annotations

def render_uploader_button(container, costs_df: pd.DataFrame, cost_type: str, month: str, year: str):
    from services.save_data import save_costs_df
    from time import time
    
    # On button click
    if container.button('Enviar informações', width='stretch', key=f'btn_{cost_type}'):

        try: # to save costs dataframe

            # Get save message
            message = save_costs_df(costs_df, cost_type, month, year)

            # Render success message
            container.success(message, icon='✅')

        except Exception as e:
            # Render error message and description
            container.error('Erro no upload', icon='❌')
            container.write(e)


def render_costs_inputs(container, cost_type: str):
    import pandas as pd
    from services.read_data import get_dataframe

    # Create empty dataframetobe edited
    empty_costs_df = get_dataframe(f'{cost_type}_placeholder')

    # Cast 'Descrição' to string
    empty_costs_df['Descrição'] = empty_costs_df['Descrição'].astype(str)

    # Render final costs editor
    final_costs_df = container.data_editor(empty_costs_df, num_rows='dynamic', key=cost_type)

    return final_costs_df

def render_costs_uploader(container, cost_type: str, header: str):
    from services.read_data import get_text
    from .general import render_date_input
    from time import time

    # Create costs input container
    costs_container = container.container()

    # Render section header and text
    costs_container.header(header)
    costs_container.markdown(get_text(cost_type))

    # Get date for the costs
    month, year = render_date_input(costs_container, key=cost_type)

    # Get costs inputs
    costs_container.caption('Preencha com seus custos')
    costs_df = render_costs_inputs(costs_container, cost_type)

    # Update dataframe with month and year
    costs_df['Mês'] = [month] * len(costs_df)
    costs_df['Ano'] = [year] * len(costs_df)

    # Render button only if 
    if (costs_df['Mês'].notna().all()) and (costs_df['Ano'].notna().all()) and (costs_df['Custo'].notna().all()):
        render_uploader_button(costs_container, costs_df, cost_type, month, year)