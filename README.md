# Professional CV Application - 2025 Version

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern, dynamic, and scalable Flask application for managing and generating professional CVs. Built as a portfolio project with clear architecture, modularity, and future-ready design for AI integration and enterprise scaling.

## 🎯 Project Overview

This application transforms a static HTML CV (2019) into a dynamic, database-driven system (2025) with intelligent profile generation, PDF export, and admin management capabilities. Designed as the foundation for a professional portfolio with a clear 2026 evolution roadmap.

### Key Features

#### ✨ 2025 Version (Current)
- **Dynamic Data Management**: SQLite database with SQLAlchemy ORM
- **Multiple CV Profiles**: QA Analyst, QA Engineer, Data Scientist
- **Intelligent Filtering**: Relevance scoring system for profile-specific content
- **Control Fields**: Active/inactive records, summary visibility, detail configuration
- **One-Page PDF Export**: WeasyPrint-powered PDF generation
- **Admin Panel**: CRUD operations with visibility and relevance configuration
- **RESTful API**: JSON endpoints for external integrations
- **Docker Ready**: Containerized deployment with Docker Compose
- **Modular Architecture**: Blueprint-based routing, service layer pattern

#### 🚀 2026 Vision (Roadmap)
- **AI Integration**: Intelligent content suggestions, automatic condensing, style recommendations
- **PostgreSQL/MySQL**: Enterprise database migration
- **Advanced Infrastructure**: Nginx, load balancing, multi-container orchestration
- **Modern Frontend**: React/Vue.js integration
- **Enhanced Security**: Flask-Login, OAuth, JWT authentication
- **Cloud Deployment**: AWS/GCP/Azure with CI/CD pipelines

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Database Models](#-database-models)
- [API Documentation](#-api-documentation)
- [Docker Deployment](#-docker-deployment)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🏗 Architecture

### Directory Structure

```
app-cv-jvb19/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py              # Base model with common fields
│   │   ├── personal_data.py
│   │   ├── education.py
│   │   ├── work_experience.py
│   │   ├── certifications.py
│   │   ├── courses.py
│   │   ├── languages.py
│   │   ├── it_products.py
│   │   └── support_tools.py
│   ├── routes/                  # Blueprint routes
│   │   ├── __init__.py
│   │   ├── main.py              # Public pages
│   │   ├── admin.py             # Admin panel
│   │   ├── profiles.py          # CV profiles
│   │   └── api.py               # REST API
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   └── pdf_generator.py    # PDF generation service
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── profile_view.html
│   │   ├── admin/
│   │   └── pdf/
│   └── static/                  # CSS, JS, images
│       ├── css/
│       ├── js/
│       └── img/
├── config.py                    # Configuration management
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization script
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Multi-container setup
├── .env.template                # Environment variables template
├── .dockerignore
└── README.md
```

### Design Patterns

- **Application Factory**: Flexible app creation with different configurations
- **Blueprint Pattern**: Modular route organization
- **Service Layer**: Business logic separation from routes
- **Repository Pattern**: Data access abstraction (ready for 2026 migration)
- **Base Model Inheritance**: DRY principle for common fields

---

## 🚀 Installation

### Prerequisites

- Python 3.11+
- pip
- (Optional) Docker and Docker Compose

### Local Setup

1. **Clone the repository**
```powershell
git clone https://github.com/jvillarrealbencomo/cv-jvillarrealbencomo19_consciente-creativo.git
cd app-cv-jvb19
```

2. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment**
```powershell
copy .env.template .env
# Edit .env with your configuration
```

5. **Initialize database**
```powershell
python init_db.py
```

6. **Run the application**
```powershell
python run.py
```

Visit `http://localhost:5000`

---

## 📖 Usage

### Admin Panel

Access the admin panel at `/admin/login` with credentials from your `.env` file.

**Default credentials:**
- Username: `admin`
- Password: `change-me-in-production`

### Creating CV Profiles

1. Navigate to Admin Dashboard
2. Add/Edit records in each section
3. Configure control fields:
   - **Active**: Enable/disable record
   - **Visible in Summary**: Show in one-page PDF
   - **Relevance Scores**: Set for each profile (0-10)
   - **Show Detail**: Configure what to display (work experience)
   - **Show Link**: Control link visibility (personal data)

### Generating PDFs

Visit profile pages and click "Download PDF":
- `/profile/qa-analyst/pdf`
- `/profile/qa-engineer/pdf`
- `/profile/data-scientist/pdf`

---

## 🗄 Database Models

### Base Model (Inherited by all models)

All models inherit common control fields:

```python
- id: Integer (Primary Key)
- active: Boolean (Enable/disable record)
- visible_in_summary: Boolean (Show in one-page PDF)
- created_at: DateTime
- updated_at: DateTime
- relevance_qa_analyst: Integer (0-10)
- relevance_qa_engineer: Integer (0-10)
- relevance_data_scientist: Integer (0-10)
```

### PersonalData

```python
- full_name: String
- professional_title: String
- email: String
- phone: String (optional)
- location: String (optional)
- summary: Text
- summary_short: String (for PDF)
- url_personal: String (optional)
- url_github: String (optional)
- url_linkedin: String (optional)
- show_link: String ('all', 'linkedin', 'github', 'personal', or combinations)
- profile_image_url: String (optional)
```

### WorkExperience

```python
- job_title: String
- company: String
- location: String (optional)
- start_date: Date
- end_date: Date (optional)
- is_current: Boolean
- description: Text (optional)
- functions: Text (daily responsibilities)
- highlighted_aspect: Text (key achievement)
- show_detail: String ('functions', 'aspect', 'both')
- technologies: Text (comma-separated)
- document_url: String (optional)
- display_order: Integer
```

### Education

```python
- degree: String
- institution: String
- location: String (optional)
- start_date: Date (optional)
- end_date: Date (optional)
- is_current: Boolean
- gpa: String (optional)
- honors: String (optional)
- description: Text (optional)
- document_url: String (optional)
- display_order: Integer
```

### Certification

```python
- name: String
- issuing_organization: String
- issue_date: Date (optional)
- expiration_date: Date (optional)
- credential_id: String (optional)
- credential_url: String (optional)
- comment: Text (optional)
- visible_comment: Boolean
- document_url: String (optional)
- display_order: Integer
```

### Course

```python
- name: String
- provider: String
- completion_date: Date (optional)
- duration_hours: Integer (optional)
- credential_url: String (optional)
- description: Text (optional)
- skills_acquired: Text (comma-separated)
- comment: Text (optional)
- visible_comment: Boolean
- document_url: String (optional)
- display_order: Integer
```

### Language

```python
- name: String
- level: String ('Native', 'Fluent', 'Advanced', 'Intermediate', 'Basic', or CEFR levels)
- certification_name: String (optional)
- certification_score: String (optional)
- display_order: Integer
```

### ITProduct

```python
- name: String
- description: Text
- role: String (optional)
- technologies: Text (comma-separated)
- start_date: Date (optional)
- end_date: Date (optional)
- is_current: Boolean
- project_url: String (optional)
- github_url: String (optional)
- demo_url: String (optional)
- impact_description: Text (optional)
- display_order: Integer
```

### SupportTool

```python
- category: String ('Programming Language', 'Framework', 'Database', 'Tool', 'Methodology', etc.)
- name: String
- proficiency_level: String ('Expert', 'Advanced', 'Intermediate', 'Basic')
- years_experience: Float (optional)
- description: Text (optional)
- display_order: Integer
```

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### GET /api/personal-data
Get active personal data.

**Response:**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "professional_title": "QA Engineer",
  "email": "john@example.com",
  "visible_links": {
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe"
  }
}
```

#### GET /api/education
Get all active education records.

#### GET /api/experience
Get all active work experience records.

#### GET /api/certifications
Get all active certifications.

#### GET /api/courses
Get all active courses.

#### GET /api/languages
Get all active languages.

#### GET /api/skills
Get all active technical skills grouped by category.

#### GET /api/profile/{profile_name}
Get filtered data for a specific profile.

**Parameters:**
- `profile_name`: qa_analyst, qa_engineer, or data_scientist
- `min_relevance` (optional): Minimum relevance score (default: 5)

**Response:**
```json
{
  "profile": "qa_analyst",
  "personal_data": { ... },
  "education": [ ... ],
  "experience": [ ... ],
  "certifications": [ ... ],
  "courses": [ ... ],
  "languages": [ ... ],
  "skills": [ ... ]
}
```

---

## 🐳 Docker Deployment

### Quick Start

```powershell
# Build and run
docker-compose up -d

# Initialize database (first time only)
docker-compose exec web python init_db.py

# View logs
docker-compose logs -f web

# Stop containers
docker-compose down
```

### Environment Variables

Create a `.env` file in the project root:

```bash
SECRET_KEY=your-production-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password
FLASK_ENV=production
```

### Volumes

Docker Compose persists data in:
- `./data` - SQLite database
- `./generated_pdfs` - Generated PDF files
- `./uploads` - Uploaded documents
- `./logs` - Application logs

---

## 💻 Development

### Running Tests

```powershell
pytest
pytest --cov=app tests/
```

### Database Migrations

```powershell
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

### Code Quality

```powershell
# Linting
flake8 app/

# Type checking
mypy app/

# Formatting
black app/
```

---

## 🗺 Roadmap

### Phase 1: Foundation (2025) ✅
- [x] Dynamic data management with SQLite
- [x] Multiple CV profiles with intelligent filtering
- [x] One-page PDF generation
- [x] Admin panel with CRUD operations
- [x] Docker containerization
- [x] RESTful API

### Phase 2: Scaling (Early 2026)
- [ ] Migrate to PostgreSQL/MySQL
- [ ] Implement Flask-Login authentication
- [ ] Add email notifications
- [ ] Create comprehensive test suite
- [ ] Set up CI/CD pipelines
- [ ] Deploy to cloud (AWS/GCP/Azure)

### Phase 3: Enhancement (Mid 2026)
- [ ] Nginx reverse proxy setup
- [ ] Load balancing configuration
- [ ] React/Vue.js frontend
- [ ] WebSocket real-time updates
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

### Phase 4: AI Integration (Late 2026)
- [ ] OpenAI/Anthropic integration
- [ ] Intelligent content suggestions
- [ ] Automatic content condensing for PDFs
- [ ] Style and wording recommendations
- [ ] Job description matching
- [ ] Resume scoring and optimization

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Juan Villarreal Bencomo**

- GitHub: [@jvillarrealbencomo](https://github.com/jvillarrealbencomo)
- LinkedIn: [Juan Villarreal Bencomo](https://linkedin.com/in/jvillarrealbencomo)

---

## 🙏 Acknowledgments

- Flask community for excellent documentation
- WeasyPrint for PDF generation capabilities
- Bootstrap for responsive UI components
- Docker for containerization simplicity

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [WeasyPrint Documentation](https://weasyprint.org/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ for portfolio and professional development**
