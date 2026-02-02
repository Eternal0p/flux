"""
Centralized configuration management for AI Sprint Brain.
Loads environment variables and defines application constants.
"""

import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# API Credentials
def get_gemini_api_key():
    """Get Gemini API key from environment or Streamlit secrets."""
    key = os.getenv('GEMINI_API_KEY')
    if key:
        return key
    try:
        if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            return st.secrets['GEMINI_API_KEY']
    except:
        pass
    return None

def get_drive_folder_id():
    """Get Google Drive folder ID from environment or Streamlit secrets."""
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    if folder_id:
        return folder_id
    try:
        if hasattr(st, 'secrets') and 'GOOGLE_DRIVE_FOLDER_ID' in st.secrets:
            return st.secrets['GOOGLE_DRIVE_FOLDER_ID']
    except:
        pass
    return None

def get_sheets_id():
    """Get Google Sheets ID from environment or Streamlit secrets."""
    sheet_id = os.getenv('GOOGLE_SHEETS_ID')
    if sheet_id:
        return sheet_id
    try:
        if hasattr(st, 'secrets') and 'GOOGLE_SHEETS_ID' in st.secrets:
            return st.secrets['GOOGLE_SHEETS_ID']
    except:
        pass
    return None

def get_service_account_path():
    """Get path to service account JSON file or dict from secrets."""
    import json
    import tempfile
    
    # Try environment variable first (local development)
    path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', 'service_account.json')
    if os.path.exists(path):
        return path
    
    # Try Streamlit secrets (cloud deployment)
    try:
        if hasattr(st, 'secrets') and 'service_account' in st.secrets:
            # Create a temporary file with the service account JSON
            service_account_info = dict(st.secrets['service_account'])
            
            # Write to temp file
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
            json.dump(service_account_info, temp_file)
            temp_file.close()
            
            return temp_file.name
    except Exception as e:
        pass
    
    return 'service_account.json'

def get_service_account_info():
    """Get service account as dictionary (for direct use)."""
    import json
    
    # Try Streamlit secrets first
    try:
        if hasattr(st, 'secrets') and 'service_account' in st.secrets:
            return dict(st.secrets['service_account'])
    except:
        pass
    
    # Try local file
    path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', 'service_account.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    
    return None

# File Upload Configuration
ALLOWED_FILE_TYPES = {
    'video': ['.mp4', '.mov'],
    'document': ['.pdf'],
    'spreadsheet': ['.xlsx', '.csv'],
    'image': ['.png', '.jpg', '.jpeg']
}

# Flatten for easy validation
ALLOWED_EXTENSIONS = []
for extensions in ALLOWED_FILE_TYPES.values():
    ALLOWED_EXTENSIONS.extend(extensions)

MAX_FILE_SIZE_MB = 100  # Maximum file size in MB

# Task Statuses
TASK_STATUSES = ["In Review", "Passed In Review", "In Stage", "Passed In Stage", "Done"]

# AI Constraints
NEGATIVE_CONSTRAINTS = [
    "Do NOT use the word 'verify' in test cases",
    "Use 'check', 'validate', or 'confirm' instead of 'verify'",
    "Be specific and actionable in all descriptions"
]

# Google Sheets Schema
SHEETS_HEADERS = [
    "Task ID",
    "Task Name", 
    "Upload Date",
    "Status",
    "File Type",
    "Evidence Link",
    "AI Summary",
    "Context Notes"
]

def validate_credentials():
    """
    Validate that all required credentials are present.
    Returns: (is_valid, missing_credentials)
    """
    missing = []
    
    if not get_gemini_api_key():
        missing.append("GEMINI_API_KEY")
    
    if not get_drive_folder_id():
        missing.append("GOOGLE_DRIVE_FOLDER_ID")
    
    if not get_sheets_id():
        missing.append("GOOGLE_SHEETS_ID")
    
    # Check if service account info is available (either from file or secrets)
    service_account_info = get_service_account_info()
    if not service_account_info:
        missing.append("GOOGLE_SERVICE_ACCOUNT_JSON (not configured)")
    
    return len(missing) == 0, missing
