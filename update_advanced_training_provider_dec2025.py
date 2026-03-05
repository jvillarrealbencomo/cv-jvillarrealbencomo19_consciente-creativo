"""
Update AdvancedTraining record 1 provider - December 2025
"""
from app import create_app, db
from app.models import AdvancedTraining

app = create_app()

with app.app_context():
    print("\n=== Updating AdvancedTraining Record 1 Provider ===\n")
    
    record1 = db.session.get(AdvancedTraining, 1)
    if record1:
        old_provider = record1.provider
        record1.provider = "UNESR"
        db.session.commit()
        
        print(f"Record 1: {record1.name}")
        print(f"  Before: {old_provider}")
        print(f"  After:  {record1.provider}\n")
        print("✅ Provider updated successfully!")
    else:
        print("❌ Record 1 not found")
