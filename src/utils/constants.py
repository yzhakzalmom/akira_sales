"""
Application-wide constants.

This module contains all magic strings, numbers, and configuration values
used throughout the application. Extracting these makes the codebase more
maintainable, testable, and self-documenting.
"""

# ============================================================================
# DATA LAYER PATHS
# ============================================================================
DATA_LAYER_BRONZE = "bronze"
DATA_LAYER_SILVER = "silver"
DATA_LAYER_GOLD = "gold"

DATA_CATEGORY_SALES = "sales"
DATA_CATEGORY_COSTS = "costs"

# ============================================================================
# FILE PATTERNS AND NAMING
# ============================================================================
SALES_FILE_PREFIX = "sales_"
COSTS_FILE_PREFIX = "costs_"
SALES_FILE_EXTENSION = ".xlsx"
COSTS_FILE_EXTENSION = ".csv"
TEXT_FILE_EXTENSION = ".md"
CSV_FILE_EXTENSION = ".csv"

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
SALES_SHEET_HEADER = "Vendas"
# Index indicating header was not found
SALES_SHEET_HEADER_NOT_FOUND_INDEX = 0
# Row range for preview display (5:15 means rows 5 to 14, inclusive)
SALES_SHEET_PREVIEW_START_ROW = 5
SALES_SHEET_PREVIEW_END_ROW = 15

# ============================================================================
# ASSET DIRECTORY NAMES
# ============================================================================
ASSET_TYPE_TEXTS = "texts"
ASSET_TYPE_DATAFRAMES = "dataframes"
ASSET_TYPE_ICONS = "icons"

# ============================================================================
# UI MESSAGES (Portuguese)
# ============================================================================
MSG_UPLOAD_SUCCESS = "Upload bem sucedido!"
MSG_UPLOAD_ERROR = "Erro no upload"
MSG_FILE_ERROR = "Erro no arquivo. Tem certeza que escolheu o arquivo certo?"
MSG_FILL_COSTS = "Preencha com seus custos"
MSG_SEND_INFO = "Enviar informações"
MSG_SEND_FILE = "Enviar arquivo"
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

