"""
Import JSON Data to PostgreSQL
Imports CV data exported from SQLite
"""
import json
import sys
from datetime import datetime
from app import create_app, db
from app.models import (
    Person, WorkExperience, Education, AdvancedTraining,
    TechnicalTool, Language, ITProduct
)

def import_data(filename='cv_data_export.json'):
    """Import all database records from JSON"""
    app = create_app()
    
    with app.app_context():
        # Read JSON file
        print(f"📂 Reading {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Export date: {data['export_date']}")
        print(f"✅ Export version: {data['export_version']}")
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("\n⚠️  Clearing existing data...")
        ITProduct.query.delete()
        Language.query.delete()
        TechnicalTool.query.delete()
        AdvancedTraining.query.delete()
        Education.query.delete()
        WorkExperience.query.delete()
        Person.query.delete()
        db.session.commit()
        
        # Import Persons
        print("\n📥 Importing Persons...")
        for p_data in data['persons']:
            person = Person(
                full_name=p_data['full_name'],
                professional_title=p_data['professional_title'],
                email=p_data['email'],
                phone=p_data['phone'],
                location=p_data['location'],
                linkedin_url=p_data['linkedin_url'],
                github_url=p_data['github_url'],
                personal_url=p_data['personal_url'],
                title_qa_analyst=p_data['title_qa_analyst'],
                title_qa_engineer=p_data['title_qa_engineer'],
                title_data_scientist=p_data['title_data_scientist'],
                summary_qa_analyst=p_data['summary_qa_analyst'],
                summary_qa_engineer=p_data['summary_qa_engineer'],
                summary_data_scientist=p_data['summary_data_scientist'],
                reference_name=p_data['reference_name'],
                reference_company=p_data['reference_company'],
                reference_phone=p_data['reference_phone'],
                profile_image_url=p_data['profile_image_url'],
                show_email=p_data['show_email'],
                show_phone=p_data['show_phone'],
                show_linkedin=p_data['show_linkedin'],
                show_github=p_data['show_github'],
                show_personal_url=p_data['show_personal_url'],
            )
            db.session.add(person)
        db.session.commit()
        print(f"   ✅ {len(data['persons'])} persons imported")
        
        # Import Work Experiences
        print("📥 Importing Work Experiences...")
        for exp_data in data['work_experiences']:
            exp = WorkExperience(
                job_title=exp_data['job_title'],
                company=exp_data['company'],
                location=exp_data['location'],
                start_date=datetime.fromisoformat(exp_data['start_date']) if exp_data['start_date'] else None,
                end_date=datetime.fromisoformat(exp_data['end_date']) if exp_data['end_date'] else None,
                is_current=exp_data.get('is_current', False),
                time_block=exp_data['time_block'],
                responsibilities_summary=exp_data['responsibilities_summary'],
                responsibilities_detailed=exp_data['responsibilities_detailed'],
                achievements=exp_data.get('achievements', exp_data.get('key_achievements')),
                show_responsibilities_summary=exp_data['show_responsibilities_summary'],
                show_responsibilities_detailed=exp_data['show_responsibilities_detailed'],
                show_achievements=exp_data.get('show_achievements', exp_data.get('show_key_achievements', True)),
                technologies=exp_data.get('technologies'),
                active=exp_data['active'],
                is_historical=exp_data['is_historical'],
                display_order=exp_data['display_order'],
                visible_qa_analyst=exp_data['visible_qa_analyst'],
                visible_qa_engineer=exp_data['visible_qa_engineer'],
                visible_data_scientist=exp_data['visible_data_scientist'],
            )
            db.session.add(exp)
        db.session.commit()
        print(f"   ✅ {len(data['work_experiences'])} work experiences imported")
        
        # Import Education
        print("📥 Importing Education...")
        for edu_data in data['education']:
            edu = Education(
                degree=edu_data['degree'],
                institution=edu_data['institution'],
                country=edu_data.get('country'),
                year_obtained=edu_data.get('year_obtained'),
                start_year=edu_data.get('start_year'),
                end_year=edu_data.get('end_year'),
                is_current=edu_data.get('is_current', False),
                details=edu_data.get('details'),
                document_url=edu_data.get('document_url'),
                image_path=edu_data['image_path'],
                image_thumbnail_path=edu_data['image_thumbnail_path'],
                image_filename=edu_data['image_filename'],
                image_mime_type=edu_data['image_mime_type'],
                active=edu_data['active'],
                display_order=edu_data['display_order'],
                visible_qa_analyst=edu_data['visible_qa_analyst'],
                visible_qa_engineer=edu_data['visible_qa_engineer'],
                visible_data_scientist=edu_data['visible_data_scientist'],
            )
            db.session.add(edu)
        db.session.commit()
        print(f"   ✅ {len(data['education'])} education records imported")
        
        # Import Advanced Training
        print("📥 Importing Advanced Training...")
        for train_data in data['advanced_training']:
            training = AdvancedTraining(
                type=train_data['type'],
                name=train_data['name'],
                provider=train_data['provider'],
                completion_date=datetime.fromisoformat(train_data['completion_date']) if train_data.get('completion_date') else None,
                description=train_data.get('description'),
                expiration_date=datetime.fromisoformat(train_data['expiration_date']) if train_data.get('expiration_date') else None,
                credential_id=train_data.get('credential_id'),
                credential_url=train_data.get('credential_url'),
                duration_hours=train_data.get('duration_hours'),
                image_path=train_data.get('image_path'),
                image_thumbnail_path=train_data.get('image_thumbnail_path'),
                image_filename=train_data.get('image_filename'),
                image_mime_type=train_data.get('image_mime_type'),
                active=train_data.get('active', True),
                display_order=train_data.get('display_order', 0),
                visible_qa_analyst=train_data.get('visible_qa_analyst', True),
                visible_qa_engineer=train_data.get('visible_qa_engineer', True),
                visible_data_scientist=train_data.get('visible_data_scientist', True),
            )
            db.session.add(training)
        db.session.commit()
        print(f"   ✅ {len(data['advanced_training'])} advanced training records imported")
        
        # Import Technical Tools
        print("📥 Importing Technical Tools...")
        for tool_data in data['technical_tools']:
            tool = TechnicalTool(
                name=tool_data['name'],
                proficiency_level=tool_data.get('proficiency_level'),
                years_experience=tool_data.get('years_experience'),
                description=tool_data.get('description'),
                usable_qa_analyst=tool_data.get('usable_qa_analyst', False),
                subcategory_qa_analyst=tool_data.get('subcategory_qa_analyst'),
                usable_qa_engineer=tool_data.get('usable_qa_engineer', False),
                subcategory_qa_engineer=tool_data.get('subcategory_qa_engineer'),
                usable_data_scientist=tool_data.get('usable_data_scientist', False),
                subcategory_data_scientist=tool_data.get('subcategory_data_scientist'),
                display_order=tool_data.get('display_order', 0),
                active=tool_data.get('active', True),
            )
            db.session.add(tool)
        db.session.commit()
        print(f"   ✅ {len(data['technical_tools'])} technical tools imported")
        
        # Import Languages
        print("📥 Importing Languages...")
        for lang_data in data['languages']:
            lang = Language(
                name=lang_data['name'],
                level_conversation=lang_data['level_conversation'],
                level_reading=lang_data['level_reading'],
                level_writing=lang_data['level_writing'],
                certification_name=lang_data.get('certification_name'),
                certification_score=lang_data.get('certification_score'),
                certification_date=datetime.fromisoformat(lang_data['certification_date']) if lang_data.get('certification_date') else None,
                display_order=lang_data.get('display_order', 0),
                active=lang_data.get('active', True),
                visible_qa_analyst=lang_data.get('visible_qa_analyst', True),
                visible_qa_engineer=lang_data['visible_qa_engineer'],
                visible_data_scientist=lang_data['visible_data_scientist'],
            )
            db.session.add(lang)
        db.session.commit()
        print(f"   ✅ {len(data['languages'])} languages imported")
        
        # Import IT Products
        print("📥 Importing IT Products...")
        for prod_data in data['it_products']:
            product = ITProduct(
                product_name=prod_data['product_name'],
                role=prod_data.get('role'),
                technologies=prod_data.get('technologies'),
                link=prod_data.get('link'),
                impact=prod_data.get('impact'),
                display_order=prod_data.get('display_order', 0),
                visible_qa_analyst=prod_data.get('visible_qa_analyst', True),
                visible_qa_engineer=prod_data.get('visible_qa_engineer', True),
                visible_data_scientist=prod_data.get('visible_data_scientist', True),
            )
            db.session.add(product)
        db.session.commit()
        print(f"   ✅ {len(data['it_products'])} IT products imported")
        
        print("\n✅ Import completed successfully!")
        print("\n⚠️  Next steps:")
        print("   1. Re-upload credential images via the web interface")
        print("   2. Re-upload person photo if needed")
        print("   3. Verify data at your Render URL")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        import_data(sys.argv[1])
    else:
        import_data()
