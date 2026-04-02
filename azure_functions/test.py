from src.etl.month_closing import *

treat_sales_sheet('2026', '03')
clean_sales('2026', '03')
identify_products('2026', '03')