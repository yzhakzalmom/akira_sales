"""
Application-wide constants.

This module contains all magic strings, numbers, and configuration values
used throughout the application. Extracting these makes the codebase more
maintainable, testable, and self-documenting.
"""

# ============================================================================
# DATA LAYER PATHS
# ============================================================================
ADLS_LAYER_BRONZE = "bronze"
ADLS_LAYER_SILVER = "silver"
ADLS_LAYER_GOLD = "gold"

ADLS_CATEGORY_SALES = "sales"
ADLS_CATEGORY_PRODUCTS_COSTS = "products_costs"
ADLS_CATEGORY_OTHER_COSTS = "other_costs"

# ============================================================================
# FILE PATTERNS AND NAMING
# ============================================================================
SALES_FILE_PREFIX = "sales_"
COSTS_FILE_PREFIX = "costs_"
RAW_FILE_PREFIX = 'raw_'
TREATED_FILE_PREFIX = 'treated_'
PRESENTATION_FILE_PREFIX = 'presentation_'
PLACEHOLDER_SUFIX = '_placeholder'

BRONZE_SALES_FILE_EXTENSION = ".xlsx"
TABULAR_STD_EXTENSION = ".parquet"
TEXT_FILE_EXTENSION = ".md"
CSV_FILE_EXTENSION = ".csv"

CSV_SEP = ';'

# ============================================================================
# DATAFRAME COLUMN NAMES
# ============================================================================
COL_DESCRICAO = "Descrição"
COL_MES = "Mês"
COL_ANO = "Ano"
COL_CUSTO = "Custo"

# ============================================================================
# SALES SHEET VALIDATION
# ============================================================================
# Header that identifies the start of sales data
SALES_SHEET_FIRST_HEADER = "Vendas"
# Index indicating header was not found
SALES_SHEET_HEADER_START_INDEX = 0
# Index indicating header was not found
SALES_SHEET_HEADER_NOT_FOUND_INDEX = 0
# Row range for preview display (5:15 means rows 5 to 14, inclusive)
SALES_SHEET_PREVIEW_START_ROW = 5
SALES_SHEET_PREVIEW_END_ROW = 15
# Sales sheet cleaning variables
SALES_SHEET_ROWS_DELETE_RANGE = range(4, 0, -1)

# ============================================================================
# ASSET DIRECTORY AND FILE NAMES
# ============================================================================
ASSET_TYPE_TEXTS = "texts"
ASSET_TYPE_DATAFRAMES = "dataframes"
ASSET_TYPE_ICONS = "icons"

SALES_UPLOADER_TEXT_FILE_NAME = 'sales_uploader'
WHITE_LOGO_FILE_NAME = 'white_logo.png'
BLACK_LOGO_FILE_NAME = 'black_logo.png'

# ============================================================================
# STREAMLIT TITLES, HEADERS AND CONFIG
# ============================================================================
MAIN_PAGE_TITLE = 'Akira ~ Uploads'
MAIN_PAGE_LAYOUT = 'wide'
MAIN_PAGE_HEADER = 'Uploads de Arquivos'

SALES_UPLOADER_HEADER = 'Planilha de Vendas 📈'
SALES_PREVIEW_SUBHEADER = 'Prévia do arquivo'

DATE_INPUT_MONTH_LABEL = 'Mês do arquivo'
DATE_INPUT_YEAR_LABEL = 'Ano do arquivo'


MAIN_PAGE_COLUMN_LAYOUT = [1, 4, 1]
DATE_INPUT_COLUMN_LAYOUT = [1, 1, 2]
DATE_INPUT_COLUMN_GAP = 'medium'
COMPONENTS_WIDTH = 'stretch'
DATA_EDITOR_NUM_ROWS = 'dynamic'

# ============================================================================
# MESSAGES (Portuguese)
# ============================================================================
MSG_UPLOAD_SUCCESS = "Upload bem sucedido!"
MSG_UPLOAD_ERROR = "Erro no upload"
MSG_FILE_ERROR = "Erro no arquivo. Tem certeza que escolheu o arquivo certo?"
MSG_FILE_NOT_FOUND = "Nenhum arquivo encontrado em"
MSG_FILL_COSTS = "Preencha com seus custos"
MSG_SEND_INFO = "Enviar informações"
MSG_SEND_FILE = "Enviar arquivo"
MSG_SALES_SHEET_UPLOAD = 'Envie planilha de vendas'
MSG_SALES_SHEET_FORMAT_ERROR = "Arquivo não está no formato padrão da planilha de vendas"

# Message template for file replacement
MSG_FILE_EXISTS_TEMPLATE = (
    "Parece que essas informações já existiam. "
    "Substituindo arquivo de {save_type} de {month}/{year}. "
)

# ============================================================================
# SAVE OPERATION TYPES
# ============================================================================
SAVE_TYPE_VENDAS = "vendas"
SAVE_TYPE_CUSTOS = "custos"

# ============================================================================
# UI ICONS (Emoji/Unicode)
# ============================================================================
ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
ICON_MAIN_PAGE = '🥋'

# ============================================================================
# UI COMPONENT KEYS
# ============================================================================
# Prefix for button keys
BUTTON_KEY_PREFIX = "btn_"
# Prefix for month selectbox keys
MONTH_KEY_PREFIX = "month_"
# Prefix for year selectbox keys
YEAR_KEY_PREFIX = "year_"

# ============================================================================
# FILE UPLOAD TYPES
# ============================================================================
# Allowed file extensions for sales sheet uploads
SALES_SHEET_ALLOWED_TYPES = ["xlsx", "xls"]

