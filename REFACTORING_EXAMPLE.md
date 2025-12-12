# Refactoring Example: Using Constants

## Before & After Comparison

### Example: `src/services/check_data.py`

#### ❌ **BEFORE (With Magic Strings/Numbers)**

```python
# Checks if the sales sheet pattern is correct and return sheet preview
def check_sales_sheet_format(container, sales_sheet) -> None:
    import pandas as pd

    # Read sales sheet into a dataframe
    sales_df = pd.read_excel(sales_sheet)

    # Variable to hold headers index. It will be incresed below
    headers_idx = 0  # ❌ Magic number: what does 0 mean?

    # Loop over the rows to find headers row
    for idx, row in sales_df.iterrows():

        # Search for 'Vendas', sheet's first header
        if row[sales_df.columns[0]] == 'Vendas':  # ❌ Magic string: 'Vendas'
            # Update header index with headers row index
            headers_idx += idx + 1
            break

    # If this header was not found, the file has a wrong pattern
    if headers_idx == 0:  # ❌ Magic number repeated
        raise Exception('Arquivo não está no formato padrão da planilha de vendas')  # ❌ Magic string

    # Create current columns list based on the headers
    current_columns = sales_df.iloc[headers_idx].tolist()

    # Create new columns list
    new_columns = [f'{i+1}_{current_columns[i]}' for i in range(len(current_columns))]

    # Update column names
    sales_df.columns = new_columns

    # Create preview dataframe that will be rendered
    preview_df = sales_df.iloc[5:15]  # ❌ Magic numbers: why 5? why 15?

    return preview_df
```

**Problems:**
- `'Vendas'` is hardcoded - what if the header changes?
- `0` appears twice with different meanings (initial value vs. not found)
- `5:15` - why these specific rows? No context
- Error message is hardcoded - can't easily translate or change

---

#### ✅ **AFTER (With Constants)**

```python
from utils.constants import (
    SALES_SHEET_HEADER,
    SALES_SHEET_HEADER_NOT_FOUND_INDEX,
    SALES_SHEET_PREVIEW_START_ROW,
    SALES_SHEET_PREVIEW_END_ROW,
    MSG_SALES_SHEET_FORMAT_ERROR
)

# Checks if the sales sheet pattern is correct and return sheet preview
def check_sales_sheet_format(container, sales_sheet) -> None:
    import pandas as pd

    # Read sales sheet into a dataframe
    sales_df = pd.read_excel(sales_sheet)

    # Variable to hold headers index. It will be increased below
    headers_idx = SALES_SHEET_HEADER_NOT_FOUND_INDEX  # ✅ Clear meaning

    # Loop over the rows to find headers row
    for idx, row in sales_df.iterrows():

        # Search for the sales sheet header identifier
        if row[sales_df.columns[0]] == SALES_SHEET_HEADER:  # ✅ Self-documenting
            # Update header index with headers row index
            headers_idx += idx + 1
            break

    # If this header was not found, the file has a wrong pattern
    if headers_idx == SALES_SHEET_HEADER_NOT_FOUND_INDEX:  # ✅ Consistent comparison
        raise Exception(MSG_SALES_SHEET_FORMAT_ERROR)  # ✅ Centralized message

    # Create current columns list based on the headers
    current_columns = sales_df.iloc[headers_idx].tolist()

    # Create new columns list
    new_columns = [f'{i+1}_{current_columns[i]}' for i in range(len(current_columns))]

    # Update column names
    sales_df.columns = new_columns

    # Create preview dataframe that will be rendered
    preview_df = sales_df.iloc[
        SALES_SHEET_PREVIEW_START_ROW:SALES_SHEET_PREVIEW_END_ROW
    ]  # ✅ Clear intent

    return preview_df
```

**Benefits:**
- ✅ `SALES_SHEET_HEADER` - if header changes, update one place
- ✅ `SALES_SHEET_HEADER_NOT_FOUND_INDEX` - clear meaning of `0`
- ✅ `SALES_SHEET_PREVIEW_START_ROW` and `SALES_SHEET_PREVIEW_END_ROW` - self-documenting
- ✅ `MSG_SALES_SHEET_FORMAT_ERROR` - easy to translate or customize
- ✅ IDE can find all usages with "Find References"
- ✅ Type checkers can catch typos

---

## More Examples

### Example 2: `app/components/costs_uploader.py`

