"""
Generate One-Page PDF CV
Quick script to generate a PDF CV with auto-optimization
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Person
from app.services.pdf_generator import PDFGenerator
from app.routes.profiles import get_profile_data_dict

def generate_one_page_pdf(profile_name='qa_engineer'):
    """Generate a one-page PDF for the specified profile"""
    app = create_app()
    
    with app.app_context():
        # Get the first active person
        person = Person.query.filter_by(active=True, is_historical=False).first()
        
        if not person:
            print("❌ No active person found in database")
            return
        
        print(f"✓ Found person: {person.full_name}")
        print(f"✓ Generating PDF for profile: {profile_name}")
        
        # Get profile data
        profile_data = get_profile_data_dict(person.id, profile_name)
        
        # Generate PDF with auto-optimization enabled
        print("✓ Generating PDF with auto-optimization (one-page guarantee)...")
        pdf_bytes = PDFGenerator.generate_cv_pdf(
            profile_data, 
            profile_name, 
            auto_optimize=True  # Enable one-page optimization
        )
        
        # Save to file
        filename = f"CV_{person.first_name}_{person.last_name}_{profile_name}_onepage.pdf"
        output_path = os.path.join('app', 'generated_pdfs', filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF generated successfully!")
        print(f"📄 File saved to: {output_path}")
        print(f"📏 Auto-optimization: ENABLED (guarantees one page)")
        
        return output_path

if __name__ == '__main__':
    profile = sys.argv[1] if len(sys.argv) > 1 else 'qa_engineer'
    
    print("=" * 60)
    print("One-Page PDF Generator")
    print("=" * 60)
    
    try:
        output = generate_one_page_pdf(profile)
        print("\n✅ Success!")
        print(f"Open the PDF: {output}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
