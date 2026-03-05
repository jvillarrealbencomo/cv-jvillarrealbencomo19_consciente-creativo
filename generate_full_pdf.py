"""
Generate complete multi-page PDF CV without page restrictions
"""
import sys
from app import create_app, db
from app.models.personal_data import Person
from app.routes.profiles import get_profile_data_dict
from app.services.pdf_generator import PDFGenerator

def generate_full_pdf(profile_name):
    """Generate complete PDF for a profile without page restrictions"""
    app = create_app()
    
    with app.app_context():
        # Get person data
        person = Person.query.first()
        if not person:
            print("❌ Error: No person found in database")
            return None
        
        print(f"✓ Found person: {person.full_name}")
        print(f"✓ Generating complete PDF for profile: {profile_name}")
        
        # Get profile data
        profile_data = get_profile_data_dict(person.id, profile_name)
        
        # Generate PDF WITHOUT auto-optimization (allows multiple pages)
        print("✓ Generating complete multi-page PDF...")
        try:
            pdf_bytes = PDFGenerator.generate_cv_pdf(
                profile_data=profile_data,
                profile_name=profile_name,
                auto_optimize=False  # DISABLED - allows full content across multiple pages
            )
            
            # Save PDF
            filename = f"CV_{person.full_name.replace(' ', '_')}_{profile_name}_complete.pdf"
            output_path = f"app/generated_pdfs/{filename}"
            
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
            
            print(f"\n✅ Complete PDF generated successfully!")
            print(f"📄 File saved to: {output_path}")
            print(f"📏 Page limit: NONE (complete content)")
            
            return output_path
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    print("=" * 60)
    print("Complete Multi-Page PDF Generator")
    print("=" * 60)
    
    # Get profile from command line or default to qa_engineer
    profile = sys.argv[1] if len(sys.argv) > 1 else "qa_engineer"
    
    output = generate_full_pdf(profile)
    
    if output:
        print(f"\n✅ Success!")
        print(f"Open the PDF: {output}")
    else:
        print("\n❌ Failed to generate PDF")
        sys.exit(1)
