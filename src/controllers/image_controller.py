from flask import Blueprint, request, jsonify, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from src.services.image_service import (
    allowed_file, crop_image, rotate_image, adjust_brightness,
    apply_filter, resize_image, flip_image, add_text,
    add_border, adjust_contrast, adjust_saturation,
    save_image, generate_preview
)

# Blueprint untuk semua endpoint yang berhubungan dengan gambar
image_bp = Blueprint('image', __name__)

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    """Endpoint untuk mengupload gambar"""
    
    # Cek apakah ada file dalam request
    if 'image' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'Tidak ada file yang dikirim'
        }), 400
    
    file = request.files['image']
    
    # Cek apakah nama file ada
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'Tidak ada file yang dipilih'
        }), 400
    
    # Cek apakah file yang diupload diizinkan
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': 'Format file tidak didukung'
        }), 400
    
    # Generate nama file yang aman dan unik
    original_filename = secure_filename(file.filename)
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Simpan file
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(upload_path)
    
    # Generate preview
    preview_filename = f"preview_{unique_filename}"
    preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
    generate_preview(upload_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
    
    return jsonify({
        'status': 'success',
        'message': 'Gambar berhasil diupload',
        'data': {
            'original_filename': original_filename,
            'filename': unique_filename,
            'preview_filename': preview_filename,
            'path': f"/uploads/{unique_filename}",
            'preview_path': f"/uploads/{preview_filename}"
        }
    }), 200

@image_bp.route('/crop', methods=['POST'])
def crop():
    """Endpoint untuk memotong gambar"""
    data = request.get_json()
    
    # Validasi data
    required_fields = ['filename', 'x', 'y', 'width', 'height']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
            
    filename = data['filename']
    x = int(data['x'])
    y = int(data['y'])
    width = int(data['width'])
    height = int(data['height'])
    
    # Buat nama file untuk hasil crop
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"crop_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Lakukan crop
    try:
        crop_image(original_path, new_path, (x, y, x + width, y + height))
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Gambar berhasil di-crop',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal melakukan crop: {str(e)}'
        }), 500

@image_bp.route('/rotate', methods=['POST'])
def rotate():
    """Endpoint untuk memutar gambar"""
    data = request.get_json()
    
    # Validasi data
    if 'filename' not in data or 'angle' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and angle'
        }), 400
    
    filename = data['filename']
    angle = float(data['angle'])
    
    # Buat nama file untuk hasil rotasi
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"rotate_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Lakukan rotasi
    try:
        rotate_image(original_path, new_path, angle)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Gambar berhasil dirotasi',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal melakukan rotasi: {str(e)}'
        }), 500

@image_bp.route('/brightness', methods=['POST'])
def brightness():
    """Endpoint untuk mengubah kecerahan gambar"""
    data = request.get_json()
    
    # Validasi data
    if 'filename' not in data or 'factor' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and factor'
        }), 400
    
    filename = data['filename']
    factor = float(data['factor'])  # nilai < 1.0 lebih gelap, > 1.0 lebih cerah
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"bright_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Ubah kecerahan
    try:
        adjust_brightness(original_path, new_path, factor)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Kecerahan gambar berhasil diubah',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal mengubah kecerahan: {str(e)}'
        }), 500

@image_bp.route('/filter', methods=['POST'])
def filter():
    """Endpoint untuk menerapkan filter pada gambar"""
    data = request.get_json()
    
    # Validasi data
    if 'filename' not in data or 'filter_type' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and filter_type'
        }), 400
    
    filename = data['filename']
    filter_type = data['filter_type']
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"filter_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Terapkan filter
    try:
        apply_filter(original_path, new_path, filter_type)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': f'Filter {filter_type} berhasil diterapkan',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal menerapkan filter: {str(e)}'
        }), 500

@image_bp.route('/resize', methods=['POST'])
def resize():
    """Endpoint untuk mengubah ukuran gambar"""
    data = request.get_json()
    
    # Validasi data
    required_fields = ['filename', 'width', 'height']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    filename = data['filename']
    width = int(data['width'])
    height = int(data['height'])
    maintain_aspect = data.get('maintain_aspect', True)
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"resize_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Ubah ukuran
    try:
        resize_image(original_path, new_path, (width, height), maintain_aspect)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Ukuran gambar berhasil diubah',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal mengubah ukuran: {str(e)}'
        }), 500

