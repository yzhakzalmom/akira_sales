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
akira_sales/
├── README.md
├── _archive/                       # Deprecated code and experiments
│   ├── dbc/
│   ├── etl/
│   ├── functions/
│   ├── old_etl/
│   ├── st_web/
│   ├── test_etl/
│   └── unfinished/
├── azure_functions/                # Azure Functions backend
│   ├── .env.example
│   ├── .funcignore
│   ├── .gitignore
│   ├── function_app.py             # Functions entrypoint
│   ├── host.json
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── uv.lock
│   └── src/
│       ├── etl/                    # month_closing
│       ├── functions/              # DataFrame helpers
│       ├── services/               # ADLS, read, save, treat, check
│       └── utils/
├── pbi/
│   ├── dashboards/                 # Power BI report
│   └── mock/                       # Synthetic inputs and outputs
└── streamlit/                      # Streamlit frontend
    ├── .dockerignore
    ├── .env.example
    ├── .gitignore
    ├── Dockerfile
    ├── docker-compose.yml
    ├── pyproject.toml
    ├── README.md
    ├── uv.lock
    ├── app/
    │   ├── Home.py                 # Login gate and navigation
    │   ├── assets/                 # Icons and page texts
    │   ├── components/
    │   └── views/                  # uploads, opcoes, execucao
    ├── scripts/
    │   ├── render_secrets.py       # Builds .streamlit/secrets.toml
    │   └── run.sh                  # Starts the app
    ├── src/
    │   ├── services/
    │   └── utils/
    └── test/
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
   ./scripts/run.sh
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
- Expose the application on port `8501` (mapped to container port 8501)

Access the application at: [http://localhost:8501]

### Build Docker Image Manually

```bash
docker build -t streamlit-app:v1 .
```

### Run Docker Container

```bash
docker run -p 8501:8501 streamlit-app:v1
```

## Azure Resources

***streamlit/*** runs on **Azure App Service** as a single container. Production images live in **Azure Container Registry**. A push to `main` that changes `streamlit/` builds `streamlit-app:<commit sha>`, pushes it, and points the Web App at that tag.

***azure_functions*** runs on **Azure Functions**. A push to `main` that changes `azure_functions/` publishes the whole Function App (Python v2, route `month-closing`).

The `v1` tag in `docker-compose.yml` is only for local runs. App Service does not track it.

### One-time Azure and GitHub setup

The workflows sign in with OpenID Connect. Create an app registration (or user-assigned managed identity) and a federated credential:

- Issuer: `https://token.actions.githubusercontent.com`
- Subject: `repo:yzhakzalmom/akira_sales:ref:refs/heads/main`
- Audience: `api://AzureADTokenExchange`

```bash
az ad app federated-credential create \
  --id <application-object-id> \
  --parameters '{
    "name": "github-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:yzhakzalmom/akira_sales:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

Grant that identity `AcrPush` on the registry and `Website Contributor` on the Web App and the Function App.

The Web App pulls images with its own managed identity. Leave the registry admin user disabled, and leave Deployment Center on **Single container** / **Azure Container Registry** with continuous deployment off. The portal option that generates a GitHub Actions workflow stays off; `.github/workflows/` is the only pipeline.

```bash
az webapp identity assign --name <webapp> --resource-group <rg>
PRINCIPAL_ID=$(az webapp identity show --name <webapp> --resource-group <rg> --query principalId -o tsv)
ACR_ID=$(az acr show --name <acr_name> --query id -o tsv)
az role assignment create --assignee "$PRINCIPAL_ID" --role AcrPull --scope "$ACR_ID"
az webapp config set \
  --name <webapp> \
  --resource-group <rg> \
  --generic-configurations '{"acrUseManagedIdentityCreds": true}'
az webapp config appsettings set \
  --name <webapp> \
  --resource-group <rg> \
  --settings WEBSITES_PORT=8501
```

`WEBSITES_PORT` is required because Streamlit listens on 8501. Other runtime settings stay in the Web App and Function App application settings.

The Function App runtime is Python 3.12. Remote build installs `azure_functions/requirements.txt`, which must stay aligned with `azure_functions/pyproject.toml`.

GitHub repository secrets:

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

GitHub repository variables:

- `ACR_NAME` (short registry name)
- `ACR_LOGIN_SERVER` (for example `myregistry.azurecr.io`)
- `AZURE_WEBAPP_NAME`
- `AZURE_RESOURCE_GROUP`
- `AZURE_FUNCTIONAPP_NAME`

### What runs on merge

| Change on `main` | Workflow | Result |
| --- | --- | --- |
| `streamlit/**` | `.github/workflows/streamlit-acr.yml` | Push `streamlit-app:<sha>` and set that image on the Web App |
| `azure_functions/**` | `.github/workflows/azure-functions.yml` | Publish the Function App with a remote build |

App Service does not look up a new tag on its own. After the push, the Streamlit workflow runs `az webapp config container set`, so the portal image tag changes from the previous value to the commit SHA. To roll back, point the Web App at an older SHA that is still in the registry.

### Build an image locally

From `streamlit/`:

```bash
az acr login --name <acr_name>
az acr build \
  --registry <acr_name> \
  --image streamlit-app:$(git rev-parse HEAD) \
  --file Dockerfile \
  .
```

That push does not update App Service. Point the Web App at the new tag yourself, or merge to `main` and let the workflow do it.

### Test Azure Functions

1. **Run local environment**
   ```bash
   cd azure_functions
   func start
   ```

2. **Make requests**
   - Use the url [http://localhost:7071/api/month-closing]
   - Use parameters `month` and `year`

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
./scripts/run.sh --server.port 8502
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
3. Test locally using `./scripts/run.sh`
4. Submit a pull request

## Support

For issues and questions, please [create an issue](https://github.com/yzhakzalmom/akira_sales/issues) or contact the development team.

