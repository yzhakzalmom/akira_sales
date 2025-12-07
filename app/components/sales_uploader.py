def get_sales_uploader_text() -> str:
    from utils.helpers import get_asset_file_path, get_months
    # Find text path
    text_path = get_asset_file_path('texts', 'sales_uploader.md')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

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

def save_sales_sheet(sales_sheet, file_month = None, file_year = None) -> None:
    from utils.helpers import get_data_path
    import streamlit as st

    # Create new file in data folder
    with open(get_data_path() / 'test.xlsx', 'wb') as f:

        # Write the file with the sales sheet content
        f.write(sales_sheet.getbuffer())

def render_sales_uploader() -> None:
    import streamlit as st
    from pathlib import Path
    from utils.helpers import get_data_path

    # Render section header and text
    st.header('Planilha de Vendas')
    st.markdown(get_sales_uploader_text())

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
        if st.button('Enviar arquivo', width='stretch'):

            
            try: # to save sales sheet
                save_sales_sheet(sales_sheet)

                # Render success message
                st.success('Upload bem sucedido', icon='✅')

            except Exception as e:
                # Render error message and description
                st.error('Erro no upload', icon='❌')
                st.write(e)