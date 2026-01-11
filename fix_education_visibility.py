"""
Fix education visibility - ensure all degrees are visible in all profiles
"""
from app import create_app, db
from app.models import Education

app = create_app()

with app.app_context():
    print("=== BEFORE FIX ===")
    educations = Education.query.filter_by(active=True).order_by(Education.id).all()
    for edu in educations:
        print(f"\nID: {edu.id} - {edu.degree}")
        print(f"  QA Analyst: {edu.visible_qa_analyst}")
        print(f"  QA Engineer: {edu.visible_qa_engineer}")
        print(f"  Data Scientist: {edu.visible_data_scientist}")
    
    print("\n\n=== FIXING VISIBILITY ===")
    # Set all education records visible to all profiles
    for edu in educations:
        edu.visible_qa_analyst = True
        edu.visible_qa_engineer = True
        edu.visible_data_scientist = True
        print(f"✓ Fixed: {edu.degree}")
    
    db.session.commit()
    
    print("\n\n=== AFTER FIX ===")
    educations = Education.query.filter_by(active=True).order_by(Education.id).all()
    for edu in educations:
        print(f"\nID: {edu.id} - {edu.degree}")
        print(f"  QA Analyst: {edu.visible_qa_analyst}")
        print(f"  QA Engineer: {edu.visible_qa_engineer}")
        print(f"  Data Scientist: {edu.visible_data_scientist}")
    
    print("\n✓ All education records are now visible in all profiles!")
