"""
Update AdvancedTraining display_order values - December 2025
"""
from app import create_app, db
from app.models import AdvancedTraining

app = create_app()

# Desired display_order values per record id
TARGETS = {
    1: 4,
    2: 0,
    3: 1,
    4: 0,
    5: 2,
    6: 3,
}

with app.app_context():
    print("\n=== Updating AdvancedTraining display_order ===\n")
    for rec_id, new_order in TARGETS.items():
        record = db.session.get(AdvancedTraining, rec_id)
        if not record:
            print(f"❌ Record {rec_id} not found")
            continue
        old_order = record.display_order
        record.display_order = new_order
        print(f"Record {rec_id} ({record.name})")
        print(f"  Before: {old_order}")
        print(f"  After:  {new_order}\n")

    db.session.commit()
    print("✅ All requested display_order updates applied!\n")
