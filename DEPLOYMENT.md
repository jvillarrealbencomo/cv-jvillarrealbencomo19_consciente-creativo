# Docker Production Deployment Guide

## Quick Start

### 1. Build and Run
```bash
# Build the Docker image
docker-compose build

# Start the application
docker-compose up -d

# Check logs
docker-compose logs -f web

# Stop the application
docker-compose down
```

### 2. Access the Application
- **Local**: http://localhost:5000
- **Production**: Configure domain in Nginx (see below)

## Production Checklist

### Security
- [ ] Change `SECRET_KEY` in docker-compose.yml or set as environment variable
- [ ] Review file upload limits (currently 5MB)
- [ ] Enable HTTPS with Nginx reverse proxy
- [ ] Restrict file upload types (currently PNG, JPG, PDF)
- [ ] Set up firewall rules
- [ ] Use non-root user (already configured as www-data)

### Data Persistence
The following directories are mounted as volumes to persist data:
- `./app/static/uploads` - Profile photos, education credentials, training certificates
- `./app/generated_pdfs` - Generated CV PDFs
- `./instance` - SQLite database

**Backup Strategy:**
```bash
# Backup all persistent data
tar -czf cv-backup-$(date +%Y%m%d).tar.gz \
    app/static/uploads \
    app/generated_pdfs \
    instance

# Restore from backup
tar -xzf cv-backup-20260106.tar.gz
```

### Database Initialization
The container will use the existing SQLite database in `instance/`. If starting fresh:

```bash
# Run migrations inside container
docker-compose exec web flask db upgrade

# Or run init script
docker-compose exec web python init_db.py
```

### Environment Variables
Set these in production (via `.env` file or docker-compose override):

```env
SECRET_KEY=your-super-secret-key-here-use-random-string
FLASK_ENV=production
MAX_CONTENT_LENGTH=5242880
```

## Nginx Reverse Proxy (Optional but Recommended)

Create `nginx.conf` for production with SSL:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream flask_app {
        server web:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        client_max_body_size 10M;

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Flask application
        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 120s;
        }
    }
}
```

Then uncomment the nginx service in `docker-compose.yml`.

## Monitoring

### Health Check
```bash
# Check container health
docker-compose ps

# Manual health check
curl http://localhost:5000/
```

### Logs
```bash
# Real-time logs
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web

# Logs for specific timeframe
docker-compose logs --since 2026-01-06T10:00:00 web
```

### Resource Usage
```bash
# Container stats
docker stats cv-app

# Disk usage
docker system df
```

## Scaling

### Horizontal Scaling
```bash
# Run multiple instances behind load balancer
docker-compose up -d --scale web=3
```

**Note**: For horizontal scaling, you'll need:
1. Shared volume/NFS for uploads
2. PostgreSQL/MySQL instead of SQLite
3. Load balancer (Nginx/HAProxy)

### Vertical Scaling
Adjust in `docker-compose.yml`:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M
```

## Maintenance

### Update Application
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
# Run migrations
docker-compose exec web flask db upgrade

# Check migration status
docker-compose exec web flask db current
```

### Clean Up
```bash
# Remove stopped containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes (WARNING: deletes data!)
docker-compose down -v
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs web

# Run interactively
docker-compose run --rm web /bin/bash
```

### Permission Issues
```bash
# Fix upload directory permissions
sudo chown -R 33:33 app/static/uploads
sudo chown -R 33:33 app/generated_pdfs
sudo chown -R 33:33 instance
```

### Out of Disk Space
```bash
# Clean Docker system
docker system prune -a

# Check volume sizes
docker system df -v
```

## Production Domain Setup

### DNS Configuration
Point your domain to server IP:
```
A record: cv.yourdomain.com -> YOUR_SERVER_IP
```

### SSL Certificate (Let's Encrypt)
```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d cv.yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/cv.yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/cv.yourdomain.com/privkey.pem ./ssl/key.pem
```

### Auto-renewal
```bash
# Add to crontab
0 3 * * * certbot renew --quiet && docker-compose restart nginx
```

## Performance Optimization

### Gunicorn Workers
Current: 4 workers, 2 threads per worker = 8 concurrent requests

Adjust in Dockerfile CMD:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--threads", "2", \
     "--timeout", "120", \
     "run:app"]
```

**Formula**: workers = (2 × CPU_cores) + 1

### Static File Caching
Using Nginx for static files improves performance significantly.

### Database
For production with high traffic, consider:
- PostgreSQL instead of SQLite
- Database connection pooling
- Read replicas

## Support

### Viewing Application Status
```bash
# All services
docker-compose ps

# Specific service
docker-compose ps web
```

### Accessing Container Shell
```bash
docker-compose exec web /bin/bash
```

### Running Management Commands
```bash
# Check database
docker-compose exec web python check_training_images.py

# Run any Python script
docker-compose exec web python your_script.py
```
