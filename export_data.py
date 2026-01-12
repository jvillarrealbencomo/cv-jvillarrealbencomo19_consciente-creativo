"""
Export SQLite Database to JSON
Exports all CV data for migration to PostgreSQL
"""
import json
from datetime import datetime
from app import create_app, db
from app.models import (
    Person, WorkExperience, Education, AdvancedTraining,
    TechnicalTool, Language, ITProduct
)

def export_data():
    """Export all database records to JSON"""
    app = create_app('development')
    
    with app.app_context():
        data = {
            'export_date': datetime.now().isoformat(),
            'export_version': '2025.2',
            'persons': [],
            'work_experiences': [],
            'education': [],
            'advanced_training': [],
            'technical_tools': [],
            'languages': [],
            'it_products': []
        }
        
        # Export Persons
        for person in Person.query.all():
            data['persons'].append({
                'id': person.id,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'phone': person.phone,
                'location': person.location,
                'linkedin': person.linkedin,
                'github': person.github,
                'portfolio_website': person.portfolio_website,
                'title_qa_analyst': person.title_qa_analyst,
                'title_qa_engineer': person.title_qa_engineer,
                'title_data_scientist': person.title_data_scientist,
                'summary_qa_analyst': person.summary_qa_analyst,
                'summary_qa_engineer': person.summary_qa_engineer,
                'summary_data_scientist': person.summary_data_scientist,
                'reference_name_1': person.reference_name_1,
                'reference_title_1': person.reference_title_1,
                'reference_contact_1': person.reference_contact_1,
                'reference_name_2': person.reference_name_2,
                'reference_title_2': person.reference_title_2,
                'reference_contact_2': person.reference_contact_2,
                'reference_name_3': person.reference_name_3,
                'reference_title_3': person.reference_title_3,
                'reference_contact_3': person.reference_contact_3,
                'photo_path': person.photo_path,
                # Visibility flags
                'email_visible_qa_analyst': person.email_visible_qa_analyst,
                'email_visible_qa_engineer': person.email_visible_qa_engineer,
                'email_visible_data_scientist': person.email_visible_data_scientist,
                'phone_visible_qa_analyst': person.phone_visible_qa_analyst,
                'phone_visible_qa_engineer': person.phone_visible_qa_engineer,
                'phone_visible_data_scientist': person.phone_visible_data_scientist,
                'location_visible_qa_analyst': person.location_visible_qa_analyst,
                'location_visible_qa_engineer': person.location_visible_qa_engineer,
                'location_visible_data_scientist': person.location_visible_data_scientist,
                'linkedin_visible_qa_analyst': person.linkedin_visible_qa_analyst,
                'linkedin_visible_qa_engineer': person.linkedin_visible_qa_engineer,
                'linkedin_visible_data_scientist': person.linkedin_visible_data_scientist,
                'github_visible_qa_analyst': person.github_visible_qa_analyst,
                'github_visible_qa_engineer': person.github_visible_qa_engineer,
                'github_visible_data_scientist': person.github_visible_data_scientist,
                'portfolio_visible_qa_analyst': person.portfolio_visible_qa_analyst,
                'portfolio_visible_qa_engineer': person.portfolio_visible_qa_engineer,
                'portfolio_visible_data_scientist': person.portfolio_visible_data_scientist,
                'references_visible_qa_analyst': person.references_visible_qa_analyst,
                'references_visible_qa_engineer': person.references_visible_qa_engineer,
                'references_visible_data_scientist': person.references_visible_data_scientist,
            })
        
        # Export Work Experiences
        for exp in WorkExperience.query.all():
            data['work_experiences'].append({
                'id': exp.id,
                'person_id': exp.person_id,
                'job_title': exp.job_title,
                'company': exp.company,
                'location': exp.location,
                'start_date': exp.start_date.isoformat() if exp.start_date else None,
                'end_date': exp.end_date.isoformat() if exp.end_date else None,
                'time_block': exp.time_block,
                'responsibilities_summary': exp.responsibilities_summary,
                'responsibilities_detailed': exp.responsibilities_detailed,
                'key_achievements': exp.key_achievements,
                'show_responsibilities_summary': exp.show_responsibilities_summary,
                'show_responsibilities_detailed': exp.show_responsibilities_detailed,
                'show_key_achievements': exp.show_key_achievements,
                'active': exp.active,
                'is_historical': exp.is_historical,
                'display_order': exp.display_order,
                'visible_qa_analyst': exp.visible_qa_analyst,
                'visible_qa_engineer': exp.visible_qa_engineer,
                'visible_data_scientist': exp.visible_data_scientist,
            })
        
        # Export Education
        for edu in Education.query.all():
            data['education'].append({
                'id': edu.id,
                'person_id': edu.person_id,
                'degree': edu.degree,
                'school': edu.school,
                'graduation_date': edu.graduation_date.isoformat() if edu.graduation_date else None,
                'country': edu.country,
                'start_date': edu.start_date.isoformat() if edu.start_date else None,
                'end_date': edu.end_date.isoformat() if edu.end_date else None,
                'document_reference': edu.document_reference,
                'image_path': edu.image_path,
                'image_thumbnail_path': edu.image_thumbnail_path,
                'image_filename': edu.image_filename,
                'image_mime_type': edu.image_mime_type,
                'active': edu.active,
                'display_order': edu.display_order,
                'visible_qa_analyst': edu.visible_qa_analyst,
                'visible_qa_engineer': edu.visible_qa_engineer,
                'visible_data_scientist': edu.visible_data_scientist,
            })
        
        # Export Advanced Training
        for training in AdvancedTraining.query.all():
            data['advanced_training'].append({
                'id': training.id,
                'person_id': training.person_id,
                'type': training.type,
                'name': training.name,
                'provider': training.provider,
                'completion_date': training.completion_date.isoformat() if training.completion_date else None,
                'is_course': training.is_course,
                'hours': training.hours,
                'credential_id': training.credential_id,
                'credential_url': training.credential_url,
                'image_path': training.image_path,
                'image_thumbnail_path': training.image_thumbnail_path,
                'image_filename': training.image_filename,
                'image_mime_type': training.image_mime_type,
                'active': training.active,
                'display_order': training.display_order,
                'visible_qa_analyst': training.visible_qa_analyst,
                'visible_qa_engineer': training.visible_qa_engineer,
                'visible_data_scientist': training.visible_data_scientist,
            })
        
        # Export Technical Tools
        for tool in TechnicalTool.query.all():
            data['technical_tools'].append({
                'id': tool.id,
                'person_id': tool.person_id,
                'tool_name': tool.tool_name,
                'proficiency_level': tool.proficiency_level,
                'years_experience': tool.years_experience,
                'subcategory_qa_analyst': tool.subcategory_qa_analyst,
                'subcategory_qa_engineer': tool.subcategory_qa_engineer,
                'subcategory_data_scientist': tool.subcategory_data_scientist,
                'display_order': tool.display_order,
                'visible_qa_analyst': tool.visible_qa_analyst,
                'visible_qa_engineer': tool.visible_qa_engineer,
                'visible_data_scientist': tool.visible_data_scientist,
            })
        
        # Export Languages
        for lang in Language.query.all():
            data['languages'].append({
                'id': lang.id,
                'person_id': lang.person_id,
                'language': lang.language,
                'conversation_level': lang.conversation_level,
                'reading_level': lang.reading_level,
                'writing_level': lang.writing_level,
                'certification': lang.certification,
                'visible_qa_analyst': lang.visible_qa_analyst,
                'visible_qa_engineer': lang.visible_qa_engineer,
                'visible_data_scientist': lang.visible_data_scientist,
            })
        
        # Export IT Products
        for product in ITProduct.query.all():
            data['it_products'].append({
                'id': product.id,
                'person_id': product.person_id,
                'product_name': product.product_name,
                'role': product.role,
                'technologies': product.technologies,
                'link': product.link,
                'impact': product.impact,
                'display_order': product.display_order,
                'visible_qa_analyst': product.visible_qa_analyst,
                'visible_qa_engineer': product.visible_qa_engineer,
                'visible_data_scientist': product.visible_data_scientist,
            })
        
        # Write to file
        filename = 'cv_data_export.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print(f"✅ Export completed: {filename}")
        print(f"\nRecords exported:")
        print(f"  - Persons: {len(data['persons'])}")
        print(f"  - Work Experiences: {len(data['work_experiences'])}")
        print(f"  - Education: {len(data['education'])}")
        print(f"  - Advanced Training: {len(data['advanced_training'])}")
        print(f"  - Technical Tools: {len(data['technical_tools'])}")
        print(f"  - Languages: {len(data['languages'])}")
        print(f"  - IT Products: {len(data['it_products'])}")
        print(f"\n⚠️  Note: Images are NOT exported. You'll need to re-upload them manually.")
        print(f"    Image paths are preserved in the export for reference.")

if __name__ == '__main__':
    export_data()
