from flask import jsonify, current_app, request
import os
import uuid
from src.services.color_adjustments_service import adjust_brightness, adjust_contrast, adjust_saturation
from src.utils.file_utils import generate_preview

def brightness():
    """Mengubah kecerahan gambar"""
    data = request.get_json()
    
    if 'filename' not in data or 'factor' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and factor'
        }), 400
    
    filename = data['filename']
    factor = float(data['factor'])
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"bright_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        adjust_brightness(original_path, new_path, factor)
        
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

def contrast():
    """Mengubah kontras gambar"""
    data = request.get_json()
    
    if 'filename' not in data or 'factor' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and factor'
        }), 400
    
    filename = data['filename']
    factor = float(data['factor'])
    
    original_path =_calc_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"contrast_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        adjust_contrast(original_path, new_path, factor)
        
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

def saturation():
    """Mengubah saturasi gambar"""
    data = request.get_json()
    
    if 'filename' not in data or 'factor' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and factor'
        }), 400
    
    filename = data['filename']
    factor = float(data['factor'])
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"sat_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        adjust_saturation(original_path, new_path, factor)
        
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