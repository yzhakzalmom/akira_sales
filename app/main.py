import streamlit as st
from pathlib import Path
from components import header, sales_uploader

# Page settings
st.set_page_config(page_title="Akira ~ Uploads", page_icon="🥋", layout="wide")

# Create main page columns
_, main_col, __ = st.columns([1, 4, 1])

# Render within the column
with main_col:
    
    # Render header
    header.render_header()

    # Render sales uploader
    sales_uploader.render_sales_uploader()

    st.divider()

    # Lógica para inserir custos com produtos
    st.title("Custos")
    st.write("Inserir custos")

    st.divider()

    # Lógica para inserir outros custos
    st.title("Outros Custos")
    st.write("Inserir outros custos")