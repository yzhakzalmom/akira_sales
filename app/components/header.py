# Render header with logo and title
def render_header(container) -> None:
    from utils.helpers import get_asset_file_path, image_to_base64
    import streamlit as st

    # Find logo path
    logo_path = get_asset_file_path('icons', 'white_logo.png')

    # Load logo as base64
    logo_base64 = image_to_base64(logo_path)

    # Create header container
    header_container = container.container()

    # Render logo and title
    header_container.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='100'>
        <h1 style='text-align: center;'>Uploads de Arquivos</h1>
    </div>
    """,
    unsafe_allow_html=True
)