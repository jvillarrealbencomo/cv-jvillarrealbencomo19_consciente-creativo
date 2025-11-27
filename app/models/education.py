"""
Education Model
Academic background and degrees
"""
from app import db
from app.models.base import BaseModel


class Education(BaseModel):
    """
    Education records with degree information
    """
    __tablename__ = 'education'
    
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)
    
    # Academic details
    gpa = db.Column(db.String(20))
    honors = db.Column(db.String(200))
    description = db.Column(db.Text)
    
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
            'location': self.location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'gpa': self.gpa,
            'honors': self.honors,
            'description': self.description,
            'document_url': self.document_url,
            'display_order': self.display_order
        })
        return data
    
    def __repr__(self):
        return f'<Education {self.degree} - {self.institution}>'
