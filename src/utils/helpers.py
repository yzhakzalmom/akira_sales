def get_akira_path():
    from pathlib import Path

    return Path(__file__).parent.parent.parent

def get_data_path():
    from pathlib import Path

    return get_akira_path() / 'data'

def get_app_path():
    from pathlib import Path

    return get_akira_path() / 'app'

def get_asset_file_path(asset_type: str, file_name: str) -> str:
    from pathlib import Path

    # Build asset file path
    asset_file_path = get_app_path() / 'assets' / asset_type / file_name

    return asset_file_path

# Return dict in the shape {month_name: month_number}
def get_months() -> dict:

    months = {
    "Janeiro": '01',
    "Fevereiro": '02',
    "Março": '03',
    "Abril": '04',
    "Maio": '05',
    "Junho": '06',
    "Julho": '07',
    "Agosto": '08',
    "Setembro": '09',
    "Outubro": '10',
    "Novembro": '11',
    "Dezembro": '12'
    }

    return months

# Return list containing every year since 2025
def get_years() -> list[int]:
    import datetime

    # Create year list containt 2025
    years_list = [2025]

    # Get today year
    today_year = datetime.datetime.now().year

    # Update years list with years until today
    years_list += [str(year + 1) for year in range(years_list[0], today_year)]

    return years_list

# Return image as base64
def image_to_base64(image_path):
    import base64

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
