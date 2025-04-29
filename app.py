from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid
import time
from datetime import datetime
import pytz

from src.controllers.image_controller import image_bp

app = Flask(__name__)
CORS(app)

# Konfigurasi aplikasi
app.config.from_pyfile('src/configs/config.py')

# Register blueprints
app.register_blueprint(image_bp, url_prefix='/api/images')

# Route untuk mengakses file yang diupload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'API berjalan dengan baik',
        'timestamp': time.time()
    }), 200

@app.route('/api', methods=['GET'])
def welcome():
    jakarta_time = datetime.now(pytz.timezone('Asia/Jakarta'))
    formatted_time = jakarta_time.strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        'status': 'success',
        'message': 'Selamat datang di API Image Processing',
        'timestamp': formatted_time
    }), 200

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint tidak ditemukan'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Terjadi kesalahan server internal'
    }), 500

if __name__ == '__main__':
    # Memastikan folder uploads ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=app.config['PORT'])