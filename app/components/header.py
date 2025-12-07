from utils.helpers import get_asset_file_path

# Return image as base64
def image_to_base64(image_path):
    import base64

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Render header with logo and title
def render_header() -> None:
    import streamlit as st

    # Find logo path
    logo_path = get_asset_file_path('icons', 'white_logo.png')

    # Load logo as base64
    logo_base64 = image_to_base64(logo_path)

    # Render logo and title
    st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='100'>
        <h1 style='text-align: center;'>Uploads de Arquivos</h1>
    </div>
    """,
    unsafe_allow_html=True
)