"""
Languages Model
Language proficiency information
"""
from app import db
from app.models.base import BaseModel


class Language(BaseModel):
    """
    Language skills with proficiency levels
    """
    __tablename__ = 'languages'
    
    name = db.Column(db.String(100), nullable=False)
    
    # Proficiency level: 'Native', 'Fluent', 'Advanced', 'Intermediate', 'Basic'
    # or use CEFR: 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'
    level = db.Column(db.String(50), nullable=False)
    
    # Optional certifications
    certification_name = db.Column(db.String(200))
    certification_score = db.Column(db.String(50))
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'level': self.level,
            'certification_name': self.certification_name,
            'certification_score': self.certification_score,
            'display_order': self.display_order
        })
        return data
    
    def __repr__(self):
        return f'<Language {self.name} - {self.level}>'
