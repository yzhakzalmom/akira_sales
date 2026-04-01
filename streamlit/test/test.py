from services.read_data import read_tabular
from services.jobs import trigger_job
from utils.constants import *

year = '2025'
taxes_df = read_tabular(layer=ADLS_LAYER_CONFIG, category=ADLS_CATEGORY_TAXES, month=None, year=year)

print(taxes_df)