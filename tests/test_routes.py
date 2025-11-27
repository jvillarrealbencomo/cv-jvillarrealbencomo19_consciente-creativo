"""
Basic Route Tests
Test application routes
"""
import pytest


def test_index_route(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200


def test_education_route(client):
    """Test education page loads"""
    response = client.get('/education')
    assert response.status_code == 200


def test_experience_route(client):
    """Test experience page loads"""
    response = client.get('/experience')
    assert response.status_code == 200


def test_api_personal_data(client, sample_personal_data):
    """Test API endpoint for personal data"""
    response = client.get('/api/personal-data')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['full_name'] == "Test User"
    assert data['email'] == "test@example.com"


def test_profile_route(client):
    """Test profile page loads"""
    response = client.get('/profile/qa-analyst')
    assert response.status_code == 200
