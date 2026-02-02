"""
Upload Evidence Page
Allows users to upload multimodal files for AI analysis.
"""

import streamlit as st
from datetime import datetime
import io

from utils.file_validator import validate_uploaded_file
from services.google_drive import get_drive_service
from services.google_sheets import get_sheets_service
from services.gemini_processor import get_gemini_processor
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Upload Evidence - FLUX",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Upload Evidence")
st.markdown("Upload your evidence files and let AI analyze them instantly.")

# Upload section
st.markdown("### Select File")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['mp4', 'mov', 'pdf', 'xlsx', 'csv', 'png', 'jpg', 'jpeg'],
    help="Supported: Videos (.mp4, .mov), Documents (.pdf), Spreadsheets (.xlsx, .csv), Images (.png, .jpg)"
)

# Context notes
context_notes = st.text_area(
    "📝 Context Notes (Optional)",
    placeholder="Add any additional context via voice-to-text or typing...",
    help="Provide context like: 'This bug happens on Login page' or 'High priority feature request'"
)

# Upload button
if uploaded_file and st.button("🚀 Upload & Analyze", type="primary", use_container_width=True):
    
    # Validate file
    is_valid, message, category = validate_uploaded_file(uploaded_file)
    
    if not is_valid:
        st.error(f"❌ {message}")
        st.stop()
    
    st.success(f"✅ {message}")
    st.info(f"📁 File Category: **{category.title()}**")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Upload to Google Drive
        status_text.text("⬆️ Uploading to Google Drive...")
        progress_bar.progress(20)
        
        drive_service = get_drive_service()
        
        # Get organized folder
        folder_id = drive_service.organize_by_date(category)
        
        # Read file data
        file_data = uploaded_file.read()
        
        # Upload file
        drive_result = drive_service.upload_file(
            file_data=file_data,
            filename=uploaded_file.name,
            mime_type=uploaded_file.type,
            folder_id=folder_id
        )
        
        evidence_link = drive_result['webViewLink']
        
        progress_bar.progress(40)
        st.success(f"✅ Uploaded to Drive: [View Evidence]({evidence_link})")
        
        # Step 2: AI Analysis
        status_text.text("🤖 Analyzing with Gemini AI...")
        progress_bar.progress(50)
        
        gemini = get_gemini_processor()
        
        # Reset file pointer
        file_data_for_ai = io.BytesIO(file_data)
        
        ai_result = gemini.process_file(
            file_data=file_data_for_ai,
            filename=uploaded_file.name,
            file_category=category,
            context_notes=context_notes
        )
        
        progress_bar.progress(80)
        
        # Extract task name and summary
        task_name = ai_result.get('task_name', f"Task from {uploaded_file.name}")
        ai_summary = ai_result.get('summary', 'No summary available')
        
        st.success(f"✅ AI Analysis Complete")
        
        # Step 3: Save to Google Sheets
        status_text.text("💾 Saving to Sprint Board...")
        progress_bar.progress(90)
        
        sheets_service = get_sheets_service()
        
        task_data = {
            'task_name': task_name,
            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'In Review',
            'file_type': category,
            'evidence_link': evidence_link,
            'ai_summary': str(ai_result),  # Store full JSON
            'context_notes': context_notes
        }
        
        task_id = sheets_service.create_task(task_data)
        
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        # Display results
        st.divider()
        st.markdown("### 🎉 Task Created Successfully!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Task Name:** {task_name}")
            st.markdown(f"**Status:** 🟡 In Review")
            st.markdown(f"**File Type:** {category.title()}")
            
            st.markdown("**AI Summary:**")
            st.info(ai_summary)
            
            if context_notes:
                st.markdown("**Your Notes:**")
                st.text(context_notes)
        
        with col2:
            st.markdown("**Quick Actions**")
            st.link_button("👁️ View Evidence", evidence_link, use_container_width=True)
            
            if st.button("➕ Upload Another", use_container_width=True):
                st.rerun()
        
        # Show full AI response in expander
        with st.expander("🔍 View Full AI Analysis"):
            st.json(ai_result)
        
        logger.info(f"Successfully created task: {task_name} (ID: {task_id})")
        
    except Exception as e:
        progress_bar.progress(0)
        status_text.text("")
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Upload failed: {str(e)}")

# Information section
if not uploaded_file:
    st.divider()
    
    st.markdown("### 📚 Supported File Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎥 Videos**
        - `.mp4`, `.mov`
        - Screen recordings of bugs
        - Demo videos
        
        **📄 Documents**
        - `.pdf`
        - Requirements, specifications
        - Design docs
        """)
    
    with col2:
        st.markdown("""
        **📊 Spreadsheets**
        - `.xlsx`, `.csv`
        - Test case lists
        - Data exports
        
        **🖼️ Images**
        - `.png`, `.jpg`, `.jpeg`
        - Screenshots, UI mockups
        - Error messages
        """)
    
    st.divider()
    
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    1. **Add Context**: Use the context notes field to provide additional information
    2. **Clear Filenames**: Use descriptive filenames for better organization
    3. **Quality**: Ensure videos are clear and images are readable
    4. **Size Limit**: Files must be under 100MB
    """)
