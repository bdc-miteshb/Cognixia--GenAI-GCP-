"""
Configuration file for the application
"""

class Config:
    """Application configuration"""
    
    # Database settings
    DATABASE_NAME = 'users.db'
    
    # Security settings
    MIN_PASSWORD_LENGTH = 6
    
    # App settings
    APP_TITLE = "Login System"
    APP_ICON = "🔐"
    LAYOUT = "wide"
