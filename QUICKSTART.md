# CV Builder - Quick Start Guide
**Version 2025** | Built with Flask, SQLAlchemy, Bootstrap 5

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)

### Installation

```bash
# 1. Clone/navigate to project
cd c:\Users\vbj20\proyectos\ProjectsPy\app-cv-jvb19

# 2. Create/activate virtual environment
python -m venv venv311
.\venv311\Scripts\Activate.ps1  # Windows
source venv311/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database (if needed)
python init_db.py

# 5. Run the application
python run.py
```

The app will start at **http://localhost:5000**

---

## 📚 Data Entry Menu

### Main Menu Structure
**Data Entry** dropdown contains:
- ✅ **Personal Info** - Name, contact details, professional titles
- ✅ **Work Experience** - Jobs with descriptions and achievements
- ✅ **Technical Tools** - Skills categorized per profile
- ✅ **Education** - Degrees and certifications
- ✅ **Advanced Training & Certifications** - Unified courses & certifications
- ✅ **Languages** - Language proficiency with CEFR levels

### Quick Links
- **Admin** - Database view and management tools
- **Profiles** - View generated CVs for different profiles

---

## 📝 Quick Data Entry Workflow

### 1. Personal Information (`/forms/person`)
```
✓ First Name: Javier
✓ Last Name: Villarreal Bencomo
✓ Professional Title: QA Professional
✓ Contact visibility toggles (Email, Phone, LinkedIn, GitHub)
✓ Profile-specific titles (QA Analyst, QA Engineer, Data Scientist)
✓ Professional Reference (Name, Company, Phone)
```

### 2. Work Experience (`/forms/experience`)
```
✓ Job Title & Company
✓ Start/End Dates (uses date pickers)
✓ Location
✓ Responsibilities (3 types):
  - Summary (one-liner)
  - Detailed (bullet points)
  - Achievements (key wins)
✓ Content Level buttons (None/Minimal/Summary/Detailed/Complete)
✓ Profile visibility (QA Analyst, QA Engineer, Data Scientist)
```

**Content Level Examples:**
- **Summary**: "Led QA for microservices platform"
- **Detailed**: Summary + 5 bullet points of responsibilities
- **Complete**: All + key achievements with metrics

### 3. Technical Tools (`/forms/tool`)
```
✓ Tool Name (e.g., Selenium, Python, Docker)
✓ Proficiency Level (Beginner/Intermediate/Advanced/Expert)
✓ Years of Experience
✓ Profile-specific configuration:
  - QA Analyst: Yes/No + 5 subcategories
  - QA Engineer: Yes/No + 5 subcategories
  - Data Scientist: Yes/No + 2 subcategories
```

### 4. Education (`/forms/education`)
```
✓ Degree (e.g., Bachelor of Science)
✓ Institution
✓ Country
✓ Year Obtained / Start/End Years
✓ Details (GPA, honors, thesis)
✓ Display Order (sort position)
✓ Document URL
```

### 5. Advanced Training & Certifications (`/forms/advanced-training`) ✅ NEW
```
✓ Type: Course or Certification (required)
✓ Name/Title
✓ Provider/Organization
✓ Completion Date
✓ Description

IF COURSE:
  ✓ Duration (hours)

IF CERTIFICATION:
  ✓ Expiration Date
  ✓ Credential ID
  ✓ Credential URL

✓ Display Order (1-6 for unified section)
✓ Profile visibility
```

### 6. Languages (`/forms/language`)
```
✓ Language Name
✓ Conversation Level (CEFR: A1-C2 or Native)
✓ Reading Level
✓ Writing Level
✓ Optional Certification:
  - Name (e.g., TOEFL, IELTS)
  - Score
  - Date
✓ Display Order
```

---

## 👥 Profiles

### Available Profiles
1. **QA Analyst** - Manual testing, methodologies
2. **QA Engineer** - Automation, engineering practices
3. **Data Scientist** - Analytics, ML, data pipelines

### How Profiles Work
- Each data entry has **profile visibility toggles**
- Same data → different CVs per profile
- Profile selector in forms applies preset visibility

### Viewing Profiles
```
/profiles/qa_analyst    - QA Analyst CV
/profiles/qa_engineer   - QA Engineer CV
/profiles/data_scientist - Data Scientist CV
```