@image_bp.route('/flip', methods=['POST'])
def flip():
    """Endpoint untuk membalik gambar"""
    data = request.get_json()
    
    # Validasi data
    if 'filename' not in data or 'direction' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and direction'
        }), 400
    
    filename = data['filename']
    direction = data['direction'].lower()  # 'horizontal' atau 'vertical'
    
    if direction not in ['horizontal', 'vertical']:
        return jsonify({
            'status': 'error',
            'message': 'Direction harus horizontal atau vertical'
        }), 400
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"flip_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Balik gambar
    try:
        flip_image(original_path, new_path, direction)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': f'Gambar berhasil dibalik {direction}',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal membalik gambar: {str(e)}'
        }), 500

@image_bp.route('/text', methods=['POST'])
def add_text_endpoint():
    """Endpoint untuk menambahkan teks pada gambar"""
    data = request.get_json()
    
    # Validasi data
    required_fields = ['filename', 'text', 'position_x', 'position_y']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    filename = data['filename']
    text = data['text']
    position = (int(data['position_x']), int(data['position_y']))
    font_size = data.get('font_size', 24)
    color = data.get('color', 'black')
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"text_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Tambahkan teks
    try:
        add_text(original_path, new_path, text, position, font_size, color)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Teks berhasil ditambahkan',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal menambahkan teks: {str(e)}'
        }), 500

@image_bp.route('/border', methods=['POST'])
def add_border_endpoint():
    """Endpoint untuk menambahkan border pada gambar"""
    data = request.get_json()
    
    # Validasi data
    required_fields = ['filename', 'width']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    filename = data['filename']
    border_width = int(data['width'])
    color = data.get('color', 'black')
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"border_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Tambahkan border
    try:
        add_border(original_path, new_path, border_width, color)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Border berhasil ditambahkan',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal menambahkan border: {str(e)}'
        }), 500

@image_bp.route('/contrast', methods=['POST'])
def contrast():
    """Endpoint untuk mengubah kontras gambar"""
    data = request.get_json()
    
    # Validasi data
    if 'filename' not in data or 'factor' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and factor'
        }), 400
    
    filename = data['filename']
    factor = float(data['factor'])  # nilai < 1.0 mengurangi kontras, > 1.0 menambah kontras
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"contrast_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Ubah kontras
    try:
        adjust_contrast(original_path, new_path, factor)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Kontras gambar berhasil diubah',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal mengubah kontras: {str(e)}'
        }), 500

@image_bp.route('/saturation', methods=['POST'])
def saturation():
    """Endpoint untuk mengubah saturasi gambar"""
    data = request.get_json()
    
    # Validasi data
    if 'filename' not in data or 'factor' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and factor'
        }), 400
    
    filename = data['filename']
    factor = float(data['factor'])  # nilai < 1.0 mengurangi saturasi, > 1.0 menambah saturasi
    
    # Buat nama file untuk hasil
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"sat_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    # Ubah saturasi
    try:
        adjust_saturation(original_path, new_path, factor)
        
        # Generate preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Saturasi gambar berhasil diubah',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal mengubah saturasi: {str(e)}'
        }), 500

@image_bp.route('/list', methods=['GET'])
def list_images():
    """Endpoint untuk mendapatkan daftar gambar yang tersedia"""
    try:
        # Ambil semua file di folder uploads
        files = []
        for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
            # Abaikan file preview
            if not filename.startswith('preview_'):
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(file_path):
                    # Cek apakah ada file preview
                    preview_filename = f"preview_{filename}"
                    preview_path = f"/uploads/{preview_filename}"
                    
                    files.append({
                        'filename': filename,
                        'path': f"/uploads/{filename}",
                        'preview_path': preview_path if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)) else None,
                        'size': os.path.getsize(file_path),
                        'modified': os.path.getmtime(file_path)
                    })
        
        return jsonify({
            'status': 'success',
            'data': {
                'images': files
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal mengambil daftar gambar: {str(e)}'
        }), 500

@image_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_image(filename):
    """Endpoint untuk menghapus gambar"""
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        preview_filename = f"preview_{filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        
        # Hapus file gambar
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Hapus file preview jika ada
        if os.path.exists(preview_path):
            os.remove(preview_path)
        
        return jsonify({
            'status': 'success',
            'message': f'Gambar {filename} berhasil dihapus'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal menghapus gambar: {str(e)}'
        }), 500