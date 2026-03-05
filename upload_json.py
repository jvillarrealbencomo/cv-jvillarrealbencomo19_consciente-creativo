"""
Temporary script to upload cv_data_export.json via web interface
Run this locally, then access the upload page in your browser
"""
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Upload JSON</title></head>
<body>
<h1>Upload cv_data_export.json</h1>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" accept=".json">
    <button type="submit">Upload</button>
</form>
{% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file.save('cv_data_export.json')
            return render_template_string(UPLOAD_TEMPLATE, message='✅ File uploaded! Now run: python import_data.py')
    return render_template_string(UPLOAD_TEMPLATE)

if __name__ == '__main__':
    app.run(port=8000)
