from pathlib import Path
from dotenv import load_dotenv
import datetime
import base64

def get_akira_path():
    return Path(__file__).parent.parent.parent

def get_app_path():
    return get_akira_path() / 'app'

def get_asset_file_path(asset_type: str, file_name: str) -> str:
    # Build asset file path
    asset_file_path = get_app_path() / 'assets' / asset_type / file_name

    return asset_file_path

# Load environment variables from .env file in project root
def load_env_file():
    # Get path to .env file in project root
    env_path = get_akira_path() / '.env'
    
    # Load .env file if it exists
    load_dotenv(dotenv_path=env_path)
    
    return env_path

# Return dict in the shape {month_name: month_number}
def get_months() -> dict:

    months = {
    "janeiro": '01',
    "fevereiro": '02',
    "março": '03',
    "abril": '04',
    "maio": '05',
    "junho": '06',
    "julho": '07',
    "agosto": '08',
    "setembro": '09',
    "outubro": '10',
    "novembro": '11',
    "dezembro": '12'
    }

    return months

# Return list containing every year since 2025
def get_years() -> list[int]:
    # Create year list containt 2025
    years_list = [2025]

    # Get today year
    today_year = datetime.datetime.now().year

    # Update years list with years until today
    years_list += [str(year + 1) for year in range(years_list[0], today_year)]

    return years_list

# Return image as base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()