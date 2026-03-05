"""
Migration: Merge Certification and Course tables into AdvancedTraining
"""
import os
from datetime import datetime
from app import create_app, db
from app.models import Certification, Course, AdvancedTraining

def migrate():
    """Merge Certification and Course into AdvancedTraining"""
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    with app.app_context():
        try:
            # Create new table
            print("Creating advanced_training table...")
            db.create_all()
            
            # Migrate certifications
            print("Migrating certifications...")
            certs = Certification.query.all()
            for cert in certs:
                training = AdvancedTraining()
                training.type = 'Certification'
                training.name = cert.name
                training.provider = cert.issuing_organization
                training.completion_date = cert.issue_date
                training.description = cert.description
                training.expiration_date = cert.expiration_date
                training.credential_id = cert.credential_id
                training.credential_url = cert.credential_url
                training.display_order = getattr(cert, 'display_order', 0)
                training.active = cert.active
                training.is_historical = cert.is_historical
                training.visible_qa_analyst = cert.visible_qa_analyst
                training.visible_qa_engineer = cert.visible_qa_engineer
                training.visible_data_scientist = cert.visible_data_scientist
                training.created_at = cert.created_at
                training.updated_at = cert.updated_at
                db.session.add(training)
            print(f"  Migrated {len(certs)} certifications")
            
            # Migrate courses
            print("Migrating courses...")
            courses = Course.query.all()
            for course in courses:
                training = AdvancedTraining()
                training.type = 'Course'
                training.name = course.name
                training.provider = course.provider
                training.completion_date = course.completion_date
                training.description = course.description
                training.duration_hours = course.duration_hours
                training.display_order = getattr(course, 'display_order', 0)
                training.active = course.active
                training.is_historical = course.is_historical
                training.visible_qa_analyst = course.visible_qa_analyst
                training.visible_qa_engineer = course.visible_qa_engineer
                training.visible_data_scientist = course.visible_data_scientist
                training.created_at = course.created_at
                training.updated_at = course.updated_at
                db.session.add(training)
            print(f"  Migrated {len(courses)} courses")
            
            # Commit new data
            db.session.commit()
            print("✓ Data migrated successfully!")
            
            # Drop old tables
            print("\nDropping old tables...")
            print("  WARNING: About to drop certification and course tables")
            response = input("Type 'YES' to confirm: ")
            if response == 'YES':
                db.session.execute(db.text("DROP TABLE IF EXISTS certification;"))
                db.session.execute(db.text("DROP TABLE IF EXISTS course;"))
                db.session.commit()
                print("✓ Old tables dropped")
            else:
                print("Skipped dropping tables. You can drop them manually later.")
            
            print("\n✓ Migration completed!")
            print(f"  Total records in advanced_training: {AdvancedTraining.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Migration error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    migrate()
