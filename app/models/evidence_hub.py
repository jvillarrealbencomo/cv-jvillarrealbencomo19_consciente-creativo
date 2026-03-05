"""
Model evidence_hub_entries (New)
Version 2026 - Updated 29-01-2026
"""
from datetime import datetime
from app import db

class EvidenceHubEntry(db.Model):
    __tablename__ = "evidence_hub_entries"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    stack = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    video_path = db.Column(db.String(255), nullable=True)
    video_filename = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)