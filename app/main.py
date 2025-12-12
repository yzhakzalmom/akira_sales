import streamlit as st
from pathlib import Path
from components import header, sales_uploader, costs_uploader
from utils.constants import *

# Page settings
st.set_page_config(page_title=MAIN_PAGE_TITLE, page_icon=ICON_MAIN_PAGE, layout=MAIN_PAGE_LAYOUT)

# Create main page container
main_container = st.container()

# Render header
header.render_header(main_container)
main_container.divider()

# Create main page columns
_, main_col, __ = main_container.columns(MAIN_PAGE_COLUMN_LAYOUT)

# Create central container
central_container = main_col.container()

# Render within the column
with main_col:

    # Render sales uploader
    sales_uploader.render_sales_uploader(central_container)
    central_container.divider()

    # Render products costs uploader
    costs_uploader.render_costs_uploader(central_container, 'products_costs', 'Custos com produtos 🥋')
    central_container.divider()

    # Render other costs uploader
    costs_uploader.render_costs_uploader(central_container, 'other_costs', 'Outros Custos 📊')
    