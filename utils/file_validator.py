"""
File validation utilities for AI Sprint Brain.
Validates file types, sizes, and MIME types.
"""

import os
from pathlib import Path
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB

def validate_file_type(filename: str) -> tuple[bool, str]:
    """
    Validate if file extension is allowed.
    
    Args:
        filename: Name of the file to validate
        
    Returns:
        (is_valid, message): Tuple of validation result and message
    """
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        return False, f"File type '{file_ext}' not allowed. Allowed types: {allowed}"
    
    return True, "File type is valid"

def validate_file_size(file_size_bytes: int) -> tuple[bool, str]:
    """
    Validate if file size is within limits.
    
    Args:
        file_size_bytes: Size of file in bytes
        
    Returns:
        (is_valid, message): Tuple of validation result and message
    """
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    
    if file_size_bytes > max_size_bytes:
        size_mb = file_size_bytes / (1024 * 1024)
        return False, f"File size ({size_mb:.1f}MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB}MB)"
    
    return True, "File size is valid"

def get_file_category(filename: str) -> str:
    """
    Determine the category of file based on extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        Category string: 'video', 'document', 'spreadsheet', or 'image'
    """
    from config import ALLOWED_FILE_TYPES
    
    file_ext = Path(filename).suffix.lower()
    
    for category, extensions in ALLOWED_FILE_TYPES.items():
        if file_ext in extensions:
            return category
    
    return "unknown"

def validate_uploaded_file(uploaded_file) -> tuple[bool, str, str]:
    """
    Comprehensive validation of an uploaded file.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        (is_valid, message, category): Validation result, message, and file category
    """
    # Validate file type
    is_valid_type, type_message = validate_file_type(uploaded_file.name)
    if not is_valid_type:
        return False, type_message, ""
    
    # Validate file size
    is_valid_size, size_message = validate_file_size(uploaded_file.size)
    if not is_valid_size:
        return False, size_message, ""
    
    # Get file category
    category = get_file_category(uploaded_file.name)
    
    return True, "File validation successful", category
