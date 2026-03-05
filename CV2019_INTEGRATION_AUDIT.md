# CV 2019 Integration Plan - Comprehensive Audit & Architecture
**Date:** December 10, 2025 | **Prepared for:** CV 2025 Integration with CV 2019 Legacy  
**Branch:** cv2019-integration | **Status:** Planning & Audit Phase

---

## 📊 Executive Summary

The CV 2019 is a **static Flask application** (stored in `/src/`) with:
- **8 main menu sections** displayed via URL routes
- **HTML templates** with embedded styling and images
- **Static assets** (CSS, JS, images) organized in `/src/static/`
- **No database** - all content is hardcoded in HTML

The CV 2025 is a **modern Flask application** with:
- **Database-driven content** (SQLAlchemy models)
- **Bootstrap 5 UI framework**
- **Modular blueprint architecture**
- **Profile-based visibility filtering**

**Goal:** Create a "CV 2019" access point within CV 2025 that preserves the original look, feel, and functionality while maintaining separation from modern features.

---

## 🗂️ CV 2019 Project Structure Analysis

### Source Directory: `/src/`

```
/src/
├── index.py                 # Flask app entry point (routes defined here)
├── requirements.txt         # Original dependencies (Flask 1.1.2, etc.)
├── Procfile                 # Heroku deployment config
├── runtime.txt              # Python 3.9 specification
└── static/
    ├── css/
    │   ├── bootstrap.min.css
    │   ├── estilos.css          # Primary custom styles
    │   ├── estilos8.css through estilos12.css  (variants)
    │   ├── animation.css        # Animation definitions
    │   └── fontello*.css        # Icon font CSS files
    ├── img/
    │   ├── font/                # Font files
    │   ├── fotoJvb.png          # Profile photo
    │   ├── ingeniero_de_sistemas.jpg     # Education cert
    │   ├── magister_scientaurum.jpg      # Master's cert
    │   ├── constancia*.png/.jpg # Work experience certs
    │   ├── capacitacionDocente*.png      # Training certs
    │   └── suficienciaIngles.png         # Language cert
    └── js/
        ├── bootstrap.js
        ├── bootstrap.min.js
        └── hacer-clic.js        # Custom click handlers

└── templates/
    ├── formatoPrincipal.html        # Old main layout template
    ├── formatoPrincipal4.html       # Used main layout template
    ├── formatoPrincipal5.html through formatoPrincipal12.html  (variants)
    ├── inicio2.html                 # Home/Intro section
    ├── educacion2.html              # Education section
    ├── experienciaLaboral.html      # Work experience section
    ├── productosInformaticos.html   # Software products section
    ├── datosPersonales.html         # Personal data section
    ├── soporteProgramacion.html     # Programming support section
    ├── cursosInformaticos.html      # Courses section
    ├── documentos.html              # Documents/certificates section
    ├── titulos.html                 # Titles section
    ├── certificaciones.html         # Certifications section
    ├── certificaciones0.html        # Certifications variant
    └── constanciasLaborales.html    # Work certificates section
```

---

## 🔀 CV 2019 Routes & Menu Structure

### Flask Routes (from `/src/index.py`):

```python
/                           → inicio2.html              # Home
/educacion                  → educacion2.html           # Education
/experienciaLaboral         → experienciaLaboral.html   # Work Experience
/productosInformaticos      → productosInformaticos.html # IT Products
/datosPersonales            → datosPersonales.html      # Personal Data
/soporteProgramacion        → soporteProgramacion.html  # Programming Support
/cursosInformatica          → cursosInformaticos.html   # Courses
/documentos                 → documentos.html           # Documents (main)
/titulos                    → titulos.html              # Titles (submenu)
/constanciasLaborales       → constanciasLaborales.html # Work Certs (submenu)
/certificaciones            → certificaciones.html      # Certifications (submenu)
```

### Menu Navigation Pattern:

The CV 2019 uses a **hierarchical menu**:

