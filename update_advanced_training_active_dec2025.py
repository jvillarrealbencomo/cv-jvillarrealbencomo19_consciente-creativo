"""
Update AdvancedTraining active flags - December 2025
"""
from app import create_app, db
from app.models import AdvancedTraining

app = create_app()

TARGETS = {
    2: False,
    4: False,
}

with app.app_context():
    print("\n=== Updating AdvancedTraining active flags ===\n")
    for rec_id, new_flag in TARGETS.items():
        record = db.session.get(AdvancedTraining, rec_id)
        if not record:
            print(f"❌ Record {rec_id} not found")
            continue
        old_flag = getattr(record, 'active', None)
        record.active = new_flag
        print(f"Record {rec_id} ({record.name})")
        print(f"  Before: {old_flag}")
        print(f"  After:  {new_flag}\n")

    db.session.commit()
    print("✅ All requested active updates applied!\n")
