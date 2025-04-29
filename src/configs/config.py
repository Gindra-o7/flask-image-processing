import os

# Konfigurasi dasar
DEBUG = True
PORT = 5000

# Konfigurasi upload file
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Kualitas gambar default
DEFAULT_JPEG_QUALITY = 85
DEFAULT_PNG_COMPRESS_LEVEL = 6

# Ukuran maksimal untuk preview
MAX_PREVIEW_SIZE = (800, 800)