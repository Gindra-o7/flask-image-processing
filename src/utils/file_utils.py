import os
import json
import uuid
import datetime
from werkzeug.utils import secure_filename
from flask import current_app

def generate_unique_filename(original_filename):
    """Membuat nama file unik untuk mencegah tabrakan nama"""
    filename = secure_filename(original_filename)
    name, ext = os.path.splitext(filename)
    unique_filename = f"{name}_{uuid.uuid4().hex}{ext}"
    return unique_filename

def get_file_extension(filename):
    """Mendapatkan ekstensi file"""
    if '.' not in filename:
        return ''
    return os.path.splitext(filename)[1].lower()

def get_file_info(file_path):
    """Mendapatkan informasi file seperti ukuran dan tanggal modifikasi"""
    if not os.path.exists(file_path):
        return None
    
    stats = os.stat(file_path)
    return {
        'size': stats.st_size,
        'created': datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
        'modified': datetime.datetime.fromtimestamp(stats.st_mtime).isoformat(),
        'is_image': get_file_extension(file_path) in current_app.config['ALLOWED_EXTENSIONS']
    }

def save_metadata(filename, metadata):
    """Menyimpan metadata terkait file"""
    metadata_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_path = os.path.join(metadata_dir, f"{filename}.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    return metadata_path

def load_metadata(filename):
    """Membaca metadata file"""
    metadata_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'metadata', f"{filename}.json")
    if not os.path.exists(metadata_path):
        return {}
    
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def clean_old_files(directory, max_age_hours=24):
    """Membersihkan file lama yang tidak dibutuhkan"""
    now = datetime.datetime.now()
    threshold = now - datetime.timedelta(hours=max_age_hours)
    
    count = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if modified_time < threshold:
                try:
                    os.remove(file_path)
                    count += 1
                except Exception:
                    pass
    
    return count

def allowed_file(filename):
    """Cek apakah ekstensi file diizinkan"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
        
def save_image(img, output_path, format=None):
    """Menyimpan gambar dengan format yang sesuai"""
    format_mapping = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.webp': 'WEBP',
        '.bmp': 'BMP',
        '.fits': 'FITS',
        '.pgm': 'PPM',
        '.tiff': 'TIFF',
        '.tif': 'TIFF'
    }
    
    # Jika format diberikan, gunakan itu, jika tidak ambil dari ekstensi file
    if format:
        save_format = format
    else:
        file_ext = os.path.splitext(output_path)[1].lower()
        save_format = format_mapping.get(file_ext, 'JPEG')
    
    # Tambahkan opsi kualitas jika format mendukung
    if save_format == 'JPEG':
        img.save(output_path, format=save_format, quality=current_app.config['DEFAULT_JPEG_QUALITY'])
    elif save_format == 'PNG':
        img.save(output_path, format=save_format, compress_level=current_app.config['DEFAULT_PNG_COMPRESS_LEVEL'])
    else:
        img.save(output_path, format=save_format)
    
    return output_path

def generate_preview(input_path, output_path, max_size=(800, 800)):
    """Membuat preview dengan ukuran yang lebih kecil dari gambar asli"""
    from PIL import Image
    with Image.open(input_path) as img:
        img.thumbnail(max_size)
        return save_image(img, output_path)
    
# Update allowed_file untuk mendukung semua format
def update_allowed_extensions():
    """Update ALLOWED_EXTENSIONS di konfigurasi untuk mendukung lebih banyak format"""
    from flask import current_app
    current_app.config['ALLOWED_EXTENSIONS'].update({
        'bmp', 'fits', 'pgm', 'tiff', 'tif'
    })
    return current_app.config['ALLOWED_EXTENSIONS']