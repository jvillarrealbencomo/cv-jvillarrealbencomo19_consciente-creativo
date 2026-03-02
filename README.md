# Professional CV Builder API

**Version 2.0** | Release Date: February 20, 2026 | API v2 | Status: Production

A Flask-based professional CV management and market intelligence platform that combines structured data entry with advanced analytics for skill gap analysis and market alignment assessment.

---

## 🎯 Overview

The **Professional CV Builder API** is a data-driven platform designed for recruiters and professionals to create, manage, and analyze curriculum vitae with quantitative market intelligence. The system integrates personal data management with a market cross-reference analytics engine that provides objective skill alignment metrics.

### Key Capabilities

- **Multi-Profile Support**: QA Analyst, QA Engineer, Data Scientist
- **Data Insights Dashboard**: Market Alignment Validation with detailed skill breakdowns, color-coded badges, and Complete Skills Mapping Matrix
- **Evidence Hub**: Video demonstrations and technical validation for each profile
- **Profile Presets**: Pre-configured skill sets and visibility settings
- **PDF Generation**: Export CVs with profile-specific formatting (One-Page and Full Export modes)
- **Advanced Training Management**: Unified courses and certifications with credential images
- **REST API**: Version-controlled endpoints for market insights with detailed skill transparency

---

## 🆕 What's New in Version 2.0

### API Versioning System
- **Dynamic metadata management** via `app_metadata` table
- All version information (year, API version, status) automatically displayed across the application
- Easy version updates without template changes

### Data Insights Module - Market Alignment Validation Dashboard
- Market Cross-Reference Model v1 for Data Scientist profile
- **Enhanced Dashboard** with detailed skill breakdowns:
  - **Chart 1**: Profile Readiness Overview (donut with centered KPI)
    - Displays matched skills (green badges) and missing skills (red badges)
    - Real-time skill-level detail behind each metric
  - **Chart 2**: Market Demand vs Profile Coverage (vertical bar)
    - Shows market demand skills, CV skills, and gap skills with color-coded badges
    - Complete skill lists for each bar segment
  - **Chart 3**: Dataset Alignment Breakdown (grouped bar - Kaggle vs O*NET)
    - Separate matched/missing skill lists for each dataset
    - Dataset-specific gap identification
- **Complete Skills Mapping Matrix**: Comprehensive table showing all skills with:
  - CV presence indicator (Yes/No badges)
  - Market presence indicator (Yes/No badges)
  - Dataset associations (Kaggle, O*NET)
  - Skill type classification (technology, library, methodology, etc.)
- Real-time readiness scoring based on market-validated datasets
- Multi-dataset benchmarking (Kaggle job postings + O*NET occupational data)

### Documentation Pages
- **System Overview**: Technical design and analytical foundation
- **Platform Overview**: Functional capabilities and module descriptions

### Infrastructure Improvements
- Fixed Advanced Training edit bug in data management
- Enhanced footer with API version and status display
- Context processors for dynamic metadata injection
- Production-ready configuration

---

## � Data Insights Methodology

The Data Insights module implements a **Market Cross-Reference Model v1** that quantifies CV market alignment using validated datasets. This section documents the exact calculation methodology, processing rules, and current limitations.

### Readiness Score Formula

The readiness score represents the percentage of market-demanded skills present in the CV:

```
Readiness Score = (matched_skill_count / market_skill_count) × 100
```

Where:
- **matched_skill_count**: Skills present in both CV and market datasets (languages excluded)
- **market_skill_count**: Total skills required by market for the profile (languages excluded)

**Example:**
- Market requires 7 skills for Data Scientist
- CV contains 6 of those 7 skills
- Readiness Score = (6 / 7) × 100 = **85.71%**

### Skill Processing Pipeline

Skills undergo a 6-stage processing pipeline before comparison:

#### 1. **Extraction** (extractor.py)
Pulls skills from the following CV sections:
- **Technical Tools**: Direct skill names (e.g., "Python", "SQL")
- **Courses**: Parsed from `skills` field
- **Work Experience**: Technologies list + tokenized narrative text (responsibilities, achievements)
- **Advanced Training**: Training names + tokenized descriptions
- **Education** (optional): Degree names + tokenized details

Sources are tracked: `technical_tools`, `courses`, `work_experience`, `advanced_training`, `education`

#### 2. **Filtering** (skill_filter.py)
Validates skills against quality criteria:

