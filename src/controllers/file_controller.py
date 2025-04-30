from flask import jsonify, current_app, request
import os
import uuid
from werkzeug.utils import secure_filename
from src.utils.file_utils import allowed_file, generate_preview

def upload_image():
    """Mengupload gambar"""
    if 'image' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'Tidak ada file yang dikirim'
        }), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'Tidak ada file yang dipilih'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': 'Format file tidak didukung'
        }), 400
    
    original_filename = secure_filename(file.filename)
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(upload_path)
    
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

def list_images():
    """Mendapatkan daftar gambar yang tersedia"""
    try:
        files = []
        for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
            if not filename.startswith('preview_'):
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(file_path):
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

def delete_image(filename):
    """Menghapus gambar"""
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        preview_filename = f"preview_{filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
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