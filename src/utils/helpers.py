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