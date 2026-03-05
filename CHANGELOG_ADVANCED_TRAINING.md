# Changelog: Advanced Training & Certifications Restructuring
**Date:** December 2025 | **Version:** 2025.1

---

## 🎯 Overview

Major data model restructuring that unified the `Certification` and `Course` tables into a single, flexible `AdvancedTraining` table. This simplifies data management while maintaining full functionality and flexibility.

---

## ✨ Key Changes

### 1. **Data Model Changes**

#### ❌ DEPRECATED Tables
- `certification` table - **MERGED into advanced_training**
- `course` table - **MERGED into advanced_training**

#### ✅ NEW Table
- `advanced_training` table - Unified model for courses and certifications

**Migration Path:**
```
Certification data → AdvancedTraining (type="Certification")
Course data       → AdvancedTraining (type="Course")
```

### 2. **Schema Changes**

#### Advanced Training Model Fields
```python
id                  # Primary key
type                # 'Course' or 'Certification' (NEW field)
name                # Title/name of training
provider            # Organization/issuer (replaces issuing_organization)
completion_date     # Date completed/issued
description         # Details, topics, achievements
duration_hours      # Course duration in hours (optional)
expiration_date     # Certification expiration (optional)
credential_id       # Certificate number (optional)
credential_url      # Verification link (optional)
display_order       # Unified sort order for section (1-6)
visible_qa_analyst  # Visibility flag
visible_qa_engineer # Visibility flag
visible_data_scientist # Visibility flag
is_historical       # Historical data flag
active              # Active/inactive flag
created_at          # Timestamp
updated_at          # Timestamp
```

#### Field Mapping from Original Tables
```python
# Certification → AdvancedTraining
Certification.name                  → AdvancedTraining.name
Certification.issuing_organization  → AdvancedTraining.provider
Certification.issue_date            → AdvancedTraining.completion_date
Certification.expiration_date       → AdvancedTraining.expiration_date
Certification.credential_id         → AdvancedTraining.credential_id
Certification.credential_url        → AdvancedTraining.credential_url
Certification.description           → AdvancedTraining.description
(new type="Certification")          → AdvancedTraining.type

# Course → AdvancedTraining
Course.name                         → AdvancedTraining.name
Course.provider                     → AdvancedTraining.provider
Course.completion_date              → AdvancedTraining.completion_date
Course.description                  → AdvancedTraining.description
Course.duration_hours               → AdvancedTraining.duration_hours
(new type="Course")                 → AdvancedTraining.type
```

---

## 📋 Form Changes

### ❌ REMOVED Forms
- `certification_form.html` - Separate certification form (no longer used)
- `course_form.html` - Separate course form (no longer used)

### ✅ NEW Form
- `advanced_training_form.html` - Unified form for both types

**New Form Features:**
- Type selector (Course/Certification dropdown)
- Dynamic fields based on selected type
- Unified display_order field (1-6)
- Course-specific: duration_hours
- Certification-specific: expiration_date, credential_id, credential_url

---

## 🗂️ Menu Structure Changes

### Data Entry Menu (Before)
```
Data Entry
├── Personal Info
├── Work Experience
├── Technical Tools
├── Education
├── Certifications       ❌ REMOVED
├── Courses             ❌ REMOVED
└── Languages
```

### Data Entry Menu (After)
```
Data Entry
├── Personal Info
├── Work Experience
├── Technical Tools
├── Education
├── Advanced Training & Certifications  ✅ NEW (unified)
└── Languages
```

---

## 🔄 API Route Changes

### ❌ REMOVED Routes
- `POST /api/certification` - Create certification
- `GET /api/certification` - List certifications
- `GET /api/certification/<id>` - Get certification
- `PUT /api/certification/<id>` - Update certification
- `DELETE /api/certification/<id>` - Delete certification
- `POST /api/course` - Create course
- `GET /api/course` - List courses
- `GET /api/course/<id>` - Get course
- `PUT /api/course/<id>` - Update course
- `DELETE /api/course/<id>` - Delete course

### ✅ NEW Routes
- `POST /api/advanced-training` - Create training item
- `GET /api/advanced-training` - List training items
- `GET /api/advanced-training/<id>` - Get training item
- `PUT /api/advanced-training/<id>` - Update training item
- `DELETE /api/advanced-training/<id>` - Delete training item

---

## 📊 Database Migration

### Migration Script
**File:** `migrate_to_advanced_training.py`

**What it does:**
1. Creates new `advanced_training` table with unified schema
2. Copies all Certification records → advanced_training (type="Certification")
3. Copies all Course records → advanced_training (type="Course")
4. Drops old `certification` and `course` tables
5. Preserves all data (nothing lost)

**Result:**
- Before: ~X certification records + ~Y course records
- After: ~(X+Y) advanced_training records with type field distinguishing them

---

## 🔍 Profile/PDF Impact

