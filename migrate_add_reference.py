"""
Migration: Add reference fields to Person table
"""
import os
from app import create_app, db

def migrate():
    """Add reference fields to person table"""
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    with app.app_context():
        try:
            # Add columns using raw SQL
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE person ADD COLUMN reference_name VARCHAR(200);"))
                conn.execute(db.text("ALTER TABLE person ADD COLUMN reference_company VARCHAR(200);"))
                conn.execute(db.text("ALTER TABLE person ADD COLUMN reference_phone VARCHAR(50);"))
                conn.commit()
            
            print("✓ Migration completed successfully!")
            print("Added 3 reference fields to person table.")
            
        except Exception as e:
            print(f"Migration error: {e}")
            print("Note: If columns already exist, this is normal.")

if __name__ == '__main__':
    migrate()
