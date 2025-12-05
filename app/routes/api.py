"""
API Routes
Version 2025 - RESTful API endpoints for data management
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models import Person, WorkExperience, TechnicalTool, Education, Certification, Course, Language, ITProduct, AdvancedTraining

bp = Blueprint('api', __name__, url_prefix='/api')


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


# Register other model endpoints
register_model_endpoints(Education, 'education')
register_model_endpoints(Certification, 'certification')
register_model_endpoints(Course, 'course')
register_model_endpoints(AdvancedTraining, 'advanced-training')
register_model_endpoints(Language, 'language')
register_model_endpoints(ITProduct, 'product')
