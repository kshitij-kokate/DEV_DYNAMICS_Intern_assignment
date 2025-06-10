# Split App - Local Setup Guide

A production-ready expense splitting application with modern UI built with Flask and PostgreSQL.

## Features

- 💰 **Expense Tracking**: Add, edit, and delete expenses with categories
- 👥 **Automatic Person Management**: People are added automatically when creating expenses
- ⚖️ **Balance Calculations**: See who owes money and who should receive money
- 🔄 **Smart Settlements**: Optimized calculations to minimize number of transactions
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 🎨 **Modern UI**: Light theme with smooth animations and Bootstrap 5

## Prerequisites

Before running the application locally, ensure you have:

- **Python 3.8+** installed
- **PostgreSQL 12+** installed and running
- **Git** (optional, for cloning)

## Local Installation

### 1. Install PostgreSQL

#### On Windows:
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the 'postgres' user
4. Ensure PostgreSQL service is running

#### On macOS:
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql

# Or download from https://www.postgresql.org/download/macos/
```

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database

```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# In PostgreSQL shell, create database and user:
CREATE DATABASE splitapp;
CREATE USER splitapp_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE splitapp TO splitapp_user;
\q
```

### 3. Set Up Python Environment

```bash
# Clone or download the project files
# cd into the project directory

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DATABASE_URL=postgresql://splitapp_user:your_password_here@localhost:5432/splitapp

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# PostgreSQL Connection Details
PGHOST=localhost
PGPORT=5432
PGDATABASE=splitapp
PGUSER=splitapp_user
PGPASSWORD=your_password_here
```

### 5. Run the Application

```bash
# Ensure virtual environment is activated
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Run the application
python main.py

# Or using Flask command
flask run --host=0.0.0.0 --port=5000
```

The application will be available at: http://localhost:5000

## Usage

1. **Add Expenses**: Click "Add Expense" to record shared expenses
2. **View Balances**: See who owes money and who should receive money
3. **Check Settlements**: Get optimized settlement recommendations
4. **Manage Expenses**: Edit or delete existing expenses

## File Structure

```
split-app/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_expense.html
│   ├── edit_expense.html
│   ├── balances.html
│   └── settlements.html
└── static/           # CSS, JS, and static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Troubleshooting

### Database Connection Issues

1. **Check PostgreSQL is running**:
   ```bash
   # On Windows (check services)
   # On macOS/Linux:
   sudo systemctl status postgresql
   ```

2. **Verify database exists**:
   ```bash
   sudo -u postgres psql -l
   ```

3. **Test connection**:
   ```bash
   psql -h localhost -U splitapp_user -d splitapp
   ```

### Common Issues

- **Port 5000 already in use**: Change port in main.py or kill existing process
- **Permission denied**: Ensure PostgreSQL user has correct permissions
- **Module not found**: Activate virtual environment and install requirements

## Development

To make changes to the application:

1. **Database changes**: Modify models.py and restart the application
2. **UI changes**: Edit templates and static files
3. **New features**: Add routes in routes.py and corresponding templates

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in .env
2. Use a production WSGI server like Gunicorn
3. Set up proper PostgreSQL security
4. Use environment variables for sensitive data
5. Set up SSL/HTTPS

## License

This project is open source and available under the MIT License.