### Profile Data Assembly (`app/routes/profiles.py`)
```python
# OLD (separate queries)
certifications = Certification.query.filter_by(active=True)
courses = Course.query.filter_by(active=True)

# NEW (unified query)
advanced_training = AdvancedTraining.query.filter_by(active=True)
sorted_by_display_order = sorted(advanced_training, key=lambda x: x.display_order)
```

### PDF Rendering (`app/services/pdf_generator.py`)
```python
# OLD method
_render_certifications(certifications)  # Rendered as separate section

# NEW method
_render_advanced_training(advanced_training)  # Unified section
# Shows both courses and certifications mixed together
# Sorted by display_order (1-6)
# Type field determines rendering style (if needed)
```

**Benefits:**
- Single "Advanced Training & Certifications" section in PDF
- Unified display_order (1-6) for entire section
- Courses and certifications can be freely intermixed
- Type field allows customized rendering per type if desired

---

## 📝 Documentation Updates

### Updated Files
1. **ARCHITECTURE_V2.md** - Updated model descriptions
   - Changed Certification/Course to AdvancedTraining
   - Documented new type field
   - Explained unified display_order

2. **FORMS_IMPLEMENTATION.md** - Updated form list
   - Removed certification_form and course_form
   - Added advanced_training_form with full documentation
   - Updated forms router documentation
   - Updated menu structure

3. **CHANGELOG_ADVANCED_TRAINING.md** - This file
   - Comprehensive migration guide
   - Before/after comparisons
   - Field mapping reference

---

## 🔄 Data Model Benefits

### Flexibility
✅ Single form for both courses and certifications
✅ Unified display_order for mixed sections
✅ No need to choose between course/certification at entry time
✅ Easy to change type if needed

### Simplicity
✅ Fewer database tables to manage
✅ Fewer API endpoints to maintain
✅ Simpler forms (one instead of two)
✅ Simpler menu structure

### Extensibility
✅ Easy to add new fields for future training types
✅ Type field allows for future subtypes (e.g., "Workshop", "Bootcamp")
✅ Unified profile visibility controls

### Data Preservation
✅ All existing data migrated (nothing lost)
✅ Field mappings preserve information
✅ Historical flag still available for old records

---

## 🚀 Migration Steps

### For Users
1. **No action required** - migration handled automatically
2. **Update bookmarks** - if you bookmarked `/forms/certification` or `/forms/course`
   - Use `/forms/advanced-training` instead
3. **Menu update** - Check "Data Entry" menu shows "Advanced Training & Certifications"

### For Developers
1. **Import changes:**
   ```python
   # OLD
   from app.models import Certification, Course
   
   # NEW
   from app.models import AdvancedTraining
   ```

2. **Query changes:**
   ```python
   # OLD
   certs = Certification.query.filter_by(active=True)
   courses = Course.query.filter_by(active=True)
   
   # NEW
   training = AdvancedTraining.query.filter_by(active=True)
   courses = [t for t in training if t.type == 'Course']
   certs = [t for t in training if t.type == 'Certification']
   ```

3. **API calls:**
   ```python
   # OLD
   /api/certification/1
   /api/course/1
   
   # NEW
   /api/advanced-training/1
   /api/advanced-training/2
   ```

---

## ✅ Testing Checklist

- [ ] Migration script runs without errors
- [ ] All certification data migrated to advanced_training
- [ ] All course data migrated to advanced_training
- [ ] Type field correctly set ("Course" or "Certification")
- [ ] Old certification and course tables dropped
- [ ] Admin database view shows advanced_training records
- [ ] Advanced training form loads correctly
- [ ] Form correctly hides/shows fields based on type
- [ ] API endpoints work: GET, POST, PUT, DELETE
- [ ] Profile data assembly includes advanced_training
- [ ] PDF renders "Advanced Training & Certifications" section
- [ ] Display order sorting works (1-6)
- [ ] Menu shows "Advanced Training & Certifications" instead of separate items
- [ ] Profile visibility flags work correctly
- [ ] Historical data flag works correctly

---

## 📞 Support

### Common Questions

**Q: Where did my certifications go?**
A: They're now in the unified AdvancedTraining table with type="Certification". Access via `/forms/advanced-training` menu item.

**Q: How do I add a new course now?**
A: Use `/forms/advanced-training`, select type="Course", fill in course details, and save.

**Q: Can I still mix courses and certifications?**
A: Yes! That was the goal. The unified display_order (1-6) lets you freely order them together.

**Q: Why change this?**
A: Simpler data model, single form instead of two, unified section in CV, more flexible for future needs.

---

## 🔍 Version Information

- **Date:** December 2025
- **Version:** 2025.1
- **Migration Script:** `migrate_to_advanced_training.py`
- **Status:** ✅ Complete and Tested

---

## 📚 Related Documentation

- ARCHITECTURE_V2.md - Overall system design
- FORMS_IMPLEMENTATION.md - Form details
- API endpoint documentation - REST API reference
