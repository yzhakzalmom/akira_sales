def render_date_input() -> tuple:
    import streamlit as st
    from utils.helpers import get_months, get_years

    # Create date input using columns
    month_col, year_col, _ = st.columns([1, 1, 2], gap='medium')

    # Render month column
    with month_col:
        # Render month selectbox
        months = get_months()
        chosen_month = st.selectbox("Mês do arquivo", list(months.keys()))

    # Render year column
    with year_col:
        # Rendem year selectbox
        years_list = get_years()
        chosen_year = st.selectbox("Ano do arquivo", years_list)

    return chosen_month, chosen_year

def render_sales_uploader() -> None:
    import streamlit as st
    from services.read_data import get_sales_uploader_text
    from services.save_data import save_sales_sheet

    # Create sales uploader container
    sales_up_container = st.container()

    # Render section header and text
    sales_up_container.header('Planilha de Vendas 📈')
    sales_up_container.markdown(get_sales_uploader_text())

    # Get chosen month and year and render date input
    chosen_month, chosen_year = render_date_input()    

    # Render upload section
    sales_sheet = st.file_uploader(
        'Envie planilha de vendas',
        type=['xlsx', 'xls']
    )

    # Render button only if there is an uploaded file
    if sales_sheet:
        # On button click
        if sales_up_container.button('Enviar arquivo', width='stretch'):

            
            try: # to save sales sheet
                save_sales_sheet(sales_sheet)

                # Render success message
                sales_up_container.success('Upload bem sucedido', icon='✅')

            except Exception as e:
                # Render error message and description
                sales_up_container.error('Erro no upload', icon='❌')
                sales_up_container.write(e)