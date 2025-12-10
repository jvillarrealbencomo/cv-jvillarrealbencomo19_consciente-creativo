"""
Forms Routes
Version 2025 - Form rendering routes
"""
from flask import Blueprint, render_template, request
from app import db
from app.models import Person, WorkExperience, TechnicalTool, Education, Certification, Course, Language, AdvancedTraining

bp = Blueprint('forms', __name__, url_prefix='/forms')


@bp.route('/person')
@bp.route('/person/<int:person_id>')
def person_form(person_id=None):
    """Person information form"""
    person = None
    if person_id:
        person = db.session.get(Person, person_id)
    else:
        # If no person_id provided, load the first active person if exists
        person = Person.query.filter_by(active=True, is_historical=False).first()
    return render_template('forms/person_form.html', person=person)


@bp.route('/experience')
@bp.route('/experience/<int:exp_id>')
def experience_form(exp_id=None):
    """Work experience form"""
    experience = None
    if exp_id:
        experience = db.session.get(WorkExperience, exp_id)
    return render_template('forms/experience_form.html', experience=experience)


@bp.route('/tool')
@bp.route('/tool/<int:tool_id>')
def tool_form(tool_id=None):
    """Technical tool form"""
    # Support both /tool/1 and /tool?tool_id=1
    if tool_id is None:
        tool_id = request.args.get('tool_id', type=int)
    
    tool = None
    if tool_id:
        tool = db.session.get(TechnicalTool, tool_id)
    return render_template('forms/tool_form.html', tool=tool)


@bp.route('/education')
@bp.route('/education/<int:edu_id>')
def education_form(edu_id=None):
    """Education form"""
    education = None
    if edu_id:
        education = db.session.get(Education, edu_id)
    return render_template('forms/education_form.html', education=education)


@bp.route('/certification')
@bp.route('/certification/<int:cert_id>')
def certification_form(cert_id=None):
    """Certification form"""
    certification = None
    if cert_id:
        certification = db.session.get(Certification, cert_id)
    return render_template('forms/certification_form.html', certification=certification)


@bp.route('/course')
@bp.route('/course/<int:course_id>')
def course_form(course_id=None):
    """Course form"""
    course = None
    if course_id:
        course = db.session.get(Course, course_id)
    return render_template('forms/course_form.html', course=course)


@bp.route('/language')
@bp.route('/language/<int:lang_id>')
def language_form(lang_id=None):
    """Language form"""
    language = None
    if lang_id:
        language = db.session.get(Language, lang_id)
    return render_template('forms/language_form.html', language=language)


@bp.route('/advanced-training')
@bp.route('/advanced-training/<int:training_id>')
def advanced_training_form(training_id=None):
    """Advanced training form (unified courses and certifications)"""
    training = None
    if training_id:
        training = db.session.get(AdvancedTraining, training_id)
    return render_template('forms/advanced_training_form.html', training=training)
