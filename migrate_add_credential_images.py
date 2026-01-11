"""
Migration: Add credential image fields to education and advanced_training tables.
Run once after deploying the cv2025-credential-images changes.
"""
import os
from app import create_app, db


STATEMENTS = [
    # Education
    "ALTER TABLE education ADD COLUMN image_path VARCHAR(500);",
    "ALTER TABLE education ADD COLUMN image_thumbnail_path VARCHAR(500);",
    "ALTER TABLE education ADD COLUMN image_filename VARCHAR(255);",
    "ALTER TABLE education ADD COLUMN image_mime_type VARCHAR(50);",
    # Advanced Training
    "ALTER TABLE advanced_training ADD COLUMN image_path VARCHAR(500);",
    "ALTER TABLE advanced_training ADD COLUMN image_thumbnail_path VARCHAR(500);",
    "ALTER TABLE advanced_training ADD COLUMN image_filename VARCHAR(255);",
    "ALTER TABLE advanced_training ADD COLUMN image_mime_type VARCHAR(50);",
]


def migrate():
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                for stmt in STATEMENTS:
                    try:
                        conn.execute(db.text(stmt))
                    except Exception as e:
                        # Column may already exist; log and continue
                        print(f"Skip statement '{stmt}': {e}")
                conn.commit()
            print("✓ Migration completed: credential image columns added (if missing).")
        except Exception as e:
            print(f"Migration failed: {e}")


if __name__ == '__main__':
    migrate()
