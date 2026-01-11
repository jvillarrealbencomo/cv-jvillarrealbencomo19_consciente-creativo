# PDF Export Modes Documentation

## Overview
The CV Builder now supports two distinct PDF export modes with different record filtering behaviors:

1. **Export PDF** - Shows ALL records (full history export)
2. **One-Page PDF** - Shows only active records (optimized for brevity)

## Export PDF Mode

### Behavior
- **Purpose**: Complete historical record export
- **Data Filtering**: Shows ALL database records regardless of `active` or `is_historical` flags
- **Layout**: Fixed 4-page export (P1 hero/summary, P2 sidebar sections, P3 work experience, P4 advanced training) with credential images shown in Education and Advanced Training
- **Use Case**: Archive, portfolio review, comprehensive documentation

### What Gets Included
- ✅ All Work Experience records (active=True AND active=False)
- ✅ All Education records (active=True AND active=False)  
- ✅ All Advanced Training records (active=True AND active=False)
- ✅ All Languages and IT Products (active=True AND active=False)
- ✅ Records marked as `is_historical=True` (preserved historical data)

### How to Trigger
```javascript
// From Home page or Preview CV
fetch(`/profile/${person_id}/pdf/${profile_name}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ one_page: false })
});
```

## One-Page PDF Mode

### Behavior
- **Purpose**: Concise, recruiter-friendly CV
- **Data Filtering**: Shows only records with `active=True` and `is_historical=False`
- **Layout**: 2-column sidebar layout with automatic trimming; credential images suppressed to preserve space
- **Use Case**: Job applications, LinkedIn profile, quick overview

### What Gets Included
- ✅ Work Experience with `active=True` and `is_historical=False`
- ✅ Education with `active=True` and `is_historical=False`
- ✅ Advanced Training with `active=True` and `is_historical=False`
- ✅ Languages and IT Products with `active=True` and `is_historical=False`
- ❌ Records with `active=False` (excluded)
- ❌ Records with `is_historical=True` (excluded)

### Auto-Optimization Features
1. Trims detailed responsibilities if content exceeds 1 page
2. Removes achievements if still too long
3. Hides older work experiences progressively
4. Maintains professional layout throughout

### How to Trigger
```javascript
// From Home page or Preview CV
fetch(`/profile/${person_id}/pdf/${profile_name}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ one_page: true })
});
```

## Managing Record Visibility

### Active Flag
- **Location**: Work Experience form, Advanced Training form
- **Field Name**: `active` (checkbox)
- **Default**: `True` for new records
- **Purpose**: Controls inclusion in One-Page PDF

**To include in One-Page PDF**: Set `active=True`  
**To exclude from One-Page PDF (but keep in Export PDF)**: Set `active=False`

### Historical Flag
- **Location**: Work Experience form (Classification & Status section)
- **Field Name**: `is_historical` (checkbox)
- **Default**: `False` for new records
- **Purpose**: Preserves records for historical reference but excludes from CVs by default

**To preserve but exclude from both PDFs**: Set `is_historical=True`

### Profile Visibility Flags
Each record has three independent visibility toggles:
- `visible_qa_analyst`
- `visible_qa_engineer`
- `visible_data_scientist`

Records must be visible for the selected profile to appear in either PDF mode.

## Implementation Details

### Backend Changes

#### `app/routes/profiles.py`

**Function: `get_profile_data_dict()`**
```python
def get_profile_data_dict(person_id, profile_name, include_inactive=False):
    """
    Args:
        include_inactive: If True, include ALL records regardless of active/is_historical
    """
    # Export PDF: include_inactive=True → query ALL records
    # One-Page PDF: include_inactive=False → query only active, non-historical
```

**Route: `generate_pdf()`**
```python
# Determine export mode from request parameter
one_page = data.get('one_page', False)
include_inactive = not one_page  # Export PDF includes all, One-Page PDF filters

profile_data = get_profile_data_dict(person_id, profile_name, include_inactive=include_inactive)
```

#### Query Filtering Logic

**Export PDF Mode (`include_inactive=True`)**:
```python
exp_models = [
    exp for exp in WorkExperience.query.all()
    if exp.is_visible_for_profile(profile_name)
]
```

**One-Page PDF Mode (`include_inactive=False`)**:
```python
exp_models = [
    exp for exp in WorkExperience.query.filter_by(active=True).all()
    if exp.is_visible_for_profile(profile_name) and not exp.is_historical
]
```

### Frontend Changes

#### `app/templates/index.html`

**Export PDF Button**:
```javascript
function generatePDF(personId, profileName) {
    fetch(`/profile/${personId}/pdf/${profileName}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ one_page: false })  // Include all records
    });
}
```

**One-Page PDF Button**:
```javascript
function generateOnepagePDF(personId, profileName) {
    fetch(`/profile/${personId}/pdf/${profileName}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ one_page: true })  // Filter to active only
    });
}
```

#### `app/templates/forms/experience_form.html`

**Active Field**:
```html
<div class="col-md-4 mb-3">
    <label class="form-label">Record Status</label>
    <div class="form-check">
        <input class="form-check-input" type="checkbox" id="activeRecord" name="active" 
               {{ 'checked' if experience is none or experience.active else '' }}>
        <label class="form-check-label" for="activeRecord">
            <strong>Active</strong> (included in One-Page PDF)
        </label>
    </div>
    <small class="form-text text-muted">Unchecked records appear only in Export PDF</small>
</div>
```

**JavaScript Checkbox Handling**:
```javascript
['show_responsibilities_summary', 'show_responsibilities_detailed', 'show_achievements',
 'visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 'is_historical', 'active']
.forEach(field => {
    const checkbox = document.querySelector(`input[name="${field}"]`);
    data[field] = checkbox ? checkbox.checked : false;
});
```

## Database Schema Reference

### BaseModel Fields (All Models Inherit)
```python
id = db.Column(db.Integer, primary_key=True)
active = db.Column(db.Boolean, default=True, nullable=False)
is_historical = db.Column(db.Boolean, default=False, nullable=False)
created_at = db.Column(db.DateTime, default=datetime.utcnow)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### ProfileVisibilityMixin Fields
```python
visible_qa_analyst = db.Column(db.Boolean, default=False, nullable=False)
visible_qa_engineer = db.Column(db.Boolean, default=False, nullable=False)
visible_data_scientist = db.Column(db.Boolean, default=False, nullable=False)
```

### WorkExperience Specific Fields
```python
time_block = db.Column(db.String(50))  # e.g., '2021-2025', '2015-2020', '1985-2009'
show_responsibilities_summary = db.Column(db.Boolean, default=True)
show_responsibilities_detailed = db.Column(db.Boolean, default=False)
show_achievements = db.Column(db.Boolean, default=True)
```

## Usage Examples

### Scenario 1: Recent Job (Active, Show in Both PDFs)
```python
work_exp = WorkExperience(
    active=True,           # ✅ Appears in One-Page PDF
    is_historical=False,   # ✅ Appears in both PDFs
    visible_qa_analyst=True,
    # ... other fields
)
```

### Scenario 2: Old Job (Archive Only, Export PDF Only)
```python
work_exp = WorkExperience(
    active=False,          # ❌ Excluded from One-Page PDF
    is_historical=False,   # ✅ Appears in Export PDF
    visible_qa_analyst=True,
    # ... other fields
)
```

### Scenario 3: Historical Record (Hidden from CVs)
```python
work_exp = WorkExperience(
    active=False,
    is_historical=True,    # ❌ Excluded from both PDFs by default
    visible_qa_analyst=True,
    # ... other fields
)
```

## Testing Checklist

### Export PDF
- [ ] Generates multi-page PDF when database has many records
- [ ] Includes records with `active=False`
- [ ] Includes records with `is_historical=True`
- [ ] Shows all Work Experience, Education, Advanced Training
- [ ] Respects profile visibility flags
- [ ] Contact information sorted by international priority

### One-Page PDF
- [ ] Generates approximately 1-page PDF
- [ ] Excludes records with `active=False`
- [ ] Excludes records with `is_historical=True`
- [ ] Shows only active, non-historical records
- [ ] Auto-trims content to fit space
- [ ] Respects profile visibility flags
- [ ] Contact information sorted by international priority

### Form Functionality
- [ ] Active checkbox visible and functional in Work Experience form
- [ ] Active field defaults to `True` for new records
- [ ] Active field persists correctly on save
- [ ] Historical checkbox works independently
- [ ] Form validation passes with both flags

## Migration Notes

No database migration required - `active` and `is_historical` fields already exist in `BaseModel`.

Existing records default to:
- `active=True` (included in both PDFs)
- `is_historical=False` (not hidden)

## Current Database State (Jan 2026)

**Work Experience**: 12 records (all active=True, is_historical=False)
**Advanced Training**: 10 records
  - 8 active (active=True)
  - 2 inactive (active=False): #2 English B1, #4 English B2

All records currently visible in all three profiles (QA Analyst, QA Engineer, Data Scientist).

## Contact Sorting Priority

Both PDF modes sort contact information by international priority:
1. Email
2. LinkedIn
3. GitHub  
4. CV URL
5. Phone

This ensures the most globally relevant contact methods appear first for international job applications.

---

**Version**: 2025.1  
**Last Updated**: January 10, 2026  
**Related Files**: 
- `app/routes/profiles.py`
- `app/templates/index.html`
- `app/templates/forms/experience_form.html`
- `app/services/pdf_generator.py`
