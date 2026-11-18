"""
Uploads page.
Allows users to upload sales data, products costs, and other costs to ADLS.
"""

import streamlit as st
from components import header, sales_uploader, costs_uploader
from utils.constants import *


def render() -> None:
    main_container = st.container()

    header.render_header(main_container, MAIN_PAGE_HEADER)
    main_container.divider()

    _, main_col, __ = main_container.columns(MAIN_PAGE_COLUMN_LAYOUT)
    central_container = main_col.container()

    with main_col:
        sales_uploader.render_sales_uploader(central_container)
        central_container.divider()

        costs_uploader.render_costs_uploader(
            central_container, ADLS_CATEGORY_PRODUCTS_COSTS, PRODUCTS_COSTS_HEADER
        )
        central_container.divider()

        costs_uploader.render_costs_uploader(
            central_container, ADLS_CATEGORY_OTHER_COSTS, OTHER_COSTS_HEADER
        )
