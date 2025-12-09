def render_uploader_button(container, cost_type: str):
    # TODO: lógica de salvamento do arquivo ao clicar no botão
    pass

def render_costs_inputs(container, cost_type: str):
    import pandas as pd
    from services.read_data import get_dataframe

    # Create empty dataframetobe edited
    empty_costs_df = get_dataframe(f'{cost_type}_placeholder')

    # Render final costs editor
    final_costs_df = container.data_editor(empty_costs_df, num_rows='dynamic', key=cost_type)

    # TODO: finalizar salvamento do df



def render_costs_uploader(container, cost_type: str):
    from services.read_data import get_text

    # Create costs input container
    costs_container = container.container()

    # Render section header and text
    costs_container.header('Custos com produtos 🥋')
    costs_container.markdown(get_text('products_costs'))

    render_costs_inputs(costs_container, cost_type)