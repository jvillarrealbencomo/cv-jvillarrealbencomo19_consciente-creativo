"""
Application metadata model
Version 2026 - App metadata storage
"""
from datetime import datetime
from app import db


class AppMetadata(db.Model):
    __tablename__ = "app_metadata"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


def ensure_app_metadata_defaults():
    defaults = [
        ("application_name", "API CV"),
        ("application_version", "2026.1.0"),
        ("release_year", "2026"),
    ]

    for key, value in defaults:
        entry = AppMetadata.query.filter_by(key=key).first()
        if entry:
            if entry.value != value:
                entry.value = value
        else:
            db.session.add(AppMetadata(key=key, value=value))

    db.session.commit()