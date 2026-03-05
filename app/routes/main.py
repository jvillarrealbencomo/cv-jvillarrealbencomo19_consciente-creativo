"""
Main Routes
Version 2025 - Public-facing pages
Version 2026 - Updated 29-01-2026
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

from app import db
from app.models import Person
from app.services.profile_presets import ProfilePresetService
from app.models import EvidenceHubEntry

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    try:
        if 'origin' not in session:
            session['origin'] = request.referrer
    except RuntimeError:
        pass
    """Home page"""
    profiles = []
    for profile_name in ProfilePresetService.get_profile_names():
        info = ProfilePresetService.get_profile_info(profile_name)
        profiles.append({
            'id': profile_name,
            'name': info.get('name'),
            'description': info.get('description')
        })

    # Get Evidence Hub entries
    evidence_hub_entries = EvidenceHubEntry.query.filter_by(active=True).order_by(EvidenceHubEntry.display_order.asc()).all()
    if not evidence_hub_entries:
        from app.routes.evidence_hub import ensure_defaults
        ensure_defaults()
        evidence_hub_entries = EvidenceHubEntry.query.filter_by(active=True).order_by(EvidenceHubEntry.display_order.asc()).all()

    # Get the primary active person (used for direct PDF export buttons)
    person = Person.query.filter_by(active=True, is_historical=False).first()
    person_id = person.id if person else None

    return render_template(
        'index.html',
        profiles=profiles,
        person_id=person_id,
        evidence_hub_entries=evidence_hub_entries
    )

@bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2025.1.0',
        'service': 'CV Application'
    })


@bp.route('/system-overview')
def system_overview():
    """System Overview page - Technical design documentation"""
    return render_template('system_overview.html')


@bp.route('/platform-overview')
def platform_overview():
    """Platform Overview page - Functional documentation"""
    return render_template('platform_overview.html')


@bp.route('/data-insights')
def data_insights():
    """Data Insights Dashboard"""
    return render_template('data_insights.html')


@bp.route('/developer/data-insights-debug')
def data_insights_debug():
    """Developer-only Data Insights Dashboard with detailed skill breakdowns"""
    return render_template('developer/data_insights_debug.html')


@bp.route('/legacy/cv2019')
def cv2019():
    """Legacy CV 2019 - Archives the old CV format with full functionality"""
    return render_template('legacy/inicio2.html')