```
MAIN MENU (8 items):
├── Inicio                   → Homepage with intro
├── Educación                → Education history
├── Experiencia Laboral      → Job positions
├── Productos Informáticos   → Software/IT products created
├── Datos Personales         → Contact info
├── Soporte de Programación  → Tech skills/tools
├── Cursos de Informática    → Training courses
└── Documentos               → Document archive
    ├── Títulos              (submenu)
    ├── Constancias Laborales (submenu)
    └── Certificaciones      (submenu)
```

---

## 🎨 CV 2019 Visual/UI Elements

### Color Scheme (from CSS analysis):
```css
Primary Background: #8B7500 (Dark Gold/Brown) - From estilos.css
Secondary: #A0860D (Lighter Gold)
Navigation: Dark backgrounds with light text
Text: Dark gray on white backgrounds
Accent: Golden/tan highlights
```

### Key CSS Files:
- **estilos.css** - Main stylesheet with layout, colors, typography
- **animation.css** - Transition and animation effects
- **bootstrap.min.css** - Bootstrap 4.5.0 framework
- **fontello.css** - Custom icon fonts

### Images Used:
- Profile photo: `fotoJvb.png`
- Education certificates: JPEG/PNG images (2-3 pages each)
- Work experience documents: PNG images
- Various document proofs

---

## 📝 Content Analysis - What Each Section Contains

### 1. **Inicio (Home)**
- Header with name "Javier Villarreal"
- Professional title: "Programador / Desarrollador Web"
- Profile photo (clickable to resize)
- Brief professional summary

### 2. **Educación (Education)**
- System Engineering degree (Universidad)
- Master's in Human Resources Management
- Structured with dates, institutions, credentials

### 3. **Experiencia Laboral (Work Experience)**
- Job positions with dates
- Companies/organizations
- Roles and responsibilities

### 4. **Productos Informáticos (IT Products)**
- Software projects created
- Technologies used
- Project descriptions

### 5. **Datos Personales (Personal Data)**
- Contact information
- Location
- Professional references

### 6. **Soporte de Programación (Programming Support)**
- Technical skills
- Tools and frameworks
- Programming languages

### 7. **Cursos de Informática (Courses)**
- Training courses completed
- Certifications earned
- Training institutions

### 8. **Documentos (Documents Archive)**
- Links to document sections
- Certificate gallery
- Proof documents

### 8a. **Documentos > Títulos (Degree Certificates)**
- System Engineering degree image
- Master's degree image

### 8b. **Documentos > Constancias Laborales (Work Certificates)**
- UPTT-IUTET work certificate
- Silboca work certificate
- CIDIAT work certificate

### 8c. **Documentos > Certificaciones (Certifications)**
- Technical training certifications
- Language proficiency certificates
- Professional development certificates

---

## 🛠️ Integration Strategy for CV 2025

### Approach: Hybrid Static + Dynamic Integration

**Core Principle:** Preserve CV 2019 exactly as-is while making it accessible from CV 2025 modern interface.

### Option 1: **Embedded Legacy Route** (RECOMMENDED)
```
CV 2025 Main App (Modern)
    ├── Database-driven profiles (QA Analyst, QA Engineer, Data Scientist)
    ├── Bootstrap 5 UI
    └── NEW: /legacy/cv2019/* routes
        ├── Serves CV 2019 templates from /src/templates/
        ├── Uses CV 2019 CSS from /src/static/css/
        ├── Uses CV 2019 images from /src/static/img/
        └── Maintains original navigation structure
```

**Advantages:**
- ✅ CV 2019 code untouched
- ✅ Clean separation from 2025 features
- ✅ Easy to maintain both versions
- ✅ Can switch between versions seamlessly
- ✅ No database needed for legacy CV
- ✅ Preserves exact original styling

### Option 2: **Integrated DB Migration** (Not Recommended)
- Would require converting CV 2019 static content to database models
- Loses original styling and layout
- Requires extensive refactoring
- More complex maintenance

---

## 📋 Integration Checklist & Implementation Plan

