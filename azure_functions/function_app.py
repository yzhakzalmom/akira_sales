import azure.functions as func
import logging
from features.monthly_pipeline import bp as monthly_automation_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

app.register_functions(monthly_automation_bp)