def get_sales_uploader_text() -> str:
    from utils.helpers import get_asset_file_path, get_months
    # Find text path
    text_path = get_asset_file_path('texts', 'sales_uploader.md')

    # Read sales uploader text
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text