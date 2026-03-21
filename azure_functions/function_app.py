import azure.functions as func
from features.monthly_executions import bp as monthly_executions_bp

# Create funcion app object
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Register blueprint function in the function app
app.register_functions(monthly_executions_bp)