"""
Temporary Data Import Route
REMOVE THIS FILE AFTER MIGRATION IS COMPLETE
"""
from flask import Blueprint, request, jsonify, render_template_string
import json
import os
from datetime import datetime
from app import db
from app.models import Person, WorkExperience, Education, AdvancedTraining, TechnicalTool, Language, ITProduct

data_import_bp = Blueprint('data_import', __name__)

UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Import CV Data</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .upload-box { border: 2px dashed #ccc; padding: 30px; text-align: center; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .success { color: green; } .error { color: red; }
    </style>
</head>
<body>
    <h1>🔄 Import CV Data from JSON</h1>
    <div class="upload-box">
        <form method="POST" enctype="multipart/form-data">
            <p>Admin Password:</p>
            <input type="password" name="pw" required style="padding: 5px; width: 200px;">
            <br><br>
            <p>Select cv_data_export.json file:</p>
            <input type="file" name="json_file" accept=".json" required>
            <br><br>
            <button type="submit">Import Data</button>
        </form>
    </div>
    {% if message %}
    <p class="{{ 'success' if success else 'error' }}">{{ message }}</p>
    {% endif %}
</body>
</html>
'''

@data_import_bp.route('/admin/import-data', methods=['GET', 'POST'])
def import_data():
    """Upload and import JSON data (admin only)"""
    # Check admin password
    admin_pw = os.environ.get('ADMIN_PASSWORD')
    provided_pw = request.args.get('pw') or request.form.get('pw')
    
    if not admin_pw or provided_pw != admin_pw:
        return render_template_string('<h1>Unauthorized</h1><p>Invalid or missing password.</p>'), 401
    
    if request.method == 'POST':
        try:
            file = request.files.get('json_file')
            if not file:
                return render_template_string(UPLOAD_TEMPLATE, message='No file selected', success=False)
            
            # Parse JSON
            data = json.load(file)
            
            # Clear existing data
            db.session.query(ITProduct).delete()
            db.session.query(Language).delete()
            db.session.query(TechnicalTool).delete()
            db.session.query(AdvancedTraining).delete()
            db.session.query(Education).delete()
            db.session.query(WorkExperience).delete()
            db.session.query(Person).delete()
            db.session.commit()
            
            # Import Person
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
            
            # Import Work Experiences
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
                    achievements=exp_data.get('achievements'),
                    show_responsibilities_summary=exp_data['show_responsibilities_summary'],
                    show_responsibilities_detailed=exp_data['show_responsibilities_detailed'],
                    show_achievements=exp_data.get('show_achievements', True),
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
            
            # Import Education
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
                    image_path=edu_data.get('image_path'),
                    image_thumbnail_path=edu_data.get('image_thumbnail_path'),
                    image_filename=edu_data.get('image_filename'),
                    image_mime_type=edu_data.get('image_mime_type'),
                    active=edu_data.get('active', True),
                    display_order=edu_data.get('display_order', 0),
                    visible_qa_analyst=edu_data.get('visible_qa_analyst', True),
                    visible_qa_engineer=edu_data.get('visible_qa_engineer', True),
                    visible_data_scientist=edu_data.get('visible_data_scientist', True),
                )
                db.session.add(edu)
            db.session.commit()
            
            # Import Advanced Training
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
            
            # Import Technical Tools
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
            
            # Import Languages
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
                    visible_qa_engineer=lang_data.get('visible_qa_engineer', True),
                    visible_data_scientist=lang_data.get('visible_data_scientist', True),
                )
                db.session.add(lang)
            db.session.commit()
            
            # Import IT Products
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
            
            message = f'✅ Import successful! {len(data["persons"])} persons, {len(data["work_experiences"])} work experiences, {len(data["education"])} education, {len(data["advanced_training"])} training, {len(data["technical_tools"])} tools, {len(data["languages"])} languages, {len(data["it_products"])} products'
            return render_template_string(UPLOAD_TEMPLATE, message=message, success=True)
            
        except Exception as e:
            db.session.rollback()
            return render_template_string(UPLOAD_TEMPLATE, message=f'❌ Error: {str(e)}', success=False)
    
    return render_template_string(UPLOAD_TEMPLATE)
