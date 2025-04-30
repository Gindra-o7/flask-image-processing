from PIL import Image, ImageDraw, ImageFont, ImageOps
from src.utils.file_utils import save_image

def add_text(input_path, output_path, text, position, font_size=24, color='black'):
    """Menambahkan teks pada gambar"""
    with Image.open(input_path) as img:
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        draw.text(position, text, fill=color, font=font)
        return save_image(img, output_path)

def add_border(input_path, output_path, border_width, color='black'):
    """Menambahkan border pada gambar"""
    with Image.open(input_path) as img:
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        img_with_border = ImageOps.expand(img, border=border_width, fill=color)
        return save_image(img_with_border, output_path)