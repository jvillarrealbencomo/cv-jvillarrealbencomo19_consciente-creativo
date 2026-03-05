# CV Application - Production Setup Script (Windows)
# Run with: .\setup-production.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CV Application - Production Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    
    # Generate random secret key
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes)
    $secretKey = [System.BitConverter]::ToString($bytes) -replace '-',''
    
    @"
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=$secretKey

# Upload Limits
MAX_CONTENT_LENGTH=5242880

# Server Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
"@ | Out-File -FilePath .env -Encoding UTF8
    
    Write-Host "✅ .env file created with random SECRET_KEY" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file already exists, skipping creation" -ForegroundColor Yellow
}

# Create required directories
Write-Host ""
Write-Host "📁 Creating required directories..." -ForegroundColor Yellow
$directories = @(
    "app\static\uploads\profiles",
    "app\static\uploads\education",
    "app\static\uploads\advanced_training",
    "app\generated_pdfs",
    "instance",
    "ssl"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Directories created" -ForegroundColor Green

# Check if database exists
if (Test-Path "instance\cv_database.db") {
    Write-Host ""
    Write-Host "✅ Database found: instance\cv_database.db" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️  No database found. You'll need to run migrations after starting." -ForegroundColor Yellow
    Write-Host "   Run: docker-compose exec web flask db upgrade" -ForegroundColor Gray
}

# Build the image
Write-Host ""
Write-Host "🔨 Building Docker image..." -ForegroundColor Cyan
docker-compose build

# Ask to start
Write-Host ""
$response = Read-Host "Do you want to start the application now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "🚀 Starting application..." -ForegroundColor Cyan
    docker-compose up -d
    
    Write-Host ""
    Write-Host "⏳ Waiting for application to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Check if app is running
    $status = docker-compose ps
    if ($status -match "Up") {
        Write-Host "✅ Application is running!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Application Status:" -ForegroundColor Cyan
        docker-compose ps
        Write-Host ""
        Write-Host "🌐 Access your application at: http://localhost:5000" -ForegroundColor Green
        Write-Host ""
        Write-Host "📝 Useful commands:" -ForegroundColor Cyan
        Write-Host "   View logs:    docker-compose logs -f web" -ForegroundColor Gray
        Write-Host "   Stop app:     docker-compose down" -ForegroundColor Gray
        Write-Host "   Restart app:  docker-compose restart" -ForegroundColor Gray
        Write-Host "   Shell access: docker-compose exec web /bin/bash" -ForegroundColor Gray
    } else {
        Write-Host "❌ Application failed to start. Check logs:" -ForegroundColor Red
        Write-Host "   docker-compose logs web" -ForegroundColor Gray
    }
} else {
    Write-Host "✅ Setup complete! Start the application with:" -ForegroundColor Green
    Write-Host "   docker-compose up -d" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📚 For more information, see DEPLOYMENT.md" -ForegroundColor Cyan
