# Production Readiness Checklist

## Pre-Deployment

### Code & Configuration
- [x] Dockerfile created with production-ready settings
- [x] docker-compose.yml configured with volumes for persistence
- [x] .dockerignore configured to exclude dev files
- [x] Gunicorn WSGI server configured (4 workers, 2 threads)
- [x] Health check endpoint configured
- [x] Non-root user (www-data) for security
- [ ] Generate SECRET_KEY (run setup-production.ps1/sh)
- [ ] Review MAX_CONTENT_LENGTH (currently 5MB)

### Data Persistence
- [x] Uploads directory mounted as volume: `./app/static/uploads`
- [x] PDFs directory mounted as volume: `./app/generated_pdfs`
- [x] Database directory mounted as volume: `./instance`
- [ ] Verify existing uploads/database copied to these directories

### Security
- [ ] Change default SECRET_KEY in .env
- [ ] Set FLASK_ENV=production
- [ ] Review file upload restrictions (PNG, JPG, PDF only)
- [ ] Consider rate limiting for uploads
- [ ] Set up HTTPS with SSL certificate (see DEPLOYMENT.md)
- [ ] Configure firewall rules on server
- [ ] Disable Flask debug mode (already set in production)

## Deployment Steps

### 1. Initial Setup
```powershell
# Windows
.\setup-production.ps1

# Linux/Mac
chmod +x setup-production.sh
./setup-production.sh
```

### 2. Verify Configuration
```bash
# Check .env file exists and has SECRET_KEY
cat .env

# Verify directories exist
ls -la app/static/uploads/
ls -la instance/
```

### 3. Build and Start
```bash
# Build image
docker-compose build

# Start in detached mode
docker-compose up -d

# Check logs
docker-compose logs -f web
```

### 4. Database Setup
```bash
# If database already exists, it will be used automatically
# If starting fresh, run migrations:
docker-compose exec web flask db upgrade

# Or initialize with seed data:
docker-compose exec web python init_db.py
```

### 5. Verify Deployment
- [ ] Application accessible at http://localhost:5000
- [ ] Health check passing: `curl http://localhost:5000/`
- [ ] Check container status: `docker-compose ps`
- [ ] Verify uploads work (test image upload)
- [ ] Verify PDF generation works
- [ ] Test all three CV profiles (QA Analyst, QA Engineer, Data Scientist)
- [ ] Verify credential images display correctly
- [ ] Check logs for errors: `docker-compose logs web`

## Post-Deployment

### Monitoring
- [ ] Set up log rotation/aggregation
- [ ] Monitor container resource usage: `docker stats cv-app`
- [ ] Set up uptime monitoring (e.g., UptimeRobot)
- [ ] Configure error alerting

### Backup Strategy
- [ ] Set up automated backups of:
  - `./app/static/uploads` (credential images)
  - `./app/generated_pdfs` (generated CVs)
  - `./instance/cv_database.db` (database)
- [ ] Test restore procedure
- [ ] Document backup schedule

### Domain & SSL (Production)
- [ ] Point domain DNS to server IP
- [ ] Install SSL certificate (Let's Encrypt recommended)
- [ ] Configure Nginx reverse proxy (see DEPLOYMENT.md)
- [ ] Set up auto-renewal for SSL certificate
- [ ] Test HTTPS access

### Performance Optimization
- [ ] Enable Nginx for static file serving
- [ ] Configure caching headers for static assets
- [ ] Consider CDN for static files (optional)
- [ ] Monitor response times
- [ ] Adjust Gunicorn workers if needed (current: 4 workers, 2 threads)

## Testing in Production

### Smoke Tests
```bash
# Health check
curl http://localhost:5000/

# Test main pages
curl http://localhost:5000/
curl http://localhost:5000/profile/1?profile=qa_engineer

# Test API endpoints
curl http://localhost:5000/api/education
curl http://localhost:5000/api/advanced-training

# Check static files
curl http://localhost:5000/static/css/modern.css
```

### Functional Tests
- [ ] Upload education credential image
- [ ] Upload training credential image
- [ ] Generate PDF for each profile
- [ ] Edit education record
- [ ] Edit training record
- [ ] Toggle profile visibility
- [ ] Verify images persist after container restart

### Load Testing (Optional)
```bash
# Install Apache Bench
# Test concurrent requests
ab -n 1000 -c 10 http://localhost:5000/
```

## Maintenance Procedures

### Regular Updates
```bash
# Pull latest code
git pull origin cv2025-credential-images

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Database Migrations
```bash
# Apply migrations
docker-compose exec web flask db upgrade

# Rollback if needed
docker-compose exec web flask db downgrade
```

### Backup Procedure
```bash
# Create backup
tar -czf backup-$(date +%Y%m%d).tar.gz \
    app/static/uploads \
    app/generated_pdfs \
    instance

# Restore backup
tar -xzf backup-20260106.tar.gz
docker-compose restart
```

## Rollback Plan

### Quick Rollback
```bash
# Stop current version
docker-compose down

# Checkout previous version
git checkout <previous-commit-hash>

# Rebuild and start
docker-compose build
docker-compose up -d
```

### Database Rollback
```bash
# If migration fails
docker-compose exec web flask db downgrade

# Restore from backup
rm instance/cv_database.db
cp backups/cv_database_backup.db instance/cv_database.db
docker-compose restart
```

## Troubleshooting Guide

### Container Won't Start
```bash
# Check logs
docker-compose logs web

# Run interactively for debugging
docker-compose run --rm web /bin/bash

# Check port conflicts
netstat -tulpn | grep 5000
```

### Upload Fails
- Check directory permissions: `ls -la app/static/uploads/`
- Verify MAX_CONTENT_LENGTH setting
- Check disk space: `df -h`
- Review logs: `docker-compose logs web | grep -i error`

### Database Issues
```bash
# Check database file
ls -lh instance/cv_database.db

# Verify database integrity
docker-compose exec web python -c "from app import create_app, db; app=create_app(); app.app_context().push(); print(db.engine.table_names())"
```

### Performance Issues
```bash
# Check resource usage
docker stats cv-app

# Check for errors in logs
docker-compose logs web | grep -i error

# Increase workers if needed (edit Dockerfile CMD)
```

## Production Environment Variables

### Required
```env
SECRET_KEY=<strong-random-key>
FLASK_ENV=production
```

### Optional
```env
MAX_CONTENT_LENGTH=5242880
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Success Criteria

- [x] Application builds successfully
- [ ] Container starts without errors
- [ ] Health check passes
- [ ] All pages load correctly
- [ ] Image uploads work for education
- [ ] Image uploads work for training
- [ ] Images display in CV preview
- [ ] PDF generation works
- [ ] Data persists across container restarts
- [ ] No errors in logs
- [ ] Response time < 2 seconds for main pages
- [ ] Backup/restore procedure tested

---

**Ready for Production**: Check all items above before deploying to production server.

**Support**: See DEPLOYMENT.md for detailed documentation.
