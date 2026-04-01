# Akira Sales

A Streamlit-based web application for uploading and managing sales data, product costs, and other costs to Azure Data Lake Storage (ADLS). The application provides an intuitive interface for data uploads and month-end closing job executions. All data is stored in Parquet format for optimal performance and cost efficiency.

## Features

- **Sales Data Upload**: Upload sales spreadsheets to ADLS bronze layer
- **Dashboard**: Interactive sales KPIs, trends, and breakdowns (uses mock data to protect client privacy)
- **Cost Management**: Upload product costs and other costs separately
- **Job Execution**: Execute month-end closing processes via Azure Functions
- **Data Validation**: Preview and validate uploaded data before processing
- **Azure Integration**: Seamless integration with Azure Data Lake Storage (ADLS)
- **Automated Data Processing**: Azure Functions automate client data transformations using medallion architecture

## Dashboard

A built-in dashboard provides a quick, visual overview of sales performance and operational costs.

- What you can see
   - Gross Revenue
   - Refunds
   - Estimated Tax
   - Plataform Payout
   - Profit
   - Net Revenue
   - Margin
   - Production Costs
   - Daily Sales
- Data source: This project used Azure Data Lake Storage Gen2 (ADLS Gen 2). However, to protect the client's privacy, the dashboard uses mock/synthetic data. The mock dataset mirrors the real schema so you can safely demo the UI and validate interactions without exposing sensitive information.

## Data Processing Pipeline

The application uses **Azure Functions** to automate data processing workflows with client data. All processed data is stored in Azure Data Lake Storage (ADLS) following the **medallion architecture** (bronze, silver, gold layers).

### Automation Workflow

Azure Function executes a 3-step automated process:

1. **Transform Sales Sheet into DataFrame**: Convert uploaded sales spreadsheets into structured DataFrames for processing
2. **Clean Sales Sheet**: Apply data cleaning operations to ensure data quality and consistency
3. **Identify Products per Sale**: Extract and identify individual products associated with each sale transaction

### Medallion Architecture

Data flows through three layers in ADLS:

- **Bronze Layer**: Raw, unprocessed data as uploaded from the Streamlit application
- **Silver Layer**: Cleaned and validated data after the transformation and cleaning steps
- **Gold Layer**: Final curated data with products identified per sale, ready for analytics and reporting

This architecture ensures data quality, traceability, and enables incremental processing while maintaining the raw data for audit purposes.

### Data Storage Format: Parquet

All treated data in ADLS is stored in **Parquet format** instead of traditional tabular files (CSV, Excel). This choice provides significant advantages for data processing and analytics:

#### Why Parquet?

- **Columnar Storage**: Data is stored column-wise rather than row-wise, enabling efficient column pruning and reducing I/O when querying specific columns
- **Compression**: Advanced compression algorithms (Snappy, Gzip, LZ4) significantly reduce storage costs and improve read/write performance
- **Schema Evolution**: Supports schema changes over time without breaking existing data, essential for evolving business requirements
- **Type Safety**: Preserves data types (dates, decimals, etc.) without conversion issues common in CSV files
- **Performance**: Optimized for analytical workloads, enabling faster queries and aggregations
- **Partitioning**: Efficient partitioning strategies enable faster data filtering and processing at scale

By using Parquet, the pipeline achieves better performance, lower storage costs, and improved data quality compared to traditional tabular file formats.

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose (optional, for containerized deployment)
- Azure credentials and Azure Functions code (simplified key) configured (for ADLS and Azure Functions access). See *streamlit/.env.example*

## Project Structure

```
akira_sales/                         # Root project folder
.
├── README.md                       # Project overview and documentation
├── _archive                        # Deprecated/old code and experiments
├── azure_functions                 # Azure Functions backend service
│   ├── .env.example                # Example environment variables
│   ├── .funcignore                 # Files ignored during Azure deploy
│   ├── .gitignore                  # Git ignore rules
│   ├── .vscode                     # VS Code workspace settings
│   ├── function_app.py             # Main Azure Functions entrypoint
│   ├── host.json                   # Azure Functions configuration
│   ├── pyproject.toml              # Python project configuration
│   ├── requirements.txt            # Python dependencies (fallback/legacy)
│   ├── src                         # Source code for functions
│   └── uv.lock                     # Locked dependency versions (uv)
├── pbi                             # Power BI assets
│   └── mock                        # Mock data for reports/testing
└── streamlit                       # Streamlit frontend application
    ├── .dockerignore               # Docker ignore rules
    ├── .env.example               # Example environment variables
    ├── .gitignore                 # Git ignore rules
    ├── Dockerfile                 # Container definition for app
    ├── README.md                  # Streamlit app documentation
    ├── app                        # Streamlit UI pages/components
    ├── docker-compose.yml         # Multi-container orchestration
    ├── pyproject.toml             # Python project configuration
    ├── src                        # Core application/business logic
    ├── test                       # Unit and integration tests
    └── uv.lock                    # Locked dependency versions (uv)
```

## Installation

