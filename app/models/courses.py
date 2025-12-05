"""
Course Model
Version 2025 - Training courses
"""
from app import db
from app.models.base import BaseModel, ProfileVisibilityMixin


class Course(BaseModel, ProfileVisibilityMixin):
    """
    Training courses with visibility control
    """
    __tablename__ = 'courses'
    
    name = db.Column(db.String(300), nullable=False)
    provider = db.Column(db.String(200), nullable=False)
    completion_date = db.Column(db.Date)
    duration_hours = db.Column(db.Integer)
    credential_url = db.Column(db.String(500))
    
    # Course details
    description = db.Column(db.Text)
    skills_acquired = db.Column(db.Text, comment="Comma-separated skills")
    
    # Document reference
    document_url = db.Column(db.String(500))
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def get_skills_list(self):
        """Parse skills string into list"""
        if not self.skills_acquired:
            return []
        return [skill.strip() for skill in self.skills_acquired.split(',')]
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'provider': self.provider,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'duration_hours': self.duration_hours,
            'credential_url': self.credential_url,
            'description': self.description,
            'skills_acquired': self.skills_acquired,
            'skills_list': self.get_skills_list(),
            'document_url': self.document_url,
            'display_order': self.display_order,
            'visible_qa_analyst': self.visible_qa_analyst,
            'visible_qa_engineer': self.visible_qa_engineer,
            'visible_data_scientist': self.visible_data_scientist
        })
        return data
    
    def __repr__(self):
        return f'<Course {self.name}>'