#### ❌ **BEFORE**
```python
def render_costs_inputs(container, cost_type: str):
    empty_costs_df = get_dataframe(f'{cost_type}_placeholder')
    empty_costs_df['Descrição'] = empty_costs_df['Descrição'].astype(str)  # ❌
    final_costs_df = container.data_editor(empty_costs_df, num_rows='dynamic', key=cost_type)
    return final_costs_df

def render_costs_uploader(container, cost_type: str, header: str):
    costs_df['Mês'] = [month] * len(costs_df)  # ❌
    costs_df['Ano'] = [year] * len(costs_df)  # ❌
    if (costs_df['Mês'].notna().all() and  # ❌
        costs_df['Ano'].notna().all() and  # ❌
        costs_df['Custo'].notna().all()):  # ❌
        ...
```

#### ✅ **AFTER**
```python
from utils.constants import COL_DESCRICAO, COL_MES, COL_ANO, COL_CUSTO

def render_costs_inputs(container, cost_type: str):
    empty_costs_df = get_dataframe(f'{cost_type}_placeholder')
    empty_costs_df[COL_DESCRICAO] = empty_costs_df[COL_DESCRICAO].astype(str)  # ✅
    final_costs_df = container.data_editor(empty_costs_df, num_rows='dynamic', key=cost_type)
    return final_costs_df

def render_costs_uploader(container, cost_type: str, header: str):
    costs_df[COL_MES] = [month] * len(costs_df)  # ✅
    costs_df[COL_ANO] = [year] * len(costs_df)  # ✅
    if (costs_df[COL_MES].notna().all() and  # ✅
        costs_df[COL_ANO].notna().all() and  # ✅
        costs_df[COL_CUSTO].notna().all()):  # ✅
        ...
```

**Benefits:**
- ✅ If column name changes (e.g., "Descrição" → "Descrição do Item"), update once
- ✅ Typos caught at import time: `COL_DESCRICAO` vs `COL_DESCRIÇÃO`
- ✅ IDE autocomplete helps prevent errors

---

### Example 3: `src/services/save_data.py`

#### ❌ **BEFORE**
```python
def save_sales_sheet(sales_sheet, month: str, year: str):
    file_subpath = f'bronze/sales/sales_{year}_{month}.xlsx'  # ❌ Multiple magic strings
    message = generate_save_return_message(file_subpath, month, year, 'vendas')  # ❌
    ...

def save_costs_df(costs_df: pd.DataFrame, cost_type:str, month: str, year: str):
    file_subpath = f'bronze/costs/{cost_type}/costs_{year}_{month}.csv'  # ❌ Repeated patterns
    message = generate_save_return_message(file_subpath, month, year, 'custos')  # ❌
    ...
```

#### ✅ **AFTER**
```python
from utils.constants import (
    DATA_LAYER_BRONZE,
    DATA_CATEGORY_SALES,
    DATA_CATEGORY_COSTS,
    SALES_FILE_PREFIX,
    COSTS_FILE_PREFIX,
    SALES_FILE_EXTENSION,
    COSTS_FILE_EXTENSION,
    SAVE_TYPE_VENDAS,
    SAVE_TYPE_CUSTOS
)

def save_sales_sheet(sales_sheet, month: str, year: str):
    file_subpath = (
        f'{DATA_LAYER_BRONZE}/{DATA_CATEGORY_SALES}/'
        f'{SALES_FILE_PREFIX}{year}_{month}{SALES_FILE_EXTENSION}'
    )  # ✅ Clear structure
    message = generate_save_return_message(file_subpath, month, year, SAVE_TYPE_VENDAS)  # ✅
    ...

def save_costs_df(costs_df: pd.DataFrame, cost_type: str, month: str, year: str):
    file_subpath = (
        f'{DATA_LAYER_BRONZE}/{DATA_CATEGORY_COSTS}/{cost_type}/'
        f'{COSTS_FILE_PREFIX}{year}_{month}{COSTS_FILE_EXTENSION}'
    )  # ✅ Consistent pattern
    message = generate_save_return_message(file_subpath, month, year, SAVE_TYPE_CUSTOS)  # ✅
    ...
```

**Benefits:**
- ✅ If file structure changes (e.g., `bronze` → `raw`), update one constant
- ✅ Consistent file naming across the codebase
- ✅ Easy to add new file types or layers

---

## Summary

### Key Takeaways

1. **Extract frequently used strings/numbers** - especially those that appear in multiple places
2. **Use descriptive constant names** - `SALES_SHEET_HEADER` is better than `HEADER`
3. **Group related constants** - organize by domain/feature
4. **Document complex constants** - add comments for non-obvious values
5. **Start small** - refactor one module at a time

### When to Extract

✅ **DO extract:**
- Column names used in multiple places
- File paths and patterns
- Error messages
- UI text that might need translation
- Configuration values
- Magic numbers with business meaning

❌ **DON'T extract:**
- One-time use strings
- User-provided values
- Calculated/derived values
- Temporary debug values

