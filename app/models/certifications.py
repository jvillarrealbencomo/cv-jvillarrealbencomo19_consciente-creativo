"""
Certifications Model
Professional certifications with optional comments
"""
from app import db
from app.models.base import BaseModel


class Certification(BaseModel):
    """
    Professional certifications with configurable comment visibility
    """
    __tablename__ = 'certifications'
    
    name = db.Column(db.String(300), nullable=False)
    issuing_organization = db.Column(db.String(200), nullable=False)
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    credential_id = db.Column(db.String(200))
    credential_url = db.Column(db.String(500))
    
    # NEW 2025: Comment system
    comment = db.Column(db.Text)  # Additional context or relevance note
    visible_comment = db.Column(db.Boolean, default=False, nullable=False)
    
    # Document reference
    document_url = db.Column(db.String(500))
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def is_expired(self):
        """Check if certification is expired"""
        if not self.expiration_date:
            return False
        from datetime import date
        return self.expiration_date < date.today()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'issuing_organization': self.issuing_organization,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'credential_id': self.credential_id,
            'credential_url': self.credential_url,
            'comment': self.comment if self.visible_comment else None,
            'visible_comment': self.visible_comment,
            'document_url': self.document_url,
            'display_order': self.display_order,
            'is_expired': self.is_expired()
        })
        return data
    
    def __repr__(self):
        return f'<Certification {self.name} - {self.issuing_organization}>'
