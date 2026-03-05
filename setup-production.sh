#!/bin/bash

# CV Application - Docker Production Setup Script
# This script helps you set up the production environment

set -e

echo "========================================"
echo "CV Application - Production Setup"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"
echo "✅ Docker Compose found: $(docker-compose --version)"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
    cat > .env << EOF
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=${SECRET_KEY}

# Upload Limits
MAX_CONTENT_LENGTH=5242880

# Server Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
EOF
    echo "✅ .env file created with random SECRET_KEY"
else
    echo "⚠️  .env file already exists, skipping creation"
fi

# Create required directories
echo ""
echo "📁 Creating required directories..."
mkdir -p app/static/uploads/profiles
mkdir -p app/static/uploads/education
mkdir -p app/static/uploads/advanced_training
mkdir -p app/generated_pdfs
mkdir -p instance
mkdir -p ssl
echo "✅ Directories created"

# Check if database exists
if [ -f instance/cv_database.db ]; then
    echo ""
    echo "✅ Database found: instance/cv_database.db"
else
    echo ""
    echo "⚠️  No database found. You'll need to run migrations after starting."
    echo "   Run: docker-compose exec web flask db upgrade"
fi

# Build the image
echo ""
echo "🔨 Building Docker image..."
docker-compose build

# Start the application
echo ""
read -p "Do you want to start the application now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting application..."
    docker-compose up -d
    
    echo ""
    echo "⏳ Waiting for application to be ready..."
    sleep 5
    
    # Check if app is running
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Application is running!"
        echo ""
        echo "📊 Application Status:"
        docker-compose ps
        echo ""
        echo "🌐 Access your application at: http://localhost:5000"
        echo ""
        echo "📝 Useful commands:"
        echo "   View logs:    docker-compose logs -f web"
        echo "   Stop app:     docker-compose down"
        echo "   Restart app:  docker-compose restart"
        echo "   Shell access: docker-compose exec web /bin/bash"
    else
        echo "❌ Application failed to start. Check logs:"
        echo "   docker-compose logs web"
    fi
else
    echo "✅ Setup complete! Start the application with:"
    echo "   docker-compose up -d"
fi

echo ""
echo "📚 For more information, see DEPLOYMENT.md"
