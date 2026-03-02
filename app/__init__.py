"""
Flask Application Factory
Version 2025 - Application initialization and configuration
Version 2026 - Updated 29-01-2026
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name (development, testing, production)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    from config import get_config
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)
    
    # Ensure required directories exist
    os.makedirs(app.config['PDF_TEMP_DIR'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_commands(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        from app.models.app_metadata import ensure_app_metadata_defaults, get_app_metadata_value
        from app.models.app_schema_version import ensure_schema_version
        from app.models.support_tools import ensure_data_scientist_tool_defaults, apply_data_scientist_skill_order
        ensure_app_metadata_defaults()
        schema_version = get_app_metadata_value("application_version", "2026.2.0")
        ensure_schema_version(schema_version)
        ensure_data_scientist_tool_defaults()
        apply_data_scientist_skill_order()

    @app.context_processor
    def inject_app_metadata():
        from app.models.app_metadata import get_app_metadata_dict
        entries = get_app_metadata_dict()
        return {
            'app_metadata': entries
        }
    
    @app.context_processor
    def inject_profile_image():
        from app.models.personal_data import Person
        person = Person.query.filter_by(active=True, is_historical=False).first()
        profile_image_url = person.profile_image_url if person and person.profile_image_url else None
        return {
            'navbar_profile_image': profile_image_url
        }
    
    return app


def register_blueprints(app):
    """Register Flask blueprints"""
    from app.routes import main, admin, profiles, api, presets, forms, data_management, data_insights
    from app.routes.legacy import legacy_bp   # <--- aquí importas tu blueprint    
    from app.routes.data_import import data_import_bp  # Temporary import route
    from app.routes.image_upload import image_upload_bp  # Temporary image upload route
    from app.routes.evidence_hub import bp as evidence_hub_bp

    app.register_blueprint(evidence_hub_bp) 
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(profiles.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(presets.bp)
    app.register_blueprint(forms.bp)
    app.register_blueprint(data_insights.bp)
    app.register_blueprint(legacy_bp)
    app.register_blueprint(data_import_bp)  # Temporary - remove after migration
    app.register_blueprint(image_upload_bp)  # Temporary - remove after migration
    
    # Register data management routes
    data_management.init_data_management_routes(app)


def register_error_handlers(app):
    """Register error handlers"""
    from flask import jsonify, render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        if request_wants_json():
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request_wants_json():
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        if request_wants_json():
            return jsonify({'error': 'Forbidden'}), 403
        return render_template('errors/403.html'), 403


def register_commands(app):
    """Register CLI commands"""
    import click
    
    @app.cli.command()
    def init_db():
        """Initialize the database with sample data"""
        from app.services.profile_presets import ProfilePresetService
        
        click.echo('Creating database tables...')
        db.create_all()
        click.echo('Database tables created.')
        
        # Optional: Add sample data
        click.echo('Sample data initialization can be added here.')
        click.echo('Database initialized successfully!')
    
    @app.cli.command()
    @click.argument('profile_name')
    def apply_preset(profile_name):
        """Apply profile preset to all records"""
        from app.services.profile_presets import ProfilePresetService
        
        if profile_name not in ProfilePresetService.get_profile_names():
            click.echo(f'Error: Invalid profile name. Choose from: {ProfilePresetService.get_profile_names()}')
            return
        
        click.echo(f'Applying preset for profile: {profile_name}')
        ProfilePresetService.apply_full_preset(db.session, profile_name)
        click.echo('Preset applied successfully!')
    
    @app.cli.command()
    def list_profiles():
        """List available profile presets"""
        from app.services.profile_presets import ProfilePresetService
        
        click.echo('Available profile presets:')
        for profile_name in ProfilePresetService.get_profile_names():
            info = ProfilePresetService.get_profile_info(profile_name)
            click.echo(f'  - {profile_name}: {info.get("name")} - {info.get("description")}')


def request_wants_json():
    """Check if request prefers JSON response"""
    from flask import request
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
