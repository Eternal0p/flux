"""
AI prompt templates for different file types and output generation.
Implements negative constraints and structured output requirements.
"""

from config import NEGATIVE_CONSTRAINTS

# Constraint reminder for all prompts
CONSTRAINTS_REMINDER = "\n\n".join([
    "IMPORTANT CONSTRAINTS:",
    *[f"- {constraint}" for constraint in NEGATIVE_CONSTRAINTS]
])

# Video Analysis Prompt
VIDEO_ANALYSIS_PROMPT = f"""You are analyzing a screen recording that demonstrates a bug or feature.

Your task:
1. Understand the temporal flow of events in the video
2. Identify the bug or feature being demonstrated
3. Extract clear steps to reproduce
4. Note any error messages or visual defects
5. Assess severity and priority

Provide your analysis in the following JSON format:
{{
    "task_name": "Brief, descriptive title",
    "summary": "Concise summary of what the video shows",
    "steps_to_reproduce": ["Step 1", "Step 2", "Step 3"],
    "expected_behavior": "What should happen",
    "actual_behavior": "What actually happens",
    "severity": "Critical|High|Medium|Low",
    "additional_notes": "Any other observations"
}}

{CONSTRAINTS_REMINDER}
"""

# PDF Document Analysis Prompt
PDF_ANALYSIS_PROMPT = f"""You are analyzing a PDF document that contains requirements, specifications, or documentation.

Your task:
1. Extract functional requirements
2. Identify constraints and limitations
3. Note acceptance criteria
4. Highlight any ambiguities or missing information
5. Summarize key points

Provide your analysis in the following JSON format:
{{
    "task_name": "Brief title based on document content",
    "summary": "High-level summary of the document",
    "functional_requirements": ["Requirement 1", "Requirement 2"],
    "constraints": ["Constraint 1", "Constraint 2"],
    "acceptance_criteria": ["Criteria 1", "Criteria 2"],
    "priority": "Critical|High|Medium|Low",
    "additional_notes": "Missing info or ambiguities"
}}

{CONSTRAINTS_REMINDER}
"""

# Spreadsheet Analysis Prompt
SPREADSHEET_ANALYSIS_PROMPT = f"""You are analyzing a spreadsheet (CSV/Excel) that contains data, tasks, or test cases.

Your task:
1. Summarize the overall content and structure
2. Identify high-priority items (based on columns like Priority, Status, Severity)
3. Extract key insights or patterns
4. Note any data quality issues
5. Provide actionable recommendations

Provide your analysis in the following JSON format:
{{
    "task_name": "Brief title based on spreadsheet content",
    "summary": "What this spreadsheet contains",
    "total_rows": "Number of data rows",
    "high_priority_items": ["Item 1", "Item 2"],
    "key_insights": ["Insight 1", "Insight 2"],
    "data_quality_issues": ["Issue 1", "Issue 2"],
    "additional_notes": "Any recommendations"
}}

{CONSTRAINTS_REMINDER}
"""

# Image/Screenshot Analysis Prompt
IMAGE_ANALYSIS_PROMPT = f"""You are analyzing an image or screenshot that may contain UI issues, visual defects, or important information.

Your task:
1. Perform OCR to extract any text
2. Identify visual UI defects (alignment, spacing, colors, etc.)
3. Note any error messages or alerts
4. Describe the context and purpose of the image
5. Assess severity of any issues

Provide your analysis in the following JSON format:
{{
    "task_name": "Brief title based on image content",
    "summary": "What the image shows",
    "extracted_text": "Any text found via OCR",
    "visual_defects": ["Defect 1", "Defect 2"],
    "ui_elements": ["Element 1", "Element 2"],
    "severity": "Critical|High|Medium|Low",
    "additional_notes": "Any context or recommendations"
}}

{CONSTRAINTS_REMINDER}
"""

# Test Case Generation Prompt
TEST_CASE_GENERATION_PROMPT = f"""You are generating test cases for TestRail based on completed tasks.

Input: A list of tasks with their summaries and evidence.

Your task:
1. Create comprehensive test cases covering all functionality
2. Format for TestRail CSV import (columns: ID, Title, Steps, Expected Result, Priority)
3. Make steps clear, specific, and actionable
4. Ensure test cases are independent and repeatable

Output format:
- CSV with headers: Test Case ID, Title, Steps, Expected Result, Priority
- Each row should be a separate test case
- Steps should be numbered and clear
- Expected results should be specific and measurable

{CONSTRAINTS_REMINDER}

Generate the CSV content now.
"""

# Requirement Document Generation Prompt
REQUIREMENT_DOCUMENT_PROMPT = f"""You are generating a professional Requirement Document based on completed tasks.

Input: A list of tasks with their summaries, evidence links, and context.

Your task:
1. Create a structured requirement document with the following sections:
   - Executive Summary
   - Functional Requirements (grouped by feature area)
   - Non-Functional Requirements
   - Constraints and Assumptions
   - Evidence References
2. Use professional language and formatting
3. Include all relevant details from the tasks
4. Cross-reference evidence links

Output the document content in Markdown format, which will be converted to PDF.

{CONSTRAINTS_REMINDER}
"""

# Email Draft Generation Prompt
EMAIL_DRAFT_PROMPT = f"""You are drafting a professional Scrum update email for a Friday end-of-week summary.

Input: A list of completed tasks from the current week.

Your task:
1. Group tasks by type (Bugs Fixed, Features Implemented, Documentation)
2. Summarize progress concisely but comprehensively
3. Use a professional, positive tone
4. Include key metrics (number of tasks completed, etc.)
5. Structure for easy scanning

Output format:
Subject: [Weekly Scrum Update] Week of [Date Range]

Body:
- Brief intro
- Accomplished This Week section with categorized tasks
- Optional: Challenges or blockers
- Optional: Next week's focus
- Professional sign-off

{CONSTRAINTS_REMINDER}
"""

def get_prompt_for_file_type(file_category: str, context_notes: str = "") -> str:
    """
    Get the appropriate analysis prompt based on file category.
    
    Args:
        file_category: Category of file ('video', 'document', 'spreadsheet', 'image')
        context_notes: Additional context provided by the user
        
    Returns:
        Formatted prompt string
    """
    prompt_map = {
        'video': VIDEO_ANALYSIS_PROMPT,
        'document': PDF_ANALYSIS_PROMPT,
        'spreadsheet': SPREADSHEET_ANALYSIS_PROMPT,
        'image': IMAGE_ANALYSIS_PROMPT
    }
    
    base_prompt = prompt_map.get(file_category, PDF_ANALYSIS_PROMPT)
    
    if context_notes:
        return f"{base_prompt}\n\nUser Context Notes:\n{context_notes}\n\nNow analyze the file."
    
    return base_prompt
