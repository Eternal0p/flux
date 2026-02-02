"""
Sprint Board Page
Kanban-style task management interface.
"""

import streamlit as st
from datetime import datetime, timedelta

from services.google_sheets import get_sheets_service
from config import TASK_STATUSES
from utils.logger import setup_logger
from utils.auth import require_auth

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Sprint Board - FLUX",
    page_icon="📋",
    layout="wide"
)

# Require authentication
require_auth()

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

# Load tasks with loading indicator
with st.spinner("📊 Loading tasks..."):
    try:
        from services.google_sheets import get_cached_tasks
        
        # Use cached data for better performance
        all_tasks = get_cached_tasks()
        
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
        
        # Display board stats
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("📊 Total", len(all_tasks), delta=None)
        
        # Calculate counts for display (from all filtered tasks, not just current page)
        all_filtered_by_status = {status: [] for status in TASK_STATUSES}
        for task in filtered_tasks:
            status = task.get('Status', 'In Review')
            if status in all_filtered_by_status:
                all_filtered_by_status[status].append(task)
        
        col2.metric("🟡 In Review", len(all_filtered_by_status.get('In Review', [])))
        col3.metric("🟠 Passed Review", len(all_filtered_by_status.get('Passed In Review', [])))
        col4.metric("🔵 In Stage", len(all_filtered_by_status.get('In Stage', [])))
        col5.metric("🟣 Passed Stage", len(all_filtered_by_status.get('Passed In Stage', [])))
        col6.metric("🟢 Done", len(all_filtered_by_status.get('Done', [])))
        
        st.divider()
        
        # Pagination controls
        pcol1, pcol2, pcol3, pcol4 = st.columns([2, 1, 1, 1])
        
        with pcol1:
            if search_query or file_type_filter != "All Types":
                st.caption(f"🔍 Showing {len(filtered_tasks)} of {len(all_tasks)} tasks")
            else:
                st.caption(f"📊 {len(filtered_tasks)} tasks")
        
        with pcol2:
            items_per_page = st.selectbox(
                "Per page",
                options=[25, 50, 100, "All"],
                index=1,
                key="items_per_page"
            )
        
        # Initialize pagination
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Calculate pagination
        if items_per_page != "All":
            total_pages = (len(filtered_tasks) + items_per_page - 1) // items_per_page
            total_pages = max(1, total_pages)
            
            # Ensure current page is valid
            if st.session_state.current_page > total_pages:
                st.session_state.current_page = total_pages
            
            with pcol3:
                if st.button("⬅️ Prev", disabled=st.session_state.current_page == 1, use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with pcol4:
                if st.button("Next ➡️", disabled=st.session_state.current_page >= total_pages, use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()
            
            # Page indicator
            if total_pages > 1:
                st.caption(f"Page {st.session_state.current_page} of {total_pages}")
            
            # Calculate slice
            start_idx = (st.session_state.current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            
            # Slice filtered tasks for current page
            page_tasks = filtered_tasks[start_idx:end_idx]
        else:
            page_tasks = filtered_tasks
        
        # Re-group paginated tasks by status
        tasks_by_status = {status: [] for status in TASK_STATUSES}
        
        for task in page_tasks:
            status = task.get('Status', 'In Review')
            if status in tasks_by_status:
                tasks_by_status[status].append(task)
        
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
                        render_task_card(task, get_sheets_service())
                
                st.markdown("---")
    
    except Exception as e:
        st.error(f"❌ **Failed to load tasks**")
        st.error(f"**Error:** {str(e)}")
        st.info("💡 **Try:**\n- Refresh the page\n- Check your internet connection\n- Verify Google Sheets access")
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
        col1, col2, col3 = st.columns(3)
        
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
                with st.spinner("Updating..."):
                    try:
                        sheets_service.update_task_status(task_id, new_status)
                        from utils.toast import success_toast
                        success_toast(f"Task moved to {new_status}")
                        st.cache_data.clear()  # Clear cache to show update
                        st.rerun()
                    except Exception as e:
                        from utils.toast import error_toast
                        error_toast(f"Failed to update: {str(e)}")
        
        with col3:
            # Edit button
            if st.button("✏️", key=f"edit_{task_id}", use_container_width=True, help="Edit task"):
                st.session_state[f"editing_{task_id}"] = True
                st.rerun()
        
        # Edit modal
        if st.session_state.get(f"editing_{task_id}", False):
            with st.expander("✏️ Edit Task", expanded=True):
                new_name = st.text_input(
                    "Task Name",
                    value=task_name,
                    key=f"name_{task_id}"
                )
                
                context_notes = task.get('Context Notes', '')
                new_notes = st.text_area(
                    "Context Notes",
                    value=context_notes,
                    key=f"notes_{task_id}",
                    height=100
                )
                
                col_save, col_cancel = st.columns(2)
                
                with col_save:
                    if st.button("💾 Save", key=f"save_{task_id}", use_container_width=True):
                        updates = {}
                        if new_name != task_name:
                            updates['Task Name'] = new_name
                        if new_notes != context_notes:
                            updates['Context Notes'] = new_notes
                        
                        if updates:
                            with st.spinner("Saving..."):
                                try:
                                    sheets_service.update_task(task_id, updates)
                                    from utils.toast import success_toast
                                    success_toast("Task updated successfully!")
                                    st.session_state[f"editing_{task_id}"] = False
                                    st.cache_data.clear()
                                    st.rerun()
                                except Exception as e:
                                    from utils.toast import error_toast
                                    error_toast(f"Failed to save: {str(e)}")
                        else:
                            st.info("No changes to save")
                
                with col_cancel:
                    if st.button("❌ Cancel", key=f"cancel_{task_id}", use_container_width=True):
                        st.session_state[f"editing_{task_id}"] = False
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

# Empty state
if 'all_tasks' in locals() and len(all_tasks) == 0:
    st.info("📭 No tasks yet. Upload your first evidence file to get started!")
    if st.button("➕ Upload Evidence"):
        st.switch_page("pages/1_📤_Upload.py")
