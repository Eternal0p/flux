"""
Google Drive integration for file storage and management.
Handles uploads, folder organization, and WebViewLink generation.
"""

import io
import os
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from utils.logger import setup_logger, log_api_call, log_error
from config import get_service_account_path, get_drive_folder_id

logger = setup_logger(__name__)

class GoogleDriveService:
    """Service for interacting with Google Drive API."""
    
    def __init__(self):
        """Initialize Google Drive service with credentials."""
        self.service = None
        self.root_folder_id = get_drive_folder_id()
        self._initialize_service()
    
    def _initialize_service(self):
        """Set up Google Drive API service."""
        try:
            service_account_path = get_service_account_path()
            
            if not os.path.exists(service_account_path):
                raise FileNotFoundError(f"Service account file not found: {service_account_path}")
            
            # Define required scopes
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=SCOPES
            )
            
            # Build Drive service
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("Google Drive service initialized successfully")
            
        except Exception as e:
            log_error(logger, e, "Failed to initialize Google Drive service")
            raise
    
    def create_folder(self, folder_name: str, parent_folder_id: str = None) -> str:
        """
        Create a folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to create
            parent_folder_id: ID of parent folder (uses root if None)
            
        Returns:
            ID of the created folder
        """
        try:
            parent_id = parent_folder_id or self.root_folder_id
            
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id, name',
                supportsAllDrives=True
            ).execute()
            
            logger.info(f"Created folder: {folder_name} (ID: {folder['id']})")
            return folder['id']
            
        except Exception as e:
            log_error(logger, e, f"Failed to create folder: {folder_name}")
            raise
    
    def upload_file(self, file_data, filename: str, mime_type: str, folder_id: str = None) -> dict:
        """
        Upload a file to Google Drive.
        
        Args:
            file_data: File data (bytes or file-like object)
            filename: Name of the file
            mime_type: MIME type of the file
            folder_id: ID of folder to upload to (uses root if None)
            
        Returns:
            Dictionary with file metadata including webViewLink
        """
        try:
            start_time = datetime.now()
            parent_id = folder_id or self.root_folder_id
            
            # Convert bytes to file-like object if needed
            if isinstance(file_data, bytes):
                file_data = io.BytesIO(file_data)
            
            file_metadata = {
                'name': filename,
                'parents': [parent_id]
            }
            
            media = MediaIoBaseUpload(
                file_data,
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink, size, createdTime',
                supportsAllDrives=True
            ).execute()
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_api_call(logger, "Google Drive", f"upload_file: {filename}", duration_ms)
            
            return {
                'id': file['id'],
                'name': file['name'],
                'webViewLink': file.get('webViewLink', ''),
                'size': file.get('size', 0),
                'createdTime': file.get('createdTime', '')
            }
            
        except Exception as e:
            log_error(logger, e, f"Failed to upload file: {filename}")
            raise
    
    def organize_by_date(self, file_category: str) -> str:
        """
        Get or create a dated folder structure for organizing uploads.
        Structure: root/YYYY/MM/category/
        
        Args:
            file_category: Category of file (video, document, etc.)
            
        Returns:
            ID of the target folder
        """
        try:
            now = datetime.now()
            year = now.strftime('%Y')
            month = now.strftime('%m')
            
            # Create/get year folder
            year_folder_id = self._get_or_create_folder(year, self.root_folder_id)
            
            # Create/get month folder
            month_folder_id = self._get_or_create_folder(month, year_folder_id)
            
            # Create/get category folder
            category_folder_id = self._get_or_create_folder(file_category, month_folder_id)
            
            return category_folder_id
            
        except Exception as e:
            log_error(logger, e, "Failed to organize by date")
            return self.root_folder_id  # Fallback to root
    
    def _get_or_create_folder(self, folder_name: str, parent_id: str) -> str:
        """
        Get existing folder ID or create if it doesn't exist.
        
        Args:
            folder_name: Name of folder
            parent_id: Parent folder ID
            
        Returns:
            Folder ID
        """
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            
            results = self.service.files().list(
                q=query,
                fields='files(id, name)',
                pageSize=1,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                return files[0]['id']
            else:
                return self.create_folder(folder_name, parent_id)
                
        except Exception as e:
            log_error(logger, e, f"Failed to get or create folder: {folder_name}")
            raise

# Singleton instance
_drive_service = None

def get_drive_service() -> GoogleDriveService:
    """Get or create Google Drive service instance."""
    global _drive_service
    if _drive_service is None:
        _drive_service = GoogleDriveService()
    return _drive_service
