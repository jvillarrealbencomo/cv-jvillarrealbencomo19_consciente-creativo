"""
Certification Model
Version 2025 - Professional certifications
"""
from app import db
from app.models.base import BaseModel, ProfileVisibilityMixin


class Certification(BaseModel, ProfileVisibilityMixin):
    """
    Professional certifications with visibility control
    """
    __tablename__ = 'certifications'
    
    name = db.Column(db.String(300), nullable=False)
    issuing_organization = db.Column(db.String(200), nullable=False)
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    credential_id = db.Column(db.String(200))
    credential_url = db.Column(db.String(500))
    
    # Description/notes
    description = db.Column(db.Text)
    
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
            'description': self.description,
            'document_url': self.document_url,
            'display_order': self.display_order,
            'is_expired': self.is_expired(),
            'visible_qa_analyst': self.visible_qa_analyst,
            'visible_qa_engineer': self.visible_qa_engineer,
            'visible_data_scientist': self.visible_data_scientist
        })
        return data
    
    def __repr__(self):
        return f'<Certification {self.name}>'
