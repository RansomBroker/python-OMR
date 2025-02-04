import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# Buat blueprint untuk mengorganisir routes
api = Blueprint('api', __name__)

# Konfigurasi folder upload dan ekstensi yang diperbolehkan
UPLOAD_FOLDER = 'images/ljk'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Pastikan folder tujuan ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Cek apakah file memiliki ekstensi yang diperbolehkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/api/upload', methods=['POST'])
def upload_file():
    # Cek apakah ada file yang dikirim
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar yang diunggah'}), 400

    file = request.files['image']
    
    # Ambil data tambahan dari form
    name = request.form.get('name')
    id_value = request.form.get('id')

    if not name or not id_value:
        return jsonify({'error': 'Data nama dan id harus disertakan'}), 400

    # Jika tidak ada file yang dipilih
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400

    # Proses file jika memenuhi persyaratan
    if file and allowed_file(file.filename):
        # Mengamankan nama file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Simpan file ke folder yang telah ditentukan
        file.save(filepath)

        # Simpan data (misalnya ke database, di sini kita hanya mengembalikannya)
        data = {
            'id': id_value,
            'nama': name,
            'gambar': filepath  # atau bisa disimpan path relatifnya
        }

        return jsonify({
            'message': 'File berhasil diunggah',
            'data': data
        }), 201
    else:
        return jsonify({'error': 'Tipe file tidak diizinkan'}), 400