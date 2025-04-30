from flask import jsonify, current_app, request
import os
import uuid
from src.services.convert_service import convert_image
from src.utils.file_utils import generate_preview, allowed_file

def convert():
    """Mengkonversi gambar ke format lain"""
    data = request.get_json()
    
    if 'filename' not in data or 'format' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields: filename and format'
        }), 400
    
    filename = data['filename']
    target_format = data['format'].lower()
    
    # Daftar format yang didukung
    supported_formats = ['bmp', 'fits', 'gif', 'jpg', 'jpeg', 'pgm', 'png', 'tiff', 'tif', 'webp']
    
    if target_format not in supported_formats:
        return jsonify({
            'status': 'error',
            'message': f'Format {target_format} tidak didukung. Format yang didukung: {", ".join(supported_formats)}'
        }), 400
    
    original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Generate nama file baru dengan ekstensi target
    new_filename = f"convert_{uuid.uuid4()}.{target_format}"
    new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
    
    try:
        convert_image(original_path, new_path, target_format)
        
        # Buat preview
        preview_filename = f"preview_{new_filename}"
        preview_path = os.path.join(current_app.config['UPLOAD_FOLDER'], preview_filename)
        generate_preview(new_path, preview_path, current_app.config['MAX_PREVIEW_SIZE'])
        
        return jsonify({
            'status': 'success',
            'message': f'Gambar berhasil dikonversi ke format {target_format}',
            'data': {
                'filename': new_filename,
                'preview_filename': preview_filename,
                'path': f"/uploads/{new_filename}",
                'preview_path': f"/uploads/{preview_filename}",
                'format': target_format
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal mengkonversi gambar: {str(e)}'
        }), 500