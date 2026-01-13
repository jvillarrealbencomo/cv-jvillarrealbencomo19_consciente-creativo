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
                'full_name': person.full_name,
                'professional_title': person.professional_title,
                'email': person.email,
                'phone': person.phone,
                'location': person.location,
                'linkedin_url': person.linkedin_url,
                'github_url': person.github_url,
                'personal_url': person.personal_url,
                'title_qa_analyst': person.title_qa_analyst,
                'title_qa_engineer': person.title_qa_engineer,
                'title_data_scientist': person.title_data_scientist,
                'summary_qa_analyst': person.summary_qa_analyst,
                'summary_qa_engineer': person.summary_qa_engineer,
                'summary_data_scientist': person.summary_data_scientist,
                'reference_name': person.reference_name,
                'reference_company': person.reference_company,
                'reference_phone': person.reference_phone,
                'profile_image_url': person.profile_image_url,
                # Visibility flags
                'show_email': person.show_email,
                'show_phone': person.show_phone,
                'show_linkedin': person.show_linkedin,
                'show_github': person.show_github,
                'show_personal_url': person.show_personal_url,
            })
        
        # Export Work Experiences
        for exp in WorkExperience.query.all():
            data['work_experiences'].append({
                'id': exp.id,
                'job_title': exp.job_title,
                'company': exp.company,
                'location': exp.location,
                'start_date': exp.start_date.isoformat() if exp.start_date else None,
                'end_date': exp.end_date.isoformat() if exp.end_date else None,
                'is_current': exp.is_current,
                'time_block': exp.time_block,
                'responsibilities_summary': exp.responsibilities_summary,
                'responsibilities_detailed': exp.responsibilities_detailed,
                'achievements': exp.achievements,
                'show_responsibilities_summary': exp.show_responsibilities_summary,
                'show_responsibilities_detailed': exp.show_responsibilities_detailed,
                'show_achievements': exp.show_achievements,
                'technologies': exp.technologies,
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
                'degree': edu.degree,
                'institution': edu.institution,
                'country': edu.country,
                'year_obtained': edu.year_obtained,
                'start_year': edu.start_year,
                'end_year': edu.end_year,
                'is_current': edu.is_current,
                'details': edu.details,
                'document_url': edu.document_url,
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
                'type': training.type,
                'name': training.name,
                'provider': training.provider,
                'completion_date': training.completion_date.isoformat() if training.completion_date else None,
                'description': training.description,
                'expiration_date': training.expiration_date.isoformat() if training.expiration_date else None,
                'credential_id': training.credential_id,
                'credential_url': training.credential_url,
                'duration_hours': training.duration_hours,
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
                'name': tool.name,
                'proficiency_level': tool.proficiency_level,
                'years_experience': tool.years_experience,
                'description': tool.description,
                'usable_qa_analyst': tool.usable_qa_analyst,
                'subcategory_qa_analyst': tool.subcategory_qa_analyst,
                'usable_qa_engineer': tool.usable_qa_engineer,
                'subcategory_qa_engineer': tool.subcategory_qa_engineer,
                'usable_data_scientist': tool.usable_data_scientist,
                'subcategory_data_scientist': tool.subcategory_data_scientist,
                'display_order': tool.display_order,
                'active': tool.active,
            })
        
        # Export Languages
        for lang in Language.query.all():
            data['languages'].append({
                'id': lang.id,
                'name': lang.name,
                'level_conversation': lang.level_conversation,
                'level_reading': lang.level_reading,
                'level_writing': lang.level_writing,
                'certification_name': lang.certification_name,
                'certification_score': lang.certification_score,
                'certification_date': lang.certification_date.isoformat() if lang.certification_date else None,
                'display_order': lang.display_order,
                'active': lang.active,
                'visible_qa_analyst': lang.visible_qa_analyst,
                'visible_qa_engineer': lang.visible_qa_engineer,
                'visible_data_scientist': lang.visible_data_scientist,
            })
        
        # Export IT Products
        for product in ITProduct.query.all():
            data['it_products'].append({
                'id': product.id,
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
