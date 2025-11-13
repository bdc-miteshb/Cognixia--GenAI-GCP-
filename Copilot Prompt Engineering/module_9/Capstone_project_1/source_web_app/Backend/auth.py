"""
Authentication class for handling user authentication and management
"""
import hashlib
from .database import Database
from .config import Config


class Authentication:
    """Handles user authentication and management"""
    
    def __init__(self):
        """Initialize authentication with database connection"""
        self.db = Database()
    
    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """
        Register a new user
        
        Args:
            username (str): Username
            password (str): Plain text password
            email (str): Email address
            
        Returns:
            dict: Result with 'success' (bool) and 'message' (str)
        """
        # Validate inputs
        if not username or not password or not email:
            return {
                'success': False,
                'message': 'All fields are required'
            }
        
        # Check password length
        if len(password) < Config.MIN_PASSWORD_LENGTH:
            return {
                'success': False,
                'message': f'Password must be at least {Config.MIN_PASSWORD_LENGTH} characters long'
            }
        
        # Check if username already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return {
                'success': False,
                'message': 'Username already exists'
            }
        
        # Hash password and create user
        hashed_password = self.hash_password(password)
        success = self.db.create_user(username, hashed_password, email)
        
        if success:
            return {
                'success': True,
                'message': 'Account created successfully!'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to create account'
            }
    
    def login_user(self, username, password):
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            dict: Result with 'success' (bool), 'message' (str), and 'user' (dict or None)
        """
        # Validate inputs
        if not username or not password:
            return {
                'success': False,
                'message': 'Username and password are required',
                'user': None
            }
        
        # Hash password and verify credentials
        hashed_password = self.hash_password(password)
        user_data = self.db.get_user_by_credentials(username, hashed_password)
        
        if user_data:
            user = {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'created_at': user_data[3]
            }
            return {
                'success': True,
                'message': 'Login successful!',
                'user': user
            }
        else:
            return {
                'success': False,
                'message': 'Invalid username or password',
                'user': None
            }
    
    def get_user_profile(self, username):
        """
        Get user profile information
        
        Args:
            username (str): Username
            
        Returns:
            dict: User profile data or None
        """
        user_data = self.db.get_user_by_username(username)
        
        if user_data:
            return {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[3],
                'created_at': user_data[4]
            }
        return None
    
    def update_email(self, username, new_email):
        """
        Update user email
        
        Args:
            username (str): Username
            new_email (str): New email address
            
        Returns:
            dict: Result with 'success' (bool) and 'message' (str)
        """
        if not new_email:
            return {
                'success': False,
                'message': 'Email cannot be empty'
            }
        
        success = self.db.update_user_email(username, new_email)
        
        if success:
            return {
                'success': True,
                'message': 'Email updated successfully!'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to update email'
            }
    
    def change_password(self, username, old_password, new_password):
        """
        Change user password
        
        Args:
            username (str): Username
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            dict: Result with 'success' (bool) and 'message' (str)
        """
        # Validate inputs
        if not old_password or not new_password:
            return {
                'success': False,
                'message': 'All fields are required'
            }
        
        # Check new password length
        if len(new_password) < Config.MIN_PASSWORD_LENGTH:
            return {
                'success': False,
                'message': f'Password must be at least {Config.MIN_PASSWORD_LENGTH} characters long'
            }
        
        # Verify old password
        hashed_old_password = self.hash_password(old_password)
        user = self.db.get_user_by_credentials(username, hashed_old_password)
        
        if not user:
            return {
                'success': False,
                'message': 'Current password is incorrect'
            }
        
        # Update password
        hashed_new_password = self.hash_password(new_password)
        success = self.db.update_user_password(username, hashed_new_password)
        
        if success:
            return {
                'success': True,
                'message': 'Password changed successfully!'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to change password'
            }
    
    def verify_password(self, username, password):
        """
        Verify if password is correct for user
        
        Args:
            username (str): Username
            password (str): Password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        hashed_password = self.hash_password(password)
        user = self.db.get_user_by_credentials(username, hashed_password)
        return user is not None