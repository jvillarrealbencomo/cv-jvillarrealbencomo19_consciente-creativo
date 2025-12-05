"""
Education Model
Version 2025 - Degree, Institution, Country, Year
"""
from app import db
from app.models.base import BaseModel, ProfileVisibilityMixin


class Education(BaseModel, ProfileVisibilityMixin):
    """
    Academic education records
    """
    __tablename__ = 'education'
    
    # Degree information
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100))
    
    # Year (can use start_date/end_date for more detail if needed)
    year_obtained = db.Column(db.Integer, comment="Graduation year")
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    is_current = db.Column(db.Boolean, default=False)
    
    # Additional details
    details = db.Column(db.Text, comment="Additional details, honors, GPA, etc.")
    
    # Document reference
    document_url = db.Column(db.String(500))
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'degree': self.degree,
            'institution': self.institution,
            'country': self.country,
            'year_obtained': self.year_obtained,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'is_current': self.is_current,
            'details': self.details,
            'document_url': self.document_url,
            'display_order': self.display_order,
            'visible_qa_analyst': self.visible_qa_analyst,
            'visible_qa_engineer': self.visible_qa_engineer,
            'visible_data_scientist': self.visible_data_scientist
        })
        return data
    
    def __repr__(self):
        return f'<Education {self.degree} - {self.institution}>'
