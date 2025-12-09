import streamlit as st
from pathlib import Path
from components import header, sales_uploader, costs_uploader

# Page settings
st.set_page_config(page_title="Akira ~ Uploads", page_icon="🥋", layout="wide")

# Create main page container
main_container = st.container()

# Render header
header.render_header(main_container)
main_container.divider()

# Create main page columns
_, main_col, __ = main_container.columns([1, 4, 1])

# Create central container
central_container = main_col.container()

# Render within the column
with main_col:

    # Render sales uploader
    sales_uploader.render_sales_uploader(central_container)
    central_container.divider()

    # Lógica para inserir custos com produtos
    costs_uploader.render_costs_uploader(central_container, 'products_costs')
    central_container.divider()

    # Lógica para inserir outros custos
    central_container.title("Outros Custos")
    central_container.write("Inserir outros custos")