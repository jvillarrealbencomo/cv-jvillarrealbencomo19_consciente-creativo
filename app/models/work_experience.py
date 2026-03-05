"""
Work Experience Model with Three-Level Visibility Control
Version 2025 - Separate visibility for summary, detailed responsibilities, and achievements
"""
from app import db
from app.models.base import BaseModel, ProfileVisibilityMixin


class WorkExperience(BaseModel, ProfileVisibilityMixin):
    """
    Work experience with granular visibility control
    Three independent visibility flags:
    - show_responsibilities_summary
    - show_responsibilities_detailed
    - show_achievements
    """
    __tablename__ = 'work_experience'
    
    # Job Details
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    
    # Time Period (supporting chronological blocks: 2021-2025, 2015-2020, 1985-2009)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)
    
    # Time block classification for organizational purposes
    time_block = db.Column(db.String(50), comment="e.g., '2021-2025', '2015-2020', '1985-2009'")
    
    # Three Types of Content with Independent Visibility
    
    # 1. Summary (brief, one-line description)
    responsibilities_summary = db.Column(db.Text)
    show_responsibilities_summary = db.Column(db.Boolean, default=True, nullable=False)
    
    # 2. Detailed responsibilities (comprehensive list)
    responsibilities_detailed = db.Column(db.Text)
    show_responsibilities_detailed = db.Column(db.Boolean, default=False, nullable=False)
    
    # 3. Key achievements/highlights
    achievements = db.Column(db.Text)
    show_achievements = db.Column(db.Boolean, default=True, nullable=False)
    
    # Additional metadata
    technologies = db.Column(db.Text, comment="Comma-separated technologies used")
    
    # Display order within time block
    display_order = db.Column(db.Integer, default=0)
    
    def get_visible_content(self):
        """
        Returns dictionary of content sections that should be displayed
        Based on visibility flags
        """
        content = {}
        
        if self.show_responsibilities_summary and self.responsibilities_summary:
            content['responsibilities_summary'] = self.responsibilities_summary
        
        if self.show_responsibilities_detailed and self.responsibilities_detailed:
            content['responsibilities_detailed'] = self.responsibilities_detailed
        
        if self.show_achievements and self.achievements:
            content['achievements'] = self.achievements
        
        return content
    
    def get_content_level(self):
        """
        Determine content detail level: 'none', 'minimal', 'summary', 'detailed', 'complete'
        """
        if not any([self.show_responsibilities_summary, 
                   self.show_responsibilities_detailed, 
                   self.show_achievements]):
            return 'none'
        
        if self.show_responsibilities_detailed and self.show_achievements:
            return 'complete'
        elif self.show_responsibilities_detailed:
            return 'detailed'
        elif self.show_achievements:
            return 'summary'
        elif self.show_responsibilities_summary:
            return 'minimal'
        
        return 'none'
    
    def set_content_level(self, level):
        """
        Set all visibility flags based on desired detail level
        Levels: 'none', 'minimal', 'summary', 'detailed', 'complete'
        """
        if level == 'none':
            self.show_responsibilities_summary = False
            self.show_responsibilities_detailed = False
            self.show_achievements = False
        elif level == 'minimal':
            self.show_responsibilities_summary = True
            self.show_responsibilities_detailed = False
            self.show_achievements = False
        elif level == 'summary':
            self.show_responsibilities_summary = True
            self.show_responsibilities_detailed = False
            self.show_achievements = True
        elif level == 'detailed':
            self.show_responsibilities_summary = True
            self.show_responsibilities_detailed = True
            self.show_achievements = False
        elif level == 'complete':
            self.show_responsibilities_summary = True
            self.show_responsibilities_detailed = True
            self.show_achievements = True
    
    def get_technologies_list(self):
        """Parse technologies string into list"""
        if not self.technologies:
            return []
        return [tech.strip() for tech in self.technologies.split(',')]
    
    def apply_profile_preset(self, profile_name):
        """Apply predefined visibility preset based on profile"""
        super().apply_profile_preset(profile_name)
        
        # Profile-specific content level defaults
        if profile_name == 'qa_analyst':
            # QA Analyst: focus on achievements
            self.set_content_level('summary')
        elif profile_name == 'qa_engineer':
            # QA Engineer: show detailed work
            self.set_content_level('complete')
        elif profile_name == 'data_scientist':
            # Data Scientist: achievements-focused
            self.set_content_level('summary')
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'job_title': self.job_title,
            'company': self.company,
            'location': self.location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'time_block': self.time_block,
            'responsibilities_summary': self.responsibilities_summary,
            'show_responsibilities_summary': self.show_responsibilities_summary,
            'responsibilities_detailed': self.responsibilities_detailed,
            'show_responsibilities_detailed': self.show_responsibilities_detailed,
            'achievements': self.achievements,
            'show_achievements': self.show_achievements,
            'technologies': self.technologies,
            'technologies_list': self.get_technologies_list(),
            'display_order': self.display_order,
            'visible_content': self.get_visible_content(),
            'content_level': self.get_content_level(),
            'visible_qa_analyst': self.visible_qa_analyst,
            'visible_qa_engineer': self.visible_qa_engineer,
            'visible_data_scientist': self.visible_data_scientist
        })
        return data
    
    def __repr__(self):
        return f'<WorkExperience {self.job_title} at {self.company} ({self.time_block})>'
