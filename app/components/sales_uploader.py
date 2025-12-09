def render_date_input(container) -> tuple:
    from utils.helpers import get_months, get_years

    # Create date input using columns
    month_col, year_col, _ = container.columns([1, 1, 2], gap='medium')

    # Render month column
    with month_col:
        # Render month selectbox
        months = get_months()
        chosen_month = container.selectbox("Mês do arquivo", list(months.keys()))

    # Render year column
    with year_col:
        # Rendem year selectbox
        years_list = get_years()
        chosen_year = container.selectbox("Ano do arquivo", years_list)

    return months[chosen_month], chosen_year

def render_sheet_preview(container, sales_sheet):
    from services.check_data import check_sales_sheet_format

    try: # to check and render sales sheet preview
        sales_preview_df = check_sales_sheet_format(container, sales_sheet)
        container.subheader('Prévia do arquivo')
        container.dataframe(sales_preview_df)

    except Exception as e:

        # Render error message and description
        container.error('Erro no arquivo. Tem certeza que escolheu o arquivo certo?', icon='❌')
        container.write(e)

def render_uploader_button(container, sales_sheet, month, year):
    from services.save_data import save_sales_sheet

    # On button click
    if container.button('Enviar arquivo', width='stretch'):

        try: # to save sales sheet
            save_sales_sheet(sales_sheet, month, year)

            # Render success message
            container.success('Upload bem sucedido', icon='✅')

        except Exception as e:
            # Render error message and description
            container.error('Erro no upload', icon='❌')
            container.write(e)

def render_sales_uploader(container) -> None:
    from services.read_data import get_text

    # Create sales uploader container
    sales_up_container = container.container()

    # Render section header and text
    sales_up_container.header('Planilha de Vendas 📈')
    sales_up_container.markdown(get_text('sales_uploader'))

    # Get chosen month and year and render date input
    chosen_month, chosen_year = render_date_input(sales_up_container)    

    # Render upload section
    sales_sheet = sales_up_container.file_uploader(
        'Envie planilha de vendas',
        type=['xlsx', 'xls']
    )

    # Render button only if there is an uploaded file
    if sales_sheet:

        render_sheet_preview(sales_up_container, sales_sheet)

        render_uploader_button(sales_up_container, sales_sheet, chosen_month, chosen_year)