"""
Test course completion date validation
"""
import pytest
from datetime import date, timedelta
from app import create_app, db
from app.models import Course


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_course_with_past_completion_date(client):
    """Test creating a course with a past completion date (should succeed)"""
    past_date = (date.today() - timedelta(days=30)).isoformat()
    
    response = client.post('/api/course', 
                          json={
                              'name': 'Python Programming',
                              'provider': 'Coursera',
                              'completion_date': past_date
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Python Programming'
    assert data['completion_date'] == past_date


def test_course_with_today_completion_date(client):
    """Test creating a course with today's completion date (should succeed)"""
    today = date.today().isoformat()
    
    response = client.post('/api/course',
                          json={
                              'name': 'JavaScript Basics',
                              'provider': 'Udemy',
                              'completion_date': today
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['completion_date'] == today


def test_course_with_future_completion_date(client):
    """Test creating a course with a future completion date (should fail)"""
    future_date = (date.today() + timedelta(days=30)).isoformat()
    
    response = client.post('/api/course',
                          json={
                              'name': 'Advanced Machine Learning',
                              'provider': 'edX',
                              'completion_date': future_date
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'future' in data['details'].lower()


def test_course_without_completion_date(client):
    """Test creating a course without completion date (should succeed)"""
    response = client.post('/api/course',
                          json={
                              'name': 'Data Science Fundamentals',
                              'provider': 'DataCamp'
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['completion_date'] is None


def test_update_course_with_future_date(client):
    """Test updating a course with a future completion date (should fail)"""
    # First create a course with valid date
    past_date = (date.today() - timedelta(days=10)).isoformat()
    response = client.post('/api/course',
                          json={
                              'name': 'Web Development',
                              'provider': 'Udacity',
                              'completion_date': past_date
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    course_id = response.get_json()['id']
    
    # Try to update with future date
    future_date = (date.today() + timedelta(days=15)).isoformat()
    response = client.put(f'/api/course/{course_id}',
                         json={
                             'completion_date': future_date
                         },
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'future' in data['details'].lower()


def test_update_course_with_valid_date(client):
    """Test updating a course with a valid past date (should succeed)"""
    # First create a course
    past_date = (date.today() - timedelta(days=10)).isoformat()
    response = client.post('/api/course',
                          json={
                              'name': 'Database Design',
                              'provider': 'LinkedIn Learning',
                              'completion_date': past_date
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    course_id = response.get_json()['id']
    
    # Update with another valid past date
    new_past_date = (date.today() - timedelta(days=5)).isoformat()
    response = client.put(f'/api/course/{course_id}',
                         json={
                             'completion_date': new_past_date
                         },
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['completion_date'] == new_past_date
