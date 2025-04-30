from PIL import Image
import math
from src.utils.file_utils import save_image

def create_collage(image_paths, output_path, layout='grid', spacing=10, background_color='white'):
    """Membuat kolase dari beberapa gambar"""
    images = [Image.open(path) for path in image_paths]
    
    if layout == 'grid':
        count = len(images)
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)
        
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        
        result_width = cols * max_width + (cols + 1) * spacing
        result_height = rows * max_height + (rows + 1) * spacing
        result = Image.new('RGB', (result_width, result_height), background_color)
        
        for i, img in enumerate(images):
            row = i // cols
            col = i % cols
            x = col * (max_width + spacing) + spacing
            y = row * (max_height + spacing) + spacing
            img_x = x + (max_width - img.width) // 2
            img_y = y + (max_height - img.height) // 2
            result.paste(img, (img_x, img_y))
    
    elif layout == 'horizontal':
        total_width = sum(img.width for img in images) + (len(images) + 1) * spacing
        max_height = max(img.height for img in images)
        result = Image.new('RGB', (total_width, max_height + 2 * spacing), background_color)
        
        x = spacing
        for img in images:
            y = spacing + (max_height - img.height) // 2
            result.paste(img, (x, y))
            x += img.width + spacing
    
    elif layout == 'vertical':
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images) + (len(images) + 1) * spacing
        result = Image.new('RGB', (max_width + 2 * spacing, total_height), background_color)
        
        y = spacing
        for img in images:
            x = spacing + (max_width - img.width) // 2
            result.paste(img, (x, y))
            y += img.height + spacing
    
    else:
        raise ValueError(f"Layout '{layout}' tidak didukung")
    
    return save_image(result, output_path)