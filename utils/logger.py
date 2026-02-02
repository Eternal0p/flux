"""
Logging utilities for AI Sprint Brain.
Provides structured logging for debugging and monitoring.
"""

import logging
import sys
from datetime import datetime

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logger(name: str, level=logging.INFO):
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Name of the logger (usually __name__)
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

def log_api_call(logger, service: str, operation: str, duration_ms: float = None):
    """
    Log an API call with timing information.
    
    Args:
        logger: Logger instance
        service: Name of the service (e.g., 'Google Drive', 'Gemini')
        operation: Operation performed (e.g., 'upload_file', 'analyze_video')
        duration_ms: Duration in milliseconds (optional)
    """
    if duration_ms:
        logger.info(f"{service} - {operation} completed in {duration_ms:.2f}ms")
    else:
        logger.info(f"{service} - {operation} started")

def log_error(logger, error: Exception, context: str = ""):
    """
    Log an error with context and stack trace.
    
    Args:
        logger: Logger instance
        error: Exception object
        context: Additional context about where the error occurred
    """
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)

# Create default application logger
app_logger = setup_logger('ai_sprint_brain')
