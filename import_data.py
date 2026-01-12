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
                first_name=p_data['first_name'],
                last_name=p_data['last_name'],
                email=p_data['email'],
                phone=p_data['phone'],
                location=p_data['location'],
                linkedin=p_data['linkedin'],
                github=p_data['github'],
                portfolio_website=p_data['portfolio_website'],
                title_qa_analyst=p_data['title_qa_analyst'],
                title_qa_engineer=p_data['title_qa_engineer'],
                title_data_scientist=p_data['title_data_scientist'],
                summary_qa_analyst=p_data['summary_qa_analyst'],
                summary_qa_engineer=p_data['summary_qa_engineer'],
                summary_data_scientist=p_data['summary_data_scientist'],
                reference_name_1=p_data['reference_name_1'],
                reference_title_1=p_data['reference_title_1'],
                reference_contact_1=p_data['reference_contact_1'],
                reference_name_2=p_data['reference_name_2'],
                reference_title_2=p_data['reference_title_2'],
                reference_contact_2=p_data['reference_contact_2'],
                reference_name_3=p_data['reference_name_3'],
                reference_title_3=p_data['reference_title_3'],
                reference_contact_3=p_data['reference_contact_3'],
                photo_path=p_data['photo_path'],
                email_visible_qa_analyst=p_data['email_visible_qa_analyst'],
                email_visible_qa_engineer=p_data['email_visible_qa_engineer'],
                email_visible_data_scientist=p_data['email_visible_data_scientist'],
                phone_visible_qa_analyst=p_data['phone_visible_qa_analyst'],
                phone_visible_qa_engineer=p_data['phone_visible_qa_engineer'],
                phone_visible_data_scientist=p_data['phone_visible_data_scientist'],
                location_visible_qa_analyst=p_data['location_visible_qa_analyst'],
                location_visible_qa_engineer=p_data['location_visible_qa_engineer'],
                location_visible_data_scientist=p_data['location_visible_data_scientist'],
                linkedin_visible_qa_analyst=p_data['linkedin_visible_qa_analyst'],
                linkedin_visible_qa_engineer=p_data['linkedin_visible_qa_engineer'],
                linkedin_visible_data_scientist=p_data['linkedin_visible_data_scientist'],
                github_visible_qa_analyst=p_data['github_visible_qa_analyst'],
                github_visible_qa_engineer=p_data['github_visible_qa_engineer'],
                github_visible_data_scientist=p_data['github_visible_data_scientist'],
                portfolio_visible_qa_analyst=p_data['portfolio_visible_qa_analyst'],
                portfolio_visible_qa_engineer=p_data['portfolio_visible_qa_engineer'],
                portfolio_visible_data_scientist=p_data['portfolio_visible_data_scientist'],
                references_visible_qa_analyst=p_data['references_visible_qa_analyst'],
                references_visible_qa_engineer=p_data['references_visible_qa_engineer'],
                references_visible_data_scientist=p_data['references_visible_data_scientist'],
            )
            db.session.add(person)
        db.session.commit()
        print(f"   ✅ {len(data['persons'])} persons imported")
        
        # Import Work Experiences
        print("📥 Importing Work Experiences...")
        for exp_data in data['work_experiences']:
            exp = WorkExperience(
                person_id=exp_data['person_id'],
                job_title=exp_data['job_title'],
                company=exp_data['company'],
                location=exp_data['location'],
                start_date=datetime.fromisoformat(exp_data['start_date']) if exp_data['start_date'] else None,
                end_date=datetime.fromisoformat(exp_data['end_date']) if exp_data['end_date'] else None,
                time_block=exp_data['time_block'],
                responsibilities_summary=exp_data['responsibilities_summary'],
                responsibilities_detailed=exp_data['responsibilities_detailed'],
                key_achievements=exp_data['key_achievements'],
                show_responsibilities_summary=exp_data['show_responsibilities_summary'],
                show_responsibilities_detailed=exp_data['show_responsibilities_detailed'],
                show_key_achievements=exp_data['show_key_achievements'],
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
                person_id=edu_data['person_id'],
                degree=edu_data['degree'],
                school=edu_data['school'],
                graduation_date=datetime.fromisoformat(edu_data['graduation_date']) if edu_data['graduation_date'] else None,
                country=edu_data['country'],
                start_date=datetime.fromisoformat(edu_data['start_date']) if edu_data['start_date'] else None,
                end_date=datetime.fromisoformat(edu_data['end_date']) if edu_data['end_date'] else None,
                document_reference=edu_data['document_reference'],
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
                person_id=train_data['person_id'],
                type=train_data['type'],
                name=train_data['name'],
                provider=train_data['provider'],
                completion_date=datetime.fromisoformat(train_data['completion_date']) if train_data['completion_date'] else None,
                is_course=train_data['is_course'],
                hours=train_data['hours'],
                credential_id=train_data['credential_id'],
                credential_url=train_data['credential_url'],
                image_path=train_data['image_path'],
                image_thumbnail_path=train_data['image_thumbnail_path'],
                image_filename=train_data['image_filename'],
                image_mime_type=train_data['image_mime_type'],
                active=train_data['active'],
                display_order=train_data['display_order'],
                visible_qa_analyst=train_data['visible_qa_analyst'],
                visible_qa_engineer=train_data['visible_qa_engineer'],
                visible_data_scientist=train_data['visible_data_scientist'],
            )
            db.session.add(training)
        db.session.commit()
        print(f"   ✅ {len(data['advanced_training'])} advanced training records imported")
        
        # Import Technical Tools
        print("📥 Importing Technical Tools...")
        for tool_data in data['technical_tools']:
            tool = TechnicalTool(
                person_id=tool_data['person_id'],
                tool_name=tool_data['tool_name'],
                proficiency_level=tool_data['proficiency_level'],
                years_experience=tool_data['years_experience'],
                subcategory_qa_analyst=tool_data['subcategory_qa_analyst'],
                subcategory_qa_engineer=tool_data['subcategory_qa_engineer'],
                subcategory_data_scientist=tool_data['subcategory_data_scientist'],
                display_order=tool_data['display_order'],
                visible_qa_analyst=tool_data['visible_qa_analyst'],
                visible_qa_engineer=tool_data['visible_qa_engineer'],
                visible_data_scientist=tool_data['visible_data_scientist'],
            )
            db.session.add(tool)
        db.session.commit()
        print(f"   ✅ {len(data['technical_tools'])} technical tools imported")
        
        # Import Languages
        print("📥 Importing Languages...")
        for lang_data in data['languages']:
            lang = Language(
                person_id=lang_data['person_id'],
                language=lang_data['language'],
                conversation_level=lang_data['conversation_level'],
                reading_level=lang_data['reading_level'],
                writing_level=lang_data['writing_level'],
                certification=lang_data['certification'],
                visible_qa_analyst=lang_data['visible_qa_analyst'],
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
                person_id=prod_data['person_id'],
                product_name=prod_data['product_name'],
                role=prod_data['role'],
                technologies=prod_data['technologies'],
                link=prod_data['link'],
                impact=prod_data['impact'],
                display_order=prod_data['display_order'],
                visible_qa_analyst=prod_data['visible_qa_analyst'],
                visible_qa_engineer=prod_data['visible_qa_engineer'],
                visible_data_scientist=prod_data['visible_data_scientist'],
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
