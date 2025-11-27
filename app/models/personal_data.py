"""
Personal Data Model
Stores personal information with configurable link visibility
"""
from app import db
from app.models.base import BaseModel


class PersonalData(BaseModel):
    """
    Personal information model with intelligent link management
    Only one active record should exist at a time
    """
    __tablename__ = 'personal_data'
    
    # Basic Information
    full_name = db.Column(db.String(200), nullable=False)
    professional_title = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))
    
    # Professional Summary
    summary = db.Column(db.Text, nullable=False)
    summary_short = db.Column(db.String(500))  # For one-page PDF
    
    # URLs
    url_personal = db.Column(db.String(300))
    url_github = db.Column(db.String(300))
    url_linkedin = db.Column(db.String(300))
    
    # Link visibility control for PDF
    # Options: 'linkedin', 'personal', 'github', 'all', 'linkedin,github', etc.
    show_link = db.Column(db.String(100), default='all', nullable=False)
    
    # Profile image
    profile_image_url = db.Column(db.String(500))
    
    def get_visible_links(self):
        """
        Returns dictionary of links that should be visible based on show_link setting
        
        Returns:
            dict: Links to display
        """
        if not self.show_link or self.show_link == 'none':
            return {}
        
        all_links = {
            'linkedin': self.url_linkedin,
            'personal': self.url_personal,
            'github': self.url_github
        }
        
        if self.show_link == 'all':
            return {k: v for k, v in all_links.items() if v}
        
        # Parse comma-separated values
        visible = [link.strip() for link in self.show_link.split(',')]
        return {k: v for k, v in all_links.items() if k in visible and v}
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'full_name': self.full_name,
            'professional_title': self.professional_title,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'summary_short': self.summary_short,
            'url_personal': self.url_personal,
            'url_github': self.url_github,
            'url_linkedin': self.url_linkedin,
            'show_link': self.show_link,
            'profile_image_url': self.profile_image_url,
            'visible_links': self.get_visible_links()
        })
        return data
    
    def __repr__(self):
        return f'<PersonalData {self.full_name}>'
