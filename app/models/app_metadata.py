"""
Application metadata model
Version 2026 - App metadata storage
"""
from datetime import datetime
from sqlalchemy import inspect
from app import db


class AppMetadata(db.Model):
    __tablename__ = "app_metadata"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


def _ensure_app_metadata_table():
    inspector = inspect(db.engine)
    if AppMetadata.__tablename__ not in inspector.get_table_names():
        AppMetadata.__table__.create(db.engine)


def ensure_app_metadata_defaults():
    _ensure_app_metadata_table()
    defaults = [
        ("application_name", "API CV"),
        ("application_version", "2026.2.0"),
        ("release_year", "2026"),
        ("api_version", "v2"),
        ("api_release_date", "2026-02-20"),
        ("api_status", "production"),
    ]

    added = False
    for key, value in defaults:
        entry = AppMetadata.query.filter_by(key=key).first()
        if not entry:
            db.session.add(AppMetadata(key=key, value=value))
            added = True

    if added:
        db.session.commit()


def get_app_metadata_dict():
    _ensure_app_metadata_table()
    entries = AppMetadata.query.all()
    if not entries:
        ensure_app_metadata_defaults()
        entries = AppMetadata.query.all()
    return {entry.key: entry.value for entry in entries}


def get_app_metadata_value(key, default=None):
    return get_app_metadata_dict().get(key, default)