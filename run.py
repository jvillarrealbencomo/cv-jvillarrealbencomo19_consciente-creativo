"""
Application Entry Point
Version 2025 - Run the Flask application
"""
import os
from flask import jsonify
from app import create_app
from app.models import Person   # importa tu modelo

# Create application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.route("/api/person/fullname")
def person_fullname():
    person = Person.query.first()  # o Person.query.order_by(Person.id.desc()).first()
    return jsonify(full_name=person.full_name)

if __name__ == '__main__':
    # Development server
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=app.config['DEBUG']
    )
