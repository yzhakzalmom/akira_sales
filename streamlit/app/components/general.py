from utils.helpers import get_months, get_years
from utils.constants import *
from datetime import datetime

# key: unique id that must be different for each selectbox
def render_date_input(container, key: str, has_month: bool = True) -> tuple | str:

    # Create date input using columns
    month_col, year_col, _ = container.columns(DATE_INPUT_COLUMN_LAYOUT, gap=DATE_INPUT_COLUMN_GAP)

    # Render month input if parameter has_month is selected
    if has_month:
        # Render month column
        with month_col:
            # Render month selectbox
            last_month_index = datetime.now().month - 2
            months = get_months()
            chosen_month = container.selectbox(DATE_INPUT_MONTH_LABEL, list(months.keys()), key=f'{MONTH_KEY_PREFIX}{key}', index=last_month_index)

    # Render year column
    with year_col:
        # Rendem year selectbox
        years_list = get_years()
        chosen_year = container.selectbox(DATE_INPUT_YEAR_LABEL, years_list, key=f'{YEAR_KEY_PREFIX}{key}')

    # Return month and year if has_month is selected
    if has_month:
        return months[chosen_month], chosen_year
    
    # Return only the year if has_month is not selected
    return chosen_year