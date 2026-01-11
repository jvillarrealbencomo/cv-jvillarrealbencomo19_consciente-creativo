"""
Generate PDF CV

Modes:
- export (default): multi-page, full content (no trimming)
- one-page: auto-optimized to ~1 page
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Person
from app.services.pdf_generator import PDFGenerator
from app.routes.profiles import get_profile_data_dict


def generate_pdf(profile_name='qa_engineer', mode='export'):
    """Generate a PDF for the specified profile.

    mode:
        - 'export': include inactive, multi-page (auto_optimize=False)
        - 'one-page': active only, auto_optimize=True
    """
    app = create_app()
    one_page = (mode == 'one-page')
    include_inactive = not one_page

    with app.app_context():
        person = Person.query.filter_by(active=True, is_historical=False).first()
        if not person:
            print("❌ No active person found in database")
            return

        print(f"✓ Found person: {person.full_name}")
        print(f"✓ Profile: {profile_name}")
        print(f"✓ Mode: {mode}")

        profile_data = get_profile_data_dict(person.id, profile_name, include_inactive=include_inactive)

        print("✓ Generating PDF...")
        pdf_bytes = PDFGenerator.generate_cv_pdf(
            profile_data,
            profile_name,
            auto_optimize=one_page
        )

        suffix = '_onepage' if one_page else '_export'
        filename = f"CV_{person.first_name}_{person.last_name}_{profile_name}{suffix}.pdf"
        output_path = os.path.join('app', 'generated_pdfs', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)

        print(f"✅ PDF generated: {output_path}")
        print(f"📏 Auto-optimization: {'ENABLED (~1 page)' if one_page else 'DISABLED (multi-page)'}")
        return output_path


if __name__ == '__main__':
    profile = 'qa_engineer'
    mode = 'export'

    # Usage: python generate_pdf.py [profile] [mode]
    # mode: export | one-page
    if len(sys.argv) >= 2:
        profile = sys.argv[1]
    if len(sys.argv) >= 3:
        mode = sys.argv[2]

    print("=" * 60)
    print("PDF Generator")
    print("=" * 60)

    try:
        output = generate_pdf(profile, mode)
        print("\n✅ Success!")
        print(f"Open the PDF: {output}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
