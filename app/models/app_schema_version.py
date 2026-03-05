"""
Schema version tracking
Version 2026 - Schema version storage
"""
from datetime import datetime
from sqlalchemy import inspect
from app import db


class AppSchemaVersion(db.Model):
    __tablename__ = "app_schema_version"

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(50), unique=True, nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def _ensure_schema_version_table():
    inspector = inspect(db.engine)
    if AppSchemaVersion.__tablename__ not in inspector.get_table_names():
        AppSchemaVersion.__table__.create(db.engine)


def ensure_schema_version(version: str):
    _ensure_schema_version_table()
    existing = AppSchemaVersion.query.filter_by(version=version).first()
    if not existing:
        db.session.add(AppSchemaVersion(version=version))
        db.session.commit()


def get_latest_schema_version():
    _ensure_schema_version_table()
    entry = AppSchemaVersion.query.order_by(AppSchemaVersion.id.desc()).first()
    return entry.version if entry else None
