"""
Data Management UI for viewing and managing CV records
Version 2026 - Updates to password-protected tables with CI and pw of production
"""
from flask import render_template, jsonify, request
from app import db
from app.models.work_experience import WorkExperience
from app.models.education import Education
from app.models.advanced_training import AdvancedTraining
from app.models.personal_data import Person
from app.models import EvidenceHubEntry

ALLOWED_ADMIN_PASSWORDS = {"9003712", "change-me-in-production"}

def _check_admin_password():
    payload = request.get_json(silent=True) or {}
    pwd = payload.get("admin_password") or request.form.get("admin_password")
    return pwd in ALLOWED_ADMIN_PASSWORDS

def init_data_management_routes(app):
    @app.route('/admin/data-management')
    def data_management():
        person = db.session.get(Person, 1)

        work_experiences = WorkExperience.query.order_by(WorkExperience.id).all()
        education = Education.query.order_by(Education.id).all()
        advanced_training = AdvancedTraining.query.order_by(AdvancedTraining.id).all()
        persons = Person.query.order_by(Person.id).all()
        evidence_hub_entries = EvidenceHubEntry.query.order_by(EvidenceHubEntry.id).all() if EvidenceHubEntry else []

        return render_template(
            'admin/data_management.html',
            person=person,
            work_experiences=work_experiences,
            education=education,
            advanced_training=advanced_training,
            persons=persons,
            evidence_hub_entries=evidence_hub_entries
        )

    @app.route('/api/data-management/record/<record_type>/<int:record_id>/restore', methods=['POST'])
    def restore_record(record_type, record_id):
        if not _check_admin_password():
            return jsonify({'error': 'Admin password required'}), 403

        model_map = {
            'experience': WorkExperience,
            'education': Education,
            'training': AdvancedTraining,
            'person': Person,
            'evidence': EvidenceHubEntry
        }
        model = model_map.get(record_type)
        if not model:
            return jsonify({'error': 'Invalid record type'}), 400
        record = db.session.get(model, record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        if not hasattr(record, 'active'):
            return jsonify({'error': 'Record type does not support restore'}), 400

        record.active = True
        db.session.commit()
        return jsonify({'message': f'{record_type.title()} record restored'}), 200

    @app.route('/api/data-management/record/<record_type>/<int:record_id>/soft-delete', methods=['POST'])
    def soft_delete_record(record_type, record_id):
        if not _check_admin_password():
            return jsonify({'error': 'Admin password required'}), 403

        model_map = {
            'experience': WorkExperience,
            'education': Education,
            'training': AdvancedTraining,
            'person': Person,
            'evidence': EvidenceHubEntry
        }
        model = model_map.get(record_type)
        if not model:
            return jsonify({'error': 'Invalid record type'}), 400
        record = db.session.get(model, record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        if not hasattr(record, 'active'):
            return jsonify({'error': 'Record type does not support soft delete'}), 400

        record.active = False
        db.session.commit()
        return jsonify({'message': f'{record_type.title()} record deleted'}), 200

    @app.route('/api/data-management/record/<record_type>/<int:record_id>/permanent-delete', methods=['POST'])
    def permanent_delete_record(record_type, record_id):
        if not _check_admin_password():
            return jsonify({'error': 'Admin password required'}), 403

        model_map = {
            'experience': WorkExperience,
            'education': Education,
            'training': AdvancedTraining,
            'person': Person,
            'evidence': EvidenceHubEntry
        }
        model = model_map.get(record_type)
        if not model:
            return jsonify({'error': 'Invalid record type'}), 400
        record = db.session.get(model, record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': f'{record_type.title()} record permanently deleted'}), 200