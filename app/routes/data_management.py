"""
Data Management UI for viewing and managing CV records
"""
from flask import render_template, jsonify, request
from app import db
from app.models.work_experience import WorkExperience
from app.models.education import Education
from app.models.advanced_training import AdvancedTraining
from app.models.personal_data import Person


def init_data_management_routes(app):
    """Initialize data management routes"""
    
    @app.route('/admin/data-management')
    def data_management():
        """Display data management UI"""
        person = db.session.get(Person, 1)  # Get first person (main CV)
        
        # Get all records grouped by type
        work_experiences = WorkExperience.query.order_by(WorkExperience.id).all()
        education = Education.query.order_by(Education.id).all()
        advanced_training = AdvancedTraining.query.order_by(AdvancedTraining.id).all()
        
        return render_template('admin/data_management.html',
                             person=person,
                             work_experiences=work_experiences,
                             education=education,
                             advanced_training=advanced_training)
    
    @app.route('/api/data-management/record/<record_type>/<int:record_id>/restore', methods=['POST'])
    def restore_record(record_type, record_id):
        """Restore a soft-deleted record (set active=True)"""
        model_map = {
            'experience': WorkExperience,
            'education': Education,
            'training': AdvancedTraining
        }
        
        model = model_map.get(record_type)
        if not model:
            return jsonify({'error': 'Invalid record type'}), 400
        
        record = db.session.get(model, record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        record.active = True
        db.session.commit()
        
        return jsonify({'message': f'{record_type.title()} record restored'}), 200
    
    @app.route('/api/data-management/record/<record_type>/<int:record_id>/soft-delete', methods=['POST'])
    def soft_delete_record(record_type, record_id):
        """Soft delete a record (set active=False)"""
        model_map = {
            'experience': WorkExperience,
            'education': Education,
            'training': AdvancedTraining
        }
        
        model = model_map.get(record_type)
        if not model:
            return jsonify({'error': 'Invalid record type'}), 400
        
        record = db.session.get(model, record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        record.active = False
        db.session.commit()
        
        return jsonify({'message': f'{record_type.title()} record deleted'}), 200
    
    @app.route('/api/data-management/record/<record_type>/<int:record_id>/permanent-delete', methods=['POST'])
    def permanent_delete_record(record_type, record_id):
        """Permanently delete a record from database"""
        model_map = {
            'experience': WorkExperience,
            'education': Education,
            'training': AdvancedTraining
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
