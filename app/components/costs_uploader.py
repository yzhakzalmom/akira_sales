from __future__ import annotations

def render_uploader_button(container, cost_df: pd.DataFrame, cost_type: str):
    if container.button('Enviar informações', width='stretch'):
        pass

def render_costs_inputs(container, cost_type: str):
    import pandas as pd
    from services.read_data import get_dataframe

    # Create empty dataframetobe edited
    empty_costs_df = get_dataframe(f'{cost_type}_placeholder')

    # Render final costs editor
    final_costs_df = container.data_editor(empty_costs_df, num_rows='dynamic', key=cost_type)

    return final_costs_df

def render_costs_uploader(container, cost_type: str, header: str):
    from services.read_data import get_text
    from .general import render_date_input

    # Create costs input container
    costs_container = container.container()

    # Render section header and text
    costs_container.header(header)
    costs_container.markdown(get_text(cost_type))

    # Get date for the costs
    month, year = render_date_input(costs_container, cost_type)

    # Get costs inputs
    costs_container.caption('Preencha com seus custos')
    costs_df = render_costs_inputs(costs_container, cost_type)

    # Update dataframe with month and year
    costs_df['Mês'] = [month] * len(costs_df)
    costs_df['Ano'] = [year] * len(costs_df)

    # Render button only if 
    if (costs_df['Mês'].notna().all()) and (costs_df['Ano'].notna().all()) and (costs_df['Custo'].notna().all()):
        render_uploader_button(costs_container, costs_df, 'products_costs')