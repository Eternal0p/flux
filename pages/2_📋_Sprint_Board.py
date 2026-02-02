"""
Sprint Board Page
Kanban-style task management interface.
"""

import streamlit as st
from datetime import datetime, timedelta

from services.google_sheets import get_sheets_service
from config import TASK_STATUSES
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Sprint Board - FLUX",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Sprint Board")
st.markdown("Manage your tasks in a Kanban-style board.")

# Filters
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    search_query = st.text_input("🔍 Search tasks", placeholder="Search by name...")

with col2:
    file_type_filter = st.selectbox(
        "📁 Filter by type",
        ["All Types", "video", "document", "spreadsheet", "image"]
    )

with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.divider()

# Load tasks
try:
    sheets_service = get_sheets_service()
    all_tasks = sheets_service.get_all_tasks()
    
    # Apply filters
    filtered_tasks = all_tasks
    
    if search_query:
        filtered_tasks = [
            task for task in filtered_tasks 
            if search_query.lower() in task.get('Task Name', '').lower()
        ]
    
    if file_type_filter != "All Types":
        filtered_tasks = [
            task for task in filtered_tasks 
            if task.get('File Type', '') == file_type_filter
        ]
    
    # Group by status
    tasks_by_status = {status: [] for status in TASK_STATUSES}
    
    for task in filtered_tasks:
        status = task.get('Status', 'In Review')
        if status in tasks_by_status:
            tasks_by_status[status].append(task)
    
    # Display board stats
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Tasks", len(all_tasks))
    col2.metric("In Review", len(tasks_by_status.get('In Review', [])))
    col3.metric("Passed Review", len(tasks_by_status.get('Passed In Review', [])))
    col4.metric("In Stage", len(tasks_by_status.get('In Stage', [])))
    col5.metric("Passed Stage", len(tasks_by_status.get('Passed In Stage', [])))
    col6.metric("Done", len(tasks_by_status.get('Done', [])))
    
    st.divider()
    
    # Kanban columns - 5 columns
    cols = st.columns(5)
    
    status_colors = {
        "In Review": "🟡",
        "Passed In Review": "🟠",
        "In Stage": "🔵",
        "Passed In Stage": "🟣",
        "Done": "🟢"
    }
    
    for idx, status in enumerate(TASK_STATUSES):
        with cols[idx]:
            st.markdown(f"### {status_colors[status]} {status}")
            st.markdown(f"*{len(tasks_by_status[status])} tasks*")
            
            tasks = tasks_by_status[status]
            
            if not tasks:
                st.info(f"No tasks in {status}")
            else:
                for task in tasks:
                    render_task_card(task, sheets_service)
            
            st.markdown("---")

except Exception as e:
    st.error(f"❌ Failed to load tasks: {str(e)}")
    logger.error(f"Board error: {str(e)}")

def render_task_card(task: dict, sheets_service):
    """Render a task card with actions."""
    
    task_id = task.get('Task ID', '')
    task_name = task.get('Task Name', 'Untitled')
    upload_date = task.get('Upload Date', '')
    status = task.get('Status', 'In Review')
    file_type = task.get('File Type', '')
    evidence_link = task.get('Evidence Link', '')
    ai_summary = task.get('AI Summary', '')
    
    # Card container
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            background: white;
        ">
            <h4 style="margin: 0 0 0.5rem 0;">{task_name}</h4>
            <p style="font-size: 0.85rem; color: #666; margin: 0;">
                📅 {upload_date}<br>
                📁 {file_type.title() if file_type else 'Unknown'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary (expandable)
        with st.expander("📝 View Summary"):
            try:
                # Try to parse JSON summary
                import json
                summary_data = json.loads(ai_summary) if ai_summary else {}
                
                if isinstance(summary_data, dict):
                    summary_text = summary_data.get('summary', ai_summary)
                else:
                    summary_text = str(ai_summary)
                    
                st.markdown(summary_text)
                
                # Show other fields if available
                if isinstance(summary_data, dict):
                    for key, value in summary_data.items():
                        if key != 'summary' and key != 'task_name':
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            except:
                st.text(ai_summary[:200] + "..." if len(ai_summary) > 200 else ai_summary)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if evidence_link:
                st.link_button("👁️ Evidence", evidence_link, use_container_width=True)
        
        with col2:
            # Status update
            new_status = st.selectbox(
                "Status",
                TASK_STATUSES,
                index=TASK_STATUSES.index(status),
                key=f"status_{task_id}",
                label_visibility="collapsed"
            )
            
            if new_status != status:
                try:
                    sheets_service.update_task_status(task_id, new_status)
                    st.success("✅ Updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)

# Empty state
if 'all_tasks' in locals() and len(all_tasks) == 0:
    st.info("📭 No tasks yet. Upload your first evidence file to get started!")
    if st.button("➕ Upload Evidence"):
        st.switch_page("pages/1_📤_Upload.py")
