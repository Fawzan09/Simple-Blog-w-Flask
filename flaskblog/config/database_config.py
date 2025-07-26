"""
Database configuration for Flask Blog
Supports both SQLite (development) and MySQL (production)
"""
import os
from urllib.parse import quote_plus

class DatabaseConfig:
    @staticmethod
    def get_database_uri():
        """
        Returns appropriate database URI based on environment
        """
        # Check if MySQL configuration is provided
        mysql_host = os.environ.get('MYSQL_HOST')
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_password = os.environ.get('MYSQL_PASSWORD')
        mysql_db = os.environ.get('MYSQL_DATABASE')
        
        if all([mysql_host, mysql_user, mysql_password, mysql_db]):
            # Use MySQL if all required environment variables are set
            password_encoded = quote_plus(mysql_password)
            return f'mysql+pymysql://{mysql_user}:{password_encoded}@{mysql_host}/{mysql_db}'
        else:
            # Fallback to SQLite for development
            return 'sqlite:///site.db'
    
    @staticmethod
    def get_mysql_config():
        """
        Returns MySQL configuration dictionary
        """
        return {
            'host': os.environ.get('MYSQL_HOST', 'localhost'),
            'user': os.environ.get('MYSQL_USER', 'flaskblog'),
            'password': os.environ.get('MYSQL_PASSWORD', ''),
            'database': os.environ.get('MYSQL_DATABASE', 'flaskblog'),
            'port': int(os.environ.get('MYSQL_PORT', 3306))
        }