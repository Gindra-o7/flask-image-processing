from flask import jsonify, current_app, request
import os
import uuid
from src.services.text_and_border_service import add_text, add_border
from src.utils.file_utils import generate_preview

def add_text_endpoint():
    """Menambahkan teks pada gambar"""
    data = request.get_json()
    
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
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"text_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        add_text(original_path, new_path, text, position, font_size, color)
        
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

def add_border_endpoint():
    """Menambahkan border pada gambar"""
    data = request.get_json()
    
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
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"border_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        add_border(original_path, new_path, border_width, color)
        
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