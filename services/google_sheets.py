"""
Google Sheets integration for task metadata storage.
Provides CRUD operations for the task database.
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import gspread
from google.oauth2 import service_account
from utils.logger import setup_logger, log_api_call, log_error
from config import get_service_account_path, get_sheets_id, SHEETS_HEADERS, TASK_STATUSES

logger = setup_logger(__name__)

class GoogleSheetsService:
    """Service for interacting with Google Sheets API."""
    
    def __init__(self):
        """Initialize Google Sheets service with credentials."""
        self.client = None
        self.sheet_id = get_sheets_id()
        self.worksheet = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Set up Google Sheets API client."""
        try:
            service_account_path = get_service_account_path()
            
            if not os.path.exists(service_account_path):
                raise FileNotFoundError(f"Service account file not found: {service_account_path}")
            
            # Define required scopes
            SCOPES = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
            
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=SCOPES
            )
            
            # Initialize gspread client
            self.client = gspread.authorize(credentials)
            
            # Open the spreadsheet
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            
            # Get or create the main worksheet
            self.worksheet = self._get_or_create_worksheet()
            
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            log_error(logger, e, "Failed to initialize Google Sheets service")
            raise
    
    def _get_or_create_worksheet(self):
        """Get the main worksheet or create it if it doesn't exist."""
        try:
            # Try to get the first worksheet
            worksheet = self.spreadsheet.sheet1
            
            # Check if headers exist
            if not worksheet.row_values(1):
                # Initialize headers
                worksheet.append_row(SHEETS_HEADERS)
                logger.info("Initialized worksheet with headers")
            
            return worksheet
            
        except Exception as e:
            log_error(logger, e, "Failed to get or create worksheet")
            raise
    
    def create_task(self, task_data: Dict[str, str]) -> str:
        """
        Create a new task record.
        
        Args:
            task_data: Dictionary with task fields
            
        Returns:
            Task ID (row number)
        """
        try:
            start_time = datetime.now()
            
            # Generate task ID (next row number)
            all_values = self.worksheet.get_all_values()
            task_id = len(all_values)  # Header is row 1, so this gives us the next row
            
            # Prepare row data matching SHEETS_HEADERS
            row = [
                str(task_id),
                task_data.get('task_name', 'Untitled Task'),
                task_data.get('upload_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                task_data.get('status', 'In Review'),
                task_data.get('file_type', ''),
                task_data.get('evidence_link', ''),
                task_data.get('ai_summary', ''),
                task_data.get('context_notes', '')
            ]
            
            # Append to sheet
            self.worksheet.append_row(row)
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_api_call(logger, "Google Sheets", f"create_task: {task_data.get('task_name')}", duration_ms)
            
            return str(task_id)
            
        except Exception as e:
            log_error(logger, e, "Failed to create task")
            raise
    
    def get_all_tasks(self) -> List[Dict[str, str]]:
        """
        Retrieve all tasks from the sheet.
        
        Returns:
            List of task dictionaries
        """
        try:
            start_time = datetime.now()
            
            # Get all records (skipping header)
            records = self.worksheet.get_all_records()
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_api_call(logger, "Google Sheets", "get_all_tasks", duration_ms)
            
            return records
            
        except Exception as e:
            log_error(logger, e, "Failed to get all tasks")
            return []
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, str]]:
        """
        Retrieve tasks filtered by status.
        
        Args:
            status: Status to filter by (from TASK_STATUSES)
            
        Returns:
            List of matching task dictionaries
        """
        try:
            all_tasks = self.get_all_tasks()
            filtered = [task for task in all_tasks if task.get('Status') == status]
            
            logger.info(f"Retrieved {len(filtered)} tasks with status: {status}")
            return filtered
            
        except Exception as e:
            log_error(logger, e, f"Failed to get tasks by status: {status}")
            return []
    
    def update_task_status(self, task_id: str, new_status: str) -> bool:
        """
        Update the status of a task.
        
        Args:
            task_id: ID of the task (row number)
            new_status: New status value
            
        Returns:
            Success boolean
        """
        try:
            if new_status not in TASK_STATUSES:
                raise ValueError(f"Invalid status: {new_status}")
            
            start_time = datetime.now()
            
            # Find the row (task_id is the row number)
            row_num = int(task_id) + 1  # +1 because row 1 is header
            
            # Find the column index for Status (4th column in SHEETS_HEADERS)
            status_col_index = SHEETS_HEADERS.index('Status') + 1  # +1 for 1-indexed
            
            # Update the cell
            self.worksheet.update_cell(row_num, status_col_index, new_status)
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_api_call(logger, "Google Sheets", f"update_task_status: {task_id} -> {new_status}", duration_ms)
            
            return True
            
        except Exception as e:
            log_error(logger, e, f"Failed to update task status: {task_id}")
            return False
    
    def update_task(self, task_id: str, updates: Dict[str, str]) -> bool:
        """
        Update multiple fields of a task.
        
        Args:
            task_id: ID of the task (row number)
            updates: Dictionary of field names and new values
            
        Returns:
            Success boolean
        """
        try:
            start_time = datetime.now()
            
            # Find the row (task_id is the row number)
            row_num = int(task_id) + 1  # +1 because row 1 is header
            
            # Update each field
            for field_name, new_value in updates.items():
                if field_name in SHEETS_HEADERS:
                    col_index = SHEETS_HEADERS.index(field_name) + 1  # +1 for 1-indexed
                    self.worksheet.update_cell(row_num, col_index, new_value)
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_api_call(logger, "Google Sheets", f"update_task: {task_id}", duration_ms)
            
            return True
            
        except Exception as e:
            log_error(logger, e, f"Failed to update task: {task_id}")
            return False
    
    def get_tasks_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, str]]:
        """
        Get tasks within a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of matching tasks
        """
        try:
            all_tasks = self.get_all_tasks()
            
            filtered = []
            for task in all_tasks:
                upload_date_str = task.get('Upload Date', '')
                if upload_date_str:
                    try:
                        upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d %H:%M:%S')
                        if start_date <= upload_date <= end_date:
                            filtered.append(task)
                    except ValueError:
                        continue
            
            logger.info(f"Retrieved {len(filtered)} tasks in date range")
            return filtered
            
        except Exception as e:
            log_error(logger, e, "Failed to get tasks by date range")
            return []

import streamlit as st

# Singleton instance with caching
@st.cache_resource
def get_sheets_service() -> GoogleSheetsService:
    """Get or create cached Google Sheets service instance."""
    return GoogleSheetsService()

# Also cache task data for 60 seconds to reduce API calls
@st.cache_data(ttl=60)
def get_cached_tasks():
    """Get cached task data (refreshes every 60 seconds)."""
    service = get_sheets_service()
    return service.get_all_tasks()

