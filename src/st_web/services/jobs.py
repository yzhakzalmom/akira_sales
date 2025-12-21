"""
Service module for interacting with Databricks Jobs API.
Handles job execution, status checking, and run management.
"""

import os
import requests
from dotenv import load_dotenv
from utils.constants import *

# Load environment variables from .env file
load_dotenv()

# Get Databricks configuration from environment variables
DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# HTTP headers for Databricks API requests
headers = {
"Authorization": f"Bearer {DATABRICKS_TOKEN}",
"Content-Type": "application/json"
}

def get_active_runs():
    """
    Check if there are any active runs for the configured Databricks job.
    
    Returns:
        bool: True if there are active runs, False otherwise.
              Returns True on error to prevent concurrent executions.
    """
    url = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/list"

    params = {
    "job_id": DATABRICKS_JOB_ID,
    "active_only": "true"
    }

    try:
        # Make API request to get active runs
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        runs = data.get('runs', [])
        
        # Return True if any active runs exist
        if runs:
            return True
        return False
    except:
        # On error, return True to be safe and prevent concurrent executions
        return True
 

def check_active_run(container):
    """
    Check for active runs and display error message in the UI if found.
    
    Args:
        container: Streamlit container object for displaying messages.
    
    Returns:
        bool: True if there are active runs or an error occurred, False otherwise.
    """
    url = f"{DATABRICKS_HOST}/api/2.1/jobs/runs/list"

    params = {
    "job_id": DATABRICKS_JOB_ID,
    "active_only": "true"
    }

    try:
        # Make API request to get active runs
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        runs = data.get('runs', [])
        
        # If active runs exist, show error and return True
        if runs:
            container.error(MSG_ACTIVE_RUN, icon=ICON_ERROR)
            return True
        return False
    except:
        # On error, show error message and return True
        container.error(MSG_CHECK_RUN_ERROR, icon=ICON_ERROR)
        return True

def trigger_job(container, month: str, year: str):
    """
    Trigger a Databricks job execution with the specified month and year parameters.
    
    Args:
        container: Streamlit container object for displaying messages.
        month: Month string to pass as job parameter.
        year: Year string to pass as job parameter.
    """
    url = f"{DATABRICKS_HOST}/api/2.2/jobs/run-now"

    # Prepare job parameters payload
    payload = {
    "job_id": DATABRICKS_JOB_ID,
    "job_parameters": {
        "month": month,
        "year": year
        }
    }

    try:
        # Make API request to trigger the job
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Extract run ID from response
        data = response.json()
        run_id = data["run_id"]
        
        # Display success message
        container.success(MSG_RUN_STARTED, icon=ICON_SUCCESS)
    
    except:
        # Display error message if job trigger fails
        container.error(MSG_RUN_ERROR, icon=ICON_ERROR)

