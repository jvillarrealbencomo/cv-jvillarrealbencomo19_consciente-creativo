"""
Enhanced Base Model with Granular Visibility Control
Version 2025 - Updated Architecture
"""
from datetime import datetime
from app import db


class TimestampMixin:
    """Mixin for timestamp fields"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BaseModel(db.Model, TimestampMixin):
    """
    Abstract base model with common fields
    All models inherit from this
    """
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    
    # Historical tracking - items can be active but not used in any current CV
    is_historical = db.Column(db.Boolean, default=False, nullable=False, 
                              comment="True if item is kept for history but not shown in any current CV")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'active': self.active,
            'is_historical': self.is_historical,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ProfileVisibilityMixin:
    """
    Mixin for profile-specific visibility
    Each profile can independently show/hide items
    """
    # Visibility per profile
    visible_qa_analyst = db.Column(db.Boolean, default=False, nullable=False)
    visible_qa_engineer = db.Column(db.Boolean, default=False, nullable=False)
    visible_data_scientist = db.Column(db.Boolean, default=False, nullable=False)
    
    def is_visible_for_profile(self, profile_name):
        """Check if item should be visible for specific profile"""
        visibility_map = {
            'qa_analyst': self.visible_qa_analyst,
            'qa_engineer': self.visible_qa_engineer,
            'data_scientist': self.visible_data_scientist
        }
        return visibility_map.get(profile_name, False)
    
    def set_visibility_for_profile(self, profile_name, visible):
        """Set visibility for specific profile"""
        if profile_name == 'qa_analyst':
            self.visible_qa_analyst = visible
        elif profile_name == 'qa_engineer':
            self.visible_qa_engineer = visible
        elif profile_name == 'data_scientist':
            self.visible_data_scientist = visible
    
    def apply_profile_preset(self, profile_name):
        """
        Apply predefined visibility preset for a profile
        Override this method in subclasses for custom logic
        """
        # Default: make visible for specified profile only
        self.visible_qa_analyst = (profile_name == 'qa_analyst')
        self.visible_qa_engineer = (profile_name == 'qa_engineer')
        self.visible_data_scientist = (profile_name == 'data_scientist')
