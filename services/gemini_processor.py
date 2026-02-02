"""
Gemini 3.0 Pro integration for multimodal AI processing.
Handles analysis of videos, PDFs, images, and spreadsheets.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import google.generativeai as genai
from PIL import Image
import io

from config import get_gemini_api_key
from prompts.templates import get_prompt_for_file_type
from utils.logger import setup_logger, log_api_call, log_error

logger = setup_logger(__name__)

class GeminiProcessor:
    """Service for processing files with Gemini 3.0 Pro."""
    
    def __init__(self):
        """Initialize Gemini API client."""
        self.model = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Set up Gemini API client."""
        try:
            api_key = get_gemini_api_key()
            
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment")
            
            genai.configure(api_key=api_key)
            
            # Use gemini-flash-latest (better free tier quota)
            # Pro model has stricter limits, Flash is faster and has higher quota
            self.model = genai.GenerativeModel('gemini-flash-latest')
            
            logger.info("Gemini API client initialized with gemini-flash-latest model")
            
        except Exception as e:
            log_error(logger, e, "Failed to initialize Gemini API")
            raise
    
    def process_file(self, file_data, filename: str, file_category: str, context_notes: str = "") -> Dict[str, Any]:
        """
        Process a file using Gemini AI based on its category.
        
        Args:
            file_data: File data (bytes or file-like object)
            filename: Name of the file
            file_category: Category ('video', 'document', 'spreadsheet', 'image')
            context_notes: Additional context from user
            
        Returns:
            Analyzed data as dictionary
        """
        try:
            start_time = datetime.now()
            
            # Get appropriate prompt
            prompt = get_prompt_for_file_type(file_category, context_notes)
            
            # Process based on category
            if file_category == 'video':
                result = self._process_video(file_data, prompt, filename)
            elif file_category == 'image':
                result = self._process_image(file_data, prompt)
            elif file_category == 'document':
                result = self._process_document(file_data, prompt, filename)
            elif file_category == 'spreadsheet':
                result = self._process_spreadsheet(file_data, prompt, filename)
            else:
                result = self._process_generic(file_data, prompt)
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_api_call(logger, "Gemini", f"process_{file_category}: {filename}", duration_ms)
            
            return result
            
        except Exception as e:
            log_error(logger, e, f"Failed to process file: {filename}")
            # Return a fallback result
            return {
                "task_name": f"Error processing {filename}",
                "summary": f"Failed to analyze file: {str(e)}",
                "error": True
            }
    
    def _process_video(self, file_data, prompt: str, filename: str) -> Dict[str, Any]:
        """Process video file with Gemini."""
        try:
            # For video, we need to upload the file first
            # Note: Gemini API has specific requirements for video uploads
            
            # Save to temp file (Gemini API requires file path for videos)
            import tempfile
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                if isinstance(file_data, bytes):
                    temp_file.write(file_data)
                else:
                    temp_file.write(file_data.read())
                temp_path = temp_file.name
            
            # Upload video to Gemini
            video_file = genai.upload_file(path=temp_path)
            
            # Wait for processing
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            # Generate content
            response = self.model.generate_content([video_file, prompt])
            
            # Clean up temp file
            import os
            os.unlink(temp_path)
            
            return self._parse_json_response(response.text)
            
        except Exception as e:
            log_error(logger, e, "Failed to process video")
            raise
    
    def _process_image(self, file_data, prompt: str) -> Dict[str, Any]:
        """Process image file with Gemini."""
        try:
            # Convert to PIL Image
            if isinstance(file_data, bytes):
                image = Image.open(io.BytesIO(file_data))
            else:
                image = Image.open(file_data)
            
            # Generate content with image
            response = self.model.generate_content([prompt, image])
            
            return self._parse_json_response(response.text)
            
        except Exception as e:
            log_error(logger, e, "Failed to process image")
            raise
    
    def _process_document(self, file_data, prompt: str, filename: str) -> Dict[str, Any]:
        """Process PDF document with Gemini."""
        try:
            # For PDFs, we need to upload the file
            import tempfile
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                if isinstance(file_data, bytes):
                    temp_file.write(file_data)
                else:
                    temp_file.write(file_data.read())
                temp_path = temp_file.name
            
            # Upload document
            doc_file = genai.upload_file(path=temp_path)
            
            # Generate content
            response = self.model.generate_content([doc_file, prompt])
            
            # Clean up
            import os
            os.unlink(temp_path)
            
            return self._parse_json_response(response.text)
            
        except Exception as e:
            log_error(logger, e, "Failed to process document")
            raise
    
    def _process_spreadsheet(self, file_data, prompt: str, filename: str) -> Dict[str, Any]:
        """Process spreadsheet with Gemini."""
        try:
            # Read spreadsheet data
            import pandas as pd
            
            if isinstance(file_data, bytes):
                file_data = io.BytesIO(file_data)
            
            # Determine file type
            if filename.endswith('.csv'):
                df = pd.read_csv(file_data)
            else:
                df = pd.read_excel(file_data)
            
            # Convert to text representation
            data_summary = f"Spreadsheet Data:\n\n"
            data_summary += f"Columns: {', '.join(df.columns.tolist())}\n"
            data_summary += f"Total Rows: {len(df)}\n\n"
            data_summary += f"First 10 rows:\n{df.head(10).to_string()}\n\n"
            
            if len(df) > 10:
                data_summary += f"Last 5 rows:\n{df.tail(5).to_string()}"
            
            # Generate content
            full_prompt = f"{prompt}\n\n{data_summary}"
            response = self.model.generate_content(full_prompt)
            
            return self._parse_json_response(response.text)
            
        except Exception as e:
            log_error(logger, e, "Failed to process spreadsheet")
            raise
    
    def _process_generic(self, file_data, prompt: str) -> Dict[str, Any]:
        """Generic file processing fallback."""
        try:
            # Just send the prompt
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            log_error(logger, e, "Failed to process file")
            raise
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from Gemini response.
        Handles cases where response includes markdown code blocks.
        """
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith('```json'):
                text = text[7:]  # Remove ```json
            if text.startswith('```'):
                text = text[3:]  # Remove ```
            if text.endswith('```'):
                text = text[:-3]  # Remove trailing ```
            
            text = text.strip()
            
            # Parse JSON
            result = json.loads(text)
            return result
            
        except json.JSONDecodeError:
            # Fallback: return raw text
            logger.warning("Failed to parse JSON, returning raw text")
            return {
                "task_name": "Untitled Task",
                "summary": response_text,
                "raw_response": True
            }
    
    def generate_test_cases(self, tasks: list) -> str:
        """
        Generate TestRail-compatible CSV from completed tasks.
        
        Args:
            tasks: List of completed task dictionaries
            
        Returns:
            CSV content as string
        """
        try:
            from prompts.templates import TEST_CASE_GENERATION_PROMPT
            
            # Build context from tasks
            tasks_context = "\n\n".join([
                f"Task {i+1}: {task.get('Task Name', 'Untitled')}\n"
                f"Summary: {task.get('AI Summary', 'No summary')}\n"
                f"Evidence: {task.get('Evidence Link', 'N/A')}"
                for i, task in enumerate(tasks)
            ])
            
            full_prompt = f"{TEST_CASE_GENERATION_PROMPT}\n\nTasks:\n{tasks_context}"
            
            response = self.model.generate_content(full_prompt)
            
            return response.text.strip()
            
        except Exception as e:
            log_error(logger, e, "Failed to generate test cases")
            return "Error generating test cases"
    
    def generate_requirement_doc(self, tasks: list) -> str:
        """
        Generate requirement document content from tasks.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Markdown content for requirement document
        """
        try:
            from prompts.templates import REQUIREMENT_DOCUMENT_PROMPT
            
            # Build context from tasks
            tasks_context = "\n\n".join([
                f"### Task {i+1}: {task.get('Task Name', 'Untitled')}\n"
                f"**Date:** {task.get('Upload Date', 'N/A')}\n"
                f"**Type:** {task.get('File Type', 'N/A')}\n"
                f"**Summary:** {task.get('AI Summary', 'No summary')}\n"
                f"**Evidence:** [{task.get('Evidence Link', 'N/A')}]({task.get('Evidence Link', '#')})"
                for i, task in enumerate(tasks)
            ])
            
            full_prompt = f"{REQUIREMENT_DOCUMENT_PROMPT}\n\nTasks:\n{tasks_context}"
            
            response = self.model.generate_content(full_prompt)
            
            return response.text.strip()
            
        except Exception as e:
            log_error(logger, e, "Failed to generate requirement document")
            return "# Error\n\nFailed to generate requirement document"
    
    def generate_scrum_email(self, tasks: list, week_start: str, week_end: str) -> str:
        """
        Generate Scrum update email from completed tasks.
        
        Args:
            tasks: List of completed task dictionaries
            week_start: Start date of the week
            week_end: End date of the week
            
        Returns:
            Email content as string
        """
        try:
            from prompts.templates import EMAIL_DRAFT_PROMPT
            
            # Build context
            tasks_context = "\n".join([
                f"- {task.get('Task Name', 'Untitled')} [{task.get('File Type', 'N/A')}]"
                for task in tasks
            ])
            
            full_prompt = f"{EMAIL_DRAFT_PROMPT}\n\n"
            full_prompt += f"Week: {week_start} to {week_end}\n"
            full_prompt += f"Completed Tasks ({len(tasks)}):\n{tasks_context}"
            
            response = self.model.generate_content(full_prompt)
            
            return response.text.strip()
            
        except Exception as e:
            log_error(logger, e, "Failed to generate email")
            return "Error generating email draft"

# Singleton instance
_gemini_processor = None

def get_gemini_processor() -> GeminiProcessor:
    """Get or create Gemini processor instance."""
    global _gemini_processor
    if _gemini_processor is None:
        _gemini_processor = GeminiProcessor()
    return _gemini_processor
