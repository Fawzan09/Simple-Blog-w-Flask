"""
Database Migration Script for Flask Blog
Handles migration from SQLite to MySQL and adds new Review table
"""

import os
import sys
import sqlite3
from urllib.parse import quote_plus

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flaskblog import create_app, db
from flaskblog.models import User, Post, Review

def create_mysql_database():
    """Create MySQL database if it doesn't exist"""
    try:
        import pymysql
        
        mysql_config = {
            'host': os.environ.get('MYSQL_HOST', 'localhost'),
            'user': os.environ.get('MYSQL_USER', 'root'),
            'password': os.environ.get('MYSQL_PASSWORD', ''),
            'port': int(os.environ.get('MYSQL_PORT', 3306))
        }
        
        database_name = os.environ.get('MYSQL_DATABASE', 'flaskblog')
        
        # Connect to MySQL server
        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.close()
        connection.close()
        
        print(f"MySQL database '{database_name}' created successfully")
        return True
    except ImportError:
        print("PyMySQL not installed. Skipping MySQL database creation.")
        return False
    except Exception as e:
        print(f"Error creating MySQL database: {e}")
        return False

def migrate_sqlite_to_mysql():
    """Migrate data from SQLite to MySQL"""
    sqlite_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'flaskblog', 'site.db')
    
    if not os.path.exists(sqlite_path):
        print("No SQLite database found. Creating fresh database.")
        return True
    
    try:
        # Check if MySQL is configured
        if not all([os.environ.get('MYSQL_HOST'), os.environ.get('MYSQL_USER'), 
                   os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_DATABASE')]):
            print("MySQL configuration not found. Keeping SQLite database.")
            return True
        
        # Create Flask app with MySQL configuration
        app = create_app()
        
        with app.app_context():
            # Drop and recreate all tables
            db.drop_all()
            db.create_all()
            
            # Connect to SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_conn.row_factory = sqlite3.Row
            
            # Migrate Users
            cursor = sqlite_conn.execute("SELECT * FROM user")
            users = cursor.fetchall()
            
            for user_row in users:
                user = User(
                    id=user_row['id'],
                    username=user_row['username'],
                    email=user_row['email'],
                    image_file=user_row['image_file'],
                    password=user_row['password']
                )
                db.session.add(user)
            
            # Migrate Posts
            cursor = sqlite_conn.execute("SELECT * FROM post")
            posts = cursor.fetchall()
            
            for post_row in posts:
                post = Post(
                    id=post_row['id'],
                    title=post_row['title'],
                    date_posted=post_row['date_posted'],
                    content=post_row['content'],
                    user_id=post_row['user_id']
                )
                db.session.add(post)
            
            # Commit the migration
            db.session.commit()
            sqlite_conn.close()
            
            print("Data migration from SQLite to MySQL completed successfully")
            return True
            
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

def initialize_database():
    """Initialize database with tables"""
    try:
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("Database tables created successfully")
            
            # Create a default admin user if no users exist
            if User.query.count() == 0:
                from flaskblog import bcrypt
                hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
                admin_user = User(
                    username='admin',
                    email='admin@flaskblog.com',
                    password=hashed_password
                )
                db.session.add(admin_user)
                db.session.commit()
                print("Default admin user created (username: admin, password: admin123)")
            
            return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    print("Flask Blog Database Migration Script")
    print("====================================")
    
    # Check if MySQL is configured
    if all([os.environ.get('MYSQL_HOST'), os.environ.get('MYSQL_USER'), 
           os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_DATABASE')]):
        print("MySQL configuration detected")
        
        # Create MySQL database
        if create_mysql_database():
            # Attempt migration
            if migrate_sqlite_to_mysql():
                print("Migration completed successfully")
            else:
                print("Migration failed, but continuing with initialization")
                initialize_database()
        else:
            print("Failed to create MySQL database")
    else:
        print("Using SQLite database")
        initialize_database()