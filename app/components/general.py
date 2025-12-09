# key: unique id that must be different for each selectbox
def render_date_input(container, key: str) -> tuple:
    from utils.helpers import get_months, get_years

    # Create date input using columns
    month_col, year_col, _ = container.columns([1, 1, 2], gap='medium')

    # Render month column
    with month_col:
        # Render month selectbox
        months = get_months()
        chosen_month = container.selectbox("Mês do arquivo", list(months.keys()), key=f'month_{key}')

    # Render year column
    with year_col:
        # Rendem year selectbox
        years_list = get_years()
        chosen_year = container.selectbox("Ano do arquivo", years_list, key=f'year_{key}')

    return months[chosen_month], chosen_year