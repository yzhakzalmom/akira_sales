# Constants Extraction Guide

## What Are Magic Strings/Numbers?

**Magic strings/numbers** are hardcoded values in your code that have meaning but aren't self-documenting. They make code harder to maintain, test, and understand.

## Examples from Your Codebase

### 🔴 **Current Code (With Magic Values)**

#### Example 1: File Paths
```python
# src/services/save_data.py
file_subpath = f'bronze/sales/sales_{year}_{month}.xlsx'  # Magic strings: 'bronze', 'sales', 'sales_', '.xlsx'
file_subpath = f'bronze/costs/{cost_type}/costs_{year}_{month}.csv'  # Magic strings repeated
```

#### Example 2: Column Names
```python
# app/components/costs_uploader.py
empty_costs_df['Descrição'] = empty_costs_df['Descrição'].astype(str)  # Magic string: 'Descrição'
costs_df['Mês'] = [month] * len(costs_df)  # Magic string: 'Mês'
costs_df['Ano'] = [year] * len(costs_df)  # Magic string: 'Ano'
costs_df['Custo'].notna().all()  # Magic string: 'Custo'
```

#### Example 3: Error Messages
```python
# src/services/check_data.py
if row[sales_df.columns[0]] == 'Vendas':  # Magic string: 'Vendas'
    ...
raise Exception('Arquivo não está no formato padrão da planilha de vendas')  # Magic string
```

#### Example 4: UI Text
```python
# app/components/costs_uploader.py
container.button('Enviar informações', ...)  # Magic string
container.error('Erro no upload', ...)  # Magic string
container.caption('Preencha com seus custos')  # Magic string
```

#### Example 5: Numeric Values
```python
# src/services/check_data.py
headers_idx = 0  # Magic number: what does 0 mean?
preview_df = sales_df.iloc[5:15]  # Magic numbers: why 5? why 15?
```

#### Example 6: File Patterns
```python
# src/services/read_data.py
text_path = get_asset_file_path('texts', f'{text_file_name}.md')  # Magic strings: 'texts', '.md'
df_path = get_asset_file_path('dataframes', f'{df_name}.csv')  # Magic strings: 'dataframes', '.csv'
```

## ✅ **Benefits of Extracting Constants**

1. **Single Source of Truth**: Change a value once, it updates everywhere
2. **Type Safety**: Catch typos at import time, not runtime
3. **Self-Documenting**: Constants have meaningful names
4. **Easier Testing**: Mock or override constants in tests
5. **Refactoring**: Find all usages with IDE "Find References"
6. **Internationalization**: Easy to swap constants for translations

## 📝 **How to Extract Constants**

### Step 1: Create a Constants Module

Create `src/utils/constants.py` with organized constants:

```python
# src/utils/constants.py

# ============================================================================
# DATA LAYER PATHS
# ============================================================================
DATA_LAYER_BRONZE = "bronze"
DATA_LAYER_SILVER = "silver"
DATA_LAYER_GOLD = "gold"

DATA_CATEGORY_SALES = "sales"
DATA_CATEGORY_COSTS = "costs"

# ============================================================================
# FILE PATTERNS
# ============================================================================
SALES_FILE_PREFIX = "sales_"
COSTS_FILE_PREFIX = "costs_"
SALES_FILE_EXTENSION = ".xlsx"
COSTS_FILE_EXTENSION = ".csv"

# ============================================================================
# COLUMN NAMES
# ============================================================================
COL_DESCRICAO = "Descrição"
COL_MES = "Mês"
COL_ANO = "Ano"
COL_CUSTO = "Custo"

# ============================================================================
# SALES SHEET VALIDATION
# ============================================================================
SALES_SHEET_HEADER = "Vendas"
SALES_SHEET_PREVIEW_START_ROW = 5
SALES_SHEET_PREVIEW_END_ROW = 15
SALES_SHEET_HEADER_NOT_FOUND_INDEX = 0

# ============================================================================
# ASSET PATHS
# ============================================================================
ASSET_TYPE_TEXTS = "texts"
ASSET_TYPE_DATAFRAMES = "dataframes"
ASSET_TYPE_ICONS = "icons"
TEXT_FILE_EXTENSION = ".md"
CSV_FILE_EXTENSION = ".csv"

# ============================================================================
# UI MESSAGES
# ============================================================================
MSG_UPLOAD_SUCCESS = "Upload bem sucedido!"
MSG_UPLOAD_ERROR = "Erro no upload"
MSG_FILE_EXISTS = "Parece que essas informações já existiam. Substituindo arquivo de {save_type} de {month}/{year}. "
MSG_SALES_SHEET_FORMAT_ERROR = "Arquivo não está no formato padrão da planilha de vendas"
MSG_FILL_COSTS = "Preencha com seus custos"
MSG_SEND_INFO = "Enviar informações"
MSG_SEND_FILE = "Enviar arquivo"
MSG_FILE_ERROR = "Erro no arquivo. Tem certeza que escolheu o arquivo certo?"

# ============================================================================
# SAVE TYPES
# ============================================================================
SAVE_TYPE_VENDAS = "vendas"
SAVE_TYPE_CUSTOS = "custos"

# ============================================================================
# UI ICONS
# ============================================================================
ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
```

