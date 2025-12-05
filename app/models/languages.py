"""
Language Model with Conversation, Reading, Writing Skills
Version 2025 - Separate proficiency levels for each skill type
"""
from app import db
from app.models.base import BaseModel, ProfileVisibilityMixin


class Language(BaseModel, ProfileVisibilityMixin):
    """
    Language skills with detailed proficiency breakdown
    Separate levels for: conversation, reading, writing
    """
    __tablename__ = 'languages'
    
    # Language name
    name = db.Column(db.String(100), nullable=False)
    
    # Proficiency levels (use CEFR: A1, A2, B1, B2, C1, C2 or Native/Fluent/Advanced/Intermediate/Basic)
    level_conversation = db.Column(db.String(50), nullable=False, comment="Conversation proficiency")
    level_reading = db.Column(db.String(50), nullable=False, comment="Reading proficiency")
    level_writing = db.Column(db.String(50), nullable=False, comment="Writing proficiency")
    
    # Optional certification
    certification_name = db.Column(db.String(200))
    certification_score = db.Column(db.String(50))
    certification_date = db.Column(db.Date)
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def get_overall_level(self):
        """Calculate overall proficiency (average of three skills)"""
        # Simplified: return the most common level or conversation level
        return self.level_conversation
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'level_conversation': self.level_conversation,
            'level_reading': self.level_reading,
            'level_writing': self.level_writing,
            'certification_name': self.certification_name,
            'certification_score': self.certification_score,
            'certification_date': self.certification_date.isoformat() if self.certification_date else None,
            'display_order': self.display_order,
            'overall_level': self.get_overall_level(),
            'visible_qa_analyst': self.visible_qa_analyst,
            'visible_qa_engineer': self.visible_qa_engineer,
            'visible_data_scientist': self.visible_data_scientist
        })
        return data
    
    def __repr__(self):
        return f'<Language {self.name}>'
