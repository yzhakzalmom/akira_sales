from st_web.utils.helpers import get_months, get_years
from utils.constants import *

# key: unique id that must be different for each selectbox
def render_date_input(container, key: str) -> tuple:

    # Create date input using columns
    month_col, year_col, _ = container.columns(DATE_INPUT_COLUMN_LAYOUT, gap=DATE_INPUT_COLUMN_GAP)

    # Render month column
    with month_col:
        # Render month selectbox
        months = get_months()
        chosen_month = container.selectbox(DATE_INPUT_MONTH_LABEL, list(months.keys()), key=f'{MONTH_KEY_PREFIX}{key}')

    # Render year column
    with year_col:
        # Rendem year selectbox
        years_list = get_years()
        chosen_year = container.selectbox(DATE_INPUT_YEAR_LABEL, years_list, key=f'{YEAR_KEY_PREFIX}{key}')

    return months[chosen_month], chosen_year