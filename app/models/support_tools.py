"""
Technical Tool Model with Profile-Specific Subcategories
Version 2025 - Different subcategories per profile with usability flags
"""
from sqlalchemy import func
from app import db
from app.models.base import BaseModel


class TechnicalTool(BaseModel):
    """
    Technical skills with profile-specific categorization
    
    Subcategories by Profile:
    - Data Scientist: 'Engineering & Big Data', 'Modeling & Core Programming'
    - QA Engineer/Analyst: 'Operating Systems & Cloud', 'Quality Engineering & CI/CD', 
                           'Test Automation', 'Databases', 'Programming Languages'
    
    Each tool has:
    - Per-profile usability flags
    - Per-profile subcategory assignment
    - Global visibility control
    """
    __tablename__ = 'technical_tools'
    
    # Tool identification
    name = db.Column(db.String(200), nullable=False)
    
    # Proficiency level (general)
    proficiency_level = db.Column(db.String(50), comment="Expert, Advanced, Intermediate, Basic")
    years_experience = db.Column(db.Float)
    
    # Description/Notes
    description = db.Column(db.Text)
    
    # === QA Analyst Configuration ===
    usable_qa_analyst = db.Column(db.Boolean, default=False, nullable=False)
    subcategory_qa_analyst = db.Column(db.String(100), comment="Operating Systems & Cloud, Quality Engineering & CI/CD, Test Automation, Databases, Programming Languages")
    
    # === QA Engineer Configuration ===
    usable_qa_engineer = db.Column(db.Boolean, default=False, nullable=False)
    subcategory_qa_engineer = db.Column(db.String(100), comment="Operating Systems & Cloud, Quality Engineering & CI/CD, Test Automation, Databases, Programming Languages")
    
    # === Data Scientist Configuration ===
    usable_data_scientist = db.Column(db.Boolean, default=False, nullable=False)
    subcategory_data_scientist = db.Column(db.String(100), comment="Engineering & Big Data, Modeling & Core Programming")
    
    # Display order within subcategory
    display_order = db.Column(db.Integer, default=0)
    
    # Valid subcategories per profile
    SUBCATEGORIES = {
        'qa_analyst': [
            'Operating Systems & Cloud',
            'Quality Engineering & CI/CD',
            'Test Automation',
            'Databases',
            'Programming Languages'
        ],
        'qa_engineer': [
            'Operating Systems & Cloud',
            'Quality Engineering & CI/CD',
            'Test Automation',
            'Databases',
            'Programming Languages'
        ],
        'data_scientist': [
            'Modeling & Data Science',
            'Data Engineering & Development',
            'Data Platforms',
            'QA & CI/CD'
        ]
    }
    
    def is_usable_for_profile(self, profile_name):
        """Check if tool is marked as usable for specific profile"""
        usability_map = {
            'qa_analyst': self.usable_qa_analyst,
            'qa_engineer': self.usable_qa_engineer,
            'data_scientist': self.usable_data_scientist
        }
        return usability_map.get(profile_name, False)
    
    def get_subcategory_for_profile(self, profile_name):
        """Get subcategory assignment for specific profile"""
        subcategory_map = {
            'qa_analyst': self.subcategory_qa_analyst,
            'qa_engineer': self.subcategory_qa_engineer,
            'data_scientist': self.subcategory_data_scientist
        }
        return subcategory_map.get(profile_name)
    
    def set_profile_config(self, profile_name, usable, subcategory):
        """Set usability and subcategory for specific profile"""
        if profile_name == 'qa_analyst':
            self.usable_qa_analyst = usable
            self.subcategory_qa_analyst = subcategory
        elif profile_name == 'qa_engineer':
            self.usable_qa_engineer = usable
            self.subcategory_qa_engineer = subcategory
        elif profile_name == 'data_scientist':
            self.usable_data_scientist = usable
            self.subcategory_data_scientist = subcategory
    
    @classmethod
    def get_valid_subcategories(cls, profile_name):
        """Get list of valid subcategories for a profile"""
        return cls.SUBCATEGORIES.get(profile_name, [])
    
    @classmethod
    def get_tools_by_profile_and_subcategory(cls, profile_name):
        """
        Get all active, usable tools for a profile grouped by subcategory
        Returns dict: {subcategory: [tool_dicts]}
        """
        if profile_name == 'qa_analyst':
            tools = cls.query.filter_by(active=True, usable_qa_analyst=True).order_by(cls.display_order).all()
            subcategory_field = 'subcategory_qa_analyst'
        elif profile_name == 'qa_engineer':
            tools = cls.query.filter_by(active=True, usable_qa_engineer=True).order_by(cls.display_order).all()
            subcategory_field = 'subcategory_qa_engineer'
        elif profile_name == 'data_scientist':
            tools = cls.query.filter_by(active=True, usable_data_scientist=True).order_by(cls.display_order).all()
            subcategory_field = 'subcategory_data_scientist'
        else:
            return {}
        
        # Group by subcategory and convert to dictionaries
        grouped = {}
        for tool in tools:
            subcategory = getattr(tool, subcategory_field)
            if subcategory:
                if subcategory not in grouped:
                    grouped[subcategory] = []
                grouped[subcategory].append(tool.to_dict())
        
        return grouped
    
    def apply_profile_preset(self, profile_name):
        """Apply predefined usability preset for a profile"""
        # By default, enable for specified profile only
        self.usable_qa_analyst = False
        self.usable_qa_engineer = False
        self.usable_data_scientist = False
        
        if profile_name in ['qa_analyst', 'qa_engineer', 'data_scientist']:
            self.set_profile_config(profile_name, True, None)
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'proficiency_level': self.proficiency_level,
            'years_experience': self.years_experience,
            'description': self.description,
            'usable_qa_analyst': self.usable_qa_analyst,
            'subcategory_qa_analyst': self.subcategory_qa_analyst,
            'usable_qa_engineer': self.usable_qa_engineer,
            'subcategory_qa_engineer': self.subcategory_qa_engineer,
            'usable_data_scientist': self.usable_data_scientist,
            'subcategory_data_scientist': self.subcategory_data_scientist,
            'display_order': self.display_order
        })
        return data
    
    def __repr__(self):
        return f'<TechnicalTool {self.name}>'


