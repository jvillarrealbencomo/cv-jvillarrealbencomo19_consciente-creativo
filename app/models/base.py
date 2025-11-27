"""
Base model with common fields for all models
"""
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """
    Abstract base model with common control fields
    All models inherit from this to ensure consistency
    """
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    visible_in_summary = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Profile relevance scores (0-10) for intelligent filtering
    relevance_qa_analyst = db.Column(db.Integer, default=5, nullable=False)
    relevance_qa_engineer = db.Column(db.Integer, default=5, nullable=False)
    relevance_data_scientist = db.Column(db.Integer, default=5, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'active': self.active,
            'visible_in_summary': self.visible_in_summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'relevance_qa_analyst': self.relevance_qa_analyst,
            'relevance_qa_engineer': self.relevance_qa_engineer,
            'relevance_data_scientist': self.relevance_data_scientist
        }
    
    def is_relevant_for_profile(self, profile_name, min_relevance=5):
        """
        Check if this record is relevant for a specific profile
        
        Args:
            profile_name: 'qa_analyst', 'qa_engineer', or 'data_scientist'
            min_relevance: Minimum relevance score (default 5)
        
        Returns:
            Boolean indicating relevance
        """
        if not self.active:
            return False
        
        relevance_map = {
            'qa_analyst': self.relevance_qa_analyst,
            'qa_engineer': self.relevance_qa_engineer,
            'data_scientist': self.relevance_data_scientist
        }
        
        return relevance_map.get(profile_name, 0) >= min_relevance
