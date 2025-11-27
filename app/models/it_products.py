"""
IT Products Model
Software products and projects developed
"""
from app import db
from app.models.base import BaseModel


class ITProduct(BaseModel):
    """
    IT products and projects portfolio
    """
    __tablename__ = 'it_products'
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(200))  # Developer, Lead, Architect, etc.
    
    # Project details
    technologies = db.Column(db.Text)  # Comma-separated technologies
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)
    
    # Links
    project_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    demo_url = db.Column(db.String(500))
    
    # Impact/Results
    impact_description = db.Column(db.Text)
    
    # Display order
    display_order = db.Column(db.Integer, default=0)
    
    def get_technologies_list(self):
        """Parse technologies string into list"""
        if not self.technologies:
            return []
        return [tech.strip() for tech in self.technologies.split(',')]
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'role': self.role,
            'technologies': self.technologies,
            'technologies_list': self.get_technologies_list(),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'project_url': self.project_url,
            'github_url': self.github_url,
            'demo_url': self.demo_url,
            'impact_description': self.impact_description,
            'display_order': self.display_order
        })
        return data
    
    def __repr__(self):
        return f'<ITProduct {self.name}>'
