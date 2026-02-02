"""
Quick Notes Page
Allows users to quickly save text notes without uploading files.
"""

import streamlit as st
from datetime import datetime

from services.google_sheets import get_sheets_service
from services.gemini_processor import get_gemini_processor
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Quick Notes - FLUX",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Quick Notes")
st.markdown("Quickly save text notes with optional AI enhancement.")

# Note input
col1, col2 = st.columns([3, 1])

with col1:
    note_title = st.text_input(
        "Note Title",
        placeholder="e.g., Bug in login page, Feature idea, Meeting notes..."
    )

with col2:
    note_status = st.selectbox(
        "Status",
        ["In Review", "Passed In Review", "In Stage", "Passed In Stage", "Done"],
        index=0
    )

note_content = st.text_area(
    "Note Content",
    placeholder="Type your notes here...\n\nYou can add:\n- Bug descriptions\n- Feature requests\n- Meeting notes\n- Quick reminders\n- Task lists",
    height=300
)

# AI enhancement option
col1, col2 = st.columns(2)

with col1:
    enhance_with_ai = st.checkbox(
        "✨ Enhance with AI",
        help="Let Gemini AI analyze and structure your note"
    )

with col2:
    if enhance_with_ai:
        enhancement_type = st.selectbox(
            "Enhancement Type",
            [
                "Auto-structure and improve",
                "Extract action items",
                "Summarize key points",
                "Convert to test cases"
            ]
        )

# Save button
if st.button("💾 Save Note", type="primary", use_container_width=True, disabled=not note_content):
    
    if not note_title:
        note_title = f"Note from {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    try:
        with st.spinner("💾 Saving your note..."):
            
            # Enhance with AI if requested
            ai_summary = note_content
            if enhance_with_ai:
                st.info("🤖 AI is enhancing your note...")
                
                gemini = get_gemini_processor()
                
                enhancement_prompts = {
                    "Auto-structure and improve": f"Please analyze and improve this note. Make it clearer, better structured, and more professional:\n\n{note_content}",
                    "Extract action items": f"Extract all action items and tasks from this note. Format as a numbered list:\n\n{note_content}",
                    "Summarize key points": f"Summarize the key points from this note in bullet points:\n\n{note_content}",
                    "Convert to test cases": f"Convert this note into test cases with steps and expected results:\n\n{note_content}"
                }
                
                prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["Auto-structure and improve"])
                
                response = gemini.model.generate_content(prompt)
                ai_summary = response.text
            
            # Save to Google Sheets
            sheets_service = get_sheets_service()
            
            task_data = {
                'task_name': note_title,
                'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': note_status,
                'file_type': 'note',
                'evidence_link': '',  # No file for text notes
                'ai_summary': ai_summary,
                'context_notes': note_content  # Original note
            }
            
            task_id = sheets_service.create_task(task_data)
            
            st.success("✅ Note saved successfully!")
            
            # Display results
            st.divider()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📌 {note_title}**")
                st.markdown(f"**Status:** {note_status}")
                
                if enhance_with_ai:
                    st.markdown("**AI-Enhanced Version:**")
                    st.info(ai_summary)
                    
                    with st.expander("📝 View Original Note"):
                        st.text(note_content)
                else:
                    st.markdown("**Your Note:**")
                    st.info(note_content)
            
            with col2:
                st.markdown("**Quick Actions**")
                if st.button("➕ Add Another Note", use_container_width=True):
                    st.rerun()
            
            logger.info(f"Saved note: {note_title} (ID: {task_id})")
    
    except Exception as e:
        st.error(f"❌ Error saving note: {str(e)}")
        logger.error(f"Note save failed: {str(e)}")

# Recent notes
st.divider()
st.markdown("### 📋 Recent Notes")

try:
    sheets_service = get_sheets_service()
    all_tasks = sheets_service.get_all_tasks()
    
    # Filter for notes only
    notes = [task for task in all_tasks if task.get('File Type') == 'note']
    
    if notes:
        # Show last 5 notes
        for note in notes[-5:][::-1]:  # Reverse to show newest first
            with st.expander(f"📝 {note.get('Task Name')} - {note.get('Upload Date')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Status:** {note.get('Status')}")
                    st.markdown("**Content:**")
                    st.text(note.get('Context Notes', 'No content'))
                
                with col2:
                    if note.get('AI Summary') != note.get('Context Notes'):
                        if st.button("🤖 View AI Version", key=f"ai_{note.get('Task ID')}"):
                            st.info(note.get('AI Summary'))
    else:
        st.info("No notes yet. Create your first note above!")

except Exception as e:
    st.warning(f"Could not load recent notes: {str(e)}")

# Tips
st.divider()
st.markdown("### 💡 Tips")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Quick Notes**
    - Fast text capture
    - No file upload needed
    - Perfect for meetings
    """)

with col2:
    st.markdown("""
    **AI Enhancement**
    - Auto-structure content
    - Extract action items
    - Improve clarity
    """)

with col3:
    st.markdown("""
    **Integration**
    - Appears on Sprint Board
    - Same 5-stage workflow
    - Searchable with other tasks
    """)
