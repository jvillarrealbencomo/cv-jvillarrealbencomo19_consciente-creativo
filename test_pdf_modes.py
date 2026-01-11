"""
Test PDF Export Modes - Verify include_inactive parameter behavior
Run this script to test both Export PDF and One-Page PDF modes
"""

from app import create_app, db
from app.routes.profiles import get_profile_data_dict
from app.models.work_experience import WorkExperience
from app.models.advanced_training import AdvancedTraining

app = create_app()

def test_export_modes():
    """Test both PDF export modes"""
    with app.app_context():
        person_id = 1
        profile_name = 'qa_engineer'
        
        print("=" * 80)
        print("PDF EXPORT MODES TEST")
        print("=" * 80)
        
        # Test Export PDF mode (include_inactive=True)
        print("\n1. EXPORT PDF MODE (include_inactive=True)")
        print("-" * 80)
        data_export = get_profile_data_dict(person_id, profile_name, include_inactive=True)
        
        work_exp_export = data_export['work_experience']
        training_export = data_export['advanced_training']
        
        print(f"Work Experience Records: {len(work_exp_export)}")
        print(f"Advanced Training Records: {len(training_export)}")
        
        # Count active vs inactive
        work_active = sum(1 for exp in work_exp_export if exp.get('active', True))
        work_inactive = len(work_exp_export) - work_active
        
        training_active = sum(1 for t in training_export if t.get('active', True))
        training_inactive = len(training_export) - training_active
        
        print(f"\nWork Experience Breakdown:")
        print(f"  - Active: {work_active}")
        print(f"  - Inactive: {work_inactive}")
        
        print(f"\nAdvanced Training Breakdown:")
        print(f"  - Active: {training_active}")
        print(f"  - Inactive: {training_inactive}")
        
        # Test One-Page PDF mode (include_inactive=False)
        print("\n\n2. ONE-PAGE PDF MODE (include_inactive=False)")
        print("-" * 80)
        data_onepage = get_profile_data_dict(person_id, profile_name, include_inactive=False)
        
        work_exp_onepage = data_onepage['work_experience']
        training_onepage = data_onepage['advanced_training']
        
        print(f"Work Experience Records: {len(work_exp_onepage)}")
        print(f"Advanced Training Records: {len(training_onepage)}")
        
        print(f"\nAll records should have active=True and is_historical=False")
        
        # Verify filtering
        for exp in work_exp_onepage:
            if not exp.get('active', True) or exp.get('is_historical', False):
                print(f"  ⚠ WARNING: Found filtered record: {exp['job_title']}")
        
        for t in training_onepage:
            if not t.get('active', True) or t.get('is_historical', False):
                print(f"  ⚠ WARNING: Found filtered record: {t['name']}")
        
        # Compare modes
        print("\n\n3. COMPARISON")
        print("-" * 80)
        print(f"Work Experience:")
        print(f"  Export PDF:   {len(work_exp_export)} records")
        print(f"  One-Page PDF: {len(work_exp_onepage)} records")
        print(f"  Difference:   {len(work_exp_export) - len(work_exp_onepage)} records")
        
        print(f"\nAdvanced Training:")
        print(f"  Export PDF:   {len(training_export)} records")
        print(f"  One-Page PDF: {len(training_onepage)} records")
        print(f"  Difference:   {len(training_export) - len(training_onepage)} records")
        
        # Expected behavior
        print("\n\n4. EXPECTED BEHAVIOR")
        print("-" * 80)
        print("✓ Export PDF should include ALL records (active=True AND active=False)")
        print("✓ One-Page PDF should include only active=True, is_historical=False records")
        print("✓ Export PDF count >= One-Page PDF count")
        
        # Validation
        print("\n\n5. VALIDATION")
        print("-" * 80)
        
        work_valid = len(work_exp_export) >= len(work_exp_onepage)
        training_valid = len(training_export) >= len(training_onepage)
        
        print(f"Work Experience: {'✓ PASS' if work_valid else '✗ FAIL'}")
        print(f"Advanced Training: {'✓ PASS' if training_valid else '✗ FAIL'}")
        
        if work_valid and training_valid:
            print("\n✓ All tests passed! PDF export modes working correctly.")
        else:
            print("\n✗ Tests failed! Check implementation.")
        
        print("\n" + "=" * 80)

if __name__ == '__main__':
    test_export_modes()
