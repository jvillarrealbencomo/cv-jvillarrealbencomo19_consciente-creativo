"""
Update API to Version 2 - Production Release
This script updates the app_metadata table with version 2.0 information
Date: 2026-02-20
"""
from app import create_app, db
from app.models.app_metadata import AppMetadata
from datetime import datetime

def update_to_version_2():
    """Update API to version 2 for production deployment"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("API Version Update Script - Version 2.0")
        print("=" * 60)
        print()
        
        # Define the new version metadata
        updates = [
            {
                'key': 'application_version',
                'value': '2026.2.0',
                'description': 'Updated application version to 2.0'
            },
            {
                'key': 'api_version',
                'value': 'v2',
                'description': 'New API version identifier'
            },
            {
                'key': 'api_release_date',
                'value': '2026-02-20',
                'description': 'API v2 production release date'
            },
            {
                'key': 'api_status',
                'value': 'production',
                'description': 'Deployment status'
            }
        ]
        
        print("Current Metadata:")
        print("-" * 60)
        existing_metadata = AppMetadata.query.all()
        for entry in existing_metadata:
            print(f"  {entry.key}: {entry.value}")
        print()
        
        print("Applying Updates:")
        print("-" * 60)
        
        updated_count = 0
        added_count = 0
        
        for update_info in updates:
            key = update_info['key']
            new_value = update_info['value']
            description = update_info['description']
            
            entry = AppMetadata.query.filter_by(key=key).first()
            
            if entry:
                # Update existing
                old_value = entry.value
                entry.value = new_value
                entry.updated_at = datetime.utcnow()
                print(f"  ✓ Updated '{key}': '{old_value}' → '{new_value}'")
                print(f"    ({description})")
                updated_count += 1
            else:
                # Add new
                new_entry = AppMetadata(key=key, value=new_value)
                db.session.add(new_entry)
                print(f"  ✓ Added '{key}': '{new_value}'")
                print(f"    ({description})")
                added_count += 1
        
        # Commit changes
        try:
            db.session.commit()
            print()
            print("=" * 60)
            print("SUCCESS!")
            print("=" * 60)
            print(f"  Records Updated: {updated_count}")
            print(f"  Records Added: {added_count}")
            print()
            
            print("Updated Metadata:")
            print("-" * 60)
            updated_metadata = AppMetadata.query.all()
            for entry in updated_metadata:
                print(f"  {entry.key}: {entry.value}")
                print(f"    (Last updated: {entry.updated_at})")
            print()
            print("API successfully updated to Version 2!")
            print("=" * 60)
            
        except Exception as e:
            db.session.rollback()
            print()
            print("ERROR: Failed to commit changes")
            print(f"  {str(e)}")
            print()
            return False
    
    return True


if __name__ == '__main__':
    success = update_to_version_2()
    exit(0 if success else 1)
