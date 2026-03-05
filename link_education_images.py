"""
Link manually copied education images to database records
Run this once to associate existing images with education records
"""
import os
from app import create_app, db
from app.models import Education
from app.services.image_service import ImageService
from PIL import Image

app = create_app()

# Manual mapping: education_id -> image filename
MAPPINGS = {
    1: "Doctor_en Ciencias_de_la_Educacion.jpg",  # PhD in Educational Sciences
    2: "ingeniero_de_sistemas.jpg",                # Systems Engineer
    3: "magister_scientaurum.jpg"                  # Master's Degree
}

with app.app_context():
    static_root = app.static_folder
    upload_dir = os.path.join(static_root, 'uploads', 'education')
    
    for edu_id, filename in MAPPINGS.items():
        edu = db.session.get(Education, edu_id)
        if not edu:
            print(f"⚠️  Education ID {edu_id} not found, skipping")
            continue
        
        src_path = os.path.join(upload_dir, filename)
        if not os.path.exists(src_path):
            print(f"⚠️  Image not found: {filename}, skipping")
            continue
        
        # Build proper paths using ImageService naming convention
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = os.path.splitext(filename)[1].lower()
        
        new_filename = f"education_{edu_id}_{ts}{ext}"
        dest_path = os.path.join(upload_dir, new_filename)
        
        # Copy file to proper name
        import shutil
        shutil.copy2(src_path, dest_path)
        
        # Generate thumbnail
        thumb_filename = f"education_{edu_id}_{ts}_thumb.jpg"
        thumb_path = os.path.join(upload_dir, thumb_filename)
        
        try:
            with Image.open(dest_path) as img:
                img.thumbnail(ImageService.THUMBNAIL_SIZE)
                img.convert("RGB").save(thumb_path, "JPEG", quality=85)
        except Exception as e:
            print(f"⚠️  Failed to generate thumbnail for {new_filename}: {e}")
            thumb_filename = None
        
        # Update database
        edu.image_path = f"uploads/education/{new_filename}"
        edu.image_thumbnail_path = f"uploads/education/{thumb_filename}" if thumb_filename else None
        edu.image_filename = filename
        edu.image_mime_type = "image/jpeg"
        
        print(f"✓ Linked {filename} to {edu.degree} (ID: {edu_id})")
    
    db.session.commit()
    print("\n✓ All images linked successfully!")
    
    print("\n=== UPDATED RECORDS ===")
    for edu in Education.query.filter_by(active=True).order_by(Education.id).all():
        print(f"{edu.id}: {edu.degree}")
        print(f"   Image: {edu.image_path}")
        print(f"   Thumb: {edu.image_thumbnail_path}")
