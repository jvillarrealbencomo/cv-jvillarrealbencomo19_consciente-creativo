"""Check which work experience records are being excluded"""
from app import create_app, db
from app.models.work_experience import WorkExperience
from app.routes.profiles import get_profile_data_dict

app = create_app()

with app.app_context():
    print("Checking Work Experience filtering for Export PDF")
    print("=" * 80)
    
    # Get all records
    all_records = WorkExperience.query.order_by(WorkExperience.id).all()
    print(f"\nTotal records in database: {len(all_records)}")
    
    # Get Export PDF data (include_inactive=True)
    export_data = get_profile_data_dict(1, 'qa_engineer', include_inactive=True)
    export_ids = [exp['id'] for exp in export_data['work_experience']]
    print(f"Records in Export PDF: {len(export_ids)}")
    print(f"Export PDF IDs: {sorted(export_ids)}")
    
    # Check which are missing
    all_ids = [exp.id for exp in all_records]
    missing_ids = set(all_ids) - set(export_ids)
    
    if missing_ids:
        print(f"\n❌ MISSING from Export PDF: {sorted(missing_ids)}")
        print("\nDetails of missing records:")
        for missing_id in sorted(missing_ids):
            rec = db.session.get(WorkExperience, missing_id)
            print(f"\nID {rec.id}: {rec.company} - {rec.job_title}")
            print(f"  Active: {rec.active}")
            print(f"  Historical: {rec.is_historical}")
            print(f"  Visible QA Engineer: {rec.visible_qa_engineer}")
            print(f"  Time Block: {rec.time_block}")
    else:
        print("\n✓ All records are included in Export PDF")
    
    # Get One-Page PDF data (include_inactive=False)
    onepage_data = get_profile_data_dict(1, 'qa_engineer', include_inactive=False)
    onepage_ids = [exp['id'] for exp in onepage_data['work_experience']]
    print(f"\n\nRecords in One-Page PDF: {len(onepage_ids)}")
    print(f"One-Page PDF IDs: {sorted(onepage_ids)}")
    
    excluded = set(all_ids) - set(onepage_ids)
    if excluded:
        print(f"\n✓ Correctly excluded from One-Page PDF: {sorted(excluded)}")
