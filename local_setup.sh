#!/bin/bash

# Split App - Local Setup Script for Unix/Linux/macOS
# This script automates the local setup process

set -e  # Exit on any error

echo "=================================================="
echo "Split App - Automated Local Setup"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL not found in PATH"
    echo "Please install PostgreSQL:"
    echo "  - Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "  - macOS: brew install postgresql"
    echo "  - Windows: Download from https://postgresql.org"
    read -p "Press Enter when PostgreSQL is installed and running..."
fi

echo "✓ PostgreSQL found: $(psql --version | head -n1)"

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements_local.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env configuration file..."
    cp .env.example .env
    
    echo "Please configure your database settings:"
    read -p "Enter PostgreSQL password for splitapp_user: " db_password
    read -p "Enter Flask secret key (or press Enter for default): " secret_key
    
    if [ -z "$secret_key" ]; then
        secret_key="dev-secret-key-change-in-production"
    fi
    
    # Update .env file
    sed -i.bak "s/your_password_here/$db_password/g" .env
    sed -i.bak "s/your-secret-key-change-this-in-production/$secret_key/g" .env
    rm .env.bak 2>/dev/null || true
    
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Setup database
echo "Setting up database..."
python setup_database.py

echo ""
echo "=================================================="
echo "Setup completed successfully!"
echo "=================================================="
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: python run_local.py"
echo "   or: python main.py"
echo ""
echo "The application will be available at: http://localhost:5000"
echo ""
echo "To deactivate virtual environment later: deactivate"