**Exclusion Rules:**
- Narrative verbs (designed, developed, implemented, managed, etc.)
- Stop words (none, n/a, other, general, system, process, metrics, etc.)
- Connectives (and, to, with, including)
- Skills > 3 words or < 2 characters
- Skills with disallowed characters (. % ( ) :)

**Inclusion Rules:**
- Must match market vocabulary or predefined skill lists
- Must be classified as: `technology`, `framework`, `language`, `library`, `methodology`, or `tool`
- Cannot be classified as: `process`, `capability`, `artifact`, `concept`, `system_feature`, `output`, `documentation`, or `meta`

#### 3. **Normalization** (normalizer.py)
Standardizes skill representation:
- Convert to lowercase
- Replace hyphens with spaces
- Collapse multiple spaces to single space
- Strip leading/trailing whitespace

**Example:** `"Scikit-Learn"` → `"scikit learn"`

#### 4. **Canonicalization** (canonicalizer.py)
Maps synonyms to canonical forms using CSV-defined synonym maps:
- Looks up normalized skill in `synonym_map` (from market datasets)
- Replaces spaces with underscores for standardization
- Collapses multiple underscores

**Example:** `"machine learning"` → `"machine_learning"` (if defined in synonym map)

#### 5. **Inference** (service.py)
Derives additional skills using predefined inference rules:

```python
INFERENCE_MAP = {
    "sqlalchemy": ["sql"],
    "flask": ["python", "api integration"],
    "backend python sql": ["python", "sql"],
    "api": ["api integration"],
    "rest api": ["api integration"]
}
```

- If CV contains `"sqlalchemy"`, automatically infers `"sql"`
- If CV contains `"flask"`, automatically infers `"python"` and `"api integration"`
- Inferred skills tracked with source: `inferred_from_<original_skill>`

#### 6. **Coverage Calculation** (service.py)
Compares market skills vs CV skills:

For each skill in market OR CV:
```python
coverage[skill] = {
    "present_in_cv": bool,        # True if skill found in CV
    "present_in_market": bool,    # True if skill in market datasets
    "datasets": ["kaggle", "onet"] # Normalized dataset tags (not filenames)
}
```

### Market Data Loading

Market skills are loaded from CSV files in the `data_insights/` directory:

**Datasets:**
- `kaggle_roles_skills.csv`: Kaggle job postings analysis
- `onet_skills.csv`: O*NET occupational database

**CSV Structure:**
```
role,skill,category,source,synonyms
data_scientist,python,programming,kaggle,py
data_scientist,machine learning,modeling,onet,ml|deep learning
```

**Loading Rules:**
1. Filters skills by `role` matching the requested profile (`data_scientist`, `qa_analyst`, `qa_engineer`)
2. Builds `synonym_map` from `synonyms` column (pipe-separated values)
3. Associates skills with source datasets (normalized tags: `kaggle`, `onet`)
4. Categories mapped to skill types via `CATEGORY_TO_TYPE` dictionary

### Processing Rules Summary

| Rule | Description | Purpose |
|------|-------------|---------|
| **Language Exclusion** | Skills classified as `language` excluded from readiness calculation | Readiness focuses on technical skills only |
| **Profile Filtering** | Only loads market skills matching selected profile | Ensures profile-specific analysis |
| **Compound Token Expansion** | Multi-word terms extracted from narrative text | Captures "machine learning", "api integration" from descriptions |
| **Market Vocabulary Validation** | Skills must exist in market datasets or predefined lists | Prevents noise from narrative text |
| **Dataset Tag Normalization** | Uses `kaggle`, `onet` tags (not filenames) | Consistent cross-referencing |
| **Case-Insensitive Matching** | All skills normalized to lowercase | Prevents duplicate counting |

### Current Limitations

1. **Single Active Profile**
   - Dashboard frontend hardcoded to `data_scientist` profile
   - API supports all 3 profiles, but UI only displays Data Scientist data

2. **Static Market Datasets**
   - Relies on manually updated CSV files
   - No real-time integration with job boards or market APIs
   - Dataset freshness depends on manual updates

3. **Fixed Inference Rules**
   - `INFERENCE_MAP` requires code changes to add new rules
   - No automatic inference learning from CV patterns

4. **Synonym Map Completeness**
   - Synonym mappings limited to CSV definitions
   - Missing synonyms may cause skill mismatches

5. **Narrative Text Noise**
   - Tokenized text from descriptions may extract non-skill terms
   - Filtering rules mitigate but cannot eliminate all noise

