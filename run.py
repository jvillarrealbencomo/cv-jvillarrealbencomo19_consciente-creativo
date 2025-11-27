"""
Main application entry point
Run this file to start the Flask development server
"""
import os
from app import create_app, db

# Get configuration from environment or default to development
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell"""
    from app.models import (PersonalData, Education, WorkExperience, ITProduct,
                            Certification, Course, Language, SupportTool)
    
    return {
        'db': db,
        'PersonalData': PersonalData,
        'Education': Education,
        'WorkExperience': WorkExperience,
        'ITProduct': ITProduct,
        'Certification': Certification,
        'Course': Course,
        'Language': Language,
        'SupportTool': SupportTool
    }


@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('✓ Database initialized')


@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    from init_db import seed_data
    seed_data()
    print('✓ Database seeded')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
