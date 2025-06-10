# Quick Start Guide - Split App Local Installation

## Automated Setup (Recommended)

### For Windows:
1. Download all project files to a folder
2. Double-click `local_setup.bat`
3. Follow the prompts to configure database credentials
4. Run `python run_local.py` when setup completes

### For macOS/Linux:
1. Download all project files to a folder
2. Open terminal in the project folder
3. Run: `chmod +x local_setup.sh && ./local_setup.sh`
4. Follow the prompts to configure database credentials
5. Run `python run_local.py` when setup completes

## Manual Setup

### Prerequisites:
- Python 3.8+
- PostgreSQL 12+

### Steps:
1. **Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements_local.txt
   ```

2. **Configure Database**
   ```bash
   # Copy environment template
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Setup Database**
   ```bash
   python setup_database.py
   ```

4. **Run Application**
   ```bash
   python run_local.py
   ```

Visit http://localhost:5000 to use the application.

## Troubleshooting

- **Database connection issues**: Check PostgreSQL is running and credentials in .env
- **Port 5000 in use**: Change port in run_local.py
- **Permission errors**: Run as administrator/sudo for database setup