"""
Support Tools Model
Programming tools, frameworks, and technical skills
"""
from app import db
from app.models.base import BaseModel


class SupportTool(BaseModel):
    """
    Technical skills and tools proficiency
    """
    __tablename__ = 'support_tools'
    
    # Category: 'Programming Language', 'Framework', 'Database', 'Tool', 'Methodology', etc.
    category = db.Column(db.String(100), nullable=False, index=True)
    
    name = db.Column(db.String(200), nullable=False)
    
    # Proficiency: 'Expert', 'Advanced', 'Intermediate', 'Basic'
    proficiency_level = db.Column(db.String(50), nullable=False)
    
    # Years of experience
    years_experience = db.Column(db.Float)
    
    # Additional notes
    description = db.Column(db.Text)
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'category': self.category,
            'name': self.name,
            'proficiency_level': self.proficiency_level,
            'years_experience': self.years_experience,
            'description': self.description,
            'display_order': self.display_order
        })
        return data
    
    def __repr__(self):
        return f'<SupportTool {self.name} ({self.category})>'