6. **Predefined Skill Categories**
   - Skill type classification uses hardcoded lists
   - New technologies require manual addition to category mappings

7. **No Temporal Analysis**
   - Readiness score is snapshot-based
   - No trending or historical comparison

8. **Education Data Optional**
   - `include_education` parameter defaults to `false`
   - May undercount skills from academic background

### Technical Implementation Files

| File | Purpose |
|------|---------|
| `app/routes/data_insights.py` | API endpoints and readiness calculation |
| `app/services/data_insights/service.py` | Main orchestration and coverage calculation |
| `app/services/data_insights/extractor.py` | CV skill extraction from database |
| `app/services/data_insights/canonicalizer.py` | Synonym mapping |
| `app/services/data_insights/market_loader.py` | CSV dataset loading |
| `app/services/data_insights/skill_filter.py` | Validation and classification |
| `app/services/data_insights/normalizer.py` | Text normalization |
| `app/templates/data_insights.html` | Frontend dashboard with Chart.js |

---

## �📋 System Requirements

- **Python**: 3.11+
- **Database**: SQLite (included)
- **Platform**: Windows/Linux/macOS
- **Web Server**: Flask development server or production WSGI server

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd app-cv-jvb19
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv311
venv311\Scripts\activate

# Linux/Mac
python3 -m venv venv311
source venv311/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration (optional for development)
```

### 5. Initialize Database
```bash
# The database will be created automatically on first run
# To manually initialize:
python init_db.py
```

### 6. Populate Technical Evidence Defaults
```bash
python populate_evidence_hub.py
```

This updates/inserts the 3 default Technical Evidence cards used on the API Home page.

### 7. Run the Application
```bash
python run.py
```

The application will be available at: `http://localhost:5000`

---

## 📁 Project Structure

```
app-cv-jvb19/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/                  # SQLAlchemy models
│   │   ├── app_metadata.py      # Dynamic version metadata
│   │   ├── personal_data.py     # Person model
│   │   ├── work_experience.py   # Experience model
│   │   ├── advanced_training.py # Unified courses/certifications
│   │   ├── education.py         # Education model
│   │   ├── support_tools.py     # Technical tools model
│   │   └── evidence_hub.py      # Evidence Hub entries
│   ├── routes/                  # Blueprint routes
│   │   ├── main.py              # Main pages
│   │   ├── admin.py             # Admin panel
│   │   ├── api.py               # PDF export API
│   │   ├── data_insights.py     # Market insights API
│   │   ├── forms.py             # Form routes
│   │   ├── profiles.py          # Profile presets
│   │   └── data_management.py   # Record management
│   ├── services/                # Business logic
│   │   ├── profile_presets/     # Preset configurations
│   │   └── data_insights/       # Analytics engine
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html            # Base template with navbar/footer
│   │   ├── index.html           # Homepage
│   │   ├── data_insights.html   # Analytics dashboard
│   │   ├── system_overview.html # Technical documentation
│   │   └── platform_overview.html # Functional documentation
│   └── static/                  # CSS, JS, images
│       └── uploads/             # User uploads (profile images, credentials)
├── data_insights/               # Market datasets
│   ├── kaggle_roles_skills.csv  # Kaggle job postings data
│   └── onet_skills.csv          # O*NET occupational data
├── cv_app.db                    # SQLite database
├── config.py                    # Flask configuration
├── run.py                       # Application entry point
└── requirements.txt             # Python dependencies
```

---

## 🔌 API Endpoints

### Market Insights API (`/api/data_insights`)

#### Get Market Insights
```http
GET /api/data_insights/market-insights?profile=data_scientist
```
Returns comprehensive skill coverage analysis with market cross-reference data.

**Response:**
```json
{
  "meta": {
    "api_version": "v2",
    "release_year": "2026",
    "api_status": "production",
    "model": "market_cross_reference_v1",
    "generated_at": "2026-02-20T00:00:00"
  },
  "coverage": { ... },
  "skills": { ... },
  "datasets": { ... }
}
```

#### Get Profile Readiness Score
```http
GET /api/data_insights/profile-readiness?profile=data_scientist
```
Returns calculated readiness percentage based on market alignment.

**Response:**
```json
{
  "meta": { ... },
  "profile": "data_scientist",
  "readiness_score": 85.71,
  "method": "matched_market_skills / total_market_skills",
  "counts": {
    "market_skill_count": 7,
    "matched_skill_count": 6
  }
}
```

