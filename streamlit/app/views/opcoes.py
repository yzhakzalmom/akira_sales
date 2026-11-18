"""
Options page.
Allows users to define parameters for inputs and execution.
"""

import streamlit as st
from components import header, products_setting, taxes_setting
from utils.constants import *


def render() -> None:
    config_container = st.container()

    header.render_header(config_container, CONFIG_PAGE_HEADER)
    config_container.divider()

    _, main_col, __ = config_container.columns(CONFIG_PAGE_COLUMN_LAYOUT)
    central_container = main_col.container()

    with main_col:
        taxes_setting.render_taxes_settings(central_container)
        central_container.divider()
        products_setting.render_products_settings(central_container)
