import azure.functions as func
from src.etl.month_closing import *
from src.utils.constants import *

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="month-closing")
def run_month_closing(req: func.HttpRequest) -> func.HttpResponse:

    try:
        year = req.params.get('year')
        month = req.params.get('month')

        if not year: # return http response indicating the lack of year param
            return func.HttpResponse(
                MSG_YEAR_PARAM_NOT_FOUND,
                status_code=400
            )
    
        if not month: # return http response indicating the lack of month param
            return func.HttpResponse(
                MSG_MONTH_PARAM_NOT_FOUND,
                status_code=400
            )

        # Execute each step of monthly automation
        treat_sales_sheet(year, month) # 1
        clean_sales(year, month) # 2
        identify_products(year, month) # 3
        calculate_taxes(year, month) # 4

        # Return http response indicating success
        return func.HttpResponse(MSG_SUCCESSFUL_MONTH_CLOSING, status_code=200)

    # Return http response indicating value error
    except ValueError as e:
        return func.HttpResponse(str(e), status_code=422)

    # Return http response indicating general errors
    except Exception as e:
        return func.HttpResponse(
            f"Internal Error: {str(e)}",
            status_code=500
        )