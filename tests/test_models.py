"""
Basic Model Tests
Test database models functionality
"""
import pytest
from datetime import date
from app.models import PersonalData, WorkExperience, Education


def test_personal_data_creation(app):
    """Test creating personal data"""
    with app.app_context():
        personal = PersonalData(
            full_name="John Doe",
            professional_title="Engineer",
            email="john@example.com",
            url_linkedin="https://linkedin.com/in/johndoe",
            url_github="https://github.com/johndoe",
            show_link="all"
        )
        
        assert personal.full_name == "John Doe"
        assert personal.email == "john@example.com"
        
        # Test get_visible_links method
        links = personal.get_visible_links()
        assert 'linkedin' in links
        assert 'github' in links


def test_work_experience_display_content(app):
    """Test work experience display content logic"""
    with app.app_context():
        exp = WorkExperience(
            job_title="QA Engineer",
            company="Tech Corp",
            start_date=date(2020, 1, 1),
            functions="Testing and automation",
            highlighted_aspect="Improved test coverage by 50%",
            show_detail="both"
        )
        
        content = exp.get_display_content()
        assert content['functions'] == "Testing and automation"
        assert content['highlighted_aspect'] == "Improved test coverage by 50%"


def test_relevance_filtering(app):
    """Test profile relevance filtering"""
    with app.app_context():
        exp = WorkExperience(
            job_title="QA Engineer",
            company="Tech Corp",
            start_date=date(2020, 1, 1),
            active=True,
            relevance_qa_analyst=3,
            relevance_qa_engineer=9,
            relevance_data_scientist=5
        )
        
        assert not exp.is_relevant_for_profile('qa_analyst', min_relevance=5)
        assert exp.is_relevant_for_profile('qa_engineer', min_relevance=5)
        assert exp.is_relevant_for_profile('data_scientist', min_relevance=5)