### Phase 1: Set Up Legacy Route Handlers
- [ ] Create `/app/routes/legacy.py` blueprint
- [ ] Add routes for each CV 2019 section:
  ```python
  /legacy/cv2019/               → inicio2.html
  /legacy/cv2019/educacion      → educacion2.html
  /legacy/cv2019/experiencia    → experienciaLaboral.html
  /legacy/cv2019/productos      → productosInformaticos.html
  /legacy/cv2019/datos          → datosPersonales.html
  /legacy/cv2019/soporte        → soporteProgramacion.html
  /legacy/cv2019/cursos         → cursosInformaticos.html
  /legacy/cv2019/documentos     → documentos.html
  /legacy/cv2019/titulos        → titulos.html
  /legacy/cv2019/constancias    → constanciasLaborales.html
  /legacy/cv2019/certificaciones → certificaciones.html
  ```

### Phase 2: Copy Static Assets
- [ ] Copy CV 2019 CSS files to `/app/static/legacy/css/`
- [ ] Copy CV 2019 images to `/app/static/legacy/img/`
- [ ] Copy CV 2019 JS files to `/app/static/legacy/js/`
- [ ] Update template references to use new paths

### Phase 3: Create Legacy Templates Wrapper
- [ ] Adapt CV 2019 templates to work from CV 2025 app
- [ ] Update Jinja2 template syntax if needed
- [ ] Create modified `formatoPrincipal4.html` that works in new location
- [ ] Update all internal links to use `/legacy/cv2019/*` paths

### Phase 4: Update Navigation
- [ ] Add "CV 2019" menu option to CV 2025 base template
- [ ] Add navigation back to CV 2025 from CV 2019
- [ ] Update all cross-links between sections

### Phase 5: Testing & Validation
- [ ] Test all CV 2019 routes load correctly
- [ ] Verify styling renders properly
- [ ] Verify images load from new paths
- [ ] Test navigation between sections
- [ ] Test links back to CV 2025

---

## 🚀 Implementation Details

### File Structure After Integration:

```
/app-cv-jvb19/
├── app/
│   ├── routes/
│   │   ├── main.py              (existing - 2025 modern routes)
│   │   ├── legacy.py            (NEW - CV 2019 legacy routes)
│   │   └── ...
│   ├── templates/
│   │   ├── base.html            (modern 2025 base)
│   │   ├── index.html           (modern 2025 home)
│   │   └── legacy/              (NEW directory)
│   │       ├── cv2019_base.html (NEW wrapper)
│   │       ├── inicio2.html
│   │       ├── educacion2.html
│   │       ├── experienciaLaboral.html
│   │       └── ... (all other CV 2019 templates)
│   └── static/
│       ├── css/                 (modern 2025 CSS)
│       ├── js/                  (modern 2025 JS)
│       ├── img/                 (modern 2025 images)
│       └── legacy/              (NEW directory)
│           ├── css/
│           │   ├── estilos.css
│           │   ├── animation.css
│           │   └── ... (other CV 2019 CSS)
│           ├── js/
│           │   └── hacer-clic.js
│           └── img/
│               ├── fotoJvb.png
│               ├── ingeniero_de_sistemas.jpg
│               └── ... (all CV 2019 images)
└── src/                        (original CV 2019 - kept for reference)
    ├── index.py
    ├── templates/
    └── static/
```

### Key Implementation Files:

#### 1. **`/app/routes/legacy.py`** (NEW)
```python
"""Legacy CV 2019 Routes"""
from flask import Blueprint, render_template

bp = Blueprint('legacy', __name__, url_prefix='/legacy/cv2019')

@bp.route('/')
def home():
    return render_template('legacy/inicio2.html')

@bp.route('/educacion')
def educacion():
    return render_template('legacy/educacion2.html')

# ... (repeat for all 11 routes)
```

#### 2. **`/app/templates/legacy/cv2019_base.html`** (NEW - Wrapper)
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}CV Javier Villarreal 2019{% endblock %}</title>
    
    <!-- CV 2019 Original Styling -->
    <link rel="stylesheet" href="{{ url_for('static', filename='legacy/css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='legacy/css/estilos.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='legacy/css/animation.css') }}">
