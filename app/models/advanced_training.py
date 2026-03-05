"""
Advanced Training Model - Unified Courses and Certifications
Version 2025 - Single table for both training types
"""
from app import db
from app.models.base import BaseModel, ProfileVisibilityMixin


class AdvancedTraining(BaseModel, ProfileVisibilityMixin):
    """
    Advanced training and certifications
    Unified model for both courses and certifications
    """
    __tablename__ = 'advanced_training'
    
    # Type discriminator
    type = db.Column(db.String(20), nullable=False, comment="'Course' or 'Certification'")
    
    # Common fields
    name = db.Column(db.String(300), nullable=False)
    provider = db.Column(db.String(200), nullable=False, comment="Issuing organization or training provider")
    completion_date = db.Column(db.Date, comment="Date completed/issued")
    description = db.Column(db.Text, comment="Details, topics covered, achievements")
    
    # Certification-specific (optional for courses)
    expiration_date = db.Column(db.Date, comment="For certifications that expire")
    credential_id = db.Column(db.String(200), comment="Certificate ID or credential number")
    credential_url = db.Column(db.String(500), comment="Verification URL")

    # Credential image paths
    image_path = db.Column(db.String(500))
    image_thumbnail_path = db.Column(db.String(500))
    image_filename = db.Column(db.String(255))
    image_mime_type = db.Column(db.String(50))
    
    # Course-specific (optional for certifications)
    duration_hours = db.Column(db.Integer, comment="Course duration in hours")
    
    # Display order within this section
    display_order = db.Column(db.Integer, default=0, comment="Sort order in CV (lower first)")
    
    @property
    def image_url(self):
        """Get full URL for image"""
        return f"/static/{self.image_path}" if self.image_path else None
    
    @property
    def image_thumbnail_url(self):
        """Get full URL for thumbnail"""
        return f"/static/{self.image_thumbnail_path}" if self.image_thumbnail_path else None
    
    def is_course(self):
        """Check if this is a course"""
        return self.type == 'Course'
    
    def is_certification(self):
        """Check if this is a certification"""
        return self.type == 'Certification'
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'type': self.type,
            'name': self.name,
            'provider': self.provider,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'description': self.description,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'credential_id': self.credential_id,
            'credential_url': self.credential_url,
            'duration_hours': self.duration_hours,
            'display_order': self.display_order,
            'image_path': self.image_path,
            'image_thumbnail_path': self.image_thumbnail_path,
            'image_filename': self.image_filename,
            'image_mime_type': self.image_mime_type,
            'image_url': f"/static/{self.image_path}" if self.image_path else None,
            'image_thumbnail_url': f"/static/{self.image_thumbnail_path}" if self.image_thumbnail_path else None,
            'visible_qa_analyst': self.visible_qa_analyst,
            'visible_qa_engineer': self.visible_qa_engineer,
            'visible_data_scientist': self.visible_data_scientist,
            'is_course': self.is_course(),
            'is_certification': self.is_certification()
        })
        return data
    
    def __repr__(self):
        return f'<AdvancedTraining {self.type}: {self.name}>'