#### Get Dashboard Data (Enhanced)
```http
GET /api/data_insights/dashboard
```
Returns data for all 3 dashboard charts with detailed skill breakdowns (Data Scientist profile only).

**Response:**
```json
{
  "meta": {
    "api_version": "v2",
    "release_year": "2026",
    "api_status": "production",
    "model": "market_cross_reference_v1",
    "generated_at": "2026-02-27T00:00:00"
  },
  "profile": "data_scientist",
  "chart1_profile_readiness": {
    "matched_skill_count": 9,
    "market_skill_count": 10,
    "readiness_score": 90.0,
    "matched_skills": ["api integration", "data visualization", ...],
    "missing_skills": ["numpy"],
    "all_market_skills": ["api integration", "data visualization", ...]
  },
  "chart2_coverage": {
    "market_demand": 10,
    "present_in_cv": 9,
    "gap": 1,
    "market_demand_skills": ["api integration", "data visualization", ...],
    "present_in_cv_skills": ["api integration", "data visualization", ...],
    "gap_skills": ["numpy"]
  },
  "chart3_dataset_alignment": {
    "kaggle": {
      "total": 5,
      "matched": 4,
      "missing": 1,
      "matched_skills": ["api integration", "feature engineering", ...],
      "missing_skills": ["numpy"],
      "alignment_percent": 80.0
    },
    "onet": {
      "total": 5,
      "matched": 5,
      "missing": 0,
      "matched_skills": ["data visualization", "machine learning", ...],
      "missing_skills": [],
      "alignment_percent": 100.0
    }
  },
  "datasets": {
    "files": ["kaggle_roles_skills.csv", "onet_skills.csv"],
    "last_updated_utc": "2026-02-09T19:30:37.854766Z"
  },
  "all_skills_detailed": {
    "python": {
      "present_in_cv": true,
      "present_in_market": true,
      "datasets": ["onet"],
      "skill_type": "technology"
    },
    ...
  }
}
```

### PDF Export API (`/api`)

#### Generate One-Page PDF
```http
POST /api/generate-pdf/one-page
Content-Type: application/json

{
  "profile": "data_scientist"
}
```

#### Generate Full Export PDF
```http
POST /api/generate-pdf/export
Content-Type: application/json

{
  "profile": "data_scientist"
}
```

---

## 🎨 Features

### 1. Homepage
- Profile selection cards (QA Analyst, QA Engineer, Data Scientist)
- Technical Evidence Hub with deterministic validation evidence cards
- Profile-specific skill highlights

#### Technical Evidence Default Cards

These defaults are aligned with the deterministic model and are synchronized through `populate_evidence_hub.py`:

| Slug | Title | Stack | Display Order |
|------|-------|-------|---------------|
| `qa-ui-automation` | UI / Automation: Selenium & Cucumber | Java · Selenium · Cucumber · Gherkin · BDD | 1 |
| `api-automation` | API Automation: Postman & Newman | Postman · Newman · JSON · Contract Validation · Deterministic Testing | 2 |
| `data-science` | Data & Market Insights (API-driven) | Python · Pandas · REST APIs · Analytical Modeling · Multi-Dataset Evaluation | 3 |

The populated descriptions are intentionally deterministic and consistent with the analytical model exposed by the API.

### 2. Data Entry Forms
- Personal Information
- Work Experience (with time blocks and visibility controls)
- Technical Tools (categorized by profile)
- Education
- Advanced Training (courses and certifications)
- Languages

### 3. Data Insights Dashboard
Available for **Data Scientist** profile:
- **Market Alignment Validation Dashboard** with detailed skill transparency
- **3 Interactive Visualizations**:
  - Profile Readiness Overview (donut chart with skill badges)
  - Market Demand vs Profile Coverage (vertical bar with skill lists)
  - Dataset Alignment Breakdown (grouped bar - Kaggle vs O*NET)
- **Skill-Level Detail**: Each chart displays actual skills behind every metric:
  - Matched skills (green badges)
  - Missing skills (red badges)
  - Dataset-specific skill breakdowns
- **Complete Skills Mapping Matrix**: Table view of all skills showing:
  - CV presence (Yes/No)
  - Market presence (Yes/No)
  - Dataset associations
  - Skill type classification
- Real-time readiness scoring with transparent calculation methodology
- Multi-source benchmarking: Kaggle job postings + O*NET occupational standards

