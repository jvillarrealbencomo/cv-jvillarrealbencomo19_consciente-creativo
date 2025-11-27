"""
Main Routes Blueprint
Public-facing pages: home, sections, etc.
"""
from flask import Blueprint, render_template, jsonify
from app.models import PersonalData, Education, WorkExperience, ITProduct, Certification, Course, Language, SupportTool
from app import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page with navigation to all sections"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    
    return render_template('index.html', personal_data=personal_data)


@bp.route('/education')
def education():
    """Education section"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    education_records = Education.query.filter_by(active=True).order_by(Education.display_order, Education.start_date.desc()).all()
    
    return render_template('education.html', 
                         personal_data=personal_data,
                         education_records=education_records)


@bp.route('/experience')
def experience():
    """Work experience section"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    experiences = WorkExperience.query.filter_by(active=True).order_by(WorkExperience.display_order, WorkExperience.start_date.desc()).all()
    
    return render_template('experience.html',
                         personal_data=personal_data,
                         experiences=experiences)


@bp.route('/it-products')
def it_products():
    """IT Products and projects section"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    products = ITProduct.query.filter_by(active=True).order_by(ITProduct.display_order, ITProduct.start_date.desc()).all()
    
    return render_template('it_products.html',
                         personal_data=personal_data,
                         products=products)


@bp.route('/certifications')
def certifications():
    """Certifications section"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    certs = Certification.query.filter_by(active=True).order_by(Certification.display_order, Certification.issue_date.desc()).all()
    
    return render_template('certifications.html',
                         personal_data=personal_data,
                         certifications=certs)


@bp.route('/courses')
def courses():
    """Training courses section"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    course_list = Course.query.filter_by(active=True).order_by(Course.display_order, Course.completion_date.desc()).all()
    
    return render_template('courses.html',
                         personal_data=personal_data,
                         courses=course_list)


@bp.route('/skills')
def skills():
    """Technical skills and tools section"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    
    # Group by category
    tools_by_category = {}
    tools = SupportTool.query.filter_by(active=True).order_by(SupportTool.category, SupportTool.display_order).all()
    
    for tool in tools:
        if tool.category not in tools_by_category:
            tools_by_category[tool.category] = []
        tools_by_category[tool.category].append(tool)
    
    languages = Language.query.filter_by(active=True).order_by(Language.display_order).all()
    
    return render_template('skills.html',
                         personal_data=personal_data,
                         tools_by_category=tools_by_category,
                         languages=languages)


@bp.route('/documents')
def documents():
    """Documents listing page"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    
    # Get all records with documents
    education_docs = Education.query.filter(Education.active == True, Education.document_url.isnot(None)).all()
    experience_docs = WorkExperience.query.filter(WorkExperience.active == True, WorkExperience.document_url.isnot(None)).all()
    cert_docs = Certification.query.filter(Certification.active == True, Certification.document_url.isnot(None)).all()
    course_docs = Course.query.filter(Course.active == True, Course.document_url.isnot(None)).all()
    
    return render_template('documents.html',
                         personal_data=personal_data,
                         education_docs=education_docs,
                         experience_docs=experience_docs,
                         cert_docs=cert_docs,
                         course_docs=course_docs)


@bp.route('/about')
def about():
    """About page with personal data"""
    personal_data = PersonalData.query.filter_by(active=True).first()
    
    return render_template('about.html', personal_data=personal_data)
