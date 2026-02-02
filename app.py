"""
AI Sprint Brain - Main Streamlit Application
A zero-cost multimodal task management system for QA and Development.
"""

import streamlit as st
from datetime import datetime
from config import validate_credentials
from utils.auth import require_auth

# Page configuration
st.set_page_config(
    page_title="FLUX - Task Management",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Require authentication
require_auth()

# Custom CSS for mobile responsiveness
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Touch-friendly buttons */
    .stButton>button {
        min-height: 44px;
        font-size: 16px;
    }
    
    /* Card styling */
    .task-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-in-review {
        background: #fff3cd;
        color: #856404;
    }
    
    .status-passed-review {
        background: #ffe5cc;
        color: #8b4513;
    }
    
    .status-in-stage {
        background: #cfe2ff;
        color: #084298;
    }
    
    .status-passed-stage {
        background: #e0d5f5;
        color: #6610f2;
    }
    
    .status-done {
        background: #d1e7dd;
        color: #0f5132;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point."""
    
    # Header
    st.markdown('<div class="main-header">⚡ FLUX</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Intelligent Task Management · <em>Made by -eternal</em></div>', unsafe_allow_html=True)
    
    # Credentials validation
    is_valid, missing = validate_credentials()
    
    if not is_valid:
        st.error("⚠️ Missing Credentials")
        st.warning("Please configure the following environment variables:")
        for item in missing:
            st.code(item)
        
        with st.expander("📖 Setup Instructions"):
            st.markdown("""
            ### Quick Setup Guide
            
            1. **Get Gemini API Key**
               - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
               - Create an API key
               - Add to `.env` file: `GEMINI_API_KEY=your_key_here`
            
            2. **Set up Google Cloud Service Account**
               - Go to [Google Cloud Console](https://console.cloud.google.com)
               - Create a new project or select existing
               - Enable Google Drive API and Google Sheets API
               - Create a service account and download JSON key
               - Save as `service_account.json` in project root
            
            3. **Create Google Drive Folder**
               - Create a new folder in your Google Drive
               - Share it with your service account email
               - Copy the folder ID from URL
               - Add to `.env`: `GOOGLE_DRIVE_FOLDER_ID=folder_id`
            
            4. **Create Google Sheet**
               - Create a new Google Sheet
               - Share it with your service account email (Editor access)
               - Copy the sheet ID from URL
               - Add to `.env`: `GOOGLE_SHEETS_ID=sheet_id`
            
            5. **Restart the application**
            """)
        
        st.stop()
    
    # Success message
    st.success("✅ All credentials configured! Ready to use.")
    
    # Main navigation
    st.sidebar.title("Navigation")
    
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Home", "📤 Upload Evidence", "📋 Sprint Board", "⚡ Generate Outputs"],
        label_visibility="collapsed"
    )
    
    # Display page content
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload Evidence":
        st.info("👈 Navigate to 'Upload Evidence' page in the sidebar or use the pages menu")
        show_upload_preview()
    elif page == "📋 Sprint Board":
        st.info("👈 Navigate to 'Sprint Board' page in the sidebar or use the pages menu")
        show_board_preview()
    elif page == "⚡ Generate Outputs":
        st.info("👈 Navigate to 'Generate Outputs' page in the sidebar or use the pages menu")
        show_generate_preview()

def show_home_page():
    """Display the home page."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚌 The Commuter Problem")
        st.markdown("""
        You're on the bus or train with valuable evidence:
        - Screen recordings of bugs
        - PDF specifications
        - Voice notes with context
        
        But you can't properly document them until you're at your desk.
        """)
    
    with col2:
        st.markdown("### ✨ The FLUX Solution")
        st.markdown("""
        Upload evidence from anywhere, and AI does the heavy lifting:
        - **Analyzes** videos, PDFs, images, spreadsheets
        - **Extracts** structured data and insights
        - **Organizes** tasks in your Sprint Board
        - **Generates** test cases, docs, and reports
        """)
    
    st.divider()
    
    st.markdown("### 🎯 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1️⃣ Upload")
        st.markdown("""
        Go to **📤 Upload Evidence** and:
        - Select a file (video, PDF, image, CSV)
        - Add optional voice-to-text notes
        - Click Upload
        """)
    
    with col2:
        st.markdown("#### 2️⃣ Review")
        st.markdown("""
        Visit **📋 Sprint Board** to:
        - See all your tasks
        - Read AI-generated summaries
        - Update task status
        - Access evidence links
        """)
    
    with col3:
        st.markdown("#### 3️⃣ Generate")
        st.markdown("""
        Use **⚡ Generate Outputs** to:
        - Create TestRail CSV
        - Export requirement docs
        - Draft Scrum emails
        """)
    
    st.divider()
    
    # Stats (if sheets service is available)
    try:
        from services.google_sheets import get_sheets_service
        
        sheets = get_sheets_service()
        tasks = sheets.get_all_tasks()
        
        if tasks:
            st.markdown("### 📊 Your Stats")
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            total = len(tasks)
            in_review = len([t for t in tasks if t.get('Status') == 'In Review'])
            passed_review = len([t for t in tasks if t.get('Status') == 'Passed In Review'])
            in_stage = len([t for t in tasks if t.get('Status') == 'In Stage'])
            passed_stage = len([t for t in tasks if t.get('Status') == 'Passed In Stage'])
            done = len([t for t in tasks if t.get('Status') == 'Done'])
            
            col1.metric("Total", total)
            col2.metric("In Review", in_review)
            col3.metric("Passed Review", passed_review)
            col4.metric("In Stage", in_stage)
            col5.metric("Passed Stage", passed_stage)
            col6.metric("Done", done)
    except:
        pass

def show_upload_preview():
    """Show preview of upload functionality."""
    st.markdown("""
    ### Upload Evidence
    
    The **Upload** page allows you to:
    - Drag and drop files or browse
    - Supported types: `.mp4`, `.mov`, `.pdf`, `.xlsx`, `.csv`, `.png`, `.jpg`
    - Add context notes via voice-to-text
    - AI automatically analyzes and creates tasks
    """)

def show_board_preview():
    """Show preview of board functionality."""
    st.markdown("""
    ### Sprint Board
    
    The **Sprint Board** displays your tasks in a 5-column Kanban layout:
    - **In Review**: Newly uploaded tasks
    - **Passed In Review**: Tasks that passed initial review
    - **In Stage**: Tasks being tested/staged
    - **Passed In Stage**: Tasks that passed staging
    - **Done**: Completed and deployed tasks
    
    Features:
    - View AI summaries
    - Update task status
    - Click evidence links to view in Google Drive
    - Filter and search tasks
    """)

def show_generate_preview():
    """Show preview of generate functionality."""
    st.markdown("""
    ### Generate Outputs
    
    The **Generate** page creates professional outputs:
    
    **📝 Test Cases**
    - Generates TestRail-compatible CSV
    - Based on completed tasks
    - Follows best practices
    
    **📄 Requirement Document**
    - Professional PDF with all requirements
    - Includes evidence references
    - Ready for stakeholder review
    
    **📧 Scrum Email**
    - Weekly summary of completed tasks
    - Grouped by type (bugs, features, docs)
    - Copy-paste ready
    """)

if __name__ == "__main__":
    main()