</head>
<body>
    <!-- Navigation back to CV 2025 -->
    <nav class="navbar navbar-dark bg-dark">
        <a href="/" class="navbar-brand">← Back to CV 2025</a>
    </nav>
    
    <!-- Original CV 2019 Content -->
    {% block content %}{% endblock %}
    
    <!-- Original scripts -->
    <script src="{{ url_for('static', filename='legacy/js/hacer-clic.js') }}"></script>
</body>
</html>
```

#### 3. Update **`/app/templates/base.html`** (EXISTING - 2025 modern)
```html
<!-- Add to navigation menu -->
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
        Archivos
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="/legacy/cv2019/">CV 2019 - Versión Original</a></li>
    </ul>
</li>
```

---

## 📊 Content Mapping: CV 2019 Sections → 2025 Routes

| CV 2019 Section | Route | Template | Content |
|-----------------|-------|----------|---------|
| Home | `/legacy/cv2019/` | inicio2.html | Intro + Photo |
| Education | `/legacy/cv2019/educacion` | educacion2.html | Degrees |
| Experience | `/legacy/cv2019/experiencia` | experienciaLaboral.html | Jobs |
| Products | `/legacy/cv2019/productos` | productosInformaticos.html | Software |
| Personal Data | `/legacy/cv2019/datos` | datosPersonales.html | Contact |
| Support | `/legacy/cv2019/soporte` | soporteProgramacion.html | Skills |
| Courses | `/legacy/cv2019/cursos` | cursosInformaticos.html | Training |
| Documents | `/legacy/cv2019/documentos` | documentos.html | Cert list |
| → Titles | `/legacy/cv2019/titulos` | titulos.html | Degree imgs |
| → Work Certs | `/legacy/cv2019/constancias` | constanciasLaborales.html | Job certs |
| → Certifications | `/legacy/cv2019/certificaciones` | certificaciones.html | Course certs |

---

## 🔗 Navigation Flow Design

### CV 2025 Main Menu:
```
Home → Profiles (QA Analyst/Engineer/Data Scientist) → Archives (CV 2019)
```

### CV 2019 Menu (Original):
```
Home → Educación → Experiencia → Productos → Datos → Soporte → Cursos → Documentos
                                                                          → Títulos
                                                                          → Constancias
                                                                          → Certificaciones
```

### Cross-Navigation:
- CV 2025 navbar includes link to `/legacy/cv2019/`
- CV 2019 navbar includes link back to CV 2025 home
- Each CV 2019 section links to others within legacy

---

## 🎯 Next Steps

**Before Implementation:**
1. ✅ Review this audit document (CURRENT STEP)
2. ✅ Confirm integration approach with user
3. ✅ Get approval on file structure and naming conventions

**After Approval:**
1. Create `/app/routes/legacy.py` with all route handlers
2. Copy `/src/static/` assets to `/app/static/legacy/`
3. Copy `/src/templates/` to `/app/templates/legacy/`
4. Update template references (Jinja2 syntax, URL paths)
5. Create wrapper template for legacy layout
6. Update navigation in CV 2025 base template
7. Test all routes and navigation
8. Commit to `cv2019-integration` branch

---

## 📌 Questions for User Clarification

1. **Asset Location:** Should CV 2019 assets be copied to `/app/static/legacy/` or served directly from `/src/static/`?
2. **Template Syntax:** Should I adapt templates to use `{{ url_for() }}` or keep original syntax?
3. **Navigation Menu:** Should CV 2019 maintain its own 8-item menu, or integrate with CV 2025 nav structure?
4. **Styling:** Should CV 2019 remain completely isolated visually, or integrate with CV 2025 base navbar?
5. **Images:** Are all CV 2019 images in `/src/static/img/` complete and should they be included as-is?
6. **Links:** Should document links in CV 2019 point to actual PDFs/images or just display text references?

---

**Status:** Ready for user approval and implementation  
**Estimated Implementation Time:** 4-6 hours for complete integration and testing
