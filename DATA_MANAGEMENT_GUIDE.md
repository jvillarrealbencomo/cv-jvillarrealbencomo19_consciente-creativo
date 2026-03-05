# Data Management Guide - CV Builder App

## Quick Summary
✅ **All CRUD operations are fully implemented** - Edit, Add, and Delete records through the app UI or API

---

## 1. EDIT EXISTING RECORDS

### Option A: Form-Based (Easiest)
Access the form directly in your browser:
- **Edit Person**: `http://localhost:5000/forms/person?person_id=1`
- **Edit TechnicalTool**: `http://localhost:5000/forms/tool?tool_id=<id>`

### Option B: API-Based (Programmatic)
```bash
# Update a TechnicalTool field
curl -X PUT http://localhost:5000/api/tool/1 \
  -H "Content-Type: application/json" \
  -d '{"usable_qa_analyst": true}'

# Update Person fields
curl -X PUT http://localhost:5000/api/person/1 \
  -H "Content-Type: application/json" \
  -d '{
    "show_github": true,
    "personal_url": "https://mi_portafolio",
    "show_personal_url": true
  }'
```

### Fields Currently Editable via Form:

**TechnicalTool:**
- ✅ `name` - Tool/Technology name
- ✅ `category` - Category/subcategory
- ✅ `provider` - Provider/vendor
- ✅ `description` - Tool description
- ✅ `proficiency_level` - Beginner/Intermediate/Advanced/Expert
- ✅ `usable_qa_analyst` - Toggle for QA Analyst profile
- ✅ `usable_qa_engineer` - Toggle for QA Engineer profile
- ✅ `usable_data_scientist` - Toggle for Data Scientist profile
- ✅ `subcategory_qa_analyst`, `subcategory_qa_engineer`, `subcategory_data_scientist` - Profile-specific categories

**Person:**
- ✅ `full_name`, `first_name`, `last_name`
- ✅ `professional_title` - Primary title
- ✅ `title_qa_analyst`, `title_qa_engineer`, `title_data_scientist` - Profile-specific titles
- ✅ `email` - Email address
- ✅ `show_email` - Show/hide email
- ✅ `phone` - Phone number
- ✅ `show_phone` - Show/hide phone
- ✅ `linkedin_url` - LinkedIn profile
- ✅ `show_linkedin` - Show/hide LinkedIn
- ✅ `github_url` - GitHub profile
- ✅ `show_github` - Show/hide GitHub ⭐ **YOU NEED THIS**
- ✅ `personal_url` - Portfolio/personal website ⭐ **YOU NEED THIS**
- ✅ `show_personal_url` - Show/hide portfolio ⭐ **YOU NEED THIS**
- ✅ `location` - Location/city
- ✅ `summary_qa_analyst`, `summary_qa_engineer`, `summary_data_scientist` - Profile summaries
- ✅ `reference_name`, `reference_company`, `reference_phone` - Reference contact

---

## 2. ADD NEW RECORDS

### Option A: Form-Based (Easiest)
Access the form for new records (no ID parameter):
- **Add TechnicalTool**: `http://localhost:5000/forms/tool`
- **Add Education**: `http://localhost:5000/forms/education`
- **Add Work Experience**: `http://localhost:5000/forms/experience`
- **Add Language**: `http://localhost:5000/forms/language`
- **Add Advanced Training**: `http://localhost:5000/forms/advanced_training`

### Option B: API-Based (Programmatic)
```bash
# Add new TechnicalTool
curl -X POST http://localhost:5000/api/tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cypress",
    "category": "Test Automation",
    "provider": "Cypress.io",
    "usable_qa_analyst": true,
    "usable_qa_engineer": true,
    "proficiency_level": "advanced"
  }'

# Add new Education
curl -X POST http://localhost:5000/api/education \
  -H "Content-Type: application/json" \
  -d '{
    "degree": "Bachelor of Science",
    "institution": "State University",
    "country": "USA",
    "year_obtained": 2015
  }'
```

---

## 3. DELETE RECORDS

### API-Based (Soft Delete)
Deleting a record sets `active = False` - it's hidden but retained in the database.

