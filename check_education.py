"""
Helper script to check education records and link manually copied images
"""
import os
from app import create_app, db
from app.models import Education

app = create_app()

with app.app_context():
    print("=== EDUCATION RECORDS IN DATABASE ===")
    educations = Education.query.filter_by(active=True).order_by(Education.id).all()
    
    if not educations:
        print("No education records found!")
    else:
        for edu in educations:
            print(f"\nID: {edu.id}")
            print(f"  Degree: {edu.degree}")
            print(f"  Institution: {edu.institution}")
            print(f"  Country: {edu.country}")
            print(f"  Year: {edu.year_obtained}")
            print(f"  Image Path: {edu.image_path}")
            print(f"  Thumbnail: {edu.image_thumbnail_path}")
    
    print("\n\n=== IMAGES IN uploads/education FOLDER ===")
    img_dir = os.path.join(app.static_folder, 'uploads', 'education')
    
    if os.path.exists(img_dir):
        files = [f for f in os.listdir(img_dir) if not f.startswith('.')]
        if files:
            for f in sorted(files):
                print(f"  - {f}")
        else:
            print("  (folder is empty)")
    else:
        print("  (folder does not exist)")
    
    print(f"\n\nTotal education records: {len(educations)}")
