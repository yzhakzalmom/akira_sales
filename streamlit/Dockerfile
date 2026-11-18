# Use Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY src ./src
COPY app ./app
COPY scripts ./scripts
COPY README.md ./

# Install the project and its dependencies using uv
RUN uv run pip install -e .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
RUN chmod +x scripts/run.sh
CMD ["./scripts/run.sh"]