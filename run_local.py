#!/usr/bin/env python3
"""
Local development server for Split App
Alternative to main.py with better local development features
"""

import os
import sys

# Load environment variables from .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")
    print("Or set environment variables manually")

# Import the Flask app
try:
    from app import app
    print("Flask application imported successfully")
except ImportError as e:
    print(f"Error importing Flask app: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements_local.txt")
    sys.exit(1)

def check_database_connection():
    """Check if database connection is working"""
    try:
        from app import db
        with app.app_context():
            # Try to execute a simple query
            db.session.execute(db.text('SELECT 1'))
            print("Database connection successful")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Please check your DATABASE_URL in .env file")
        print("Run setup_database.py to create the database")
        return False

def main():
    """Main function to run the local development server"""
    print("=" * 50)
    print("Split App - Local Development Server")
    print("=" * 50)
    
    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Warning: DATABASE_URL not set!")
        print("Please create a .env file or set environment variables")
        print("Example DATABASE_URL: postgresql://user:password@localhost:5432/splitapp")
    
    # Check database connection
    if not check_database_connection():
        print("\nDatabase setup required. Run: python setup_database.py")
        return
    
    # Get configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\nStarting development server on http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run the Flask development server
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    main()