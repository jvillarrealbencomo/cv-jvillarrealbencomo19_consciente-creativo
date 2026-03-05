"""Debug script to check PDF data issues"""
from app import create_app, db
from app.models.work_experience import WorkExperience
from app.models.advanced_training import AdvancedTraining
from app.routes.profiles import get_profile_data_dict

app = create_app()

with app.app_context():
    print("=" * 80)
    print("ISSUE 1: Work Experience Export PDF missing 4 records")
    print("=" * 80)
    
    # Get data for Export PDF (include_inactive=True)
    profile_data = get_profile_data_dict(1, 'qa_engineer', include_inactive=True)
    work_exp = profile_data['work_experience']
    
    print(f"\nExport PDF Work Experience count: {len(work_exp)}")
    print("\nRecords included:")
    for i, exp in enumerate(work_exp, 1):
        print(f"{i}. ID {exp['id']}: {exp['company']} - {exp['job_title']}")
    
    # Check all records
    all_exps = WorkExperience.query.order_by(WorkExperience.id).all()
    print(f"\n\nTotal Work Experience in database: {len(all_exps)}")
    print(f"Active: {sum(1 for e in all_exps if e.active)}")
    print(f"Visible for qa_engineer: {sum(1 for e in all_exps if e.visible_qa_engineer)}")
    print(f"Historical: {sum(1 for e in all_exps if e.is_historical)}")
    
    print("\n\nAll records:")
    for exp in all_exps:
        status = []
        if not exp.active:
            status.append("INACTIVE")
        if exp.is_historical:
            status.append("HISTORICAL")
        if not exp.visible_qa_engineer:
            status.append("NOT_VISIBLE_QA_ENG")
        status_str = " | ".join(status) if status else "OK"
        print(f"ID {exp.id}: {exp.company[:30]:30} - {status_str}")
    
    print("\n" + "=" * 80)
    print("ISSUE 2: Advanced Training - English B2 appearing incorrectly")
    print("=" * 80)
    
    training = AdvancedTraining.query.order_by(AdvancedTraining.id).all()
    print("\nAdvanced Training Records:")
    for t in training:
        print(f"ID {t.id}: Name=[{t.name}] | Provider=[{t.provider}] | Type={t.type} | Active={t.active}")
    
    print("\n" + "=" * 80)
    print("ISSUE 3: Form routing for Advanced Training edit")
    print("=" * 80)
    print("\nChecking forms routing...")
    print("Record ID 9:")
    rec9 = AdvancedTraining.query.get(9)
    if rec9:
        print(f"  Type: {rec9.type}")
        print(f"  Name: {rec9.name}")
        print(f"  Route should be: forms.{'certification_form' if rec9.type == 'certification' else 'course_form'}")
