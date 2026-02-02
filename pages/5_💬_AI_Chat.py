"""
AI Chat Page
Intelligent chat assistant that can discuss tasks and evidence using Gemini.
"""

import streamlit as st
from datetime import datetime

from services.google_sheets import get_sheets_service
from services.google_drive import get_drive_service
from services.gemini_processor import get_gemini_processor
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="AI Chat - FLUX",
    page_icon="💬",
    layout="wide"
)

st.title("💬 AI Chat Assistant")
st.markdown("Chat with AI about your tasks, evidence, and workflow.")

# Add custom CSS for animations
st.markdown("""
<style>
    /* Typing indicator animation */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .stChatMessage {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Thinking indicator */
    .thinking-indicator {
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history in session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "context_loaded" not in st.session_state:
    st.session_state.context_loaded = False

# Load context button
if not st.session_state.context_loaded:
    st.info("💡 Click 'Load Context' to let the AI access your tasks and evidence for more intelligent responses.")
    
    if st.button("🔄 Load Context from Drive & Sheets", type="primary"):
        with st.spinner("Loading your tasks and evidence..."):
            try:
                sheets_service = get_sheets_service()
                all_tasks = sheets_service.get_all_tasks()
                
                # Build context
                context_summary = f"You have {len(all_tasks)} tasks in total.\n\n"
                
                # Group by status
                from config import TASK_STATUSES
                for status in TASK_STATUSES:
                    tasks_in_status = [t for t in all_tasks if t.get('Status') == status]
                    if tasks_in_status:
                        context_summary += f"{status}: {len(tasks_in_status)} tasks\n"
                        for task in tasks_in_status[:3]:  # Show first 3 of each status
                            context_summary += f"  - {task.get('Task Name')} ({task.get('File Type')})\n"
                
                # Recent tasks
                context_summary += f"\nRecent tasks:\n"
                for task in all_tasks[-5:]:
                    context_summary += f"- {task.get('Task Name')}: {task.get('AI Summary', 'No summary')[:100]}...\n"
                
                st.session_state.task_context = context_summary
                st.session_state.all_tasks = all_tasks
                st.session_state.context_loaded = True
                
                st.success("✅ Context loaded! AI can now discuss your tasks intelligently.")
                st.rerun()
            
            except Exception as e:
                st.error(f"Failed to load context: {str(e)}")

# Chat interface
st.divider()

# Display chat messages
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your tasks, evidence, or workflow..."):
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Show typing indicator
            message_placeholder.markdown("🤔 Thinking...")
            
            gemini = get_gemini_processor()
            
            # Build context-aware prompt
            if st.session_state.context_loaded:
                system_context = f"""You are an AI assistant for a task management system called "FLUX". 

Here's the current state of the user's tasks:

{st.session_state.task_context}

The user has a 5-stage workflow: In Review → Passed In Review → In Stage → Passed In Stage → Done.

Answer the user's question based on this context. Be helpful, concise, and actionable.

User question: {prompt}"""
            else:
                system_context = f"""You are an AI assistant for a task management system called "FLUX". 

The user hasn't loaded their context yet, so you don't have access to their specific tasks. 
You can still help with general questions about task management, workflows, and best practices.

Note: Suggest they click "Load Context" if they want to discuss their specific tasks.

User question: {prompt}"""
            
            # Generate response
            response = gemini.model.generate_content(system_context)
            full_response = response.text
            
            # Simulate typing effect
            displayed_text = ""
            words = full_response.split()
            
            for i, word in enumerate(words):
                displayed_text += word + " "
                if i % 5 == 0:  # Update every 5 words for smooth animation
                    message_placeholder.markdown(displayed_text + "▌")
                    
            # Show final response
            message_placeholder.markdown(full_response)
            
            # Save assistant response
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": full_response
            })
            
            logger.info(f"Chat exchange - User: {prompt[:50]}... | AI: {full_response[:50]}...")
        
        except Exception as e:
            error_msg = f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try:\n- Reloading the page\n- Checking your internet connection\n- Verifying your Gemini API key is valid"
            message_placeholder.markdown(error_msg)
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": error_msg
            })
            logger.error(f"Chat error: {str(e)}")

# Sidebar with quick actions
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("🔄 Reload Context", use_container_width=True):
        st.session_state.context_loaded = False
        st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("### 💡 Suggested Questions")
    
    suggestions = [
        "What tasks are in review?",
        "Summarize my completed tasks",
        "What should I work on next?",
        "Show me high priority items",
        "What's the status of [task name]?",
        "How many tasks do I have total?",
        "What tasks passed staging?",
        "List all bugs in progress"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=suggestion, use_container_width=True):
            # Simulate user asking the question
            st.session_state.chat_messages.append({"role": "user", "content": suggestion})
            st.rerun()
    
    st.divider()
    
    st.markdown("### ℹ️ Context Status")
    if st.session_state.context_loaded:
        st.success("✅ Context loaded")
        st.metric("Tasks Loaded", len(st.session_state.get("all_tasks", [])))
    else:
        st.warning("⚠️ Context not loaded")
        st.info("Load context to enable AI to discuss your specific tasks")

# Initial welcome message
if len(st.session_state.chat_messages) == 0:
    st.info("""
    👋 **Welcome to AI Chat!**
    
    I can help you with:
    - 📊 Analyzing your task status
    - 🔍 Finding specific tasks
    - 📈 Tracking your progress
    - 💡 Suggesting next actions
    - ❓ Answering questions about your workflow
    
    **Tip**: Load context first for personalized responses about your tasks!
    """)
