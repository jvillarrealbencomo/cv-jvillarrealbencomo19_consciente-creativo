"""
Person Model with Granular Contact Field Visibility
Version 2025 - Each contact field has independent visibility control
"""
from app import db
from app.models.base import BaseModel


class Person(BaseModel):
    """
    Personal data with per-field visibility control
    Each contact method (email, phone, LinkedIn, GitHub, URL) can be independently shown/hidden
    """
    __tablename__ = 'person'
    
    # Basic Information
    full_name = db.Column(db.String(200), nullable=False)
    professional_title = db.Column(db.String(200), nullable=False)
    
    # Profile-specific titles
    title_qa_analyst = db.Column(db.String(200))
    title_qa_engineer = db.Column(db.String(200))
    title_data_scientist = db.Column(db.String(200))
    
    # Contact Information with Individual Visibility Flags
    email = db.Column(db.String(120))
    show_email = db.Column(db.Boolean, default=True, nullable=False)
    
    phone = db.Column(db.String(50))
    show_phone = db.Column(db.Boolean, default=True, nullable=False)
    
    linkedin_url = db.Column(db.String(300))
    show_linkedin = db.Column(db.Boolean, default=True, nullable=False)
    
    github_url = db.Column(db.String(300))
    show_github = db.Column(db.Boolean, default=True, nullable=False)
    
    personal_url = db.Column(db.String(300))
    show_personal_url = db.Column(db.Boolean, default=True, nullable=False)
    
    # Location
    location = db.Column(db.String(200))
    
    # Professional Summaries (profile-specific)
    summary_qa_analyst = db.Column(db.Text)
    summary_qa_engineer = db.Column(db.Text)
    summary_data_scientist = db.Column(db.Text)
    
    # Profile image
    profile_image_url = db.Column(db.String(500))
    
    # Professional Reference
    reference_name = db.Column(db.String(200))
    reference_company = db.Column(db.String(200))
    reference_phone = db.Column(db.String(50))

    # Computed name parts for backward compatibility with templates expecting first_name / last_name
    @property
    def first_name(self):
        if not self.full_name:
            return ''
        return self.full_name.split(' ', 1)[0]

    @property
    def last_name(self):
        if not self.full_name:
            return ''
        parts = self.full_name.split(' ', 1)
        return parts[1] if len(parts) > 1 else ''
    
    def get_visible_contacts(self):
        """
        Returns dictionary of contact fields that should be visible
        Each field independently controlled
        """
        contacts = {}
        
        if self.show_email and self.email:
            contacts['email'] = self.email
        
        if self.show_phone and self.phone:
            contacts['phone'] = self.phone
        
        if self.show_linkedin and self.linkedin_url:
            contacts['linkedin'] = self.linkedin_url
        
        if self.show_github and self.github_url:
            contacts['github'] = self.github_url
        
        if self.show_personal_url and self.personal_url:
            contacts['personal_url'] = self.personal_url
        
        return contacts
    
    def get_title_for_profile(self, profile_name):
        """Get profile-specific title or fallback to default"""
        title_map = {
            'qa_analyst': self.title_qa_analyst or self.professional_title,
            'qa_engineer': self.title_qa_engineer or self.professional_title,
            'data_scientist': self.title_data_scientist or self.professional_title
        }
        return title_map.get(profile_name, self.professional_title)
    
    def get_summary_for_profile(self, profile_name):
        """Get profile-specific summary"""
        summary_map = {
            'qa_analyst': self.summary_qa_analyst,
            'qa_engineer': self.summary_qa_engineer,
            'data_scientist': self.summary_data_scientist
        }
        return summary_map.get(profile_name)
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'professional_title': self.professional_title,
            'title_qa_analyst': self.title_qa_analyst,
            'title_qa_engineer': self.title_qa_engineer,
            'title_data_scientist': self.title_data_scientist,
            'email': self.email,
            'show_email': self.show_email,
            'phone': self.phone,
            'show_phone': self.show_phone,
            'linkedin_url': self.linkedin_url,
            'show_linkedin': self.show_linkedin,
            'github_url': self.github_url,
            'show_github': self.show_github,
            'personal_url': self.personal_url,
            'show_personal_url': self.show_personal_url,
            'location': self.location,
            'summary_qa_analyst': self.summary_qa_analyst,
            'summary_qa_engineer': self.summary_qa_engineer,
            'summary_data_scientist': self.summary_data_scientist,
            'profile_image_url': self.profile_image_url,
            'reference_name': self.reference_name,
            'reference_company': self.reference_company,
            'reference_phone': self.reference_phone,
            'visible_contacts': self.get_visible_contacts()
        })
        return data
    
    def __repr__(self):
        return f'<Person {self.full_name}>'
