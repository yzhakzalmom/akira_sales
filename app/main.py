import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(page_title="Akira", page_icon=":robot_face:", layout="wide")

# Lógica para carregar planilha de vendas
st.title("Vendas")
st.write("Carregue a planilha de vendas")

# Lógica para inserir custos com produtos
st.title("Custos")
st.write("Inserir custos")

# Lógica para inserir outros custos
st.title("Outros Custos")
st.write("Inserir outros custos")