def ensure_data_scientist_tool_defaults():
    defaults = [
        {
            "name": "Machine Learning",
            "subcategory": "Modeling & Data Science",
        },
        {
            "name": "Statistical Modeling",
            "subcategory": "Modeling & Data Science",
        },
        {
            "name": "Feature Engineering",
            "subcategory": "Modeling & Data Science",
        },
        {
            "name": "Data Visualization",
            "subcategory": "Modeling & Data Science",
        },
        {
            "name": "Data Pipelines",
            "subcategory": "Data Engineering & Development",
        },
        {
            "name": "API Development",
            "subcategory": "Data Engineering & Development",
        },
    ]

    updated = False
    for item in defaults:
        name = item["name"]
        existing = TechnicalTool.query.filter(func.lower(TechnicalTool.name) == name.lower()).first()
        if existing:
            if not existing.usable_data_scientist:
                existing.usable_data_scientist = True
                updated = True
            if not existing.subcategory_data_scientist:
                existing.subcategory_data_scientist = item["subcategory"]
                updated = True
            if existing.display_order == 0:
                existing.display_order = 999
                updated = True
        else:
            tool = TechnicalTool(
                name=name,
                usable_data_scientist=True,
                subcategory_data_scientist=item["subcategory"],
                display_order=999,
            )
            db.session.add(tool)
            updated = True

    if updated:
        db.session.commit()


def apply_data_scientist_skill_order():
    category_order = {
        "Modeling & Data Science": [
            "Machine Learning",
            "Statistical Modeling",
            "Feature Engineering",
            "Data Visualization",
        ],
        "Data Engineering & Development": [
            "Python (Flask, Jupyter)",
            "C++",
            "Java",
            "SQLAlchemy",
            "Data Pipelines",
            "API Development",
        ],
        "Data Platforms": [
            "BigQuery",
            "PySpark",
            "SQL Server",
            "MySQL",
            "GCP",
            "DataStage",
        ],
        "QA & CI/CD": [
            "JIRA",
            "Xray",
            "Jenkins",
            "SonarQube",
            "Postman",
            "Selenium",
            "Cucumber",
        ],
    }

    updated = False
    for category, names in category_order.items():
        for idx, name in enumerate(names, start=1):
            existing = TechnicalTool.query.filter(func.lower(TechnicalTool.name) == name.lower()).first()
            if not existing:
                existing = TechnicalTool(
                    name=name,
                    usable_data_scientist=True,
                    subcategory_data_scientist=category,
                    display_order=idx,
                )
                db.session.add(existing)
                updated = True
                continue

            if not existing.usable_data_scientist:
                existing.usable_data_scientist = True
                updated = True
            if existing.subcategory_data_scientist != category:
                existing.subcategory_data_scientist = category
                updated = True
            if existing.display_order != idx:
                existing.display_order = idx
                updated = True

    combined = TechnicalTool.query.filter(
        func.lower(TechnicalTool.name) == "data pipelines / api development"
    ).first()
    if combined and combined.usable_data_scientist:
        combined.usable_data_scientist = False
        updated = True

    if updated:
        db.session.commit()
