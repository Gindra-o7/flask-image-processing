from PIL import Image
from src.utils.file_utils import save_image, allowed_file
import os

def convert_image(input_path, output_path, target_format):
    """Mengkonversi gambar ke format target"""
    format_mapping = {
        'bmp': 'BMP',
        'fits': 'FITS',
        'gif': 'GIF',
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'pgm': 'PPM',
        'png': 'PNG',
        'tiff': 'TIFF',
        'tif': 'TIFF',
        'webp': 'WEBP'
    }
    
    if target_format.lower() not in format_mapping:
        raise ValueError(f"Format '{target_format}' tidak didukung.")
    
    pil_format = format_mapping[target_format.lower()]
    
    with Image.open(input_path) as img:
        # Untuk format yang tidak mendukung alpha, hilangkan channel alpha
        if pil_format in ['JPEG', 'BMP'] and img.mode == 'RGBA':
            # Ganti background dengan warna putih
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 adalah channel alpha
            img = background
        
        # Format spesifik yang memerlukan mode khusus
        if pil_format == 'FITS':
            if img.mode not in ['L', 'I', 'F']:
                img = img.convert('L')  # Konversi ke grayscale
        elif pil_format == 'PPM':
            if img.mode != 'RGB':
                img = img.convert('RGB')
        
        # Tentukan format berdasarkan ekstensi output
        if pil_format == 'JPEG':
            return save_image(img, output_path, format=pil_format)
        else:
            # Untuk format lain, gunakan save() langsung untuk menghindari isu dengan save_image()
            img.save(output_path, format=pil_format)
            return output_path