"""
Simple authentication utility for FLUX.
Password-based access control.
"""

import streamlit as st
import hashlib

# Password hash (for security - don't store plain text)
# Password: 987654321
PASSWORD_HASH = "c18f0a5262d2956fe5beace7bde6f2e0dcbbda83945b0b310cc0cc4abe29ee4e"

def hash_password(password: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str) -> bool:
    """Check if the provided password is correct."""
    return hash_password(password) == PASSWORD_HASH

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)

def login(password: str) -> bool:
    """Attempt to log in with provided password."""
    if check_password(password):
        st.session_state['authenticated'] = True
        return True
    return False

def logout():
    """Log out the current user."""
    st.session_state['authenticated'] = False

def require_auth():
    """
    Require authentication to access the current page.
    Shows login form if not authenticated.
    Returns True if authenticated, False otherwise.
    """
    if is_authenticated():
        return True
    
    # Show login form
    st.markdown("# 🔒 FLUX Login")
    st.markdown("Enter password to access FLUX")
    
    with st.form("login_form"):
        password = st.text_input(
            "Password", 
            type="password",
            placeholder="Enter password..."
        )
        submit = st.form_submit_button("🔓 Login", use_container_width=True)
        
        if submit:
            if login(password):
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    
    st.stop()  # Stop execution if not authenticated
    return False
