import streamlit as st
from pathlib import Path
from components import header, sales_uploader

# Page settings
st.set_page_config(page_title="Akira ~ Uploads", page_icon="🥋", layout="wide")

# Create main page container
main_container = st.container()

# Create main page columns
_, main_col, __ = main_container.columns([1, 4, 1])

# Create central container
central_container = main_col.container()

# Render within the column
with main_col:

    # Render header
    header.render_header(central_container)

    # Render sales uploader
    sales_uploader.render_sales_uploader(central_container)

    central_container.divider()

    # Lógica para inserir custos com produtos
    central_container.title("Custos")
    central_container.write("Inserir custos")

    central_container.divider()

    # Lógica para inserir outros custos
    central_container.title("Outros Custos")
    central_container.write("Inserir outros custos")