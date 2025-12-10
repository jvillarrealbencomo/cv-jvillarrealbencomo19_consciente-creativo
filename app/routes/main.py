"""
Main Routes
Version 2025 - Public-facing pages
"""
from flask import Blueprint, render_template, jsonify
from app.services.profile_presets import ProfilePresetService

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page"""
    profiles = []
    for profile_name in ProfilePresetService.get_profile_names():
        info = ProfilePresetService.get_profile_info(profile_name)
        profiles.append({
            'id': profile_name,
            'name': info.get('name'),
            'description': info.get('description')
        })
    
    return render_template('index.html', profiles=profiles)


@bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2025.1.0',
        'service': 'CV Application'
    })


@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@bp.route('/legacy/cv2019')
def cv2019():
    """Legacy CV 2019 - Archives the old CV format with full functionality"""
    return render_template('cv2019.html')