---

## 🎯 Key Features

### Granular Visibility Control
✅ **Person**: Individual toggles for each contact (email, phone, LinkedIn, etc.)
✅ **Experience**: Three-level content visibility (summary/detailed/achievements)
✅ **Tools**: Profile-specific usability and subcategories
✅ **All**: Profile-specific visibility (visible to QA Analyst? Engineer? Scientist?)

### Display Ordering
✅ **Education**: display_order field
✅ **Advanced Training**: display_order 1-6 (unified for courses & certifications)
✅ **Tools**: display_order within each subcategory
✅ **Languages**: display_order

### Professional References
✅ Name, Company, Phone stored in Person model

### Time Block Organization
✅ **WorkExperience**: Grouped by time periods (2021-2025, 2015-2020, 1985-2009)

---

## 📊 Admin Features

### Database View
Navigate to **Admin** → scroll down to **Database Viewer**

Shows all table contents:
- Person (1 record)
- WorkExperience (multiple)
- TechnicalTool (multiple)
- Education (multiple)
- AdvancedTraining (multiple) ✅ NEW
- Language (multiple)
- ITProduct (multiple)

### Hidden Admin Routes
(For direct database manipulation)
- `/admin/database/consulta` - View all tables
- `/admin/update/advanced-training` - Batch update Advanced Training records
- `/admin/update/education-order` - Update education display_order
- `/admin/update/tool-order` - Update tool display_order
- And more...

---

## 🔄 API Usage

### REST Endpoints

#### Personal Information
```
GET  /api/person           - Get person record
POST /api/person           - Create/update person
```

#### Work Experience
```
GET    /api/work-experience       - List all
POST   /api/work-experience       - Create new
GET    /api/work-experience/<id>  - Get specific
PUT    /api/work-experience/<id>  - Update
DELETE /api/work-experience/<id>  - Delete
```

#### Technical Tools
```
GET    /api/tool            - List all
POST   /api/tool            - Create new
PUT    /api/tool/<id>       - Update
DELETE /api/tool/<id>       - Delete
```

#### Education
```
GET    /api/education       - List all
POST   /api/education       - Create new
PUT    /api/education/<id>  - Update
DELETE /api/education/<id>  - Delete
```

#### Advanced Training (NEW)
```
GET    /api/advanced-training        - List all
POST   /api/advanced-training        - Create new
PUT    /api/advanced-training/<id>   - Update
DELETE /api/advanced-training/<id>   - Delete
```

#### Languages
```
GET    /api/language        - List all
POST   /api/language        - Create new
PUT    /api/language/<id>   - Update
DELETE /api/language/<id>   - Delete
```

### Example: Adding a Course
```bash
curl -X POST http://localhost:5000/api/advanced-training \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Course",
    "name": "Advanced Python",
    "provider": "Udemy",
    "completion_date": "2025-01-15",
    "description": "Learned async programming and design patterns",
    "duration_hours": 40,
    "display_order": 2,
    "visible_qa_analyst": false,
    "visible_qa_engineer": true,
    "visible_data_scientist": true
  }'
```

---

## 🎨 UI Navigation

### Home Page
```
http://localhost:5000/
- Profile cards with links to CVs
- Data entry shortcuts
- Features overview
```

### Data Entry Menu
```
Dropdown: "Data Entry"
├── Personal Info (/forms/person)
├── Work Experience (/forms/experience)
├── Technical Tools (/forms/tool)
├── Education (/forms/education)
├── Advanced Training & Certifications (/forms/advanced-training)
└── Languages (/forms/language)
```

### Admin Interface
```
http://localhost:5000/admin/
- Dashboard with statistics
- Database viewer
- Hidden management routes
```

---

## 📋 Common Tasks

### Add a New Work Experience
1. Click **Data Entry** → **Work Experience**
2. Fill in job details
3. Write responsibilities (summary + detailed)
4. Write achievements
5. Set content level using buttons
6. Select visible profiles
7. Click **Save Experience**

### Add a Course
1. Click **Data Entry** → **Advanced Training & Certifications**
2. Select type: **Course**
3. Enter name, provider, dates
4. Enter duration in hours
5. Set display order (1-6)
6. Click **Save**

