"""
API Routes Blueprint
RESTful API for external integrations (2026 vision)
"""
from flask import Blueprint, jsonify, request
from app.models import (PersonalData, Education, WorkExperience, ITProduct,
                        Certification, Course, Language, SupportTool)
from app import db

bp = Blueprint('api', __name__)


@bp.route('/personal-data')
def get_personal_data():
    """Get active personal data"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    if not personal_data:
        return jsonify({'error': 'No active personal data found'}), 404
    return jsonify(personal_data.to_dict())


@bp.route('/education')
def get_education():
    """Get all active education records"""
    education = Education.query.filter_by(active=True).order_by(Education.display_order).all()
    return jsonify([e.to_dict() for e in education])


@bp.route('/experience')
def get_experience():
    """Get all active work experience records"""
    experiences = WorkExperience.query.filter_by(active=True).order_by(WorkExperience.display_order, WorkExperience.start_date.desc()).all()
    return jsonify([e.to_dict() for e in experiences])


@bp.route('/products')
def get_products():
    """Get all active IT products"""
    products = ITProduct.query.filter_by(active=True).order_by(ITProduct.display_order).all()
    return jsonify([p.to_dict() for p in products])


@bp.route('/certifications')
def get_certifications():
    """Get all active certifications"""
    certifications = Certification.query.filter_by(active=True).order_by(Certification.display_order).all()
    return jsonify([c.to_dict() for c in certifications])


@bp.route('/courses')
def get_courses():
    """Get all active courses"""
    courses = Course.query.filter_by(active=True).order_by(Course.display_order).all()
    return jsonify([c.to_dict() for c in courses])


@bp.route('/languages')
def get_languages():
    """Get all active languages"""
    languages = Language.query.filter_by(active=True).order_by(Language.display_order).all()
    return jsonify([l.to_dict() for l in languages])


@bp.route('/skills')
def get_skills():
    """Get all active technical skills"""
    tools = SupportTool.query.filter_by(active=True).order_by(SupportTool.category, SupportTool.display_order).all()
    
    # Group by category
    tools_by_category = {}
    for tool in tools:
        if tool.category not in tools_by_category:
            tools_by_category[tool.category] = []
        tools_by_category[tool.category].append(tool.to_dict())
    
    return jsonify(tools_by_category)


@bp.route('/profile/<profile_name>')
def get_profile(profile_name):
    """
    Get filtered data for a specific profile
    
    Profiles: qa_analyst, qa_engineer, data_scientist
    """
    if profile_name not in ['qa_analyst', 'qa_engineer', 'data_scientist']:
        return jsonify({'error': 'Invalid profile name'}), 400
    
    min_relevance = request.args.get('min_relevance', 5, type=int)
    
    personal_data = PersonalData.query.filter_by(active=True).first()
    
    education = [
        e.to_dict() for e in Education.query.filter_by(active=True).all()
        if e.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    experience = [
        e.to_dict() for e in WorkExperience.query.filter_by(active=True).all()
        if e.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    products = [
        p.to_dict() for p in ITProduct.query.filter_by(active=True).all()
        if p.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    certifications = [
        c.to_dict() for c in Certification.query.filter_by(active=True).all()
        if c.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    courses = [
        c.to_dict() for c in Course.query.filter_by(active=True).all()
        if c.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    languages = [
        l.to_dict() for l in Language.query.filter_by(active=True).all()
        if l.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    tools = [
        t.to_dict() for t in SupportTool.query.filter_by(active=True).all()
        if t.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    return jsonify({
        'profile': profile_name,
        'personal_data': personal_data.to_dict() if personal_data else None,
        'education': education,
        'experience': experience,
        'products': products,
        'certifications': certifications,
        'courses': courses,
        'languages': languages,
        'skills': tools
    })
