# Profile Preset System Documentation
**Version 2025 - Profile-Specific Configuration Management**

## Overview

The Profile Preset System provides a centralized way to manage profile-specific configurations across the CV application. It enables:

- **Three distinct CV profiles**: QA Analyst, QA Engineer, Data Scientist
- **Automatic visibility configuration** for all data models
- **Profile-specific categorization** of technical tools
- **Content-level management** for work experiences
- **Contact field granularity** for personal information

---

## Available Profiles

### 1. QA Analyst
- **Focus**: Manual testing, test planning, quality processes
- **Default Title**: "QA Analyst"
- **Tool Categories**:
  - Quality Engineering & CI/CD (priority)
  - Test Automation
  - Operating Systems & Cloud
  - Databases
  - Programming Languages
- **Experience Content Level**: Summary (medium detail)
- **Contact Visibility**: Email, Phone, LinkedIn, Personal URL (GitHub hidden)

### 2. QA Engineer
- **Focus**: Test automation, CI/CD integration, technical testing
- **Default Title**: "QA Engineer"
- **Tool Categories**:
  - Test Automation (priority)
  - Quality Engineering & CI/CD
  - Programming Languages
  - Operating Systems & Cloud
  - Databases
- **Experience Content Level**: Detailed (more technical detail)
- **Contact Visibility**: All fields visible (including GitHub)

### 3. Data Scientist
- **Focus**: Machine learning, statistical analysis, data engineering
- **Default Title**: "Data Scientist"
- **Tool Categories**:
  - Modeling & Core Programming (priority)
  - Engineering & Big Data
- **Experience Content Level**: Complete (full detail)
- **Contact Visibility**: Email, LinkedIn, GitHub, Personal URL (Phone hidden for professional distance)

---

## API Endpoints

### List All Profiles
```http
GET /api/presets/
```
Returns array of available profiles with basic information.

**Response:**
```json
{
  "profiles": [
    {
      "id": "qa_analyst",
      "name": "QA Analyst",
      "description": "Quality Assurance Analyst profile...",
      "default_title": "QA Analyst"
    }
  ],
  "count": 3
}
```

### Get Profile Details
```http
GET /api/presets/<profile_name>
```
Returns complete configuration for a specific profile.

**Response:**
```json
{
  "profile_name": "qa_engineer",
  "configuration": {
    "profile_info": {...},
    "person_contacts": {
      "show_email": true,
      "show_phone": true,
      "show_linkedin": true,
      "show_github": true,
      "show_personal_url": true
    },
    "experience_defaults": {
      "default_level": "detailed",
      "show_responsibilities_summary": true,
      "show_responsibilities_detailed": true,
      "show_achievements": true
    },
    "tool_categories": [...],
    "section_visibility": {...}
  }
}
```

### Get Tool Categories
```http
GET /api/presets/<profile_name>/tool-categories
```
Returns tool subcategories for a specific profile in priority order.

### Apply Profile Preset (Bulk)
```http
POST /api/presets/<profile_name>/apply
Content-Type: application/json

{
  "dry_run": false,
  "sections": ["work_experience", "technical_tools"]
}
```
Applies preset configuration to all records in the database.

**Dry Run**: Set `dry_run: true` to preview changes without applying.

### Apply Person Preset
```http
POST /api/presets/person/<person_id>/apply/<profile_name>
```
Applies contact visibility preset to a specific person record.

### Apply Experience Preset
```http
POST /api/presets/experience/<exp_id>/apply/<profile_name>
```
Applies content visibility preset to a specific work experience record.

### Apply Tool Preset
```http
POST /api/presets/tool/<tool_id>/apply/<profile_name>
Content-Type: application/json

{
  "subcategory": "Test Automation",
  "usable": true
}
```
Applies tool configuration to a specific technical tool record.

### Compare Profiles
```http
POST /api/presets/compare
Content-Type: application/json

{
  "profiles": ["qa_analyst", "qa_engineer", "data_scientist"]
}
```
Returns side-by-side comparison of multiple profiles.

---

## Python Service Usage

### Import the Service
```python
from app.services.profile_presets import ProfilePresetService
```

### Get Available Profiles
```python
profile_names = ProfilePresetService.get_profile_names()
# Returns: ['qa_analyst', 'qa_engineer', 'data_scientist']
```

### Get Profile Information
```python
info = ProfilePresetService.get_profile_info('qa_engineer')
# Returns: {'name': 'QA Engineer', 'description': '...', 'default_title': '...'}
```

### Apply Presets to Models

#### Person Model
```python
from app.models import Person

person = db.session.get(Person, person_id)
ProfilePresetService.apply_person_preset(person, 'qa_engineer')
db.session.commit()

# Check visible contacts
visible_contacts = person.get_visible_contacts()
# Returns: {'email': '...', 'phone': '...', 'linkedin': '...', 'github': '...'}
```

#### WorkExperience Model
```python
from app.models import WorkExperience

experience = db.session.get(WorkExperience, exp_id)
ProfilePresetService.apply_experience_preset(experience, 'data_scientist')
db.session.commit()

# Check content level
level = experience.get_content_level()
# Returns: 'complete'
```

#### TechnicalTool Model
```python
from app.models import TechnicalTool

tool = db.session.get(TechnicalTool, tool_id)
ProfilePresetService.apply_tool_preset(tool, 'qa_analyst', subcategory='Test Automation')
db.session.commit()

# Check configuration
is_usable = tool.is_usable_for_profile('qa_analyst')
subcategory = tool.get_subcategory_for_profile('qa_analyst')
```

