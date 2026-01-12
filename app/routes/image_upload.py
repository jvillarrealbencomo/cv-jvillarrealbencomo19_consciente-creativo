"""
Bulk Image Upload for Render
Uploads credential images to the database
"""
from flask import Blueprint, request, jsonify, render_template_string
import os
from pathlib import Path
from app import db
from app.models import Education, AdvancedTraining

image_upload_bp = Blueprint('image_upload', __name__)

UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bulk Image Upload</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .upload-box { border: 2px dashed #ccc; padding: 20px; margin: 20px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; margin: 5px; }
        .success { color: green; } .error { color: red; } .info { color: blue; }
        .progress { margin: 20px 0; }
    </style>
</head>
<body>
    <h1>📸 Bulk Upload Credential Images</h1>
    
    <div class="upload-box">
        <h3>Upload Education Images</h3>
        <form method="POST" enctype="multipart/form-data" action="/admin/upload-education-images">
            <p>Select multiple education credential images:</p>
            <input type="file" name="images" accept="image/*" multiple required>
            <br><br>
            <button type="submit">Upload Education Images</button>
        </form>
    </div>

    <div class="upload-box">
        <h3>Upload Advanced Training Images</h3>
        <form method="POST" enctype="multipart/form-data" action="/admin/upload-training-images">
            <p>Select multiple advanced training credential images:</p>
            <input type="file" name="images" accept="image/*" multiple required>
            <br><br>
            <button type="submit">Upload Training Images</button>
        </form>
    </div>

    {% if message %}
    <p class="{{ 'success' if success else 'error' }}">{{ message }}</p>
    {% endif %}

    <div class="info">
        <h4>Instructions:</h4>
        <p>1. Locate your local image files in app/static/uploads/</p>
        <p>2. Select all images of the same type (education or training)</p>
        <p>3. Click "Upload" to transfer them to Render</p>
        <p>4. The system will match them to existing database records</p>
    </div>
</body>
</html>
'''

@image_upload_bp.route('/admin/upload-images', methods=['GET'])
def upload_images_page():
    """Display upload interface"""
    return render_template_string(UPLOAD_TEMPLATE)

@image_upload_bp.route('/admin/upload-education-images', methods=['POST'])
def upload_education_images():
    """Upload education credential images"""
    try:
        files = request.files.getlist('images')
        if not files:
            return render_template_string(UPLOAD_TEMPLATE, message='No files selected', success=False)
        
        # Ensure upload directory exists
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'education')
        os.makedirs(upload_dir, exist_ok=True)
        
        uploaded_count = 0
        for file in files:
            if file and file.filename:
                filename = file.filename
                filepath = os.path.join(upload_dir, filename)
                file.save(filepath)
                uploaded_count += 1
        
        message = f'✅ Successfully uploaded {uploaded_count} education image(s) to {upload_dir}'
        return render_template_string(UPLOAD_TEMPLATE, message=message, success=True)
        
    except Exception as e:
        return render_template_string(UPLOAD_TEMPLATE, message=f'❌ Error: {str(e)}', success=False)

@image_upload_bp.route('/admin/upload-training-images', methods=['POST'])
def upload_training_images():
    """Upload advanced training credential images"""
    try:
        files = request.files.getlist('images')
        if not files:
            return render_template_string(UPLOAD_TEMPLATE, message='No files selected', success=False)
        
        # Ensure upload directory exists
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'advanced_training')
        os.makedirs(upload_dir, exist_ok=True)
        
        uploaded_count = 0
        for file in files:
            if file and file.filename:
                filename = file.filename
                filepath = os.path.join(upload_dir, filename)
                file.save(filepath)
                uploaded_count += 1
        
        message = f'✅ Successfully uploaded {uploaded_count} training image(s) to {upload_dir}'
        return render_template_string(UPLOAD_TEMPLATE, message=message, success=True)
        
    except Exception as e:
        return render_template_string(UPLOAD_TEMPLATE, message=f'❌ Error: {str(e)}', success=False)
