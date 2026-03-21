import azure.functions as func
from etl.monthly_data_treatment import *

bp = func.Blueprint()

@bp.route(route='monthly-pipeline')
def run_monthly_automation(req: func.HttpRequest) -> func.HttpResponse:

    year = req.params.get('year')
    month = req.params.get('month')

    treat_sales_sheet(year, month)
    clean_sales(year, month)
    identify_products(year, month)

    return func.HttpResponse(str(req.get_json()), status_code=200)