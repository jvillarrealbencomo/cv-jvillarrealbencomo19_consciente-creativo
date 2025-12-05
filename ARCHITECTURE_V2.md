# Enhanced CV Application Architecture - Version 2025
## Granular Visibility Control & Profile-Specific Configuration

This document explains the updated architecture that fully addresses the granular visibility requirements and profile-specific configurations.

---

## 🎯 Key Improvements Over Previous Version

### 1. **Person Model - Per-Field Contact Visibility**
Each contact field now has its **own independent visibility flag**:

```python
# Old approach (WRONG):
show_link = "all"  # One flag for everything

# New approach (CORRECT):
show_email = True
show_phone = False
show_linkedin = True
show_github = True
show_personal_url = False
```

**Benefits:**
- Granular control: Show LinkedIn but hide phone
- Profile-specific contact strategies
- Historical data preservation (email stored but not shown)

---

### 2. **TechnicalTool Model - Profile-Specific Subcategories**

Each tool is configured **independently per profile** with different subcategories:

#### Data Scientist Subcategories:
- Engineering & Big Data
- Modeling & Core Programming

#### QA Engineer/Analyst Subcategories:
- Operating Systems & Cloud
- Quality Engineering & CI/CD
- Test Automation
- Databases
- Programming Languages

```python
# Example: Python tool configuration
tool = TechnicalTool(name="Python")

# Data Scientist: Core programming
tool.usable_data_scientist = True
tool.subcategory_data_scientist = "Modeling & Core Programming"

# QA Engineer: Programming language
tool.usable_qa_engineer = True
tool.subcategory_qa_engineer = "Programming Languages"

# QA Analyst: Not shown
tool.usable_qa_analyst = False
```

**Benefits:**
- Same tool appears in different categories per profile
- Historical tools (BASIC, FORTRAN) stored but not marked as usable
- Flexible categorization per career focus

---

### 3. **WorkExperience Model - Three-Level Content Visibility**

Each experience record has **three independent visibility flags**:

1. **responsibilities_summary**: Brief one-liner
2. **responsibilities_detailed**: Comprehensive bullet points
3. **achievements**: Key highlights/results

```python
# Example: Senior position
experience.show_responsibilities_summary = True   # Always show job title
experience.show_responsibilities_detailed = True  # Full details
experience.show_achievements = True               # Key wins

# Example: Old position (space-saving)
old_job.show_responsibilities_summary = True      # Title only
old_job.show_responsibilities_detailed = False    # Skip details
old_job.show_achievements = False                 # Skip achievements
```

**Content Levels** (convenience method):
- `none`: Hide everything
- `minimal`: Summary only
- `summary`: Summary + achievements
- `detailed`: Summary + detailed responsibilities
- `complete`: Everything

**Benefits:**
- Fine-grained control for PDF space management
- Historical preservation (old jobs stored with full detail, shown minimally)
- Easy adjustment: toggle from "complete" to "summary" to fit one page

---

### 4. **Language Model - Three Skill Types**

Languages now track **three separate proficiency levels**:

```python
language = Language(
    name="English",
    level_conversation="C1",  # Advanced
    level_reading="C2",       # Fluent
    level_writing="B2"        # Upper-Intermediate
)
```

**Benefits:**
- Accurate skill representation
- Certification alignment (TOEFL, IELTS have separate scores)
- Professional honesty (conversation ≠ writing skill)

---

### 5. **Historical Data Preservation**

New `is_historical` flag on all models:

```python
# Old language kept for history but not shown in any CV
language = Language(
    name="BASIC",
    active=True,
    is_historical=True,  # Stored but not used
    visible_qa_analyst=False,
    visible_qa_engineer=False,
    visible_data_scientist=False
)
```

**The Version 2025 Menu** shows ALL data (including historical), while **PDF exports** filter based on visibility flags.

---

## 📊 Data Model Summary

### Person (1 record)
```python
- full_name
- professional_title (default)
- title_qa_analyst, title_qa_engineer, title_data_scientist
- email + show_email
- phone + show_phone
- linkedin_url + show_linkedin
- github_url + show_github
- personal_url + show_personal_url
- location
- summary_qa_analyst, summary_qa_engineer, summary_data_scientist
- profile_image_url
```

### WorkExperience (Many records)
```python
- job_title, company, location
- start_date, end_date, is_current
- time_block ("2021-2025", "2015-2020", "1985-2009")
- responsibilities_summary + show_responsibilities_summary
- responsibilities_detailed + show_responsibilities_detailed
- achievements + show_achievements
- technologies
- visible_qa_analyst, visible_qa_engineer, visible_data_scientist
- is_historical
```

### TechnicalTool (Many records)
```python
- name
- proficiency_level, years_experience
- usable_qa_analyst + subcategory_qa_analyst
- usable_qa_engineer + subcategory_qa_engineer
- usable_data_scientist + subcategory_data_scientist
- is_historical
```

### Language (Many records)
```python
- name
- level_conversation, level_reading, level_writing
- certification_name, certification_score, certification_date
- visible_qa_analyst, visible_qa_engineer, visible_data_scientist
- is_historical
```

### Education (Many records)
```python
- degree, institution, country
- year_obtained (or start_year/end_year)
- details
- document_url
- visible_qa_analyst, visible_qa_engineer, visible_data_scientist
- is_historical
```