### 4. Admin Panel
- Database management dashboard
- Record statistics
- Data visibility controls
- Advanced training management

### 5. Data Management
- View all records by category
- Edit/Delete functionality with admin password protection
- Soft delete and restore capabilities
- Profile visibility toggles

### 6. Documentation
- **System Overview**: Analytical and architectural foundation
- **Platform Overview**: Functional capabilities and modules

---

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///cv_app.db

# Upload Configuration
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# PDF Configuration
PDF_TEMP_DIR=app/static/temp

# Admin Password (for data management)
ADMIN_PASSWORD=9003712
```

### App Metadata (Database)

Version information is stored in the `app_metadata` table:

| Key                  | Value          | Description                    |
|----------------------|----------------|--------------------------------|
| application_name     | API CV         | Application name               |
| application_version  | 2026.2.0       | Semantic version               |
| release_year         | 2026           | Release year                   |
| api_version          | v2             | API version identifier         |
| api_release_date     | 2026-02-20     | Release date                   |
| api_status           | production     | Deployment status              |

To update version for future releases, run:
```bash
python update_api_version.py
```

---

## 📊 Database Schema

### Core Tables
- `person` - Personal information
- `work_experience` - Professional experience with visibility controls
- `advanced_training` - Unified courses and certifications
- `education` - Academic credentials
- `technical_tools` - Skills and tools with profile categorization
- `languages` - Language proficiencies
- `evidence_hub_entries` - Evidence Hub cards
- `app_metadata` - Dynamic system metadata

### Profile Visibility Fields
Each record includes visibility flags:
- `visible_qa_analyst`
- `visible_qa_engineer`
- `visible_data_scientist`

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pdf_modes.py

# Run with coverage
pytest --cov=app tests/
```

---

## 📦 Deployment

### Production Checklist

1. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Database Migration**
   ```bash
   flask db upgrade
   ```

3. **Update App Metadata**
   ```bash
   python update_api_version.py
   ```

4. **Static Files**
   - Ensure all uploads are backed up
   - Set proper file permissions

5. **WSGI Server**
   ```bash
   # Using Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
   ```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

---

## 📖 Additional Documentation

- [VERSION_MANAGEMENT.txt](VERSION_MANAGEMENT.txt) - Complete versioning guide
- [GETTING_STARTED.md](GETTING_STARTED.md) - Detailed setup instructions
- [ARCHITECTURE_V2.md](ARCHITECTURE_V2.md) - System architecture
- [DATA_MANAGEMENT_GUIDE.md](DATA_MANAGEMENT_GUIDE.md) - Data management guide
- [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) - Production deployment
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Full documentation index

---

## 🛠️ Tech Stack

### Backend
- **Flask 2.x** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Migrate** - Database migrations
- **ReportLab** - PDF generation
- **Python 3.11** - Programming language

### Frontend
- **Bootstrap 5.3.0** - UI framework
- **Bootstrap Icons 1.11.0** - Icon library
- **Chart.js 4.4.0** - Data visualization
- **Jinja2** - Template engine

### Database
- **SQLite** - Development/Production database

---

## 🔐 Security

- Admin password protection for data management actions
- Environment variable configuration for sensitive data
- CSRF protection (Flask-WTF recommended for production)
- SQL injection prevention via SQLAlchemy ORM
- File upload validation and size limits

---

## 📝 License

[Add your license information here]

---

## 👥 Authors

**Javier Villarreal Bencomo**
- Professional CV Builder API
- Email: [your-email@example.com]
- LinkedIn: [your-linkedin-profile]

---

## 🙏 Acknowledgments

- **Market Data Sources**: Kaggle, O*NET
- **Analytical Foundation**: Hindmarsh-Rose model research background
- **Framework**: Flask community
- **UI Components**: Bootstrap team

---

## 📞 Support

For issues, questions, or contributions:
1. Check existing documentation in the project
2. Review [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
3. Open an issue on GitHub
4. Contact the development team

---

## 🗺️ Roadmap

### Planned Features
- [ ] Multi-language support (English/Spanish)
- [ ] Additional profile types
- [ ] Enhanced analytics dashboard
- [ ] Real-time skill trend analysis
- [ ] API rate limiting
- [ ] User authentication system
- [ ] Export to additional formats (DOCX, JSON)

---

**Version 2.0** | Built with ❤️ using Flask & Bootstrap | © 2026 Javier Villarreal Bencomo
