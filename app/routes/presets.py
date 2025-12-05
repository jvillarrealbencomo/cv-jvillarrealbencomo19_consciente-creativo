"""
Profile Presets API Routes
Version 2025 - Endpoints for managing profile presets
"""
from flask import Blueprint, jsonify, request
from app import db
from app.services.profile_presets import ProfilePresetService

bp = Blueprint('presets', __name__, url_prefix='/api/presets')


@bp.route('/', methods=['GET'])
def list_profiles():
    """
    Get list of available profiles
    
    Returns:
        JSON array of profile information
    """
    profiles = []
    for profile_name in ProfilePresetService.get_profile_names():
        profile_info = ProfilePresetService.get_profile_info(profile_name)
        profiles.append({
            'id': profile_name,
            'name': profile_info.get('name'),
            'description': profile_info.get('description'),
            'default_title': profile_info.get('default_title')
        })
    
    return jsonify({
        'profiles': profiles,
        'count': len(profiles)
    })


@bp.route('/<profile_name>', methods=['GET'])
def get_profile_details(profile_name):
    """
    Get detailed configuration for a specific profile
    
    Args:
        profile_name: Profile identifier
        
    Returns:
        JSON with complete profile configuration
    """
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Profile not found'}), 404
    
    summary = ProfilePresetService.create_profile_summary(profile_name)
    
    return jsonify({
        'profile_name': profile_name,
        'configuration': summary
    })


@bp.route('/<profile_name>/tool-categories', methods=['GET'])
def get_tool_categories(profile_name):
    """
    Get tool subcategories for a specific profile
    
    Args:
        profile_name: Profile identifier
        
    Returns:
        JSON array of category names in priority order
    """
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Profile not found'}), 404
    
    categories = ProfilePresetService.get_tool_categories(profile_name)
    
    return jsonify({
        'profile_name': profile_name,
        'categories': categories,
        'count': len(categories)
    })


@bp.route('/<profile_name>/apply', methods=['POST'])
def apply_profile_preset(profile_name):
    """
    Apply profile preset to all records in database
    
    Args:
        profile_name: Profile identifier
        
    Request body (optional):
        {
            "dry_run": false,  // If true, return what would be changed without applying
            "sections": ["work_experience", "technical_tools"]  // Limit to specific sections
        }
        
    Returns:
        JSON with application results
    """
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Profile not found'}), 404
    
    data = request.get_json() or {}
    dry_run = data.get('dry_run', False)
    sections = data.get('sections', None)
    
    try:
        if dry_run:
            # Return preview of what would be changed
            summary = ProfilePresetService.create_profile_summary(profile_name)
            return jsonify({
                'profile_name': profile_name,
                'dry_run': True,
                'changes_preview': summary,
                'message': 'Preview only - no changes applied'
            })
        
        # Apply preset to database
        ProfilePresetService.apply_full_preset(db.session, profile_name)
        
        return jsonify({
            'profile_name': profile_name,
            'success': True,
            'message': f'Profile preset "{profile_name}" applied successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to apply preset',
            'details': str(e)
        }), 500


@bp.route('/compare', methods=['POST'])
def compare_profiles():
    """
    Compare configurations between multiple profiles
    
    Request body:
        {
            "profiles": ["qa_analyst", "qa_engineer", "data_scientist"]
        }
        
    Returns:
        JSON with side-by-side comparison
    """
    data = request.get_json()
    if not data or 'profiles' not in data:
        return jsonify({'error': 'profiles array required'}), 400
    
    profiles = data['profiles']
    
    # Validate profiles
    invalid = [p for p in profiles if p not in ProfilePresetService.get_profile_names()]
    if invalid:
        return jsonify({'error': f'Invalid profiles: {invalid}'}), 400
    
    # Build comparison
    comparison = {}
    for profile_name in profiles:
        comparison[profile_name] = ProfilePresetService.create_profile_summary(profile_name)
    
    return jsonify({
        'comparison': comparison,
        'profile_count': len(profiles)
    })


@bp.route('/person/<int:person_id>/apply/<profile_name>', methods=['POST'])
def apply_person_preset(person_id, profile_name):
    """
    Apply profile preset to specific Person record
    
    Args:
        person_id: Person record ID
        profile_name: Profile identifier
        
    Returns:
        JSON with updated person data
    """
    from app.models import Person
    
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Profile not found'}), 404
    
    person = db.session.get(Person, person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404
    
    try:
        ProfilePresetService.apply_person_preset(person, profile_name)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'person_id': person_id,
            'profile_name': profile_name,
            'person': person.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to apply person preset',
            'details': str(e)
        }), 500


@bp.route('/experience/<int:exp_id>/apply/<profile_name>', methods=['POST'])
def apply_experience_preset(exp_id, profile_name):
    """
    Apply profile preset to specific WorkExperience record
    
    Args:
        exp_id: WorkExperience record ID
        profile_name: Profile identifier
        
    Returns:
        JSON with updated experience data
    """
    from app.models import WorkExperience
    
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Profile not found'}), 404
    
    experience = db.session.get(WorkExperience, exp_id)
    if not experience:
        return jsonify({'error': 'Experience not found'}), 404
    
    try:
        ProfilePresetService.apply_experience_preset(experience, profile_name)
        ProfilePresetService.apply_model_preset(experience, profile_name, visible=True)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'experience_id': exp_id,
            'profile_name': profile_name,
            'experience': experience.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to apply experience preset',
            'details': str(e)
        }), 500


@bp.route('/tool/<int:tool_id>/apply/<profile_name>', methods=['POST'])
def apply_tool_preset(tool_id, profile_name):
    """
    Apply profile preset to specific TechnicalTool record
    
    Args:
        tool_id: TechnicalTool record ID
        profile_name: Profile identifier
        
    Request body (optional):
        {
            "subcategory": "Test Automation",  // Override default subcategory
            "usable": true  // Override default usability
        }
        
    Returns:
        JSON with updated tool data
    """
    from app.models import TechnicalTool
    
    if profile_name not in ProfilePresetService.get_profile_names():
        return jsonify({'error': 'Profile not found'}), 404
    
    tool = db.session.get(TechnicalTool, tool_id)
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    data = request.get_json() or {}
    subcategory = data.get('subcategory')
    usable = data.get('usable', True)
    
    try:
        ProfilePresetService.apply_tool_preset(tool, profile_name, subcategory, usable)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tool_id': tool_id,
            'profile_name': profile_name,
            'tool': tool.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to apply tool preset',
            'details': str(e)
        }), 500
