#!/usr/bin/env python3
"""
Database setup script for Split App
Run this script to create the database and tables locally
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Make sure environment variables are set manually.")

def create_database():
    """Create the database if it doesn't exist"""
    
    # Database connection parameters
    db_host = os.environ.get('PGHOST', 'localhost')
    db_port = os.environ.get('PGPORT', '5432')
    db_user = os.environ.get('PGUSER', 'splitapp_user')
    db_password = os.environ.get('PGPASSWORD', 'password')
    db_name = os.environ.get('PGDATABASE', 'splitapp')
    
    print(f"Setting up database '{db_name}' on {db_host}:{db_port}")
    
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user='postgres',  # Use postgres superuser to create database
            password=input("Enter PostgreSQL postgres user password: ")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print("Database created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")
        
        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"Creating user '{db_user}'...")
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
            print("User created successfully!")
        else:
            print(f"User '{db_user}' already exists.")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE "{db_name}" TO {db_user}')
        
        cursor.close()
        conn.close()
        
        print("Database setup completed successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"Error setting up database: {e}")
        return False
    except KeyboardInterrupt:
        print("\nSetup cancelled by user.")
        return False

def create_tables():
    """Create application tables"""
    try:
        # Import Flask app to create tables
        from app import app, db
        
        with app.app_context():
            print("Creating application tables...")
            db.create_all()
            print("Tables created successfully!")
            return True
            
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("Split App - Database Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\nWarning: .env file not found!")
        print("Please copy .env.example to .env and configure your database settings.")
        print("Example:")
        print("  cp .env.example .env")
        print("  # Edit .env with your database credentials")
        
        create_env = input("\nDo you want to create a basic .env file now? (y/n): ").lower()
        if create_env == 'y':
            with open('.env', 'w') as f:
                db_password = input("Enter password for splitapp_user: ")
                secret_key = input("Enter Flask secret key (or press Enter for default): ") or "dev-secret-key-change-in-production"
                
                f.write(f"""# Database Configuration
DATABASE_URL=postgresql://splitapp_user:{db_password}@localhost:5432/splitapp

# Flask Configuration
FLASK_SECRET_KEY={secret_key}
FLASK_ENV=development
FLASK_DEBUG=True

# PostgreSQL Connection Details
PGHOST=localhost
PGPORT=5432
PGDATABASE=splitapp
PGUSER=splitapp_user
PGPASSWORD={db_password}
""")
            print(".env file created!")
            
            # Reload environment variables
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
    
    # Create database and user
    if not create_database():
        print("Failed to setup database. Please check your PostgreSQL installation and try again.")
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        print("Failed to create tables. Please check your configuration and try again.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nYou can now run the application with:")
    print("  python main.py")
    print("\nOr using Flask:")
    print("  flask run")
    print("\nThe application will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()