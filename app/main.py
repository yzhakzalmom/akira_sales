import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import base64

# Configurações da página
st.set_page_config(page_title="Upload Arquivos Akira", page_icon="🥋", layout="wide")

# Carrega caminho da logo e converte para base64
logo_path = Path(__file__).parent / "icons" / "white_logo.png"

# Converte a imagem para base64 para usar no HTML
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = image_to_base64(logo_path)

# Lógica para carregar planilha de vendas
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='100'>
        <h1 style='text-align: center;'>Uploads Arquivos Akira</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.title("Vendas")
st.write("Carregue a planilha de vendas")

# Lógica para inserir custos com produtos
st.title("Custos")
st.write("Inserir custos")

# Lógica para inserir outros custos
st.title("Outros Custos")
st.write("Inserir outros custos")