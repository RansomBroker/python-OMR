import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from main import scan_answer

# Create a blueprint to organize routes
api = Blueprint('api', __name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'images/ljk'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Make sure the destination folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Cek apakah file memiliki ekstensi yang diperbolehkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if there is a file being sent
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar yang diunggah'}), 400

    file = request.files['image']
    
    # Retrieve additional data from the form
    name = request.form.get('name')
    id_value = request.form.get('id')

    if not name or not id_value:
        return jsonify({'error': 'Data nama dan id harus disertakan'}), 400

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400

    # Process the file if it meets the requirements
    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file
        file.save(filepath)

        # Proses gambar
        get_answer = scan_answer('images\lembar jawaban.jpg', filepath)

        return jsonify({'result': get_answer})
    else:
        return jsonify({'error': 'Tipe file tidak diizinkan'}), 400