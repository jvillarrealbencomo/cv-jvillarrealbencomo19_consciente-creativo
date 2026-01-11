"""
API Routes
Version 2025 - RESTful API endpoints for data management
"""
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Person, WorkExperience, TechnicalTool, Education, Certification, Course, Language, ITProduct, AdvancedTraining
from app.services.image_service import ImageService

bp = Blueprint('api', __name__, url_prefix='/api')


ALLOWED_IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}


def _allowed_image(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_IMAGE_EXTS


def _get_request_data():
    """Return request data as dict supporting JSON and multipart forms."""
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        return request.form.to_dict()
    return request.get_json() or {}


def _parse_bool_fields(data, fields):
    for field in fields:
        if field in data:
            if isinstance(data[field], str):
                data[field] = data[field].lower() in ('true', '1', 'yes', 'on')
            else:
                data[field] = bool(data[field])


def _parse_int_fields(data, fields):
    for field in fields:
        if field in data:
            try:
                data[field] = int(data[field]) if data[field] not in (None, '') else None
            except (TypeError, ValueError):
                data[field] = None


def _parse_date_fields(data, fields):
    for field in fields:
        if field in data:
            if data[field] in (None, ''):
                data[field] = None
            elif isinstance(data[field], str):
                try:
                    data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                except ValueError:
                    data[field] = None


# Person endpoints
@bp.route('/person', methods=['GET', 'POST'])
def person_list():
    """List all people or create new person"""
    if request.method == 'POST':
        data = request.get_json() or {}
        # Remove client-provided id to avoid type mismatch on Integer PK
        if 'id' in data:
            data.pop('id', None)
        # Map first_name/last_name into full_name if provided
        first = data.pop('first_name', '').strip()
        last = data.pop('last_name', '').strip()
        if not data.get('full_name'):
            data['full_name'] = (first + ' ' + last).strip() if first or last else first or last or 'Unnamed'
        # Derive professional_title fallback from provided profile-specific titles
        if not data.get('professional_title'):
            data['professional_title'] = data.get('title_qa_engineer') or data.get('title_qa_analyst') or data.get('title_data_scientist') or 'Professional'
        try:
            # Initialize Person with required fields explicitly to avoid SQLite placeholder mismatch
            person = Person(
                full_name=data.pop('full_name', 'Unnamed'),
                professional_title=data.pop('professional_title', 'Professional')
            )
            # Set remaining provided fields
            for key, value in data.items():
                if hasattr(person, key) and not key.startswith('_'):
                    # Coerce common boolean string values to bool
                    if isinstance(value, str) and value.lower() in ('true','false','on','off'):
                        value = value.lower() in ('true','on')
                    setattr(person, key, value)
            db.session.add(person)
            db.session.commit()
            return jsonify(person.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create person', 'details': str(e)}), 400
    
    # Return only current (non-historical) active people
    people = Person.query.filter_by(active=True, is_historical=False).all()
    return jsonify([p.to_dict() for p in people])


@bp.route('/person/history', methods=['GET'])
def person_history():
    """Get all person records including historical versions"""
    # Return all records ordered by creation date (newest first)
    all_people = Person.query.filter_by(active=True).order_by(Person.created_at.desc()).all()
    return jsonify([p.to_dict() for p in all_people])


@bp.route('/person/<int:person_id>', methods=['GET', 'PUT', 'DELETE'])
def person_detail(person_id):
    """Get, update, or delete a person"""
    person = db.session.get(Person, person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404
    
    if request.method == 'DELETE':
        person.active = False
        db.session.commit()
        return '', 204
    
    if request.method == 'PUT':
        try:
            data = request.get_json() or {}
            # Remove client-provided id to avoid accidental PK assignment
            if 'id' in data:
                data.pop('id', None)
            first = data.pop('first_name', '').strip()
            last = data.pop('last_name', '').strip()
            if (first or last) and not data.get('full_name'):
                data['full_name'] = (first + ' ' + last).strip()
            if 'professional_title' not in data:
                # refresh fallback if profile-specific titles updated
                if any(k in data for k in ['title_qa_engineer','title_qa_analyst','title_data_scientist']):
                    data['professional_title'] = data.get('title_qa_engineer') or data.get('title_qa_analyst') or data.get('title_data_scientist') or person.professional_title
            for key, value in data.items():
                if hasattr(person, key):
                    if isinstance(value, str) and value.lower() in ('true','false','on','off'):
                        value = value.lower() in ('true','on')
                    setattr(person, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update person', 'details': str(e)}), 400
    
    return jsonify(person.to_dict())


@bp.route('/person/<int:person_id>/image', methods=['POST', 'DELETE'])
def person_image_upload(person_id):
    """Upload or clear profile image for a person"""
    person = db.session.get(Person, person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404

    if request.method == 'DELETE':
        person.profile_image_url = None
        db.session.commit()
        return '', 204

    if 'image' not in request.files:
        return jsonify({'error': 'No file part "image" provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    if not _allowed_image(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    filename = secure_filename(file.filename)
    _, ext = os.path.splitext(filename)
    # Use deterministic name per person to avoid orphaned files
    filename = f"person_{person_id}{ext.lower()}"

    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'profiles')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    person.profile_image_url = f"/static/uploads/profiles/{filename}"
    db.session.commit()

    return jsonify({'profile_image_url': person.profile_image_url}), 200


# WorkExperience endpoints
@bp.route('/experience', methods=['GET', 'POST'])
def experience_list():
    """List all work experiences or create new"""
    if request.method == 'POST':
        data = request.get_json() or {}
        # Remove client-provided id and UI-only fields
        for field in ['id', 'contentLevel']:
            data.pop(field, None)
        
        # Convert date strings to date objects (YYYY-MM-DD)
        from datetime import datetime
        for field in ['start_date', 'end_date']:
            if field in data and data[field]:
                if isinstance(data[field], str):
                    try:
                        data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                    except ValueError:
                        data[field] = None
        
        # Convert boolean strings
        boolean_fields = ['is_current', 'show_responsibilities_summary', 'show_responsibilities_detailed', 
                         'show_achievements', 'visible_qa_analyst', 'visible_qa_engineer', 
                         'visible_data_scientist', 'is_historical']
        for field in boolean_fields:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].lower() in ('true', '1', 'yes')
        
        try:
            exp = WorkExperience(**data)
            db.session.add(exp)
            db.session.commit()
            return jsonify(exp.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create experience', 'details': str(e)}), 400
    
    experiences = WorkExperience.query.filter_by(active=True).all()
    return jsonify([e.to_dict() for e in experiences])


@bp.route('/experience/<int:exp_id>', methods=['GET', 'PUT', 'DELETE'])
def experience_detail(exp_id):
    """Get, update, or delete a work experience"""
    exp = db.session.get(WorkExperience, exp_id)
    if not exp:
        return jsonify({'error': 'Experience not found'}), 404
    
    if request.method == 'DELETE':
        exp.active = False
        db.session.commit()
        return '', 204
    
    if request.method == 'PUT':
        data = request.get_json() or {}
        # Remove id and UI-only fields
        for field in ['id', 'contentLevel']:
            data.pop(field, None)
        
        # Convert date strings (YYYY-MM-DD)
        from datetime import datetime
        for field in ['start_date', 'end_date']:
            if field in data and data[field]:
                if isinstance(data[field], str):
                    try:
                        data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                    except ValueError:
                        data[field] = None
        
        # Convert boolean strings
        boolean_fields = ['is_current', 'show_responsibilities_summary', 'show_responsibilities_detailed', 
                         'show_achievements', 'visible_qa_analyst', 'visible_qa_engineer', 
                         'visible_data_scientist', 'is_historical']
        for field in boolean_fields:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].lower() in ('true', '1', 'yes')
        
        try:
            for key, value in data.items():
                if hasattr(exp, key):
                    setattr(exp, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update experience', 'details': str(e)}), 400
    
    return jsonify(exp.to_dict())


# TechnicalTool endpoints
@bp.route('/tool', methods=['GET', 'POST'])
def tool_list():
    """List all technical tools or create new"""
    if request.method == 'POST':
        data = request.get_json() or {}
        # Remove client-provided id
        if 'id' in data:
            data.pop('id', None)
        
        # Convert boolean strings
        boolean_fields = ['usable_qa_analyst', 'usable_qa_engineer', 'usable_data_scientist', 'is_historical']
        for field in boolean_fields:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].lower() in ('true', '1', 'yes')
        
        try:
            tool = TechnicalTool(**data)
            db.session.add(tool)
            db.session.commit()
            return jsonify(tool.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create tool', 'details': str(e)}), 400
    
    tools = TechnicalTool.query.filter_by(active=True).all()
    return jsonify([t.to_dict() for t in tools])


@bp.route('/tool/<int:tool_id>', methods=['GET', 'PUT', 'DELETE'])
def tool_detail(tool_id):
    """Get, update, or delete a technical tool"""
    tool = db.session.get(TechnicalTool, tool_id)
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    if request.method == 'DELETE':
        tool.active = False
        db.session.commit()
        return '', 204
    
    if request.method == 'PUT':
        data = request.get_json() or {}
        # Remove id if present
        if 'id' in data:
            data.pop('id', None)
        
        # Convert boolean strings
        boolean_fields = ['usable_qa_analyst', 'usable_qa_engineer', 'usable_data_scientist', 'is_historical']
        for field in boolean_fields:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].lower() in ('true', '1', 'yes')
        
        try:
            for key, value in data.items():
                if hasattr(tool, key):
                    setattr(tool, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update tool', 'details': str(e)}), 400
    
    return jsonify(tool.to_dict())


# Education endpoints (supporting credential images)
@bp.route('/education', methods=['GET', 'POST'])
def education_list():
    if request.method == 'POST':
        data = _get_request_data()
        data.pop('id', None)

        _parse_int_fields(data, ['year_obtained', 'start_year', 'end_year', 'display_order'])
        _parse_bool_fields(data, ['visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 'is_current', 'is_historical'])

        # Normalize empty strings
        for field in ['details', 'document_url', 'country']:
            if field in data and data[field] == '':
                data[field] = None

        try:
            edu = Education(**data)
            db.session.add(edu)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create education', 'details': str(e)}), 400

        file = request.files.get('credential_image') or request.files.get('image')
        if file and file.filename:
            try:
                saved = ImageService.save_credential_image(file, 'education', edu.id)
                if saved:
                    edu.image_path = saved['image_path']
                    edu.image_thumbnail_path = saved['thumbnail_path']
                    edu.image_filename = saved['filename']
                    edu.image_mime_type = saved['mime_type']
                    db.session.commit()
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': 'Invalid image', 'details': str(e)}), 400

        return jsonify(edu.to_dict()), 201

    educations = Education.query.filter_by(active=True).order_by(Education.display_order.asc()).all()
    return jsonify([e.to_dict() for e in educations])


@bp.route('/education/<int:edu_id>', methods=['GET', 'PUT', 'DELETE'])
def education_detail(edu_id):
    edu = db.session.get(Education, edu_id)
    if not edu:
        return jsonify({'error': 'Education not found'}), 404

    if request.method == 'DELETE':
        edu.active = False
        db.session.commit()
        return '', 204

    if request.method == 'PUT':
        data = _get_request_data()
        data.pop('id', None)

        _parse_int_fields(data, ['year_obtained', 'start_year', 'end_year', 'display_order'])
        _parse_bool_fields(data, ['visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 'is_current', 'is_historical'])

        for field in ['details', 'document_url', 'country']:
            if field in data and data[field] == '':
                data[field] = None

        remove_image = False
        if 'remove_image' in data:
            val = str(data.pop('remove_image')).lower()
            remove_image = val in ('true', '1', 'yes', 'on')

        try:
            for key, value in data.items():
                if hasattr(edu, key):
                    setattr(edu, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update education', 'details': str(e)}), 400

        old_image = (edu.image_path, edu.image_thumbnail_path)

        file = request.files.get('credential_image') or request.files.get('image')
        if file and file.filename:
            try:
                saved = ImageService.save_credential_image(file, 'education', edu.id)
                if saved:
                    edu.image_path = saved['image_path']
                    edu.image_thumbnail_path = saved['thumbnail_path']
                    edu.image_filename = saved['filename']
                    edu.image_mime_type = saved['mime_type']
                    db.session.commit()
                    ImageService.delete_credential_image(old_image[0], old_image[1])
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': 'Invalid image', 'details': str(e)}), 400

        if remove_image and old_image[0]:
            ImageService.delete_credential_image(old_image[0], old_image[1])
            edu.image_path = None
            edu.image_thumbnail_path = None
            edu.image_filename = None
            edu.image_mime_type = None
            db.session.commit()

    return jsonify(edu.to_dict())


# Advanced Training endpoints (courses + certifications) with images
@bp.route('/advanced-training', methods=['GET', 'POST'])
def advanced_training_list():
    if request.method == 'POST':
        data = _get_request_data()
        data.pop('id', None)

        _parse_date_fields(data, ['completion_date', 'expiration_date'])
        _parse_int_fields(data, ['duration_hours', 'display_order'])
        _parse_bool_fields(data, ['visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 'is_historical'])

        for field in ['credential_id', 'credential_url', 'description']:
            if field in data and data[field] == '':
                data[field] = None

        # remove_image can be present from the form but is not a model field; drop it to avoid **kwargs errors
        if 'remove_image' in data:
            data.pop('remove_image', None)

        try:
            training = AdvancedTraining(**data)
            db.session.add(training)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create advanced training', 'details': str(e)}), 400

        file = request.files.get('credential_image') or request.files.get('image')
        if file and file.filename:
            try:
                saved = ImageService.save_credential_image(file, 'advanced_training', training.id)
                if saved:
                    training.image_path = saved['image_path']
                    training.image_thumbnail_path = saved['thumbnail_path']
                    training.image_filename = saved['filename']
                    training.image_mime_type = saved['mime_type']
                    db.session.commit()
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': 'Invalid image', 'details': str(e)}), 400

        return jsonify(training.to_dict()), 201

    trainings = AdvancedTraining.query.filter_by(active=True).order_by(AdvancedTraining.display_order.asc()).all()
    return jsonify([t.to_dict() for t in trainings])


@bp.route('/advanced-training/<int:training_id>', methods=['GET', 'PUT', 'DELETE'])
def advanced_training_detail(training_id):
    training = db.session.get(AdvancedTraining, training_id)
    if not training:
        return jsonify({'error': 'AdvancedTraining not found'}), 404

    if request.method == 'DELETE':
        training.active = False
        db.session.commit()
        return '', 204

    if request.method == 'PUT':
        data = _get_request_data()
        data.pop('id', None)

        _parse_date_fields(data, ['completion_date', 'expiration_date'])
        _parse_int_fields(data, ['duration_hours', 'display_order'])
        _parse_bool_fields(data, ['visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 'is_historical'])

        for field in ['credential_id', 'credential_url', 'description']:
            if field in data and data[field] == '':
                data[field] = None

        remove_image = False
        if 'remove_image' in data:
            val = str(data.pop('remove_image')).lower()
            remove_image = val in ('true', '1', 'yes', 'on')

        try:
            for key, value in data.items():
                if hasattr(training, key):
                    setattr(training, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update advanced training', 'details': str(e)}), 400

        old_image = (training.image_path, training.image_thumbnail_path)

        file = request.files.get('credential_image') or request.files.get('image')
        if file and file.filename:
            try:
                saved = ImageService.save_credential_image(file, 'advanced_training', training.id)
                if saved:
                    training.image_path = saved['image_path']
                    training.image_thumbnail_path = saved['thumbnail_path']
                    training.image_filename = saved['filename']
                    training.image_mime_type = saved['mime_type']
                    db.session.commit()
                    ImageService.delete_credential_image(old_image[0], old_image[1])
            except ValueError as e:
                db.session.rollback()
                return jsonify({'error': 'Invalid image', 'details': str(e)}), 400

        if remove_image and old_image[0]:
            ImageService.delete_credential_image(old_image[0], old_image[1])
            training.image_path = None
            training.image_thumbnail_path = None
            training.image_filename = None
            training.image_mime_type = None
            db.session.commit()

    return jsonify(training.to_dict())


# Generic CRUD endpoints for other models
def register_model_endpoints(model_class, endpoint_prefix):
    """Register standard CRUD endpoints with unique endpoint names."""

    def list_create():
        if request.method == 'POST':
            data = request.get_json() or {}
            # Remove client-provided id
            if 'id' in data:
                data.pop('id', None)
            
            # Convert date strings to date objects (handle empty strings)
            from datetime import datetime
            for field in ['issue_date', 'expiration_date', 'completion_date', 'certification_date']:
                if field in data:
                    if data[field] == '' or data[field] is None:
                        data[field] = None
                    elif isinstance(data[field], str):
                        try:
                            data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                        except ValueError:
                            data[field] = None
            
            # Convert empty strings to None for optional text fields
            optional_text_fields = ['credential_id', 'credential_url', 'description', 'document_url', 
                                   'details', 'skills_acquired', 'location', 'certification_name', 
                                   'certification_score']
            for field in optional_text_fields:
                if field in data and data[field] == '':
                    data[field] = None
            
            # Convert boolean strings
            boolean_fields = ['visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 
                             'is_current', 'is_historical']
            for field in boolean_fields:
                if field in data and isinstance(data[field], str):
                    data[field] = data[field].lower() in ('true', '1', 'yes')
            
            try:
                instance = model_class(**data)
                db.session.add(instance)
                db.session.commit()
                return jsonify(instance.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Failed to create {model_class.__name__}', 'details': str(e)}), 400

        instances = model_class.query.filter_by(active=True).all()
        return jsonify([i.to_dict() for i in instances])

    def detail(item_id):
        instance = db.session.get(model_class, item_id)
        if not instance:
            return jsonify({'error': f'{model_class.__name__} not found'}), 404

        if request.method == 'DELETE':
            instance.active = False
            db.session.commit()
            return '', 204

        if request.method == 'PUT':
            data = request.get_json() or {}
            # Remove id if present
            if 'id' in data:
                data.pop('id', None)
            
            # Convert date strings (handle empty strings)
            from datetime import datetime
            for field in ['issue_date', 'expiration_date', 'completion_date', 'certification_date']:
                if field in data:
                    if data[field] == '' or data[field] is None:
                        data[field] = None
                    elif isinstance(data[field], str):
                        try:
                            data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                        except ValueError:
                            data[field] = None
            
            # Convert empty strings to None for optional text fields
            optional_text_fields = ['credential_id', 'credential_url', 'description', 'document_url', 
                                   'details', 'skills_acquired', 'location', 'certification_name', 
                                   'certification_score']
            for field in optional_text_fields:
                if field in data and data[field] == '':
                    data[field] = None
            
            # Convert boolean strings
            boolean_fields = ['visible_qa_analyst', 'visible_qa_engineer', 'visible_data_scientist', 
                             'is_current', 'is_historical']
            for field in boolean_fields:
                if field in data and isinstance(data[field], str):
                    data[field] = data[field].lower() in ('true', '1', 'yes')
            
            try:
                for key, value in data.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Failed to update {model_class.__name__}', 'details': str(e)}), 400

        return jsonify(instance.to_dict())

    # Register routes with unique endpoint names
    bp.add_url_rule(f'/{endpoint_prefix}', view_func=list_create, methods=['GET', 'POST'], endpoint=f'{endpoint_prefix}_list')
    bp.add_url_rule(f'/{endpoint_prefix}/<int:item_id>', view_func=detail, methods=['GET', 'PUT', 'DELETE'], endpoint=f'{endpoint_prefix}_detail')


# Register remaining model endpoints (education and advanced_training have custom handlers above)
register_model_endpoints(Certification, 'certification')
register_model_endpoints(Course, 'course')
register_model_endpoints(Language, 'language')
register_model_endpoints(ITProduct, 'product')
