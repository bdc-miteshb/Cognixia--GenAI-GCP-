"""
Frontend UI for the Login System using Streamlit
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import Backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from Backend.auth import Authentication
from Backend.config import Config


class Frontend:
    """Handles all frontend UI components"""
    
    def __init__(self):
        """Initialize frontend with authentication"""
        self.auth = Authentication()
        self.init_session_state()
    
    @staticmethod
    def init_session_state():
        """Initialize session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
    
    def configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title=Config.APP_TITLE,
            page_icon=Config.APP_ICON,
            layout=Config.LAYOUT
        )
    
    def render_login_tab(self):
        """Render the login tab"""
        st.subheader("Login to your account")
        
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                if login_username and login_password:
                    result = self.auth.login_user(login_username, login_password)
                    
                    if result['success']:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.user_data = result['user']
                        st.success(result['message'])
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.warning("Please enter both username and password")
    
    def render_signup_tab(self):
        """Render the signup tab"""
        st.subheader("Create a new account")
        
        signup_username = st.text_input("Username", key="signup_username")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_password_confirm = st.text_input(
            "Confirm Password", 
            type="password", 
            key="signup_password_confirm"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Sign Up", type="primary", use_container_width=True):
                if signup_username and signup_password and signup_email:
                    if signup_password == signup_password_confirm:
                        result = self.auth.register_user(
                            signup_username, 
                            signup_password, 
                            signup_email
                        )
                        
                        if result['success']:
                            st.success(result['message'])
                            st.info("Please login with your credentials.")
                        else:
                            st.error(result['message'])
                    else:
                        st.error("Passwords do not match")
                else:
                    st.warning("Please fill in all fields")
    
    def render_login_page(self):
        """Render the login/signup page"""
        st.title(f"{Config.APP_ICON} Welcome to the App")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            self.render_login_tab()
        
        with tab2:
            self.render_signup_tab()
    
    def render_sidebar(self):
        """Render the sidebar navigation"""
        with st.sidebar:
            st.header("Navigation")
            page = st.radio(
                "Go to", 
                ["Home", "Profile", "Settings"],
                key="navigation"
            )
            st.divider()
            
            if st.button("Logout", type="primary", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_data = None
                st.rerun()
            
            return page
    
    def render_home_page(self):
        """Render the home dashboard page"""
        st.header("🏠 Home Dashboard")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Total Projects", value="12", delta="2")
        
        with col2:
            st.metric(label="Tasks Completed", value="45", delta="5")
        
        with col3:
            st.metric(label="Active Users", value="8", delta="-1")
        
        st.divider()
        
        # Recent Activity
        st.subheader("Recent Activity")
        activities = [
            "📊 Project Alpha - Updated 2 hours ago",
            "✅ Task completed - 5 hours ago",
            "👥 New user joined - Yesterday",
            "📝 Document uploaded - 2 days ago"
        ]
        
        for activity in activities:
            st.write(activity)
        
        st.divider()
        
        # Quick Actions
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📁 Create New Project", use_container_width=True):
                st.info("Project creation feature coming soon!")
        
        with col2:
            if st.button("📊 View Reports", use_container_width=True):
                st.info("Reports feature coming soon!")
        
        with col3:
            if st.button("⚙️ Manage Tasks", use_container_width=True):
                st.info("Task management feature coming soon!")
    
    def render_profile_page(self):
        """Render the profile page"""
        st.header("👤 User Profile")
        
        # Get user profile data
        user_profile = self.auth.get_user_profile(st.session_state.username)
        
        if user_profile:
            # Display user information
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Username:**")
                st.info(user_profile['username'])
                
                st.write("**Email:**")
                st.info(user_profile['email'])
            
            with col2:
                st.write("**User ID:**")
                st.info(user_profile['id'])
                
                st.write("**Member Since:**")
                st.info(user_profile['created_at'])
            
            st.divider()
            
            # Update email section
            st.subheader("Update Email")
            new_email = st.text_input(
                "New Email", 
                value=user_profile['email'],
                key="new_email"
            )
            
            if st.button("Update Email", type="primary"):
                if new_email != user_profile['email']:
                    result = self.auth.update_email(st.session_state.username, new_email)
                    
                    if result['success']:
                        st.success(result['message'])
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.info("Email is the same as current email")
        else:
            st.error("Failed to load profile data")
    
    def render_settings_page(self):
        """Render the settings page"""
        st.header("⚙️ Settings")
        
        # Change password section
        st.subheader("Change Password")
        
        old_password = st.text_input("Current Password", type="password", key="old_pass")
        new_password = st.text_input("New Password", type="password", key="new_pass")
        confirm_password = st.text_input(
            "Confirm New Password", 
            type="password", 
            key="confirm_pass"
        )
        
        if st.button("Change Password", type="primary"):
            if old_password and new_password and confirm_password:
                if new_password == confirm_password:
                    result = self.auth.change_password(
                        st.session_state.username,
                        old_password,
                        new_password
                    )
                    
                    if result['success']:
                        st.success(result['message'])
                    else:
                        st.error(result['message'])
                else:
                    st.error("New passwords do not match")
            else:
                st.warning("Please fill in all fields")
        
        st.divider()
        
        # Preferences section
        st.subheader("Preferences")
        
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "Auto"],
            index=0,
            key="theme_select"
        )
        
        notifications = st.checkbox("Enable notifications", value=True)
        
        if st.button("Save Preferences"):
            st.info("Preferences feature coming soon!")
        
        st.divider()
        
        # Danger zone
        st.subheader("⚠️ Danger Zone")
        st.warning("Deleting your account is permanent and cannot be undone.")
        
        if st.button("Delete Account", type="secondary"):
            st.error("Account deletion is disabled for safety")
    
    def render_dashboard(self):
        """Render the main dashboard"""
        st.title(f"👋 Welcome, {st.session_state.username}!")
        
        # Render sidebar and get selected page
        page = self.render_sidebar()
        
        # Render selected page
        if page == "Home":
            self.render_home_page()
        elif page == "Profile":
            self.render_profile_page()
        elif page == "Settings":
            self.render_settings_page()
    
    def run(self):
        """Main method to run the application"""
        self.configure_page()
        
        if st.session_state.logged_in:
            self.render_dashboard()
        else:
            self.render_login_page()


# Main entry point
if __name__ == "__main__":
    app = Frontend()
    app.run()