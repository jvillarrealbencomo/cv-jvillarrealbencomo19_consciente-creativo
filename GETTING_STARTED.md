# 🚀 Getting Started - Complete Setup Guide

## Overview

This guide will walk you through setting up and running your modernized Flask CV application for the first time.

---

## Prerequisites Check

Before starting, ensure you have:

- ✅ Python 3.11 or higher
- ✅ pip (Python package manager)
- ✅ Git (for version control)
- ✅ (Optional) Docker Desktop (for containerized deployment)

Check your versions:
```powershell
python --version
pip --version
git --version
docker --version
```

---

## Option 1: Local Development Setup (Recommended for Development)

### Step 1: Set Up Python Environment

```powershell
# Navigate to project directory
cd c:\Users\vbj20\proyectos\ProjectsPy\app-cv-jvb19

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
```

### Step 2: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will install:
# - Flask 3.0
# - SQLAlchemy 2.0
# - WeasyPrint (PDF generation)
# - And all other dependencies
```

**Note for Windows**: If WeasyPrint fails to install, you may need GTK3:
1. Download GTK3 Runtime: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Install it
3. Run `pip install -r requirements.txt` again

### Step 3: Configure Environment

```powershell
# Copy environment template
copy .env.template .env

# Open .env in your text editor and customize:
# - SECRET_KEY (generate a random string)
# - ADMIN_USERNAME (your admin username)
# - ADMIN_PASSWORD (strong password)
```

Generate a secure secret key:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Initialize Database

```powershell
# Create database and populate with sample data
python init_db.py

# You should see:
# ✓ Tables created successfully
# ✓ Seed data added successfully
```

### Step 5: Run the Application

```powershell
# Start development server
python run.py

# You should see:
# * Running on http://127.0.0.1:5000
```

### Step 6: Access the Application

Open your browser and visit:
- **Home Page**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
  - Username: `admin` (or your .env value)
  - Password: `change-me-in-production` (or your .env value)

---

## Option 2: Docker Deployment (Recommended for Production)

### Step 1: Configure Environment

```powershell
# Create .env file
copy .env.template .env

# Edit .env with your production settings
# IMPORTANT: Use strong passwords and secret keys!
```

### Step 2: Build and Run with Docker

```powershell
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f web

# Initialize database (first time only)
docker-compose exec web python init_db.py
```

### Step 3: Access the Application

- **Application**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

### Managing Docker Containers

```powershell
# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View running containers
docker-compose ps

# Access container shell
docker-compose exec web /bin/bash

# View logs
docker-compose logs -f web

# Rebuild after code changes
docker-compose up -d --build
```

---

## Verifying Your Setup

### 1. Check Homepage
Visit http://localhost:5000 - you should see the welcome page with profile cards.

### 2. Test Profile Views
- http://localhost:5000/profile/qa-analyst
- http://localhost:5000/profile/qa-engineer
- http://localhost:5000/profile/data-scientist

### 3. Test API Endpoints
```powershell
# Get personal data (PowerShell)
Invoke-RestMethod -Uri http://localhost:5000/api/personal-data | ConvertTo-Json

