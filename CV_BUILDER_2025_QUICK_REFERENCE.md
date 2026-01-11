# CV Builder 2025 - Quick Reference Guide
**Version:** 2025.2  
**Last Updated:** January 10, 2026  
**Status:** ✅ Production Ready

---

## Overview

A profile-based CV generation system that creates tailored resumes for different professional roles from a single dataset. Built with Flask, SQLAlchemy, and WeasyPrint.

**Key Capabilities:**
- Multi-Profile Support (QA Analyst, QA Engineer, Data Scientist)
- Dual PDF Export Modes (Complete Archive vs. One-Page Optimized)
- Credential Image Management
- Active/Historical Record Tracking
- Real-time CV Preview

---

## UI Design System

### Color Philosophy
**The colors are applied semantically rather than decoratively, reinforcing the hierarchy of actions, minimizing visual noise, and aligning with common SaaS conventions familiar to recruiters and hiring managers.**

### Color Meanings

| Color | Purpose | Examples |
|-------|---------|----------|
| **🔵 Blue** | Primary actions, main navigation | Preview CV, Edit, Save, Form headers |
| **⚪ Gray** | Neutral/technical actions | Export PDF, View/Hide, Secondary options |
| **🟡 Amber** | High-value results | One-Page PDF (optimized output) |
| **🟢 Green** | Valid/active states | Active badges, enabled toggles |
| **🔴 Red** | Destructive actions only | Delete (icon-only) |

### Button Standards
```
Home Screen:
  Preview CV    → Blue (primary)
  Edit Profile  → Blue outline
  Export PDF    → Gray (technical)
  One-Page PDF  → Amber (premium)

Forms:
  Save/Complete → Blue (primary)
  Alternatives  → Gray outline

Data Management:
  Edit          → Blue
  View/Hide     → Gray
  Delete        → Red (icon-only)
```

---

## Core Features

### 1. Multi-Profile CVs
Generate role-specific CVs from one dataset by toggling visibility per profile.

**Profiles:** QA Analyst, QA Engineer, Data Scientist

**How:** Each field has three visibility flags (one per profile). Profile presets auto-configure for optimal presentation.

### 2. Dual PDF Export Modes

#### Export PDF (Gray Button)
- **Purpose:** Complete archive/portfolio
- **Pages:** 4 fixed pages with all content
- **Data:** ALL records (active, inactive, historical)
- **Images:** Credential images included
- **Use Case:** Documentation, comprehensive review

#### One-Page PDF (Amber Button)
- **Purpose:** Recruiter-optimized CV
- **Pages:** ~1 page, auto-trimmed
- **Data:** Active, non-historical records only
- **Images:** Suppressed to save space
- **Use Case:** Job applications, quick overview

### 3. Record State Management
Control what appears in each PDF mode:

| State | Export PDF | One-Page PDF |
|-------|-----------|--------------|
| Active + Current | ✅ | ✅ |
| Active + Historical | ✅ | ❌ |
| Inactive | ✅ | ❌ |

**Benefits:** Preserve all career data while showing only relevant content per context.

### 4. Credential Images
Upload certificates, diplomas, and credentials (PNG, JPG, PDF).

**Auto-Processing:**
- 200x200px thumbnails
- Secure storage
- Shown in Export PDF, hidden in One-Page PDF

### 5. Visibility Control
**Three Levels for Work Experience:**
- Minimal: Title, company, dates
- Summary: + Brief overview
- Detailed: + Full responsibilities + achievements

**Profile-Specific:** Each field toggles independently per profile.

---

## Data Models

### Person
Contact info, profile titles, summaries, references, hero photo

### Work Experience
Job history, time blocks (2021-2025, 2015-2020, etc.), three-level content, active/historical flags

### Education
Degrees, schools, dates, credential images, display order

### Advanced Training
Courses and certifications (unified model), credential images, type badges

### Technical Tool
Technologies, proficiency, profile-specific subcategories

### Language
Conversation/reading/writing levels, certifications

### IT Product
Project portfolio, technologies, impact

---

## Quick Start

### Installation
```powershell
python -m venv venv311
.\venv311\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
$env:FLASK_APP = "run.py"
python -m flask run
```

**Access:**
- Local: http://localhost:5000
- Network: http://192.168.100.156:5000

### Workflow
1. **Add Person** → Contact info, titles, summaries, photo
2. **Add Work Experience** → Jobs, dates, responsibilities, set active/inactive
3. **Add Education** → Degrees, upload credential images
4. **Add Training** → Courses/certifications, upload certificates
5. **Preview CV** → Switch profiles, review content
6. **Generate PDFs:**
   - Export PDF (gray) → Complete archive, 4 pages
   - One-Page PDF (amber) → Optimized, ~1 page

### Data Management
**Access:** Menu → Admin → Data Management

**Actions:**
- Edit (blue pencil) → Modify record
- Hide (gray eye-slash) → Mark inactive (export only)
- Restore (gray eye) → Mark active (include in one-page)
- Delete (red trash) → Soft delete

**Status Badges:**
- Green: Active (in one-page PDF)
- Gray: Inactive (export only)
- Pastel Amber: Historical (archived)

---

## Technical Architecture

### Stack
- Backend: Flask, SQLAlchemy
- PDF: WeasyPrint
- Frontend: Bootstrap 5, JavaScript
- Images: Pillow

### Key Files
```
app/
├── models/              Data models
├── routes/              API endpoints
│   ├── profiles.py      CV generation
│   ├── api.py          REST endpoints
│   └── data_management.py
├── services/
│   ├── pdf_generator.py PDF rendering
│   ├── image_service.py Image upload
│   └── profile_presets.py
├── templates/
│   ├── index.html       Home
│   ├── profile_view.html CV preview
│   ├── forms/           Data entry
│   └── admin/           Management
└── static/uploads/      User images
```

### Security
- File validation (type whitelist, 5MB max)
- Filename sanitization
- Soft deletes (restore capability)

---

## CLI Commands

### Generate PDFs
```powershell
# Export PDF (complete, 4 pages)
python .\generate_pdf.py qa_engineer export

# One-Page PDF (optimized)
python .\generate_pdf.py qa_engineer one-page
```

### Database
```powershell
python init_db.py          # Initialize
python view_records.py     # View all data
```

---

## Version History

**2025.2 (January 2026)**
- Credential image upload
- Semantic UI color system
- One-Page PDF → Amber button
- Consolidated documentation

**2025.1 (December 2025)**
- Advanced Training unified model
- Dual PDF export modes
- Active/Inactive/Historical states
- Data management interface

---

## Documentation

**For Complete Details:** See `CV_BUILDER_2025_COMPLETE_GUIDE.md`

**Specialized Topics:**
- PDF_EXPORT_MODES_DOCUMENTATION.md
- CREDENTIAL_IMAGES_IMPLEMENTATION.md
- VERSION_2025_1_SUMMARY.md
- DEPLOYMENT.md

---

**Quick Reference Version**  
For comprehensive technical details, consult the complete guide.
