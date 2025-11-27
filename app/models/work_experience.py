"""
Work Experience Model
Professional experience with intelligent detail management
"""
from app import db
from app.models.base import BaseModel


class WorkExperience(BaseModel):
    """
    Work experience with configurable detail display
    """
    __tablename__ = 'work_experience'
    
    # Job details
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)
    
    # Job description
    description = db.Column(db.Text)
    
    # NEW 2025: Configurable details
    functions = db.Column(db.Text)  # Daily functions and responsibilities
    highlighted_aspect = db.Column(db.Text)  # Key achievement or aspect to highlight
    
    # Control what to show: 'functions', 'aspect', 'both'
    show_detail = db.Column(db.String(50), default='both', nullable=False)
    
    # Technologies used (comma-separated for simple querying)
    technologies = db.Column(db.Text)
    
    # Document reference
    document_url = db.Column(db.String(500))
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def get_display_content(self):
        """
        Returns the content to display based on show_detail setting
        
        Returns:
            dict: Content to display
        """
        content = {
            'description': self.description,
            'functions': None,
            'highlighted_aspect': None
        }
        
        if self.show_detail == 'functions':
            content['functions'] = self.functions
        elif self.show_detail == 'aspect':
            content['highlighted_aspect'] = self.highlighted_aspect
        elif self.show_detail == 'both':
            content['functions'] = self.functions
            content['highlighted_aspect'] = self.highlighted_aspect
        
        return content
    
    def get_technologies_list(self):
        """Parse technologies string into list"""
        if not self.technologies:
            return []
        return [tech.strip() for tech in self.technologies.split(',')]
    
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
            'description': self.description,
            'functions': self.functions,
            'highlighted_aspect': self.highlighted_aspect,
            'show_detail': self.show_detail,
            'technologies': self.technologies,
            'technologies_list': self.get_technologies_list(),
            'document_url': self.document_url,
            'display_order': self.display_order,
            'display_content': self.get_display_content()
        })
        return data
    
    def __repr__(self):
        return f'<WorkExperience {self.job_title} at {self.company}>'
