from flask import jsonify, current_app, request
import os
import uuid
from src.services.basic_operations_service import crop_image, rotate_image, resize_image, flip_image
from src.utils.file_utils import generate_preview

def crop():
    """Memotong gambar"""
    data = request.get_json()
    
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
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"crop_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        crop_image(original_path, new_path, (x, y, x + width, y + height))
        
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

def rotate():
    """Memutar gambar"""
    data = request.get_json()
    
    if 'filename' not in data or 'angle' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and angle'
        }), 400
    
    filename = data['filename']
    angle = float(data['angle'])
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"rotate_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        rotate_image(original_path, new_path, angle)
        
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

def resize():
    """Mengubah ukuran gambar"""
    data = request.get_json()
    
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
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"resize_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        resize_image(original_path, new_path, (width, height), maintain_aspect)
        
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

def flip():
    """Membalik gambar"""
    data = request.get_json()
    
    if 'filename' not in data or 'direction' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and direction'
        }), 400
    
    filename = data['filename']
    direction = data['direction'].lower()
    
    if direction not in ['horizontal', 'vertical']:
        return jsonify({
            'status': 'error',
            'message': 'Direction harus horizontal atau vertical'
        }), 400
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"flip_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        flip_image(original_path, new_path, direction)
        
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