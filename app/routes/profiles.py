"""
Profile-specific CV Routes
Generate tailored CVs for QA Analyst, QA Engineer, Data Scientist
"""
from flask import Blueprint, render_template, send_file
from app.models import PersonalData, Education, WorkExperience, ITProduct, Certification, Course, Language, SupportTool
from app.services.pdf_generator import PDFGenerator
from app import db

bp = Blueprint('profiles', __name__)


def get_profile_data(profile_name, min_relevance=5):
    """
    Get filtered data for a specific profile
    
    Args:
        profile_name: 'qa_analyst', 'qa_engineer', or 'data_scientist'
        min_relevance: Minimum relevance score (0-10)
    
    Returns:
        dict: Filtered data for the profile
    """
    personal_data = PersonalData.query.filter_by(active=True).first()
    
    # Filter records based on profile relevance
    education = [
        e for e in Education.query.filter_by(active=True).order_by(Education.display_order).all()
        if e.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    experience = [
        e for e in WorkExperience.query.filter_by(active=True).order_by(WorkExperience.display_order, WorkExperience.start_date.desc()).all()
        if e.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    products = [
        p for p in ITProduct.query.filter_by(active=True).order_by(ITProduct.display_order).all()
        if p.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    certifications = [
        c for c in Certification.query.filter_by(active=True).order_by(Certification.display_order, Certification.issue_date.desc()).all()
        if c.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    courses = [
        c for c in Course.query.filter_by(active=True).order_by(Course.display_order).all()
        if c.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    languages = [
        l for l in Language.query.filter_by(active=True).order_by(Language.display_order).all()
        if l.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    tools = [
        t for t in SupportTool.query.filter_by(active=True).order_by(SupportTool.category, SupportTool.display_order).all()
        if t.is_relevant_for_profile(profile_name, min_relevance)
    ]
    
    # Group tools by category
    tools_by_category = {}
    for tool in tools:
        if tool.category not in tools_by_category:
            tools_by_category[tool.category] = []
        tools_by_category[tool.category].append(tool)
    
    return {
        'personal_data': personal_data,
        'education': education,
        'experience': experience,
        'products': products,
        'certifications': certifications,
        'courses': courses,
        'languages': languages,
        'tools_by_category': tools_by_category,
        'profile_name': profile_name
    }


@bp.route('/qa-analyst')
def qa_analyst():
    """QA Analyst profile view"""
    data = get_profile_data('qa_analyst')
    return render_template('profile_view.html', 
                         profile_title='QA Analyst',
                         **data)


@bp.route('/qa-engineer')
def qa_engineer():
    """QA Engineer profile view"""
    data = get_profile_data('qa_engineer')
    return render_template('profile_view.html',
                         profile_title='QA Engineer',
                         **data)


@bp.route('/data-scientist')
def data_scientist():
    """Data Scientist profile view"""
    data = get_profile_data('data_scientist')
    return render_template('profile_view.html',
                         profile_title='Data Scientist',
                         **data)


@bp.route('/qa-analyst/pdf')
def qa_analyst_pdf():
    """Generate PDF for QA Analyst profile"""
    data = get_profile_data('qa_analyst')
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.generate_profile_pdf(data, 'QA Analyst')
    return send_file(pdf_path, as_attachment=True, download_name='CV_QA_Analyst.pdf')


@bp.route('/qa-engineer/pdf')
def qa_engineer_pdf():
    """Generate PDF for QA Engineer profile"""
    data = get_profile_data('qa_engineer')
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.generate_profile_pdf(data, 'QA Engineer')
    return send_file(pdf_path, as_attachment=True, download_name='CV_QA_Engineer.pdf')


@bp.route('/data-scientist/pdf')
def data_scientist_pdf():
    """Generate PDF for Data Scientist profile"""
    data = get_profile_data('data_scientist')
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.generate_profile_pdf(data, 'Data Scientist')
    return send_file(pdf_path, as_attachment=True, download_name='CV_Data_Scientist.pdf')
