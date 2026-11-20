"""
Job execution page.
Allows users to trigger Azure Functions after verifying required data files exist.
"""

import streamlit as st
from components import header, jobs_execution
from utils.constants import *


def render() -> None:
    jobs_container = st.container()

    header.render_header(jobs_container, JOBS_PAGE_HEADER)
    jobs_container.divider()

    _, main_col, __ = jobs_container.columns(JOBS_PAGE_COLUMN_LAYOUT)
    central_container = main_col.container()

    with main_col:
        jobs_execution.render_execution_trigger(central_container)
