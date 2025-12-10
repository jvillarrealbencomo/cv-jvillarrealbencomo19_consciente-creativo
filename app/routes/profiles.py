"""
Profile Routes
Version 2025 - Profile viewing and CV generation
"""
from flask import Blueprint, render_template, jsonify, send_file, request
from datetime import datetime
from app import db
from app.models import Person, WorkExperience, TechnicalTool, Education, Certification, Course, Language, ITProduct, AdvancedTraining
from app.services.pdf_generator import PDFGenerator
from app.services.profile_presets import ProfilePresetService
import re
from copy import deepcopy

bp = Blueprint('profiles', __name__, url_prefix='/profile')


@bp.route('/<int:person_id>')
def view_profile(person_id):
    """View profile page"""
    person = db.session.get(Person, person_id)
    if not person:
        return "Person not found", 404
    
    # Get default profile or from query param
    profile_name = request.args.get('profile', 'qa_engineer')
    
    return render_template('profile_view.html', person=person, profile_name=profile_name)


@bp.route('/<int:person_id>/data/<profile_name>')
def profile_data(person_id, profile_name):
    """Get all data for a profile in JSON format"""
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Invalid profile'}), 400
    
    data = get_profile_data_dict(person_id, profile_name)
    if data is None:
        return jsonify({'error': 'Person not found'}), 404
    
    return jsonify(data)


@bp.route('/<int:person_id>/pdf/<profile_name>/onepage', methods=['POST'])
def generate_one_page_pdf(person_id, profile_name):
    """Generate one-page optimized PDF CV for a profile"""
    from flask import make_response
    from app.services.pdf_generator import PDFGenerator
    
    person = db.session.get(Person, person_id)
    if not person:
        return "Person not found", 404
    
    if profile_name not in ProfilePresetService.get_profile_names():
        return "Invalid profile", 400
    
    # Get profile data
    profile_data = get_profile_data_dict(person_id, profile_name)
    
    try:
        # Generate one-page PDF with auto-optimization enabled
        pdf_bytes = PDFGenerator.generate_cv_pdf(profile_data, profile_name, auto_optimize=True)
        
        # Create response
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=CV_{person.first_name}_{person.last_name}_{profile_name}_onepage.pdf'
        
        return response
    except Exception as e:
        return jsonify({
            'error': 'PDF generation failed',
            'details': str(e)
        }), 500


@bp.route('/<int:person_id>/pdf/<profile_name>', methods=['POST'])
def generate_pdf(person_id, profile_name):
    """Generate PDF CV for a profile"""
    from flask import make_response
    from app.services.pdf_generator import PDFGenerator
    
    person = db.session.get(Person, person_id)
    if not person:
        return "Person not found", 404
    
    if profile_name not in ProfilePresetService.get_profile_names():
        return "Invalid profile", 400
    
    # Get section states from request
    data = request.get_json() or {}
    section_states = data.get('section_states', {})
    auto_optimize = data.get('auto_optimize', False)  # Default to FALSE so user sees full PDF first
    
    # Get profile data
    profile_data = get_profile_data_dict(person_id, profile_name)
    
    # Apply section states to filter data
    if not section_states.get('summary', True):
        profile_data['summary'] = None
    if not section_states.get('experience', True):
        profile_data['work_experience'] = []
    if not section_states.get('tools', True):
        profile_data['technical_tools'] = {}
    if not section_states.get('education', True):
        profile_data['education'] = []
    if not section_states.get('certifications', True):
        profile_data['advanced_training'] = []
    if not section_states.get('languages', True):
        profile_data['languages'] = []
    
    try:
        # Generate PDF
        pdf_bytes = PDFGenerator.generate_cv_pdf(profile_data, profile_name, auto_optimize=auto_optimize)
        
        # Create response
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=CV_{person.first_name}_{person.last_name}_{profile_name}.pdf'
        
        return response
    except Exception as e:
        return jsonify({
            'error': 'PDF generation failed',
            'details': str(e)
        }), 500


def get_profile_data_dict(person_id, profile_name):
    """Helper function to get complete profile data as dictionary"""
    person = db.session.get(Person, person_id)
    if not person:
        return None
    
    # Collect all data filtered by profile visibility
    # WorkExperience: apply custom ordering
    # Block order priority: 2021-2025 first (newest), then 2015-2020, then 1985-2009 (oldest)
    block_priority = {"2021-2025": 0, "2015-2020": 1, "1985-2009": 2}

    # Fetch and filter experiences by visibility
    exp_models = [
        exp for exp in WorkExperience.query.filter_by(active=True).all()
        if exp.is_visible_for_profile(profile_name) and not exp.is_historical
    ]

    # Sort experiences: by time_block priority, then display_order, then by end_date desc, start_date desc
    def exp_sort_key(exp):
        block_idx = block_priority.get((exp.time_block or '').strip(), 999)
        # Use display_order if set, otherwise 0
        disp = exp.display_order if isinstance(getattr(exp, 'display_order', None), int) else 0
        # For dates, None means ongoing; treat as far future for descending order
        end = exp.end_date or datetime.max.date()
        start = exp.start_date or datetime.min.date()
        # Return tuple for sorting: block first, then display_order, then dates desc
        return (block_idx, disp, -int(end.strftime('%Y%m%d')), -int(start.strftime('%Y%m%d')))

    exp_models_sorted = sorted(exp_models, key=exp_sort_key)

    data = {
        'person': person.to_dict(),
        'visible_contacts': person.get_visible_contacts(),
        'title': person.get_title_for_profile(profile_name),
        'summary': person.get_summary_for_profile(profile_name),
        'work_experience': [exp.to_dict() for exp in exp_models_sorted],
        'technical_tools': {},
        'education': [
            edu.to_dict() for edu in Education.query.filter_by(active=True).all()
            if edu.is_visible_for_profile(profile_name) and not edu.is_historical
        ],
        'advanced_training': sorted([
            training.to_dict() for training in AdvancedTraining.query.filter_by(active=True).all()
            if training.is_visible_for_profile(profile_name) and not training.is_historical
        ], key=lambda x: x.get('display_order', 999)),
        'languages': [
            lang.to_dict() for lang in Language.query.filter_by(active=True).all()
            if lang.is_visible_for_profile(profile_name) and not lang.is_historical
        ],
        'it_products': [
            prod.to_dict() for prod in ITProduct.query.filter_by(active=True).all()
            if prod.is_visible_for_profile(profile_name) and not prod.is_historical
        ]
    }
    
    # Get technical tools grouped by subcategory
    data['technical_tools'] = TechnicalTool.get_tools_by_profile_and_subcategory(profile_name)
    
    return data
