from flask import jsonify, current_app, request
import os
import uuid
from src.services.filters_service import apply_filter
from src.utils.file_utils import generate_preview

def filter():
    """Menerapkan filter pada gambar"""
    data = request.get_json()
    
    if 'filename' not in data or 'filter_type' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and filter_type'
        }), 400
    
    filename = data['filename']
    filter_type = data['filter_type']
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"filter_{uuid.uuid4()}{file_extension}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        apply_filter(original_path, new_path, filter_type)
        
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