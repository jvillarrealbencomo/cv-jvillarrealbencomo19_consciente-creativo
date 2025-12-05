"""
Database Initialization Script
Version 2025 - Creates all tables with proper schema
"""
import os
from app import create_app, db

def init_database(confirm=True):
    """Initialize database with all tables"""
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    with app.app_context():
        if confirm:
            print("⚠️  WARNING: This will DELETE all existing data!")
            response = input("Type 'YES' to confirm: ")
            if response != 'YES':
                print("Cancelled.")
                return
        
        print("Dropping all existing tables...")
        db.drop_all()
        
        print("Creating all tables from models...")
        db.create_all()
        
        print("✓ Database initialized successfully!")
        print(f"Tables created: {', '.join(db.metadata.tables.keys())}")

if __name__ == '__main__':
    init_database()