```bash
# Delete a TechnicalTool
curl -X DELETE http://localhost:5000/api/tool/1

# Delete a Person record (if needed)
curl -X DELETE http://localhost:5000/api/person/1

# Delete Education, WorkExperience, Language, etc.
curl -X DELETE http://localhost:5000/api/education/<id>
curl -X DELETE http://localhost:5000/api/experience/<id>
curl -X DELETE http://localhost:5000/api/language/<id>
curl -X DELETE http://localhost:5000/api/advanced_training/<id>
```

---

## 4. YOUR SPECIFIC NEEDS - HOW TO DO THEM

### ✅ Change TechnicalTool.usable_qa_analyst
**Via Form:**
1. Go to: `http://localhost:5000/forms/tool?tool_id=<id>`
2. Find the "QA Analyst Profile" section
3. Check/uncheck the "QA Analyst Profile" checkbox
4. Click Save

**Via API:**
```bash
curl -X PUT http://localhost:5000/api/tool/<id> \
  -H "Content-Type: application/json" \
  -d '{"usable_qa_analyst": true}'
```

---

### ✅ Change Person.show_github, personal_url, show_personal_url
**Via Form:**
1. Go to: `http://localhost:5000/forms/person?person_id=1`
2. Scroll to "Online Presence" section
3. Check/uncheck "Show GitHub URL" checkbox
4. Enter portfolio URL in "Personal Portfolio URL" field
5. Check/uncheck "Show Personal URL" checkbox
6. Click Save

**Via API:**
```bash
curl -X PUT http://localhost:5000/api/person/1 \
  -H "Content-Type: application/json" \
  -d '{
    "show_github": true,
    "personal_url": "https://mi_portafolio",
    "show_personal_url": true
  }'
```

---

### ✅ Add New TechnicalTool for Specific Profiles
**Via Form:**
1. Go to: `http://localhost:5000/forms/tool` (no ID parameter)
2. Fill in tool information (name, category, provider, etc.)
3. In "Profile-Specific Settings" section, check only the profiles you want (e.g., QA Analyst)
4. Click Save

**Via API:**
```bash
curl -X POST http://localhost:5000/api/tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Tool Name",
    "category": "Testing",
    "provider": "Tool Provider",
    "usable_qa_analyst": true,
    "usable_qa_engineer": false,
    "usable_data_scientist": false
  }'
```

---

### ✅ Delete Records
**Via API (soft delete):**
```bash
curl -X DELETE http://localhost:5000/api/tool/<id>
curl -X DELETE http://localhost:5000/api/person/<id>
```

---

## 5. AVAILABLE ENDPOINTS

### Person
- `GET /api/person` - List all persons
- `POST /api/person` - Create new person
- `GET /api/person/<id>` - Get person details
- `PUT /api/person/<id>` - Update person
- `DELETE /api/person/<id>` - Delete person

### TechnicalTool
- `GET /api/tool` - List all tools
- `POST /api/tool` - Create new tool
- `GET /api/tool/<id>` - Get tool details
- `PUT /api/tool/<id>` - Update tool
- `DELETE /api/tool/<id>` - Delete tool

### Other Models (Education, Language, WorkExperience, AdvancedTraining)
- Same pattern as above: `/api/education`, `/api/language`, `/api/experience`, `/api/advanced_training`

---

## 6. NOTES

- **Boolean fields** in API requests accept: `true`, `false`, `"true"`, `"false"`, `"1"`, `"0"`, `"yes"`, `"no"`
- **Soft deletes** only hide records (set `active=False`) - use database directly if hard delete is needed
- **All form endpoints** support both create (GET with no ID) and edit (GET with ID) operations
- **Forms are already built** - all fields you need are already implemented and editable

---

## 7. QUICK REFERENCE - YOUR IMMEDIATE NEEDS

| Task | URL/Command |
|------|------------|
| Edit TechnicalTool #1 usable_qa_analyst | `http://localhost:5000/forms/tool?tool_id=1` |
| Edit Person #1 github/portfolio settings | `http://localhost:5000/forms/person?person_id=1` |
| Add new TechnicalTool | `http://localhost:5000/forms/tool` |
| Delete TechnicalTool #1 | `DELETE /api/tool/1` |
| API update tool | `PUT /api/tool/<id>` with JSON body |
| API update person | `PUT /api/person/1` with JSON body |

Everything is ready to use! 🎯
