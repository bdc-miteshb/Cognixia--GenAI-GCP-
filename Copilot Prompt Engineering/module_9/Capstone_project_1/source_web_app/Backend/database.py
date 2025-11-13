"""
Database class for handling all database operations
"""
import sqlite3
from datetime import datetime
from .config import Config


class Database:
    """Handles all database operations"""
    
    def __init__(self, db_name=None):
        """Initialize database connection"""
        self.db_name = db_name or Config.DATABASE_NAME
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, password, email):
        """
        Create a new user in the database
        
        Args:
            username (str): Username
            password (str): Hashed password
            email (str): User email
            
        Returns:
            bool: True if user created successfully, False otherwise
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                (username, password, email)
            )
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def get_user_by_username(self, username):
        """
        Get user by username
        
        Args:
            username (str): Username to search for
            
        Returns:
            tuple: User data (id, username, password, email, created_at) or None
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, username, password, email, created_at FROM users WHERE username = ?',
                (username,)
            )
            
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_user_by_credentials(self, username, hashed_password):
        """
        Get user by username and password
        
        Args:
            username (str): Username
            hashed_password (str): Hashed password
            
        Returns:
            tuple: User data or None
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, username, email, created_at FROM users WHERE username = ? AND password = ?',
                (username, hashed_password)
            )
            
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def update_user_email(self, username, new_email):
        """
        Update user email
        
        Args:
            username (str): Username
            new_email (str): New email address
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE users SET email = ? WHERE username = ?',
                (new_email, username)
            )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating email: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def update_user_password(self, username, new_hashed_password):
        """
        Update user password
        
        Args:
            username (str): Username
            new_hashed_password (str): New hashed password
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE users SET password = ? WHERE username = ?',
                (new_hashed_password, username)
            )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def delete_user(self, username):
        """
        Delete a user from database
        
        Args:
            username (str): Username to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def get_all_users(self):
        """
        Get all users (without passwords)
        
        Returns:
            list: List of tuples containing user data
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username, email, created_at FROM users')
            
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            if conn:
                conn.close()