# Or use curl if installed
curl http://localhost:5000/api/personal-data
```

### 4. Test Admin Panel
1. Go to http://localhost:5000/admin/login
2. Login with your credentials
3. You should see the dashboard with statistics

### 5. Test PDF Generation
1. Visit any profile page
2. Click "Download PDF" button
3. PDF should download (check Downloads folder)

---

## Customizing Your CV

### 1. Update Personal Information

1. Login to admin panel
2. Go to "Personal Data"
3. Update with your information:
   - Full name
   - Professional title
   - Email, phone, location
   - Professional summary
   - URLs (LinkedIn, GitHub, personal website)
   - Configure which links to show: `all`, `linkedin,github`, etc.

### 2. Add Your Experience

1. Admin → Work Experience
2. Click "Create New"
3. Fill in details:
   - Job title, company, dates
   - Description
   - **Functions**: Your daily responsibilities
   - **Highlighted Aspect**: Key achievement
   - **Show Detail**: Choose what to display (`functions`, `aspect`, `both`)
   - **Relevance Scores**: Rate 0-10 for each profile
   - **Active**: Enable the record
   - **Visible in Summary**: Show in one-page PDF

### 3. Configure Profile Relevance

For each record, set relevance scores (0-10):
- **QA Analyst**: How relevant is this for QA Analyst role?
- **QA Engineer**: How relevant for QA Engineer role?
- **Data Scientist**: How relevant for Data Scientist role?

Records with score ≥ 5 will appear in that profile's CV.

### 4. Control PDF Content

Use the **Visible in Summary** checkbox to decide what appears in the one-page PDF. This is separate from **Active** which controls if the item appears on the website at all.

Strategy:
- Mark 3-5 work experiences as visible in summary
- Include 2-3 most relevant certifications
- Keep PDF content concise for one page

---

## Project Structure Tour

```
app-cv-jvb19/
├── app/                      # Main application package
│   ├── models/              # Database models (8 models)
│   ├── routes/              # Route blueprints (main, admin, profiles, api)
│   ├── services/            # Business logic (PDF generation)
│   ├── templates/           # HTML templates (Jinja2)
│   └── static/              # CSS, JS, images
├── config.py                # Configuration for dev/prod/test
├── run.py                   # Application entry point
├── init_db.py               # Database setup script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Multi-container setup
├── .env.template            # Environment variables template
├── README.md                # Comprehensive documentation
└── QUICKSTART.md           # This file
```

---

## Common Tasks

### Resetting the Database

```powershell
# Delete existing database
rm cv_dev.db

# Reinitialize with sample data
python init_db.py
```

### Viewing Database Contents

```powershell
# Open Flask shell
flask shell

# Query personal data
>>> PersonalData.query.all()

# Query work experience
>>> WorkExperience.query.filter_by(active=True).all()

# Exit shell
>>> exit()
```

### Running Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_models.py
```

### Updating Dependencies

```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Update a package
pip install --upgrade flask

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Troubleshooting

### Issue: "Port 5000 already in use"

```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F

# Or change port in run.py:
# app.run(host='0.0.0.0', port=5001, debug=True)
```

### Issue: "WeasyPrint not installing"

Install GTK3 Runtime for Windows:
1. Download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Install
3. Restart PowerShell
4. `pip install weasyprint`

### Issue: "Database locked"

```powershell
# Stop all Flask processes
# Delete database
rm cv_dev.db
# Reinitialize
python init_db.py
```

### Issue: "Import errors"

```powershell
# Make sure you're in venv
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Can't login to admin"

Check your `.env` file:
- ADMIN_USERNAME should match your login
- ADMIN_PASSWORD should match your password
- Restart the Flask app after changing .env

---

## Next Steps

1. ✅ **Customize Your Data**
   - Replace sample data with your actual CV
   - Configure relevance scores
   - Test all three profile PDFs

2. ✅ **Customize Appearance**
   - Modify `app/static/css/modern.css`
   - Update `app/templates/base.html`
   - Customize PDF template in `app/templates/pdf/cv_template.html`

3. ✅ **Add Your Branding**
   - Add logo to `app/static/img/`
   - Update colors in CSS
   - Customize footer

4. ✅ **Test Thoroughly**
   - Test all routes
   - Generate PDFs for all profiles
   - Test admin CRUD operations
   - Check mobile responsiveness

5. ✅ **Prepare for Deployment**
   - Choose hosting (Heroku, AWS, Azure, DigitalOcean)
   - Set up custom domain
   - Configure SSL certificate
   - Set production environment variables

---

## Getting Help

- **Documentation**: See [README.md](README.md) for complete documentation
- **Implementation Details**: Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Issues**: Create an issue on GitHub

---

## Quick Commands Reference

```powershell
# Development
.\venv\Scripts\Activate.ps1    # Activate venv
python run.py                   # Run app
python init_db.py              # Setup database
flask shell                     # Interactive shell

# Docker
docker-compose up -d            # Start
docker-compose down             # Stop
docker-compose logs -f          # View logs
docker-compose exec web bash   # Shell access

# Testing
pytest                          # Run tests
pytest --cov=app               # With coverage

# Database
flask db init                   # Initialize migrations
flask db migrate               # Create migration
flask db upgrade               # Apply migration
```

---

**You're all set! 🎉 Start customizing your CV application!**
