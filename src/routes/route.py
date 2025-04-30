from flask import Blueprint
from src.controllers.file_controller import upload_image, list_images, delete_image
from src.controllers.basic_operations_controller import crop, rotate, resize, flip
from src.controllers.color_adjustments_controller import brightness, contrast, saturation
from src.controllers.filters_controller import filter
from src.controllers.text_and_border_controller import add_text_endpoint, add_border_endpoint
from src.controllers.convert_controller import convert
from src.controllers.collage_controller import create_collage_endpoint

# Blueprint untuk semua endpoint yang berhubungan dengan gambar
image_bp = Blueprint('image', __name__)

# Rute untuk pengelolaan file
image_bp.route('/upload', methods=['POST'])(upload_image)
image_bp.route('/list', methods=['GET'])(list_images)
image_bp.route('/delete/<filename>', methods=['DELETE'])(delete_image)

# Rute untuk operasi dasar
image_bp.route('/crop', methods=['POST'])(crop)
image_bp.route('/rotate', methods=['POST'])(rotate)
image_bp.route('/resize', methods=['POST'])(resize)
image_bp.route('/flip', methods=['POST'])(flip)

# Rute untuk penyesuaian warna
image_bp.route('/brightness', methods=['POST'])(brightness)
image_bp.route('/contrast', methods=['POST'])(contrast)
image_bp.route('/saturation', methods=['POST'])(saturation)

# Rute untuk filter
image_bp.route('/filter', methods=['POST'])(filter)

# Rute untuk teks dan border
image_bp.route('/text', methods=['POST'])(add_text_endpoint)
image_bp.route('/border', methods=['POST'])(add_border_endpoint)

# Rute untuk konversi format
image_bp.route('/convert', methods=['POST'])(convert)

# Rute untuk kolase
image_bp.route('/collage', methods=['POST'])(create_collage_endpoint)