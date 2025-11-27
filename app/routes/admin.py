"""
Admin Routes Blueprint
CRUD operations and configuration panel
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from app.models import (PersonalData, Education, WorkExperience, ITProduct, 
                        Certification, Course, Language, SupportTool)
from app import db
from config import config as app_config

bp = Blueprint('admin', __name__)


def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Basic auth - upgrade to Flask-Login in 2026
        config = app_config['development']
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Successfully logged out', 'info')
    return redirect(url_for('main.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    stats = {
        'personal_data': PersonalData.query.count(),
        'education': Education.query.filter_by(active=True).count(),
        'experience': WorkExperience.query.filter_by(active=True).count(),
        'products': ITProduct.query.filter_by(active=True).count(),
        'certifications': Certification.query.filter_by(active=True).count(),
        'courses': Course.query.filter_by(active=True).count(),
        'languages': Language.query.filter_by(active=True).count(),
        'tools': SupportTool.query.filter_by(active=True).count()
    }
    
    return render_template('admin/dashboard.html', stats=stats)


# Personal Data Management
@bp.route('/personal-data', methods=['GET', 'POST'])
@login_required
def manage_personal_data():
    """Manage personal data"""
    personal_data = PersonalData.query.first()
    
    if request.method == 'POST':
        if not personal_data:
            personal_data = PersonalData()
            db.session.add(personal_data)
        
        # Update fields
        personal_data.full_name = request.form.get('full_name')
        personal_data.professional_title = request.form.get('professional_title')
        personal_data.email = request.form.get('email')
        personal_data.phone = request.form.get('phone')
        personal_data.location = request.form.get('location')
        personal_data.summary = request.form.get('summary')
        personal_data.summary_short = request.form.get('summary_short')
        personal_data.url_personal = request.form.get('url_personal')
        personal_data.url_github = request.form.get('url_github')
        personal_data.url_linkedin = request.form.get('url_linkedin')
        personal_data.show_link = request.form.get('show_link')
        personal_data.active = bool(request.form.get('active'))
        
        db.session.commit()
        flash('Personal data updated successfully', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/personal_data.html', personal_data=personal_data)


# Education Management
@bp.route('/education')
@login_required
def list_education():
    """List all education records"""
    education_records = Education.query.order_by(Education.display_order, Education.start_date.desc()).all()
    return render_template('admin/education_list.html', education_records=education_records)


@bp.route('/education/create', methods=['GET', 'POST'])
@login_required
def create_education():
    """Create new education record"""
    if request.method == 'POST':
        education = Education(
            degree=request.form.get('degree'),
            institution=request.form.get('institution'),
            location=request.form.get('location'),
            description=request.form.get('description'),
            active=bool(request.form.get('active')),
            visible_in_summary=bool(request.form.get('visible_in_summary')),
            relevance_qa_analyst=int(request.form.get('relevance_qa_analyst', 5)),
            relevance_qa_engineer=int(request.form.get('relevance_qa_engineer', 5)),
            relevance_data_scientist=int(request.form.get('relevance_data_scientist', 5))
        )
        
        db.session.add(education)
        db.session.commit()
        flash('Education record created successfully', 'success')
        return redirect(url_for('admin.list_education'))
    
    return render_template('admin/education_form.html', education=None)


@bp.route('/education/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_education(id):
    """Edit education record"""
    education = Education.query.get_or_404(id)
    
    if request.method == 'POST':
        education.degree = request.form.get('degree')
        education.institution = request.form.get('institution')
        education.location = request.form.get('location')
        education.description = request.form.get('description')
        education.active = bool(request.form.get('active'))
        education.visible_in_summary = bool(request.form.get('visible_in_summary'))
        education.relevance_qa_analyst = int(request.form.get('relevance_qa_analyst', 5))
        education.relevance_qa_engineer = int(request.form.get('relevance_qa_engineer', 5))
        education.relevance_data_scientist = int(request.form.get('relevance_data_scientist', 5))
        
        db.session.commit()
        flash('Education record updated successfully', 'success')
        return redirect(url_for('admin.list_education'))
    
    return render_template('admin/education_form.html', education=education)


@bp.route('/education/<int:id>/toggle-active', methods=['POST'])
@login_required
def toggle_education_active(id):
    """Toggle education record active status"""
    education = Education.query.get_or_404(id)
    education.active = not education.active
    db.session.commit()
    return jsonify({'active': education.active})


# Work Experience Management
@bp.route('/experience')
@login_required
def list_experience():
    """List all work experience records"""
    experiences = WorkExperience.query.order_by(WorkExperience.display_order, WorkExperience.start_date.desc()).all()
    return render_template('admin/experience_list.html', experiences=experiences)


@bp.route('/experience/create', methods=['GET', 'POST'])
@login_required
def create_experience():
    """Create new work experience record"""
    if request.method == 'POST':
        experience = WorkExperience(
            job_title=request.form.get('job_title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            description=request.form.get('description'),
            functions=request.form.get('functions'),
            highlighted_aspect=request.form.get('highlighted_aspect'),
            show_detail=request.form.get('show_detail', 'both'),
            technologies=request.form.get('technologies'),
            active=bool(request.form.get('active')),
            visible_in_summary=bool(request.form.get('visible_in_summary')),
            relevance_qa_analyst=int(request.form.get('relevance_qa_analyst', 5)),
            relevance_qa_engineer=int(request.form.get('relevance_qa_engineer', 5)),
            relevance_data_scientist=int(request.form.get('relevance_data_scientist', 5))
        )
        
        db.session.add(experience)
        db.session.commit()
        flash('Work experience created successfully', 'success')
        return redirect(url_for('admin.list_experience'))
    
    return render_template('admin/experience_form.html', experience=None)


@bp.route('/experience/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_experience(id):
    """Edit work experience record"""
    experience = WorkExperience.query.get_or_404(id)
    
    if request.method == 'POST':
        experience.job_title = request.form.get('job_title')
        experience.company = request.form.get('company')
        experience.location = request.form.get('location')
        experience.description = request.form.get('description')
        experience.functions = request.form.get('functions')
        experience.highlighted_aspect = request.form.get('highlighted_aspect')
        experience.show_detail = request.form.get('show_detail', 'both')
        experience.technologies = request.form.get('technologies')
        experience.active = bool(request.form.get('active'))
        experience.visible_in_summary = bool(request.form.get('visible_in_summary'))
        experience.relevance_qa_analyst = int(request.form.get('relevance_qa_analyst', 5))
        experience.relevance_qa_engineer = int(request.form.get('relevance_qa_engineer', 5))
        experience.relevance_data_scientist = int(request.form.get('relevance_data_scientist', 5))
        
        db.session.commit()
        flash('Work experience updated successfully', 'success')
        return redirect(url_for('admin.list_experience'))
    
    return render_template('admin/experience_form.html', experience=experience)


# API endpoints for quick toggles
@bp.route('/api/toggle-active/<model_name>/<int:id>', methods=['POST'])
@login_required
def api_toggle_active(model_name, id):
    """API endpoint to toggle active status"""
    model_map = {
        'education': Education,
        'experience': WorkExperience,
        'product': ITProduct,
        'certification': Certification,
        'course': Course,
        'language': Language,
        'tool': SupportTool
    }
    
    Model = model_map.get(model_name)
    if not Model:
        return jsonify({'error': 'Invalid model'}), 400
    
    record = Model.query.get_or_404(id)
    record.active = not record.active
    db.session.commit()
    
    return jsonify({'active': record.active})


@bp.route('/api/toggle-visibility/<model_name>/<int:id>', methods=['POST'])
@login_required
def api_toggle_visibility(model_name, id):
    """API endpoint to toggle visibility in summary"""
    model_map = {
        'education': Education,
        'experience': WorkExperience,
        'product': ITProduct,
        'certification': Certification,
        'course': Course,
        'language': Language,
        'tool': SupportTool
    }
    
    Model = model_map.get(model_name)
    if not Model:
        return jsonify({'error': 'Invalid model'}), 400
    
    record = Model.query.get_or_404(id)
    record.visible_in_summary = not record.visible_in_summary
    db.session.commit()
    
    return jsonify({'visible_in_summary': record.visible_in_summary})