### Step 2: Refactor Your Code

#### Before:
```python
# src/services/save_data.py
def save_sales_sheet(sales_sheet, month: str, year: str):
    file_subpath = f'bronze/sales/sales_{year}_{month}.xlsx'
    message = generate_save_return_message(file_subpath, month, year, 'vendas')
    ...
```

#### After:
```python
# src/services/save_data.py
from utils.constants import (
    DATA_LAYER_BRONZE,
    DATA_CATEGORY_SALES,
    SALES_FILE_PREFIX,
    SALES_FILE_EXTENSION,
    SAVE_TYPE_VENDAS
)

def save_sales_sheet(sales_sheet, month: str, year: str):
    file_subpath = f'{DATA_LAYER_BRONZE}/{DATA_CATEGORY_SALES}/{SALES_FILE_PREFIX}{year}_{month}{SALES_FILE_EXTENSION}'
    message = generate_save_return_message(file_subpath, month, year, SAVE_TYPE_VENDAS)
    ...
```

#### Before:
```python
# app/components/costs_uploader.py
empty_costs_df['Descrição'] = empty_costs_df['Descrição'].astype(str)
costs_df['Mês'] = [month] * len(costs_df)
if (costs_df['Mês'].notna().all()) and (costs_df['Ano'].notna().all()) and (costs_df['Custo'].notna().all()):
    ...
```

#### After:
```python
# app/components/costs_uploader.py
from utils.constants import COL_DESCRICAO, COL_MES, COL_ANO, COL_CUSTO

empty_costs_df[COL_DESCRICAO] = empty_costs_df[COL_DESCRICAO].astype(str)
costs_df[COL_MES] = [month] * len(costs_df)
if (costs_df[COL_MES].notna().all() and 
    costs_df[COL_ANO].notna().all() and 
    costs_df[COL_CUSTO].notna().all()):
    ...
```

## 🎯 **Best Practices**

1. **Group Related Constants**: Use sections with comments
2. **Use Descriptive Names**: `COL_MES` is better than `MONTH_COL`
3. **Follow Naming Conventions**: UPPER_SNAKE_CASE for constants
4. **Document Complex Constants**: Add comments for non-obvious values
5. **Keep Constants Immutable**: Don't modify them at runtime
6. **Organize by Domain**: Group by feature/domain (UI, Data, Validation, etc.)

## 📊 **When NOT to Extract**

- **One-time use**: If a string is used only once and very context-specific
- **User input**: Values that come from user input shouldn't be constants
- **Calculated values**: Values derived from other values
- **Temporary/debug values**: Values that change frequently during development

## 🔄 **Migration Strategy**

1. Start with the most frequently used strings/numbers
2. Extract one module at a time
3. Update imports as you go
4. Test after each module refactor
5. Use IDE "Find and Replace" carefully (check context)

