"""
Populate Evidence Hub Entries
"""
from app import create_app, db
from app.models.evidence_hub import EvidenceHubEntry

def populate_evidence_hub():
    """Populate evidence hub with default entries"""
    app = create_app()
    
    with app.app_context():
        defaults = [
            {
                'slug': 'qa-ui-automation',
                'title': 'UI / Automation: Selenium & Cucumber',
                'stack': 'Java · Selenium · Cucumber · Gherkin · BDD',
                'description': 'Comprehensive UI test validation executed through structured automation suites. Includes reproducible test runs, and documented validation workflows',
                'display_order': 1
            },
            {
                'slug': 'api-automation',
                'title': 'API Automation: Postman & Newman',
                'stack': 'Postman · Newman · JSON · Contract Validation · Deterministic Testing',
                'description': 'Demonstrates deterministic contract validation of critical analytical endpoints, ensuring structural integrity, reproducible execution, and reliability of the analytical engine',
                'display_order': 2
            },
            {
                'slug': 'data-science',
                'title': 'Data & Market Insights (API-driven)',
                'stack': 'Python · Pandas · REST APIs · Analytical Modeling · Multi-Dataset Evaluation',
                'description': 'Demonstrates how CV data is processed through a deterministic analytical engine that cross-references multiple public market datasets, computes a reproducible readiness score, and exposes structured results via REST APIs',
                'display_order': 3
            },
        ]

        for item in defaults:
            # Remove duplicates
            duplicates = EvidenceHubEntry.query.filter_by(slug=item['slug']).all()
            for duplicate in duplicates[1:]:
                db.session.delete(duplicate)

            # Update or insert entry
            entry = EvidenceHubEntry.query.filter_by(slug=item['slug']).first()
            if entry:
                entry.title = item['title']
                entry.stack = item['stack']
                entry.description = item['description']
                entry.display_order = item['display_order']
                print(f"✓ Updated: {item['slug']}")
            else:
                db.session.add(EvidenceHubEntry(**item))
                print(f"✓ Created: {item['slug']}")
        
        db.session.commit()
        print("\n✓ Evidence Hub populated successfully!")
        
        # Display entries
        print("\nCurrent entries:")
        entries = EvidenceHubEntry.query.order_by(EvidenceHubEntry.display_order).all()
        for e in entries:
            print(f"  {e.display_order}. {e.title}")
            print(f"     Stack: {e.stack}")
            print(f"     Description: {e.description}\n")

if __name__ == '__main__':
    populate_evidence_hub()