### Local Development

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/yzhakzalmom/akira_sales.git
   cd akira_sales/streamlit
   ```

2. **Install dependencies using uv**:
   ```bash
   uv venv
   uv run pip install -e .
   source .venv/Scripts/activate
   ```

3. **Configure environment variables**:
   Create a `.env` file with your Azure and Databricks credentials based on `.env.example` file

4. **Run the application**:
   ```bash
   uv run streamlit run app/Uploads.py
   ```

5. **Access the application**:
   Open your browser and navigate to [http://localhost:8501]

## Docker Deployment

### Build and Run with Docker Compose

The easiest way to run the application in a containerized environment:

```bash
docker compose up -d --build
```

This will:
- Build the Docker image
- Start the container
- Expose the application on port `8081` (mapped to container port 8501)

Access the application at: [http://localhost:8081]

### Build Docker Image Manually

```bash
docker build -t streamlit-app:v1 .
```

### Run Docker Container

```bash
docker run -p 8081:8501 streamlit-app:v1
```

## Azure Resources

***streamlit/*** is deployed to **Azure App Services** for production hosting. The Dockerfile is optimized for Azure environments:

- Listens on `0.0.0.0` for proper network binding
- Exposes port 8501 for Streamlit
- Uses multi-stage build approach with `uv` for efficient package management

***azure_functions*** is deployed to **Azure Functins** for cloud functions executions

### Common steps
1. **Login to Azure via Azure CLI**
   ```bash
   # This will open Microsoft Azure login in a web page
   az login
   ```

1. **Connect with your Azure Container Registry
   ```bash
   az acr login --name <acr_name>
   ```

### Deploy to Azure Container Registry

1. **Build and push the image to Azure Container Registry (ACR)**:
   ```bash
   az acr build --registry <your-registry-name> --image streamlit-app:v1 .
   ```

1. **Alternatively, you can use VS Code extensions**
   - Extensions: *Azure* and *Containers*
   1. Build Docker Image (see *Docker Deployment*)
   1. Double check your Azure extension login
   1. Right click your image in *Containers > Image*
   1. Click *Push...*
   1. Select *Azure Subscription > Registry > Image name*

### Test Azure Functions

1. **Run local environment**
   ```bash
   cd azure_functions
   func start
   ```

2. **Make requests**
   - Use the url [http://localhost:7071/api/month-closing]
   - Use parameters `month` and `year`

### Deploy to Azure App Services
   - Configure Azure App Service to use the container image from ACR
   - Set up continuous deployment (CD) for automatic updates
   - Configure environment variables in Azure App Service settings
   - Use Azure Portal or Azure CLI to deploy and manage the application

#### Azure App Services Benefits

- **Managed Service**: Automatic scaling, patching, and monitoring
- **Integration**: Seamless integration with other Azure services (ADLS, Databricks)
- **Cost-Effective**: Pay only for the resources you use with flexible pricing tiers
- **Security**: Built-in authentication, SSL certificates, and network isolation options

## Usage

### Uploading Sales Data

1. Navigate to the main page
2. Use the **"Planilha de Vendas"** section to upload your sales spreadsheet
3. Preview the data to ensure correctness
4. Select the month and year for the data
5. Click upload to send the file to ADLS

### Uploading Costs

1. Use the **"Custos com produtos"** section for product costs
2. Use the **"Outros Custos"** section for other operational costs
3. Fill in the required fields (description, cost, month, year)
4. Upload to ADLS

### Job Execution

1. Navigate to the **"Execução"** page
2. Configure the files for month-end closing
3. Execute the closing process

### Taxes Settings
1. Navigate to the **Opções** page
1. Input taxes information for the chosen year
1. Upload do ADLS

## Development

### Project Dependencies

The project uses modern Python packaging with `pyproject.toml`. Main dependencies include:

- **Streamlit**: Web framework for the UI
- **Pandas**: Data manipulation and analysis
- **Azure Storage File Datalake**: Azure ADLS integration
- **Azure Identity**: Authentication for Azure services

See `pyproject.toml` for the complete list of dependencies.

### Adding New Dependencies

To add a new dependency:

1. Update `pyproject.toml` with the new package
2. Reinstall the package:
   ```bash
   uv run pip install -e .
   ```

### Code Structure

- **Components** (`streamlit/app/components/`): Reusable Streamlit components
- **Services** (`streamlit/src/services/`): Business logic, ADLS client, data operations
- **Utils** (`streamlit/src/utils/`): Constants and helper functions

## Environment Variables

The application required environment variables are described in `.env.example`

## Troubleshooting

### Port Already in Use

If port 8501 is already in use, you can change the port in the Streamlit command:
```bash
uv run streamlit run app/Home.py --server.port 8502
```

Or modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8082:8501"
```

### Docker Build Issues

If you encounter issues building the Docker image:

1. Ensure you have the latest version of Docker
2. Check that all required files are present (not ignored by `.dockerignore`)
3. Verify the `pyproject.toml` file is valid

### Azure Connection Issues

If you're having trouble connecting to Azure ADLS:

1. Verify your Azure credentials are correctly configured
2. Check network connectivity and firewall rules
3. Ensure your Azure service principal or managed identity has the necessary permissions

## Contributing

1. Create a feature branch
2. Make your changes
3. Test locally using `uv run streamlit run app/Home.py`
4. Submit a pull request

## Support

For issues and questions, please [create an issue](https://github.com/yzhakzalmom/akira_sales/issues) or contact the development team.

