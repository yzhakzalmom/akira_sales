from .general import render_date_input
from services.check_data import check_sales_sheet_format
from services.save_data import save_sales_sheet
from services.read_data import get_text
from utils.constants import *

def render_sheet_preview(container, sales_sheet):

    try: # to check and render sales sheet preview
        sales_preview_df = check_sales_sheet_format(sales_sheet)
        container.subheader(SALES_PREVIEW_SUBHEADER)
        container.dataframe(sales_preview_df)

    except Exception as e:

        # Render error message and description
        container.error(MSG_FILE_ERROR, icon=ICON_ERROR)
        container.write(e)

def render_uploader_button(container, sales_sheet, month: str, year: str):

    # On button click
    if container.button(MSG_SEND_FILE, width=COMPONENTS_WIDTH):

        try: # to save sales sheet

            # Get save message
            message = save_sales_sheet(sales_sheet, month, year)

            # Render success message
            container.success(message, icon=ICON_SUCCESS)

        except Exception as e:
            # Render error message and description
            container.error(MSG_UPLOAD_ERROR, icon=ICON_ERROR)
            container.write(e)

def render_sales_uploader(container) -> None:

    # Create sales uploader container
    sales_up_container = container.container()

    # Render section header and text
    sales_up_container.header(SALES_UPLOADER_HEADER)
    sales_up_container.markdown(get_text(SALES_UPLOADER_TEXT_FILE_NAME))

    # Get chosen month and year and render date input
    month, year = render_date_input(sales_up_container, SALES_UPLOADER_TEXT_FILE_NAME)    

    # Render upload section
    sales_sheet = sales_up_container.file_uploader(
        MSG_SALES_SHEET_UPLOAD,
        type=SALES_SHEET_ALLOWED_TYPES
    )

    # Render button only if there is an uploaded file
    if sales_sheet:

        render_sheet_preview(sales_up_container, sales_sheet)

        render_uploader_button(sales_up_container, sales_sheet, month, year)