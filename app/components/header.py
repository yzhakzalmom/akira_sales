from utils.helpers import get_asset_file_path, image_to_base64
from utils.constants import *

# Render header with logo and title
def render_header(container) -> None:

    # Find logo path
    logo_path = get_asset_file_path(ASSET_TYPE_ICONS, WHITE_LOGO_FILE_NAME)

    # Load logo as base64
    logo_base64 = image_to_base64(logo_path)

    # Create header container
    header_container = container.container()

    # Render logo and title
    header_container.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='100'>
        <h1 style='text-align: center;'>{MAIN_PAGE_HEADER}</h1>
    </div>
    """,
    unsafe_allow_html=True
)