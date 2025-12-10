# Akira Sales Management System 🥋

A comprehensive sales data management and processing system designed to handle Mercado Livre sales data, product costs, and other business costs. The system provides a user-friendly Streamlit web interface for data uploads and implements a robust data pipeline using a medallion architecture. The final purpose is to present insights on the sales data to the client on PowerBI.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Development](#development)
- [Technologies](#technologies)

## ✨ Features

- **Sales Data Upload**: Upload and process monthly sales sheets from Mercado Livre
- **Cost Management**: Upload and manage product costs and other business costs
- **Data Validation**: Automatic format checking and validation of uploaded files
- **Data Processing**: Automated data transformation pipeline with bronze, silver, and gold layers
- **Dashboard Integration**: Processed data ready for Power BI dashboards
- **Workflow Orchestration**: Apache Airflow integration for automated data processing workflows

## 📁 Project Structure

```
akira_sales/
├── app/                    # Streamlit web application
│   ├── assets/            # Static assets (icons, texts, placeholder data)
│   ├── components/        # UI components (uploaders, header, general)
│   └── main.py            # Main Streamlit app entry point
├── data/                  # Data storage (medallion architecture)
│   ├── bronze/           # Raw data layer
│   ├── silver/           # Cleaned/transformed data layer
│   └── gold/             # Final processed data layer
├── notebooks/             # Jupyter notebooks for data processing
│   ├── BS_treat_sales_sheet.ipynb
│   ├── GG_identify_products.ipynb
│   └── SG_clean_sales.ipynb
├── src/                   # Source code
│   ├── functions/        # Helper functions
│   ├── services/         # Business logic services
│   └── utils/            # Utility functions
├── dashboards/           # Power BI dashboard files
└── main.py               # CLI entry point
```

## 🔧 Requirements

- Python >= 3.12
- Windows OS (uses `pywin32` and `xlwings` for Excel integration)

## 🚀 Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd akira_sales
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

## 💻 Usage

### Running the Streamlit Application

To start the web interface for uploading and managing sales data:

```bash
streamlit run app/main.py
```

The application will open in your default web browser, typically at `http://localhost:8501`.

### Using the Application

1. **Upload Sales Sheet**:
   - Select the month and year for the sales data
   - Upload the Excel file containing sales data
   - Review the preview
   - Click "Enviar arquivo" to save

2. **Upload Product Costs**:
   - Fill products costs table
   - Review and confirm

3. **Upload Other Costs**:
   - Fill other business costs
   - Review and confirm

### Data Processing

The system uses a medallion architecture:

- **Bronze Layer**: Raw uploaded data stored as-is
- **Silver Layer**: Cleaned and validated data
- **Gold Layer**: Final processed data ready for analysis and dashboards

Data processing workflows can be orchestrated using Apache Airflow.

## 🔄 Data Pipeline

The project implements a medallion data architecture:

1. **Bronze (Raw)**: Initial data uploads stored in `data/bronze/`
2. **Silver (Cleaned)**: Processed and validated data in `data/silver/`
3. **Gold (Final)**: Aggregated and enriched data in `data/gold/`

Jupyter notebooks in the `notebooks/` directory handle the transformation steps:
- `BS_treat_sales_sheet.ipynb`: Initial sales sheet treatment
- `GG_identify_products.ipynb`: Product identification and matching
- `SG_clean_sales.ipynb`: Final sales data cleaning

## 🛠️ Development

### Project Setup

The project uses `uv` for dependency management. The `pyproject.toml` file contains all project dependencies and metadata.

### Key Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **OpenPyXL / xlwings**: Excel file handling
- **Apache Airflow**: Workflow orchestration
- **Pillow**: Image processing for UI assets

### Code Structure

- `app/components/`: Reusable UI components
- `src/services/`: Business logic and data services
- `src/utils/`: Utility functions and helpers
- `src/functions/`: Data processing functions

## 🏗️ Technologies

- **Python 3.12+**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data processing
- **Apache Airflow 3.1.4**: Workflow orchestration
- **OpenPyXL**: Excel file reading/writing
- **xlwings**: Excel automation (Windows)
- **Power BI**: Business intelligence and visualization

## 📝 License

[Add your license information here]

## 👥 Contributors

- Yzhak Zalmom ([GitHub](https://github.com/yzhakzalmom))

---

**Version**: 0.1.0

