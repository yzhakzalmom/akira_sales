"""
Main Streamlit page for file uploads.
Allows users to upload sales data, products costs, and other costs to ADLS.
"""

import streamlit as st
from components import header, sales_uploader, costs_uploader
from utils.constants import *

# Configure page settings
st.set_page_config(page_title=MAIN_PAGE_TITLE, page_icon=ICON_MAIN_PAGE, layout=MAIN_PAGE_LAYOUT)

# Create main page container
main_container = st.container()

# Render page header
header.render_header(main_container, MAIN_PAGE_HEADER)
main_container.divider()

# Create main page columns with centered layout
_, main_col, __ = main_container.columns(MAIN_PAGE_COLUMN_LAYOUT)

# Create central container within the middle column
central_container = main_col.container()

# Render all uploader components within the column
with main_col:

    # Render sales data uploader component
    sales_uploader.render_sales_uploader(central_container)
    central_container.divider()

    # Render products costs uploader component
    costs_uploader.render_costs_uploader(central_container, ADLS_CATEGORY_PRODUCTS_COSTS, PRODUCTS_COSTS_HEADER)
    central_container.divider()

    # Render other costs uploader component
    costs_uploader.render_costs_uploader(central_container, ADLS_CATEGORY_OTHER_COSTS, OTHER_COSTS_HEADER)
    