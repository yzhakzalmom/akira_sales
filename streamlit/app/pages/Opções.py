"""
Streamlit page for configs.
Allows users to define parameters for inputs and execution.
"""

import streamlit as st
from components import header
from utils.constants import *

# Configure page settings
st.set_page_config(page_title=CONFIG_PAGE_TITLE, page_icon=MAIN_ICON, layout=CONFIG_PAGE_LAYOUT)

# Create main page container
config_container = st.container()

# Render page header
header.render_header(config_container, CONFIG_PAGE_HEADER)
config_container.divider()

# Create main page columns with centered layout
_, main_col, __ = config_container.columns(CONFIG_PAGE_COLUMN_LAYOUT)

# Create central container within the middle column
central_container = main_col.container()

# Render job execution interface within the column
# with main_col:
    # jobs_execution.render_execution_trigger(central_container)