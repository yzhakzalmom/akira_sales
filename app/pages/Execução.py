"""
Streamlit page for job execution interface.
Allows users to trigger Databricks jobs after verifying required data files exist.
"""

import streamlit as st
from components import header, jobs_execution
from utils.constants import *

# Configure page settings
st.set_page_config(page_title=JOBS_PAGE_TITLE, page_icon=ICON_JOBS_PAGE, layout=JOBS_PAGE_LAYOUT)

# Create main page container
jobs_container = st.container()

# Render page header
header.render_header(jobs_container, JOBS_PAGE_HEADER)
jobs_container.divider()

# Create main page columns with centered layout
_, main_col, __ = jobs_container.columns(JOBS_PAGE_COLUMN_LAYOUT)

# Create central container within the middle column
central_container = main_col.container()

# Render job execution interface within the column
with main_col:
    jobs_execution.render_execution_trigger(central_container)