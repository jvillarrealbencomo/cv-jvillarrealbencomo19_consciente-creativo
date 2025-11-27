# Quick Start Guide

## For Development

### 1. Initial Setup (Windows PowerShell)

```powershell
# Navigate to project
cd c:\Users\vbj20\proyectos\ProjectsPy\app-cv-jvb19

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.template .env
```

### 2. Configure Environment

Edit `.env` file:
```
SECRET_KEY=your-secret-key-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

### 3. Initialize Database

```powershell
# Create database and seed with sample data
python init_db.py
```

### 4. Run Application

```powershell
# Start development server
python run.py
```

Visit: `http://localhost:5000`

## For Production (Docker)

### 1. Configure Environment

```powershell
# Create .env file
copy .env.template .env
# Edit with production credentials
```

### 2. Deploy with Docker

```powershell
# Build and start containers
docker-compose up -d

# Initialize database (first time only)
docker-compose exec web python init_db.py

# View logs
docker-compose logs -f web
```

Visit: `http://localhost:5000`

## Common Commands

### Database Management

```powershell
# Reset database (WARNING: deletes all data)
rm cv_dev.db
python init_db.py

# Flask shell (interact with models)
flask shell
```

### Docker Management

```powershell
# Stop containers
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# View container status
docker-compose ps

# Access container shell
docker-compose exec web /bin/bash
```

## Default Admin Access

- URL: `http://localhost:5000/admin/login`
- Username: `admin` (or from .env)
- Password: `change-me-in-production` (or from .env)

⚠️ **IMPORTANT**: Change default credentials before production deployment!

## Troubleshooting

### WeasyPrint Issues on Windows

If you encounter WeasyPrint installation errors:

```powershell
# Install GTK3 Runtime
# Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
# Then reinstall requirements
pip install -r requirements.txt
```

### Port Already in Use

```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Database Locked

```powershell
# Stop all Flask processes
# Delete .db file
rm cv_dev.db
# Reinitialize
python init_db.py
```

## Next Steps

1. ✅ Access admin panel and configure your personal data
2. ✅ Add your education, experience, and skills
3. ✅ Configure relevance scores for each profile
4. ✅ Generate and download PDF CVs
5. ✅ Customize templates in `app/templates/`
6. ✅ Add your custom CSS in `app/static/css/`

## Support

For questions or issues, refer to the main [README.md](README.md) or create an issue on GitHub.