#### Generic Model (with ProfileVisibilityMixin)
```python
from app.models import Certification

cert = db.session.get(Certification, cert_id)
ProfilePresetService.apply_model_preset(cert, 'qa_engineer', visible=True)
db.session.commit()

# Check visibility
is_visible = cert.is_visible_for_profile('qa_engineer')
```

### Bulk Apply Preset
```python
# Apply preset to all records in database
ProfilePresetService.apply_full_preset(db.session, 'qa_engineer')
# This applies the preset to all Person, WorkExperience, TechnicalTool,
# Education, Certification, Course, Language, and ITProduct records
```

### Get Tool Categories
```python
categories = ProfilePresetService.get_tool_categories('data_scientist')
# Returns: ['Modeling & Core Programming', 'Engineering & Big Data']
```

### Get Section Visibility
```python
visibility = ProfilePresetService.get_section_visibility('qa_analyst')
# Returns: {
#   'work_experience': True,
#   'certifications': True,
#   'courses': True,
#   'education': True,
#   'languages': True,
#   'technical_tools': True,
#   'it_products': False
# }
```

### Create Profile Summary
```python
summary = ProfilePresetService.create_profile_summary('qa_engineer')
# Returns comprehensive dictionary with all profile settings
```

---

## CLI Commands

### Initialize Database
```bash
flask init-db
```
Creates database tables and optionally adds sample data.

### Apply Profile Preset
```bash
flask apply-preset qa_engineer
```
Applies the specified profile preset to all records in the database.

### List Profiles
```bash
flask list-profiles
```
Displays all available profile presets with descriptions.

---

## Preset Configuration Details

### Person Contact Presets
Controls which contact fields are visible for each profile:
- `show_email`: Email address visibility
- `show_phone`: Phone number visibility
- `show_linkedin`: LinkedIn URL visibility
- `show_github`: GitHub URL visibility
- `show_personal_url`: Personal website visibility

### Experience Content Presets
Controls work experience detail level:
- **None**: All content hidden
- **Minimal**: Only basic info (title, company, dates)
- **Summary**: Basic info + responsibilities summary
- **Detailed**: Summary + detailed responsibilities
- **Complete**: All content including achievements

### Tool Category Presets
Each profile has distinct tool subcategories:
- **QA Profiles**: Operating Systems, Quality Engineering, Test Automation, Databases, Programming
- **Data Scientist**: Engineering & Big Data, Modeling & Core Programming

### Section Visibility Presets
Controls which model types appear in the CV:
- All profiles show: work_experience, certifications, courses, education, languages, technical_tools
- it_products: Hidden for qa_analyst, visible for qa_engineer and data_scientist

---

## Workflow Examples

### Creating a New Profile from Scratch
```python
# 1. Create person record
person = Person(
    first_name='John',
    last_name='Doe',
    email='john@example.com'
)
db.session.add(person)
db.session.commit()

# 2. Apply QA Engineer preset
ProfilePresetService.apply_person_preset(person, 'qa_engineer')
db.session.commit()

# Result: All contacts visible, title set to "QA Engineer"
```

### Switching Between Profiles
```python
# Apply Data Scientist preset to existing person
ProfilePresetService.apply_person_preset(person, 'data_scientist')

# Apply to all work experiences
for exp in person.work_experiences:
    ProfilePresetService.apply_experience_preset(exp, 'data_scientist')

# Apply to all tools
for tool in TechnicalTool.query.all():
    ProfilePresetService.apply_tool_preset(tool, 'data_scientist')

db.session.commit()
```

### Customizing After Preset Application
```python
# Apply preset first
ProfilePresetService.apply_person_preset(person, 'qa_analyst')

# Then customize
person.show_github = True  # Override preset to show GitHub
person.title_qa_analyst = 'Senior QA Analyst'  # Custom title

db.session.commit()
```

### Preview Before Applying
```python
# Get preset configuration without applying
summary = ProfilePresetService.create_profile_summary('qa_engineer')

# Review settings
print(summary['person_contacts'])
print(summary['experience_defaults'])
print(summary['tool_categories'])

# Apply if satisfied
ProfilePresetService.apply_full_preset(db.session, 'qa_engineer')
```

---

## Integration with Models

All presets work seamlessly with the model methods:

```python
# Person model integration
person.get_visible_contacts()  # Returns only contacts with show_* = True
person.get_title_for_profile('qa_engineer')  # Returns profile-specific title
person.get_summary_for_profile('qa_engineer')  # Returns profile-specific summary

# WorkExperience model integration
exp.get_content_level()  # Returns current visibility level
exp.set_content_level('summary')  # Sets all visibility flags
exp.get_visible_content()  # Returns dict of visible content sections

# TechnicalTool model integration
tool.is_usable_for_profile('qa_analyst')  # Check if tool is marked usable
tool.get_subcategory_for_profile('qa_analyst')  # Get assigned subcategory
TechnicalTool.get_tools_by_profile_and_subcategory('qa_analyst')  # Grouped dict

# Generic visibility check (all models with ProfileVisibilityMixin)
model.is_visible_for_profile('data_scientist')
```

---

## Best Practices

1. **Apply presets before customization**: Start with a preset, then fine-tune individual records
2. **Use dry_run for bulk operations**: Preview changes before applying to all records
3. **Maintain profile consistency**: When switching profiles, apply the preset to all related models
4. **Preserve historical data**: Use `is_historical` flag to keep old data without showing it
5. **Test preset changes**: Use the compare endpoint to understand differences between profiles
6. **Document custom configurations**: If you override preset values, document why

---

## Future Enhancements

- User-defined custom profiles
- Profile versioning and history
- Preset templates export/import
- A/B testing different profile configurations
- Analytics on which profile configurations generate better results
