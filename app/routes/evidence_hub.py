"""
Model  evidence_hub (New)
Version 2026 - Updated 29-01-2026
"""
import os
from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import EvidenceHubEntry

bp = Blueprint('evidence_hub', __name__)

ALLOWED_EXTENSIONS = {'.mp4', '.webm', '.mov'}

def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

def ensure_upload_dir() -> str:
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'evidence_videos')
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def ensure_defaults():
    defaults = [
        {
            'slug': 'qa-ui-automation',
            'title': 'UI Automation: Selenium and Cucumber',
            'stack': 'Java · Selenium · Cucumber · Maven',
            'description': 'Comprehensive UI tests that validate real user flows end to end',
            'display_order': 1
        },
        {
            'slug': 'api-automation',
            'title': 'API Automation: Postman and Newman',
            'stack': 'Postman · Newman · JSON · CI Ready',
            'description': 'Automated validation of critical API endpoints with assertions and reports',
            'display_order': 2
        },
        {
            'slug': 'data-science',
            'title': 'Data & Market Insights (API-driven)',
            'stack': 'Python · Pandas · API Integration · Analytical Modeling',
            'description': 'Demonstrates how public datasets and CV data are cross-referenced using a structured scoring model, exposed through REST APIs, and visualized in an interactive dashboard',
             'display_order': 3
        },
    ]

    for item in defaults:
        # Remove duplicates
        duplicates = EvidenceHubEntry.query.filter_by(slug=item['slug']).all()
        for duplicate in duplicates[1:]:  # Keep the first entry, delete the rest
            db.session.delete(duplicate)

        # Update or insert entry
        entry = EvidenceHubEntry.query.filter_by(slug=item['slug']).first()
        if entry:
            entry.title = item['title']
            entry.stack = item['stack']
            entry.description = item['description']
            entry.display_order = item['display_order']
        else:
            db.session.add(EvidenceHubEntry(**item))
    db.session.commit()

@bp.route('/api/evidence-hub')
def evidence_hub_list():
    ensure_defaults()
    entries = EvidenceHubEntry.query.filter_by(active=True).order_by(EvidenceHubEntry.display_order.asc()).all()
    return jsonify([
        {
            'slug': e.slug,
            'title': e.title,
            'stack': e.stack,
            'description': e.description,
            'video_path': e.video_path,
            'video_filename': e.video_filename
        } for e in entries
    ])

@bp.route('/api/evidence-hub/<slug>')
def evidence_hub_detail(slug):
    entry = EvidenceHubEntry.query.filter_by(slug=slug, active=True).first_or_404()
    return jsonify({
        'slug': entry.slug,
        'title': entry.title,
        'stack': entry.stack,
        'description': entry.description,
        'video_path': entry.video_path,
        'video_filename': entry.video_filename
    })

@bp.route('/evidence-hub/<slug>', methods=['GET', 'POST'])
def evidence_hub_watch_or_upload(slug):
    ensure_defaults()
    entry = EvidenceHubEntry.query.filter_by(slug=slug).first_or_404()

    if request.method == 'POST':
        admin_pw = os.environ.get('ADMIN_PASSWORD')
        provided_pw = request.form.get('pw')

        if admin_pw == "change-me-in-production":
            current_app.logger.warning(
                "ADMIN_PASSWORD is using default insecure value"
            )

        if not admin_pw or provided_pw != admin_pw:
            return render_template('evidence_hub_upload.html', entry=entry, error='Invalid or missing password.'), 401

        file = request.files.get('video_file')
        if not file or file.filename == '':
            return render_template('evidence_hub_upload.html', entry=entry, error='No file selected.'), 400

        if not allowed_file(file.filename):
            return render_template('evidence_hub_upload.html', entry=entry, error='Invalid file type. Use MP4/WEBM/MOV.'), 400

        upload_dir = ensure_upload_dir()
        filename = secure_filename(file.filename)
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)

        entry.video_path = f'/static/uploads/evidence_videos/{filename}'
        entry.video_filename = filename
        entry.updated_at = datetime.utcnow()
        db.session.commit()

    if entry.video_path:
        return render_template('evidence_hub_video.html', entry=entry)

    return render_template('evidence_hub_upload.html', entry=entry)


@bp.route('/populate-evidence-hub', methods=['POST'])
def populate_evidence_hub():
    """Populate the evidence_hub_entries table with default data."""
    try:
        ensure_defaults()
        return jsonify({"status": "success", "message": "Evidence Hub table populated."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@bp.route('/admin/evidence-hub/reset', methods=['POST'])
def reset_evidence_hub():
    admin_pw = os.environ.get('ADMIN_PASSWORD')
    if request.form.get('pw') != admin_pw:
        return jsonify({"error": "unauthorized"}), 401

    EvidenceHubEntry.query.delete()
    db.session.commit()
    ensure_defaults()
    return jsonify({"status": "reset complete"})
    