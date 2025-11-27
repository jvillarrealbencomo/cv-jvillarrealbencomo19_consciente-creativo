"""
Test Configuration
Basic test setup for pytest
"""
import pytest
from app import create_app, db
from app.models import PersonalData, Education, WorkExperience


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI test runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_personal_data(app):
    """Create sample personal data for testing"""
    with app.app_context():
        personal = PersonalData(
            full_name="Test User",
            professional_title="Test Engineer",
            email="test@example.com",
            summary="Test summary",
            summary_short="Short summary",
            active=True,
            visible_in_summary=True
        )
        db.session.add(personal)
        db.session.commit()
        return personal
