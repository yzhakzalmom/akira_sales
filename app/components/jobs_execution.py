"""
Component module for rendering job execution interface.
Handles UI components for triggering Databricks jobs and verifying required files.
"""

from PIL.ImageOps import contain
import pandas as pd
from .general import render_date_input
from services.read_data import get_asset_text
from services.check_data import check_data_folder_exists
from services.jobs import trigger_job, check_active_run
from utils.constants import *

def render_trigger_button(container, month: str, year: str):
    """
    Render a button to trigger the Databricks job if no active runs exist.
    
    Args:
        container: Streamlit container object for rendering UI components.
        month: Month string for the job execution.
        year: Year string for the job execution.
    """
    # Only render button if there are no active runs
    if not check_active_run(container):
        # On button click, trigger the job
        if container.button(MSG_TRIGGER_JOB, width=COMPONENTS_WIDTH):
            trigger_job(container, month, year)

def render_files_confirmation(container, month: str, year: str):
    """
    Check if required data files exist and display their status in a dataframe.
    
    Args:
        container: Streamlit container object for rendering UI components.
        month: Month string to check files for.
        year: Year string to check files for.
    
    Returns:
        bool: True if all required files exist (sales, products costs, other costs), False otherwise.
    """
    # Display subheader for file confirmation section
    container.write(JOB_FILE_CONF_SUBHEADER)

    # Check existence of each required file category in ADLS
    sales_exist = check_data_folder_exists(f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_SALES}/{year}/{month}')
    products_costs_exist = check_data_folder_exists(f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_PRODUCTS_COSTS}/{year}/{month}')
    other_costs_exist = check_data_folder_exists(f'{ADLS_LAYER_BRONZE}/{ADLS_CATEGORY_OTHER_COSTS}/{year}/{month}')

    # Create dataframe to display file existence status
    check_files_df = pd.DataFrame({
        'Arquivo': ['Vendas', 'Custos de Produtos', 'Outros Custos'],
        'Existe': [sales_exist, products_costs_exist, other_costs_exist]
    })

    # Display the dataframe in the container
    container.dataframe(check_files_df)

    # Return True only if all required files exist
    return (sales_exist and products_costs_exist and other_costs_exist)

def render_execution_trigger(container):
    """
    Main function to render the complete job execution interface.
    Includes header, instructions, date input, file confirmation, and trigger button.
    
    Args:
        container: Streamlit container object for rendering UI components.
    """
    # Create execution container
    exec_container = container.container()

    # Render section header and instructions
    exec_container.header(JOBS_EXECUTION_HEADER)
    exec_container.markdown(get_asset_text(JOBS_EXECUTION_TEXT_FILE_NAME))

    # Render date input and get selected month and year
    month, year = render_date_input(exec_container, JOBS_EXECUTION_TEXT_FILE_NAME)

    # Check if all required files exist for the selected date
    files_exist = render_files_confirmation(exec_container, month, year)

    # Only render trigger button if all required files exist
    if files_exist:
        render_trigger_button(exec_container, month, year)