### Add a Certification
1. Click **Data Entry** → **Advanced Training & Certifications**
2. Select type: **Certification**
3. Enter name, provider, dates
4. Enter credential info (ID, URL)
5. Set display order (1-6)
6. Click **Save**

### View QA Engineer Profile
1. Go to **Profiles** → **QA Engineer**
   Or directly: http://localhost:5000/profiles/qa_engineer
2. See CV with:
   - Only QA Engineer-visible items
   - Proper content levels
   - Correct tool categories
   - Professional title for QA Engineer

### Hide Contact Information
1. Go to **Data Entry** → **Personal Info**
2. Toggle visibility switches for:
   - Email
   - Phone
   - LinkedIn
   - GitHub
   - Personal Website
3. Preview updates in real-time
4. Click **Save Changes**

---

## 🐛 Troubleshooting

### Form Not Saving?
- Check browser console for JavaScript errors
- Verify required fields are filled (marked with *)
- Try refreshing the page

### API Returns 400 Error?
- Check JSON format is valid
- Ensure all required fields are present
- Verify field types (dates as YYYY-MM-DD, booleans as true/false)

### Data Not Appearing in Profile?
- Check visibility toggles are enabled
- Ensure record is marked `active=True`
- Verify profile selector matches
- Check `is_historical` flag (if True, only shown in admin view)

### Database Issues?
- Check `/admin/database/consulta` to view all tables
- Use hidden routes for direct updates if needed
- Don't delete records; mark `active=False` instead

---

## 📚 Related Documentation

- **ARCHITECTURE_V2.md** - System design & data models
- **FORMS_IMPLEMENTATION.md** - Form details
- **CHANGELOG_ADVANCED_TRAINING.md** - Recent changes
- **PROFILE_PRESETS.md** - Preset system documentation

---

## 💡 Tips & Tricks

✅ **Display Order Matters**: Lower numbers appear first
✅ **Content Levels Save Time**: Use buttons instead of individual toggles
✅ **Profile Selector Helps**: Apply presets for quick setup
✅ **Live Preview**: Watch changes update in real-time
✅ **Historical Flag**: Mark old items as historical to hide them
✅ **Time Blocks**: Organize experiences by decade for clarity

---

## 🎓 Example Data

### Sample Person
```
Name: Javier Villarreal Bencomo
QA Analyst Title: Senior QA Analyst
QA Engineer Title: Senior QA Engineer
Data Scientist Title: Senior Data Scientist
Email: javier@example.com (visible)
Phone: +56-9-1234-5678 (hidden)
LinkedIn: linkedin.com/in/jvillarrealbencomo (visible)
Reference: John Smith at TechCorp (123) 456-7890
```

### Sample Experience
```
Job Title: Senior QA Engineer
Company: TechCorp
Period: 2021-2025 (current)
Summary: Lead QA automation for cloud platform
Detailed: 5 bullet points about responsibilities
Achievements: Reduced release time by 40%, improved coverage to 95%
Content Level: Detailed (show summary + detailed + achievements)
Visible to: QA Engineer, QA Analyst
```

### Sample Tool
```
Name: Selenium WebDriver
Proficiency: Expert
Years: 8

QA Analyst:
  ✓ Visible in: Test Automation

QA Engineer:
  ✓ Visible in: Test Automation

Data Scientist:
  ✗ Not visible
```

---

## 🚀 Next Steps

1. **Enter your data** - Start with Personal Info
2. **Add experiences** - Include all relevant jobs
3. **Configure tools** - Mark what's relevant per profile
4. **View profiles** - Check how different CVs look
5. **Fine-tune visibility** - Adjust toggles for each profile
6. **Generate PDF** - (feature in progress)

---

## 📞 Support & Questions

For issues or questions:
1. Check the **Admin** interface for data integrity
2. Review **ARCHITECTURE_V2.md** for system design
3. Check **FORMS_IMPLEMENTATION.md** for form-specific help
4. Review **CHANGELOG_ADVANCED_TRAINING.md** for recent changes

---

**Last Updated:** December 2025
**Version:** 2025.1
**Author:** Javier Villarreal Bencomo
