from PIL import Image, ImageDraw
from src.utils.file_utils import save_image

def apply_vignette(input_path, output_path, intensity=1.0):
    """Menambahkan efek vignette (tepi gelap) pada gambar"""
    with Image.open(input_path) as img:
        has_alpha = img.mode == 'RGBA'
        if has_alpha:
            img_rgb = img.convert('RGB')
            alpha = img.getchannel('A')
        else:
            img_rgb = img.convert('RGB')
        
        width, height = img.size
        center_x = width / 2
        center_y = height / 2
        radius = min(center_x, center_y)
        mask = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(mask)
        
        for r in range(int(radius), int(width * 1.5)):
            opacity = int(255 * (1 - (r - radius) / (radius * intensity * 2)))
            if opacity < 0:
                break
            draw.ellipse((center_x - r, center_y - r, center_x + r, center_y + r), fill=opacity)
        
        vignette_img = img_rgb.copy()
        vignette_img.putalpha(mask)
        vignette_img = Image.composite(vignette_img, Image.new('RGB', img.size, (0, 0, 0)), mask)
        
        if has_alpha:
            vignette_img = vignette_img.convert('RGBA')
            vignette_img.putalpha(alpha)
        
        return save_image(vignette_img, output_path)