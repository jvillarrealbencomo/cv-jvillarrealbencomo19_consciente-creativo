"""
Database Initialization Script
Version 2026 - Idempotent schema initialization
"""
import os
from sqlalchemy import inspect
from app import create_app, db

SCHEMA_VERSION = "2026.1.0"


def init_database(reset=False):
    """Initialize database with all tables (idempotent)."""
    app = create_app(os.environ.get('FLASK_ENV', 'development'))

    with app.app_context():
        if reset:
            print("⚠️  WARNING: This will DELETE all existing data!")
            response = input("Type 'YES' to confirm: ")
            if response != 'YES':
                print("Cancelled.")
                return
            print("Dropping all existing tables...")
            db.drop_all()

        inspector = inspect(db.engine)
        already_initialized = "app_schema_version" in inspector.get_table_names()

        print("Creating missing tables from models...")
        db.create_all()

        from app.models.app_metadata import ensure_app_metadata_defaults, get_app_metadata_value
        from app.models.app_schema_version import ensure_schema_version, get_latest_schema_version

        ensure_app_metadata_defaults()
        schema_version = get_app_metadata_value("application_version", SCHEMA_VERSION)
        ensure_schema_version(schema_version)

        latest = get_latest_schema_version()
        if already_initialized or latest:
            print(f"✓ Database already initialized (schema version: {latest}).")
        else:
            print("✓ Database initialized successfully!")

        print(f"Tables present: {', '.join(db.metadata.tables.keys())}")


if __name__ == '__main__':
    init_database()