### Certification (Many records)
```python
- name, issuing_organization
- issue_date, expiration_date
- credential_id, credential_url
- description, document_url
- visible_qa_analyst, visible_qa_engineer, visible_data_scientist
- is_historical
```

### Course (Many records)
```python
- name, provider
- completion_date, duration_hours
- description, skills_acquired
- credential_url, document_url
- visible_qa_analyst, visible_qa_engineer, visible_data_scientist
- is_historical
```

### ITProduct (Many records)
```python
- name, description, role
- technologies
- start_date, end_date, is_current
- project_url, github_url, demo_url
- impact_description
- visible_qa_analyst, visible_qa_engineer, visible_data_scientist
- is_historical
```

---

## 🎨 Profile Presets System

Each profile has a **preset template** that can be applied with one click:

### QA Analyst Preset
```python
- Work Experience: "summary" level (achievements-focused)
- TechnicalTools: Categorized as QA-specific
- Focus: Testing methodologies, manual/automated testing
```

### QA Engineer Preset
```python
- Work Experience: "complete" level (detailed technical work)
- TechnicalTools: Emphasize automation, CI/CD, programming
- Focus: Engineering practices, tool development
```

### Data Scientist Preset
```python
- Work Experience: "summary" level (results-focused)
- TechnicalTools: Categorized for data science (Engineering & Big Data, Modeling)
- Focus: Analytics, ML, data pipelines
```

### Applying Presets
```python
# In admin interface: "Apply QA Engineer Template" button
# This calls:
for experience in all_experiences:
    experience.apply_profile_preset('qa_engineer')
    # Sets visibility flags and content levels

for tool in all_tools:
    tool.apply_profile_preset('qa_engineer')
    # Sets usability and subcategory
```

---

## 🔄 Workflow Examples

### Example 1: Adding New Experience

```python
# User adds job in LinkedIn-style form
experience = WorkExperience(
    job_title="Senior QA Engineer",
    company="Tech Corp",
    start_date="2021-01-01",
    time_block="2021-2025",
    responsibilities_summary="Lead QA for cloud platform",
    responsibilities_detailed="• Designed test automation framework\n• Mentored 3 junior engineers\n• Implemented CI/CD pipelines",
    achievements="Reduced release cycle time by 40%, improved test coverage from 60% to 95%",
    
    # Initial visibility (user can adjust)
    show_responsibilities_summary=True,
    show_responsibilities_detailed=True,
    show_achievements=True,
    
    # Profile visibility (can use presets)
    visible_qa_analyst=True,
    visible_qa_engineer=True,
    visible_data_scientist=False
)
```

### Example 2: Historical Language

```python
# Old language from 1990s - kept for history
language = Language(
    name="FORTRAN",
    level_conversation="N/A",
    level_reading="Intermediate",
    level_writing="Basic",
    active=True,
    is_historical=True,  # Not shown in any CV
    visible_qa_analyst=False,
    visible_qa_engineer=False,
    visible_data_scientist=False
)

# Appears in "Version 2025 Menu" (full history)
# Does NOT appear in any PDF export
```

### Example 3: Profile-Specific Tool

```python
tool = TechnicalTool(
    name="Selenium WebDriver",
    proficiency_level="Expert",
    years_experience=8,
    
    # QA Analyst: Show in Test Automation
    usable_qa_analyst=True,
    subcategory_qa_analyst="Test Automation",
    
    # QA Engineer: Show in Test Automation
    usable_qa_engineer=True,
    subcategory_qa_engineer="Test Automation",
    
    # Data Scientist: Not relevant
    usable_data_scientist=False,
    subcategory_data_scientist=None
)
```

---

## 📏 One-Page PDF Strategy

### Automatic Content Reduction
When PDF exceeds one page, system applies rules in order:

1. **Level 1**: Switch all experiences from "complete" to "summary"
2. **Level 2**: Hide detailed responsibilities, keep achievements
3. **Level 3**: Show only summary for old time blocks (pre-2015)
4. **Level 4**: Reduce font size by 0.5pt
5. **Level 5**: Hide courses, keep certifications
6. **Level 6**: Hide old certifications (> 5 years)
7. **Level 7**: Truncate achievement text to 1 line

### Manual Control
User can also:
- Toggle individual visibility flags
- Adjust content level per experience
- Mark items as historical

---

## 🎯 Benefits of This Architecture

### 1. **Data Preservation**
- All career history stored
- Nothing deleted, only visibility toggled
- Easy to resurrect old items for specific applications

### 2. **Flexibility**
- Same data → multiple CV variants
- Easy profile switching
- Quick adjustments for specific job applications

### 3. **Maintainability**
- Clear separation of concerns
- Profile-specific logic encapsulated
- Easy to add new profiles

### 4. **User Control**
- Granular flags for fine-tuning
- Preset templates for quick start
- Live preview shows impact

### 5. **Professional Quality**
- Accurate skill representation (3-level languages)
- Context-appropriate categorization (tool subcategories)
- Space-efficient (3-level experience content)

---

## 🚀 Next Implementation Steps

1. ✅ Models created with granular visibility
2. ⏳ Create LinkedIn-style data entry forms
3. ⏳ Build profile preset system
4. ⏳ Implement dynamic preview with page warnings
5. ⏳ Enhance PDF generator with auto-trimming

---

This architecture now fully satisfies your requirements for granular control, profile-specific configuration, and historical data preservation!
