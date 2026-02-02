"""
Generate Outputs Page
AI-powered generation of test cases, requirement docs, and scrum emails.
"""

import streamlit as st
from datetime import datetime, timedelta
import io

from services.google_sheets import get_sheets_service
from services.gemini_processor import get_gemini_processor
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Generate Outputs - FLUX",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Generate Outputs")
st.markdown("Transform your tasks into professional deliverables with AI.")

# Tabs for different outputs
tab1, tab2, tab3 = st.tabs(["📝 Test Cases", "📄 Requirement Doc", "📧 Scrum Email"])

# Load tasks
try:
    sheets_service = get_sheets_service()
    all_tasks = sheets_service.get_all_tasks()
    done_tasks = [task for task in all_tasks if task.get('Status') == 'Done']
    
except Exception as e:
    st.error(f"❌ Failed to load tasks: {str(e)}")
    st.stop()

# TAB 1: Test Cases
with tab1:
    st.markdown("### Generate Test Cases (CSV)")
    st.markdown("Creates TestRail-compatible CSV from completed tasks.")
    
    st.info(f"📊 Found **{len(done_tasks)}** completed tasks")
    
    if len(done_tasks) == 0:
        st.warning("⚠️ No completed tasks found. Mark some tasks as 'Done' to generate test cases.")
    else:
        # Preview tasks
        with st.expander(f"📋 Preview {len(done_tasks)} Tasks"):
            for task in done_tasks[:10]:  # Show first 10
                st.markdown(f"- **{task.get('Task Name')}** ({task.get('File Type')})")
            if len(done_tasks) > 10:
                st.markdown(f"... and {len(done_tasks) - 10} more")
        
        if st.button("🚀 Generate Test Cases CSV", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is generating test cases..."):
                try:
                    gemini = get_gemini_processor()
                    csv_content = gemini.generate_test_cases(done_tasks)
                    
                    # Store in session state
                    st.session_state['test_cases_csv'] = csv_content
                    st.session_state['test_cases_timestamp'] = datetime.now()
                    
                    from utils.toast import success_toast
                    success_toast("Test cases generated successfully!")
                    
                    logger.info(f"Generated test cases CSV")
                    
                except Exception as e:
                    from utils.toast import error_toast
                    error_toast(f"Generation failed: {str(e)}")
                    logger.error(f"Test case generation error: {str(e)}")
        
        # Show preview if available
        if 'test_cases_csv' in st.session_state:
            csv_content = st.session_state['test_cases_csv']
            timestamp = st.session_state.get('test_cases_timestamp', datetime.now())
            
            st.success(f"✅ Generated on {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Tabs for different views
            preview_tab1, preview_tab2 = st.tabs(["📊 Table View", "📝 Raw CSV"])
            
            with preview_tab1:
                # Display as table
                import pandas as pd
                from io import StringIO
                try:
                    df = pd.read_csv(StringIO(csv_content))
                    st.dataframe(df, use_container_width=True, height=400)
                    st.caption(f"📊 {len(df)} test cases generated")
                except Exception as e:
                    st.code(csv_content[:500] + "..." if len(csv_content) > 500 else csv_content)
            
            with preview_tab2:
                st.code(csv_content, language="csv")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filename = f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_content,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.code(csv_content, language=None)
                    st.info("👆 Use the copy button in the code block above")
            
            with col3:
                if st.button("🔄 Generate New", use_container_width=True):
                    del st.session_state['test_cases_csv']
                    st.rerun()

# TAB 2: Requirement Document
with tab2:
    st.markdown("### Generate Requirement Document (PDF)")
    st.markdown("Creates a professional requirement document from all tasks.")
    
    st.info(f"📊 Found **{len(all_tasks)}** total tasks")
    
    if len(all_tasks) == 0:
        st.warning("⚠️ No tasks found. Upload some evidence first.")
    else:
        # Filter options
        include_filter = st.multiselect(
            "Include tasks with status:",
            ["In Review", "In Progress", "Done"],
            default=["Done"]
        )
        
        filtered_tasks = [task for task in all_tasks if task.get('Status') in include_filter]
        
        st.info(f"Will include **{len(filtered_tasks)}** tasks in the document")
        
        if st.button("🚀 Generate Requirement Document", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is generating requirement document..."):
                try:
                    gemini = get_gemini_processor()
                    markdown_content = gemini.generate_requirement_doc(filtered_tasks)
                    
                    st.success("✅ Requirement document generated!")
                    
                    # Display preview
                    st.markdown("### Preview")
                    with st.expander("View Full Content"):
                        st.markdown(markdown_content)
                    
                    # Download as markdown
                    filename = f"requirements_{datetime.now().strftime('%Y%m%d')}.md"
                    st.download_button(
                        label="⬇️ Download Markdown",
                        data=markdown_content,
                        file_name=filename,
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                    # Optional: PDF conversion
                    st.info("💡 Tip: Convert to PDF using tools like Pandoc or online markdown-to-PDF converters")
                    
                    logger.info(f"Generated requirement document: {filename}")
                    
                except Exception as e:
                    st.error(f"❌ Generation failed: {str(e)}")
                    logger.error(f"Requirement doc generation error: {str(e)}")

# TAB 3: Scrum Email
with tab3:
    st.markdown("### Generate Scrum Update Email")
    st.markdown("Creates a professional weekly summary email.")
    
    # Date range
    col1, col2 = st.columns(2)
    
    with col1:
        # Default to last Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday)
        
        week_start = st.date_input(
            "Week Start",
            value=last_monday,
            max_value=today
        )
    
    with col2:
        week_end = st.date_input(
            "Week End",
            value=today,
            max_value=today
        )
    
    # Get tasks in range
    try:
        week_tasks = sheets_service.get_tasks_by_date_range(
            datetime.combine(week_start, datetime.min.time()),
            datetime.combine(week_end, datetime.max.time())
        )
        
        completed_week_tasks = [task for task in week_tasks if task.get('Status') == 'Done']
        
        st.info(f"📊 Found **{len(completed_week_tasks)}** completed tasks in this week")
        
        if len(completed_week_tasks) == 0:
            st.warning("⚠️ No completed tasks in this date range.")
        else:
            # Preview
            with st.expander(f"📋 Preview {len(completed_week_tasks)} Tasks"):
                for task in completed_week_tasks:
                    st.markdown(f"- **{task.get('Task Name')}** - {task.get('Upload Date')}")
            
            if st.button("🚀 Generate Email Draft", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is drafting your email..."):
                    try:
                        gemini = get_gemini_processor()
                        email_content = gemini.generate_scrum_email(
                            completed_week_tasks,
                            week_start.strftime('%Y-%m-%d'),
                            week_end.strftime('%Y-%m-%d')
                        )
                        
                        st.success("✅ Email draft generated!")
                        
                        # Display email
                        st.markdown("### Email Preview")
                        st.text_area(
                            "Email Content",
                            value=email_content,
                            height=400,
                            label_visibility="collapsed"
                        )
                        
                        # Copy button
                        st.code(email_content, language=None)
                        
                        st.info("💡 Click the copy button in the top-right of the code block above")
                        
                        logger.info("Generated scrum email")
                        
                    except Exception as e:
                        st.error(f"❌ Generation failed: {str(e)}")
                        logger.error(f"Email generation error: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Failed to load tasks: {str(e)}")

# Info section
st.divider()

st.markdown("### 💡 Tips")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Test Cases**
    - Ensure tasks are marked as "Done"
    - CSV is compatible with TestRail
    - Edit in Excel if needed
    """)

with col2:
    st.markdown("""
    **Requirement Docs**
    - Include all relevant statuses
    - Review AI-generated content
    - Convert MD to PDF externally
    """)

with col3:
    st.markdown("""
    **Scrum Emails**
    - Select correct date range
    - Review before sending
    - Customize if needed
    """)
