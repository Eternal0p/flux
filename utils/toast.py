"""
Toast notification utility for FLUX.
Provides success, error, info, and warning notifications.
"""

import streamlit as st
from datetime import datetime
import time

def show_toast(message: str, icon: str = "ℹ️", duration: int = 3):
    """
    Show a toast notification.
    
    Args:
        message: Message to display
        icon: Emoji icon
        duration: Duration in seconds
    """
    toast_placeholder = st.empty()
    
    toast_html = f"""
    <style>
        @keyframes slideIn {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        
        @keyframes slideOut {{
            from {{
                transform: translateX(0);
                opacity: 1;
            }}
            to {{
                transform: translateX(100%);
                opacity: 0;
            }}
        }}
        
        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            padding: 12px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
        }}
        
        .toast-icon {{
            font-size: 24px;
        }}
        
        .toast-message {{
            font-size: 14px;
            color: #333;
        }}
    </style>
    
    <div class="toast">
        <span class="toast-icon">{icon}</span>
        <span class="toast-message">{message}</span>
    </div>
    """
    
    toast_placeholder.markdown(toast_html, unsafe_allow_html=True)
    time.sleep(duration)
    toast_placeholder.empty()

def success_toast(message: str):
    """Show success toast."""
    st.success(f"✅ {message}", icon="✅")

def error_toast(message: str):
    """Show error toast."""
    st.error(f"❌ {message}", icon="❌")

def info_toast(message: str):
    """Show info toast."""
    st.info(f"ℹ️ {message}", icon="ℹ️")

def warning_toast(message: str):
    """Show warning toast."""
    st.warning(f"⚠️ {message}", icon="⚠️")
