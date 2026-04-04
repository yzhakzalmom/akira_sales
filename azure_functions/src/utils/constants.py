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
ADLS_LAYER_CONFIG = 'config'

ADLS_CATEGORY_SALES = "sales"
ADLS_CATEGORY_PRODUCTS_COSTS = "products_costs"
ADLS_CATEGORY_OTHER_COSTS = "other_costs"
ADLS_CATEGORY_PRODUCTS_PER_SALE = 'products_per_sale'
ADLS_CATEGORY_TAXES = 'taxes'
ADLS_CATEGORY_TAX_PER_SALE = 'tax_per_sale'
# ============================================================================
# FILE PATTERNS AND NAMING
# ============================================================================
SALES_FILE_PREFIX = "sales"
COSTS_FILE_PREFIX = "costs"
RAW_FILE_PREFIX = 'raw'
TREATED_FILE_PREFIX = 'treated'
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
COL_INCLUIR_LUCRO = "Incluir no Lucro"

TAXES_COL_MES = 'Mês'
TAXES_COL_NUM_MES = 'num_mes'
TAXES_COL_PCT = 'Imposto (%)'
TAXES_COL_OBS = 'Observação'
TAXES_COL_YEAR = 'ano'
TAXES_COLS = [TAXES_COL_NUM_MES, TAXES_COL_MES, TAXES_COL_PCT, TAXES_COL_OBS, TAXES_COL_YEAR]

PLACEHOLDER_PRODUCTS_COSTS_COLS = [COL_DESCRICAO, COL_CUSTO]
PRODUCTS_COSTS_COLS = [COL_DESCRICAO, COL_CUSTO, COL_MES, COL_ANO]

PLACEHOLDER_OTHER_COSTS_COLS = [COL_DESCRICAO, COL_CUSTO, COL_INCLUIR_LUCRO]
OTHER_COSTS_COLS = [COL_DESCRICAO, COL_CUSTO, COL_INCLUIR_LUCRO, COL_MES, COL_ANO]

PLACEHOLDER_COLS = {
    ADLS_CATEGORY_OTHER_COSTS: PLACEHOLDER_OTHER_COSTS_COLS,
    ADLS_CATEGORY_PRODUCTS_COSTS: PLACEHOLDER_PRODUCTS_COSTS_COLS
}

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
# List of required suffixes to mantain in the sheet
SALES_SHEET_REQUIRED_SUFFIXES = ['Vendas', 'Anúncios', 'Publicidade']

# ============================================================================
# ASSET DIRECTORY AND FILE NAMES
# ============================================================================
ASSET_TYPE_TEXTS = "texts"
ASSET_TYPE_DATAFRAMES = "dataframes"
ASSET_TYPE_ICONS = "icons"

SALES_UPLOADER_TEXT_FILE_NAME = 'sales_uploader'
JOBS_EXECUTION_TEXT_FILE_NAME = 'job_execution'
TAXES_SETTINGS_FILE_NAME = 'taxes_settings'

WHITE_LOGO_FILE_NAME = 'white_logo.png'
BLACK_LOGO_FILE_NAME = 'black_logo.png'

# ============================================================================
# STREAMLIT TITLES, HEADERS AND CONFIG
# ============================================================================

# UPLOADS
MAIN_PAGE_TITLE = 'Akira ~ Uploads'
MAIN_PAGE_LAYOUT = 'wide'
MAIN_PAGE_HEADER = 'Uploads de Arquivos'
MAIN_PAGE_COLUMN_LAYOUT = [1, 4, 1]
SALES_UPLOADER_HEADER = 'Planilha de Vendas 📈'
SALES_PREVIEW_SUBHEADER = 'Prévia do arquivo'
PRODUCTS_COSTS_HEADER = 'Custos com produtos 🥋'
OTHER_COSTS_HEADER = 'Outros Custos 📊'
COSTS_DATA_EDITOR_NUM_ROWS = 'dynamic'

# JOBS
JOBS_PAGE_TITLE = 'Akira ~ Execuções'
JOBS_PAGE_LAYOUT = 'wide'
JOBS_PAGE_HEADER = 'Execuções - Fechamento de Mês'
JOBS_PAGE_COLUMN_LAYOUT = [1, 4, 1]
JOBS_EXECUTION_HEADER = 'Execução do Fechamento'
JOB_FILE_CONF_SUBHEADER = 'Confirmação de arquivos'

# CONFIG
CONFIG_PAGE_TITLE = 'Akira ~ Opções'
CONFIG_PAGE_LAYOUT = 'wide'
CONFIG_PAGE_HEADER = 'Opções - Parâmetros e Predefinições'
CONFIG_PAGE_COLUMN_LAYOUT = [1, 4, 1]

TAXES_SETTINGS_HEADER = 'Imposto Mensal 🏦'
TAXES_DATA_EDITOR_NUM_ROWS = 'fixed'
TAXES_DATA_EDITOR_HEIGHT = 'content'
TAXES_PCT_COL_MIN = 1
TAXES_PCT_COL_MAX = 100

# DATE INPUT
DATE_INPUT_MONTH_LABEL = 'Mês do arquivo'
DATE_INPUT_YEAR_LABEL = 'Ano do arquivo'
DATE_INPUT_COLUMN_LAYOUT = [1, 1, 2]
DATE_INPUT_COLUMN_GAP = 'medium'

# GENERAL
COMPONENTS_WIDTH = 'stretch'

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
MSG_TRIGGER_JOB = 'Iniciar execução'
MSG_RUN_DONE = 'Fechamento de mês executado com sucesso!'
MSG_RUN_ERROR = 'Erro na execução'
MSG_CHECK_RUN_ERROR = 'Não foi possível checar as execuções ativas'
MSG_ACTIVE_RUN = 'Não é possível executar, há uma execução ativa no momento.'
MSG_JOB_RUNNING = 'Executando fechamento...'
MSG_MONTH_PARAM_NOT_FOUND = 'Parâmetro de Mês ausente'
MSG_YEAR_PARAM_NOT_FOUND = 'Parâmetro de Ano ausente'
MSG_SUCCESSFUL_MONTH_CLOSING = 'Fechamento de mês bem sucedido!'
MSG_FILL_TAXES = 'Preencha o imposto em cada mês'

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
MAIN_ICON = '🥋'

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