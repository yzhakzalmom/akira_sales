# Akira Sales

A Streamlit-based web application for uploading and managing sales data, product costs, and other costs to Azure Data Lake Storage (ADLS). The application provides an intuitive interface for data uploads and month-end closing job executions.

## Features

- **Sales Data Upload**: Upload sales spreadsheets to ADLS bronze layer
- **Cost Management**: Upload product costs and other costs separately
- **Job Execution**: Execute month-end closing processes
- **Data Validation**: Preview and validate uploaded data before processing
- **Azure Integration**: Seamless integration with Azure Data Lake Storage

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose (optional, for containerized deployment)
- Azure and Databricks credentials configured (for ADLS and Databricks Notebooks and Jobs access)

## Project Structure

```
akira_sales/
├── app/                    # Streamlit application
│   ├── components/         # Reusable UI components
│   ├── pages/              # Streamlit pages
│   └── Home.py            # Main application entry point
├── src/                    # Source code
│   ├── services/           # Business logic and ADLS integration
│   ├── utils/              # Utility functions and constants
│   └── functions/          # Helper functions
├── pyproject.toml          # Project dependencies and metadata
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
└── .dockerignore           # Docker ignore patterns
```

## Installation

### Local Development

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/yzhakzalmom/akira_sales.git
   cd akira_sales
   ```

2. **Install dependencies using uv**:
   ```bash
   uv run pip install -e .
   ```

3. **Configure environment variables**:
   Create a `.env` file with your Azure and Databricks credentials based on `.env.example` file

4. **Run the application**:
   ```bash
   uv run streamlit run app/Home.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`

## Docker Deployment

### Build and Run with Docker Compose

The easiest way to run the application in a containerized environment:

```bash
docker compose up --build
```

This will:
- Build the Docker image
- Start the container
- Expose the application on port `8081` (mapped to container port 8501)

Access the application at: `http://localhost:8081`

### Build Docker Image Manually

```bash
docker build -t streamlit-app:v1 .
```

### Run Docker Container

```bash
docker run -p 8081:8501 streamlit-app:v1
```

## Azure Container Apps Deployment

This application is configured for deployment to Azure Container Apps. The Dockerfile is optimized for Azure environments:

- Listens on `0.0.0.0` for proper network binding
- Exposes port 8501 for Streamlit
- Uses multi-stage build approach with `uv` for efficient package management

### Deployment Steps

1. **Build and push the image to Azure Container Registry (ACR)**:
   ```bash
   az acr build --registry <your-registry-name> --image streamlit-app:v1 .
   ```

2. **Deploy to Azure Container Apps**:
   Use the Azure Portal or Azure CLI to deploy the container image to your Container App environment.

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

- **Components** (`app/components/`): Reusable Streamlit components
- **Services** (`src/services/`): Business logic, ADLS client, data operations
- **Utils** (`src/utils/`): Constants and helper functions

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

