# CV Builder 2025 - Complete Guide
**Version:** 2025.2  
**Last Updated:** January 10, 2026  
**Branch:** cv2025-credential-images  
**Status:** ✅ Production Ready

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [UI Design System](#ui-design-system)
3. [Core Features](#core-features)
4. [PDF Export Modes](#pdf-export-modes)
5. [Data Models](#data-models)
6. [Key Implementations](#key-implementations)
7. [Quick Start Guide](#quick-start-guide)
8. [Technical Architecture](#technical-architecture)

---

## Overview

### What is CV Builder 2025?
A sophisticated, profile-based CV generation system that creates tailored resumes for different professional roles. Built with Flask, SQLAlchemy, and WeasyPrint.

### Key Capabilities
- ✅ **Multi-Profile Support**: Generate role-specific CVs (QA Analyst, QA Engineer, Data Scientist)
- ✅ **Granular Visibility Control**: Field-level visibility per profile
- ✅ **Dual PDF Export Modes**: Complete archive vs. optimized one-page
- ✅ **Credential Image Management**: Upload and display certificates, diplomas, and credentials
- ✅ **Active/Historical Record Tracking**: Full data preservation with selective display
- ✅ **Real-time Preview**: Live CV preview with profile switching
- ✅ **Data Management Interface**: Centralized record management and visibility control

---

## UI Design System

### Color Semantic System
**The color system is based on semantic meaning and the hierarchy of actions, not on decoration.**

#### Primary Colors & Their Meaning

**🔵 Blue - Primary Actions & Trust**
- **Purpose**: Main actions, primary navigation, form headers
- **Rationale**: Reinforces clarity, professionalism, and trust
- **Usage**:
  - Preview CV button (solid blue `#0d6efd`)
  - Edit buttons (primary actions)
  - Form headers (darker blue `#0056b3` for hierarchy)
  - Complete/Save buttons
- **Variants**:
  - Header blue: `#0056b3` (darker, authoritative)
  - Button blue: `#0d6efd` (vibrant, actionable)
  - Outline blue: For secondary navigation (Edit Profile)

**⚪ Gray - Neutral & Technical Actions**
- **Purpose**: Secondary actions, technical operations, neutral states
- **Rationale**: Avoids visual competition with primary actions
- **Usage**:
  - Export PDF button (technical document generation)
  - View/Hide/Restore actions in data management
  - Inactive record badges
  - Content level selector buttons (None, Minimal, Summary, Detailed)
- **Shades**:
  - `btn-secondary`: Standard gray buttons
  - `bg-secondary`: Inactive badges
  - `bg-light`: Current status indicators

**🟡 Amber - High-Value Results**
- **Purpose**: Important outcomes that aren't dangerous
- **Rationale**: Indicates value and importance without conveying risk
- **Usage**:
  - One-Page PDF button (`btn-warning`) - highlights the optimized result
  - Historical record badges (soft pastel `#ffd699`) - important but archived
- **Why Amber for One-Page PDF**: Signals a premium, optimized output—the "golden" version recruiters need

**🟢 Green - Valid & Active States**
- **Purpose**: Confirmation of positive states
- **Rationale**: Universal indicator of "good" status
- **Usage**:
  - Active record badges (`bg-success`)
  - Visibility toggles (when enabled)
- **Principle**: Used sparingly to avoid eye strain

**🔴 Red - Destructive Actions Only**
- **Purpose**: Irreversible or data-removing operations
- **Rationale**: Reserved for critical warnings
- **Usage**:
  - Delete buttons (permanent removal)
  - Icon-only implementation to reduce alarm
- **Rule**: Never used for important features (moved One-Page PDF to amber)

#### Button Hierarchy Standards

**Screen 1: Home (CV Builder)**
```
Preview CV       → btn-primary (solid blue)    [Main action]
Edit Profile     → btn-outline-primary         [Secondary nav]
Export PDF       → btn-secondary (gray)        [Technical output]
One-Page PDF     → btn-warning (amber)         [Premium output]
```

**Screen 2: Work Experience Form**
```
Complete         → btn-primary                 [Highest value]
Detailed         → btn-outline-secondary       [Alternative]
Summary          → btn-outline-secondary       [Alternative]
Minimal          → btn-outline-secondary       [Alternative]
None             → btn-outline-secondary       [Alternative]
Save Experience  → btn-primary                 [Commit action]
```

**Screen 3: Data Management**
```
Edit (✏️)         → btn-primary (blue)          [Modify data]
View/Hide (👁)    → btn-secondary (gray)        [Visibility toggle]
Delete (🗑)       → btn-danger (red, icon-only) [Destructive]
```

#### Badge Color Standards
```
Active           → bg-success (green)          [Included in one-page]
Inactive         → bg-secondary (gray)         [Export only]
Historical       → bg-warning (#ffd699 pastel) [Archived]
Current          → bg-light (light gray)       [Non-historical]
```

### Design Principles
1. **Semantic over Decorative**: Colors convey function, not aesthetics
2. **Hierarchy First**: Visual weight indicates action importance
3. **Consistency Across Contexts**: Same action = same color everywhere
4. **Recruiter-Friendly**: Professional palette, minimal cognitive load
5. **Accessibility**: Sufficient contrast, meaningful without color alone

---

## Core Features

### 1. Multi-Profile CV Generation
Create role-specific CVs from a single dataset by toggling field visibility per profile.

**Available Profiles:**
- **QA Analyst**: Focus on testing methodologies, manual testing, quality processes
- **QA Engineer**: Emphasis on automation, CI/CD, technical skills
- **Data Scientist**: Highlights analytics, ML, statistical tools

**How It Works:**
- Each data field has three visibility flags: `visible_qa_analyst`, `visible_qa_engineer`, `visible_data_scientist`
- Profile presets automatically configure visibility for optimal presentation
- Preview updates in real-time when switching profiles

### 2. Granular Visibility Control
Field-level control over what appears in each CV.

**Three-Level Content Visibility (Work Experience):**
- **Minimal**: Job title, company, dates only
- **Summary**: + Responsibilities summary (2-3 sentences)
- **Detailed**: + Detailed responsibilities + Key achievements

**Benefits:**
- Tailor content depth per profile
- Hide sensitive information
- Show relevant experience only

### 3. Active/Historical Record Management
Preserve all career data while controlling what appears in CVs.

**Record States:**
- **Active + Current**: Appears in both Export and One-Page PDFs
- **Active + Historical**: Appears in Export PDF only (preserved data)
- **Inactive**: Appears in Export PDF only (hidden from one-page)
- **Deleted**: Soft-deleted (can be restored)

**Use Cases:**
- Keep old roles for reference without cluttering current CV
- Test new content before making it active
- Archive outdated certifications while preserving history

### 4. Credential Image Management
Upload and display certificates, diplomas, and credential documents.

**Supported Formats:**
- Images: PNG, JPG, WEBP (displayed as thumbnails)
- Documents: PDF (link to view)
- Max Size: 5MB per file

**Auto-Processing:**
- Generates 200x200px thumbnails for images
- Secure filename storage with timestamps
- Safe cleanup on replace/delete

**Where Images Appear:**
- ✅ CV Preview (thumbnails with view links)
- ✅ Export PDF (credential images included)
- ❌ One-Page PDF (suppressed to save space)

---

## PDF Export Modes

### Export PDF - Complete Archive
**Purpose**: Comprehensive historical documentation

**Characteristics:**
- **Layout**: Fixed 4-page structure
  - Page 1: Hero photo + Name/Title + Professional Summary
  - Page 2: Sidebar sections (Technical Skills, Languages, Education, References, Contact)
  - Page 3: Work Experience (all periods)
  - Page 4: Advanced Training & Certifications
- **Data Filtering**: Shows ALL records regardless of `active` or `is_historical` flags
- **Images**: Includes credential images in Education and Advanced Training
- **Use Case**: Portfolio reviews, archive, comprehensive documentation

**What's Included:**
- ✅ All active and inactive records
- ✅ Historical data (`is_historical=True`)
- ✅ All time periods (1985-2025)
- ✅ Credential images and thumbnails
- ✅ Detailed content for all experiences

**Button Color**: Gray (`btn-secondary`) - Technical document generation

### One-Page PDF - Recruiter-Optimized
**Purpose**: Concise, recruiter-friendly CV

**Characteristics:**
- **Layout**: 2-column sidebar layout with auto-trimming
- **Data Filtering**: Only records with `active=True` AND `is_historical=False`
- **Images**: Suppressed to preserve space
- **Use Case**: Job applications, LinkedIn, quick overview
- **Auto-Optimization**: Progressively trims content to fit one page

**What's Included:**
- ✅ Active, non-historical records only
- ✅ Recent experiences (typically 2015-2025)
- ✅ Condensed responsibilities
- ❌ Inactive records excluded
- ❌ Historical records excluded
- ❌ Credential images excluded

**Trimming Strategy:**
1. Remove detailed responsibilities if content exceeds 1 page
2. Remove achievements if still too long
3. Hide older experiences progressively (by time block)
4. Maintain professional layout throughout

**Button Color**: Amber (`btn-warning`) - Premium optimized output

### Comparison Table

| Feature | Export PDF | One-Page PDF |
|---------|-----------|--------------|
| **Pages** | 4 fixed pages | ~1 page (auto-trimmed) |
| **Active Records** | ✅ Included | ✅ Included |
| **Inactive Records** | ✅ Included | ❌ Excluded |
| **Historical Records** | ✅ Included | ❌ Excluded |
| **Credential Images** | ✅ Shown | ❌ Suppressed |
| **Content Depth** | Full detail | Optimized/trimmed |
| **Time Range** | All periods | Recent only |
| **Button Color** | Gray | Amber |

---

## Data Models

### 1. Person
Core identity and contact information with profile-specific customization.

**Key Fields:**
- `first_name`, `last_name`, `email`, `phone`, `location`
- `linkedin`, `github`, `portfolio_website`
- `title_qa_analyst`, `title_qa_engineer`, `title_data_scientist`
- `summary_qa_analyst`, `summary_qa_engineer`, `summary_data_scientist`
- `reference_name_1/2/3`, `reference_title_1/2/3`, `reference_contact_1/2/3`
- `photo_path` (headshot image)

**Visibility Control**: Each contact field has three visibility flags per profile

**Image Upload**: Hero photo displayed in CV header

### 2. Work Experience
Career history with time block organization and three-level content control.

**Key Fields:**
- `job_title`, `company`, `location`
- `start_date`, `end_date`
- `time_block` ("2021-2025", "2015-2020", "2010-2014", "1985-2009", or None/"Other")
- `responsibilities_summary` (brief overview)
- `responsibilities_detailed` (full bullet points)
- `key_achievements` (major accomplishments)
- `active` (include in one-page PDF)
- `is_historical` (archived but preserved)

**Visibility Flags:**
- `show_responsibilities_summary`
- `show_responsibilities_detailed`
- `show_key_achievements`
- `visible_qa_analyst`, `visible_qa_engineer`, `visible_data_scientist`

**Display Order**: Sorted by time_block → display_order → start_date DESC

**Time Block Logic**:
- Groups experiences for better organization
- "Other" block handles records without time_block assignment
- Auto-assigned from dates if not manually set

### 3. Education
Academic credentials with diploma/degree images.

**Key Fields:**
- `degree`, `school`, `graduation_date`, `country`
- `start_date`, `end_date` (optional, overrides single year)
- `document_reference` (document number/code)
- `image_path`, `image_thumbnail_path`, `image_filename`, `image_mime_type`
- `display_order`, `active`

**Image Support**: Upload credential images (diplomas, transcripts)

**Date Display**: Shows graduation year OR "start_date - end_date" if both present

### 4. Advanced Training (Unified Courses & Certifications)
Professional development with type differentiation.

**Key Fields:**
- `type` ("course" or "certification")
- `name`, `provider`, `completion_date`
- `is_course` (boolean flag, True for courses)
- `hours` (course duration)
- `credential_id`, `credential_url` (certification-specific)
- `image_path`, `image_thumbnail_path`, `image_filename`, `image_mime_type`
- `display_order` (unified 1-6 ordering)
- `active`

**Display**: Ordered by display_order, type badge indicates course vs. certification

**Migration Note**: Merged from separate `courses` and `certifications` tables in Dec 2025

### 5. Technical Tool
Technologies, frameworks, tools with profile-specific categorization.

**Key Fields:**
- `tool_name`, `proficiency_level`, `years_experience`
- `subcategory_qa_analyst`, `subcategory_qa_engineer`, `subcategory_data_scientist`
- `display_order`

**Subcategory Examples**:
- QA Analyst: "Testing Tools", "Bug Tracking", "Test Management"
- QA Engineer: "Automation Frameworks", "CI/CD", "API Testing"
- Data Scientist: "Programming Languages", "ML Libraries", "Data Viz"

### 6. Language
Language proficiency with separate skill tracking.

**Key Fields:**
- `language`, `conversation_level`, `reading_level`, `writing_level`
- `certification` (optional)

**Proficiency Levels**: Native, Fluent, Conversational, Basic

### 7. IT Product
Project portfolio with technical details.

**Key Fields:**
- `product_name`, `role`, `technologies`, `link`
- `impact` (business results)
- `display_order`

---

## Key Implementations

### Credential Image Upload System
**Files**: `app/services/image_service.py`, `app/routes/api.py`

**Features:**
- Secure file validation (PNG, JPG, PDF; 5MB max)
- Auto-thumbnail generation (200x200px JPEG)
- Safe filename patterns: `education_{id}_{timestamp}.ext`
- Storage: `app/static/uploads/education/` and `.../advanced_training/`
- Cleanup: Removes old files on replace/delete

**API Endpoints:**
```python
POST /api/education              # Create with optional image
PUT  /api/education/{id}         # Update/replace/remove image
POST /api/advanced-training      # Create with optional image
PUT  /api/advanced-training/{id} # Update/replace/remove image
```

**Form Integration:**
- `multipart/form-data` submission
- File preview before upload
- "Remove existing image" checkbox
- Current image thumbnail display

### PDF Generation Pipeline
**Files**: `app/services/pdf_generator.py`

**Flow:**
1. Fetch profile data via `get_profile_data_dict(person_id, profile_name, include_inactive)`
2. Apply profile visibility filters
3. Generate HTML based on mode:
   - Export: `_generate_split_export_html()` (4 pages, images included)
   - One-Page: `_generate_html()` (2-column, images suppressed, auto-trim)
4. Render with WeasyPrint
5. Return PDF binary

**Image Handling:**
- Convert relative URLs to `file://` paths for WeasyPrint
- Constrain sizes: hero 150px, credentials 100px max-height
- Conditional rendering via `include_images` parameter

**Trimming Algorithm (One-Page):**
```python
def _trim_to_one_page(experiences):
    # 1. Remove detailed responsibilities
    # 2. Remove achievements
    # 3. Hide older time blocks (2010-2014, 1985-2009)
    # 4. Fallback: Hide 2015-2020 if still too long
```

### Data Management Interface
**Files**: `app/templates/admin/data_management.html`, `app/routes/data_management.py`

**Features:**
- Tabbed interface (Work Experience, Education, Advanced Training)
- Record visibility at a glance (badges)
- Quick actions: Edit (blue), Hide/Restore (gray), Delete (red)
- Soft delete with restore capability
- Active/Inactive/Historical status indicators

**Color-Coded Badges:**
- Active (green): Included in one-page PDF
- Inactive (gray): Export PDF only
- Historical (pastel amber): Archived but preserved
- Current (light gray): Non-historical status

### Profile Preset System
**Files**: `app/services/profile_presets.py`

**Presets Define:**
- Field visibility per profile
- Content level defaults (summary vs. detailed)
- Section ordering and emphasis

**Auto-Apply:**
- When creating new records
- Via "Apply Profile Preset" button in forms
- Ensures consistent profile-specific presentation

**Example:**
```python
QA_ANALYST_PRESET = {
    'show_responsibilities_summary': True,
    'show_responsibilities_detailed': False,
    'show_key_achievements': True
}
```

### Real-Time CV Preview
**Files**: `app/templates/profile_view.html`, `app/routes/profiles.py`

**Features:**
- Profile selector dropdown (QA Analyst, QA Engineer, Data Scientist)
- Live refresh on profile change
- Section visibility toggles
- Credential image thumbnails with view links
- Export and One-Page PDF buttons

**Technical:**
- AJAX fetch of profile data
- Dynamic HTML rendering
- CSS-based layout matching PDF output

---

## Quick Start Guide

### Installation

**1. Clone and Setup Environment**
```powershell
git clone <repository-url>
cd app-cv-jvb19
python -m venv venv311
.\venv311\Scripts\Activate.ps1
pip install -r requirements.txt
```

**2. Initialize Database**
```powershell
python init_db.py
```

**3. Run Development Server**
```powershell
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
python -m flask run
```

**4. Access Application**
- **Local:** http://localhost:5000 or http://127.0.0.1:5000
- **Network:** http://192.168.100.156:5000 (accessible from other devices on same network)
- Home: http://192.168.100.156:5000
- Preview CV: http://192.168.100.156:5000/profile/1
- Data Management: http://192.168.100.156:5000/admin/data

### Basic Workflow

**Step 1: Add Person**
1. Home → "Start Building" → Add Person
2. Fill contact info (name, email, location)
3. Add profile-specific titles and summaries
4. Upload hero photo (optional)
5. Save

**Step 2: Add Work Experience**
1. Menu → Data Entry → Work Experience → Add New
2. Enter job details (title, company, dates)
3. Set time block classification
4. Add responsibilities (summary, detailed, achievements)
5. Set visibility flags per profile
6. Mark as Active (include in one-page) or Inactive (export only)
7. Save

**Step 3: Add Education**
1. Menu → Data Entry → Education → Add New
2. Enter degree, school, graduation date
3. Upload credential image (diploma, transcript)
4. Set display order
5. Save

**Step 4: Add Advanced Training**
1. Menu → Data Entry → Advanced Training → Add New
2. Select type (Course or Certification)
3. Enter name, provider, completion date
4. For courses: add hours
5. For certifications: add credential ID and URL
6. Upload credential image (certificate)
7. Set display order (1-6)
8. Save

**Step 5: Preview CV**
1. Home → Select Profile Card → "Preview CV"
2. Switch profiles using dropdown (QA Analyst, QA Engineer, Data Scientist)
3. Click "Refresh" to reload after data changes
4. Review sections and credential images

**Step 6: Generate PDFs**
1. **Export PDF** (complete archive):
   - Home → Profile Card → "Export PDF" (gray button)
   - Or Preview CV → "Export PDF" (gray button)
   - Includes all records, credential images, 4 pages

2. **One-Page PDF** (recruiter-optimized):
   - Home → Profile Card → "One-Page PDF" (amber button)
   - Or Preview CV → "One-Page PDF" (amber button)
   - Active records only, no images, auto-trimmed to ~1 page

### Data Management Tasks

**View All Records**
1. Menu → Admin → Data Management
2. Select tab (Work Experience, Education, Advanced Training)
3. Review status badges (Active, Inactive, Historical)

**Edit Record**
1. Data Management → Find record → Click Edit (blue pencil icon)
2. Modify fields
3. Save

**Hide from One-Page PDF**
1. Data Management → Find record → Click Hide (gray eye-slash icon)
2. Record marked as Inactive (still appears in Export PDF)

**Restore to One-Page PDF**
1. Data Management → Find inactive record → Click Restore (gray eye icon)
2. Record marked as Active

**Delete Record**
1. Data Management → Find record → Click Delete (red trash icon)
2. Confirm deletion
3. Record soft-deleted (can be restored from database)

---

## Technical Architecture

### Technology Stack
- **Backend**: Flask 2.3+, Python 3.11
- **Database**: SQLAlchemy ORM, SQLite (dev) / PostgreSQL (production)
- **PDF Generation**: WeasyPrint 59+
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Image Processing**: Pillow (PIL)

### Project Structure
```
app-cv-jvb19/
├── app/
│   ├── __init__.py
│   ├── models/              # Data models
│   │   ├── person.py
│   │   ├── work_experience.py
│   │   ├── education.py
│   │   ├── advanced_training.py
│   │   ├── languages.py
│   │   ├── support_tools.py
│   │   └── ...
│   ├── routes/              # API and page routes
│   │   ├── profiles.py      # CV generation and preview
│   │   ├── api.py           # REST endpoints
│   │   ├── forms.py         # Form rendering
│   │   └── data_management.py
│   ├── services/            # Business logic
│   │   ├── pdf_generator.py # PDF rendering
│   │   ├── image_service.py # Image upload/processing
│   │   └── profile_presets.py
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html       # Home page
│   │   ├── profile_view.html # CV preview
│   │   ├── forms/           # Data entry forms
│   │   └── admin/           # Management interfaces
│   └── static/
│       ├── css/
│       ├── js/
│       └── uploads/         # User-uploaded images
│           ├── education/
│           ├── advanced_training/
│           └── person/
├── migrations/              # Database migrations
├── tests/                   # Unit and integration tests
├── generate_pdf.py          # CLI PDF generation
├── init_db.py               # Database initialization
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

### Database Schema Highlights

**Visibility Control Pattern** (all tables):
```python
visible_qa_analyst = db.Column(db.Boolean, default=True)
visible_qa_engineer = db.Column(db.Boolean, default=True)
visible_data_scientist = db.Column(db.Boolean, default=True)
```

**State Management Pattern** (Work Experience, Education, Training):
```python
active = db.Column(db.Boolean, default=True)          # Include in one-page PDF
is_historical = db.Column(db.Boolean, default=False)  # Archived data
display_order = db.Column(db.Integer, default=0)      # Section ordering
```

**Image Storage Pattern** (Education, Advanced Training):
```python
image_path = db.Column(db.String(500))
image_thumbnail_path = db.Column(db.String(500))
image_filename = db.Column(db.String(255))
image_mime_type = db.Column(db.String(50))
```

### API Design Patterns

**REST Endpoints:**
- `GET /api/{resource}` - List all
- `GET /api/{resource}/{id}` - Get one
- `POST /api/{resource}` - Create (with optional file upload)
- `PUT /api/{resource}/{id}` - Update (with optional file replace/remove)
- `DELETE /api/{resource}/{id}` - Soft delete

**Profile Data Endpoint:**
```python
GET /profile/{person_id}/data/{profile_name}
# Returns filtered data for specific profile
# Used by CV preview and PDF generation
```

**PDF Generation Endpoint:**
```python
POST /profile/{person_id}/pdf/{profile_name}
Body: { "one_page": true/false, "section_states": {...} }
# Returns PDF binary
```

### File Upload Security
- **Validation**: File type whitelist (PNG, JPG, WEBP, PDF)
- **Size Limit**: 5MB max
- **Filename Sanitization**: `secure_filename()` + timestamp
- **Storage**: Outside web root, served via Flask route
- **Cleanup**: Orphaned file removal on delete/replace

### PDF Rendering Pipeline
1. **Data Fetch**: Query database with profile filters
2. **HTML Generation**: Jinja2 templates with inline CSS
3. **Image Resolution**: Convert URLs to `file://` absolute paths
4. **WeasyPrint Render**: HTML → PDF with CSS layout
5. **Optimization**: One-page mode applies trimming algorithm
6. **Binary Response**: Return PDF as `application/pdf`

---

## File Reference

### Documentation Files
- **CV_BUILDER_2025_COMPLETE_GUIDE.md** (this file) - Comprehensive guide
- **PDF_EXPORT_MODES_DOCUMENTATION.md** - PDF generation details
- **CREDENTIAL_IMAGES_IMPLEMENTATION.md** - Image upload feature
- **VERSION_2025_1_SUMMARY.md** - Version changelog
- **DOCUMENTATION_INDEX.md** - Documentation catalog
- **QUICKSTART.md** - Quick start guide
- **DEPLOYMENT.md** - Production deployment
- **PRODUCTION_CHECKLIST.md** - Pre-deployment checklist

### Migration Scripts
- **migrate_add_credential_images.py** - Add image fields to education/training
- **migrate_to_advanced_training.py** - Merge courses/certifications
- **init_db.py** - Initialize database

### Utility Scripts
- **generate_pdf.py** - CLI PDF generation
- **list_export_records.py** - Debug record visibility
- **view_records.py** - Display database contents
- **check_*.py** - Validation utilities

---

## Version History

### Version 2025.2 (January 2026)
- ✅ Credential image upload for education and advanced training
- ✅ UI color system standardization (semantic color meanings)
- ✅ One-Page PDF button changed to amber (high-value result)
- ✅ Data management interface color refinements
- ✅ Historical badge soft pastel amber (#ffd699)
- ✅ Form header vs. button blue distinction
- ✅ Complete consolidated documentation

### Version 2025.1 (December 2025)
- ✅ Advanced Training unified model (courses + certifications)
- ✅ Dual PDF export modes (Export vs. One-Page)
- ✅ Active/Inactive/Historical record states
- ✅ Time block organization for work experience
- ✅ Data management interface
- ✅ Profile preset system
- ✅ Real-time CV preview
- ✅ Three-level content visibility

### Version 2019 (Legacy)
- Static CV generation
- Single profile only
- No visibility controls
- Available via archive menu

---

## Support & Contact

### Documentation Updates
All documentation is version-controlled in the repository. For updates:
1. Review existing docs in `*.md` files
2. Update relevant sections
3. Commit with descriptive message

### Issue Reporting
- Check existing documentation first
- Include error messages and screenshots
- Specify browser/OS for UI issues
- Note which profile/mode was active

### Branch Strategy
- `main` - Stable production code
- `cv2025-credential-images` - Latest development (current)
- `version-2025` - Version 2025.1 baseline
- `version-2019` - Legacy archive

---

## Appendix: CLI Commands

### Generate PDFs from Command Line
```powershell
# Export PDF (complete archive, 4 pages)
python .\generate_pdf.py qa_engineer export

# One-Page PDF (recruiter-optimized, ~1 page)
python .\generate_pdf.py qa_engineer one-page

# Available profiles: qa_analyst, qa_engineer, data_scientist
```

### Database Utilities
```powershell
# Initialize/reset database
python init_db.py

# View all records
python view_records.py

# List export visibility
python list_export_records.py

# Check time block assignments
python check_time_blocks.py
```

### Development Server
```powershell
# Set environment
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"

# Run server (localhost only)
python -m flask run

# Run on all network interfaces (accessible from other devices)
python run.py
# Access at: http://192.168.100.156:5000

# Run on specific port
python -m flask run --port 5001
```

**Network Access:**
- `python -m flask run` → localhost only (127.0.0.1:5000)
- `python run.py` → all interfaces (0.0.0.0) accessible at http://192.168.100.156:5000

---

**End of Complete Guide**  
For specific feature details, see individual documentation files listed in File Reference section.
