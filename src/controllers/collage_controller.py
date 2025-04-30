from flask import jsonify, current_app, request
import os
import uuid
from src.services.collage_service import create_collage
from src.utils.file_utils import generate_preview

def create_collage_endpoint():
    """Membuat kolase dari beberapa gambar"""
    data = request.get_json()
    
    if 'filenames' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required field: filenames (array of image filenames)'
        }), 400
    
    filenames = data['filenames']
    layout = data.get('layout', 'grid')  # Default: grid
    spacing = int(data.get('spacing', 10))  # Default: 10px
    background_color = data.get('background_color', 'white')  # Default: white
    
    if not isinstance(filenames, list) or len(filenames) < 2:
        return jsonify({
            'status': 'error',
            'message': 'Minimal dua gambar diperlukan untuk membuat kolase'
        }), 400
    
    if layout not in ['grid', 'horizontal', 'vertical']:
        return jsonify({
            'status': 'error',
            'message': 'Layout harus salah satu dari: grid, horizontal, vertical'
        }), 400
    
    # Persiapkan path input dan output
    image_paths = [os.path.join(current_app.config['UPLOAD_FOLDER'], filename) for filename in filenames]
    
    # Cek apakah semua file ada
    for path in image_paths:
        if not os.path.exists(path):
            return jsonify({
                'status': 'error',
                'message': f'File tidak ditemukan: {os.path.basename(path)}'
            }), 404
    
    # Nama file output
    new_filename = f"collage_{uuid.uuid4()}.png"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        create_collage(image_paths, new_path, layout, spacing, background_color)
        
        # Buat preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': 'Kolase berhasil dibuat',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}",
                'layout': layout
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal membuat kolase: {str(e)}'
        }), 500