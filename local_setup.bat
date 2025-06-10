@echo off
REM Split App - Local Setup Script for Windows
REM This script automates the local setup process

echo ==================================================
echo Split App - Automated Local Setup
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is required but not installed.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if errorlevel 1 (
    echo Warning: PostgreSQL not found in PATH
    echo Please install PostgreSQL from https://postgresql.org
    echo Make sure PostgreSQL is added to your PATH
    pause
)

echo ✓ PostgreSQL found
psql --version

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements_local.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env configuration file...
    copy .env.example .env
    
    echo Please configure your database settings:
    set /p db_password="Enter PostgreSQL password for splitapp_user: "
    set /p secret_key="Enter Flask secret key (or press Enter for default): "
    
    if "%secret_key%"=="" set secret_key=dev-secret-key-change-in-production
    
    REM Update .env file using PowerShell
    powershell -Command "(gc .env) -replace 'your_password_here', '%db_password%' | Out-File -encoding ASCII .env"
    powershell -Command "(gc .env) -replace 'your-secret-key-change-this-in-production', '%secret_key%' | Out-File -encoding ASCII .env"
    
    echo ✓ .env file created
) else (
    echo ✓ .env file already exists
)

REM Setup database
echo Setting up database...
python setup_database.py

echo.
echo ==================================================
echo Setup completed successfully!
echo ==================================================
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the app: python run_local.py
echo    or: python main.py
echo.
echo The application will be available at: http://localhost:5000
echo.
echo To deactivate virtual environment later: deactivate
pause