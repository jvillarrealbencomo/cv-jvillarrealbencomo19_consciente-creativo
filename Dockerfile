FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Pillow (image processing)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p \
    app/static/uploads/profiles \
    app/static/uploads/education \
    app/static/uploads/advanced_training \
    app/generated_pdfs \
    instance

# Set permissions (www-data user in production)
RUN chown -R www-data:www-data /app

# Switch to non-root user for security
USER www-data

# Expose port
EXPOSE 5000

# Environment variables (can be overridden in docker-compose or at runtime)
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/', timeout=5)" || exit 1

# Run with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
