"""
Update AdvancedTraining record 3 - Set description to None
"""
from app import create_app, db
from app.models import AdvancedTraining

app = create_app()

with app.app_context():
    # Get record 3
    record3 = db.session.get(AdvancedTraining, 3)
    
    if record3:
        print(f"\n=== Updating AdvancedTraining Record 3 ===")
        print(f"Name: {record3.name}")
        print(f"Before - description: {record3.description}")
        
        # Update description to None
        record3.description = None
        db.session.commit()
        
        print(f"After - description: {record3.description}")
        print("\n✅ Record 3 updated successfully!")
    else:
        print("❌ Record 3 not found")
