from PIL import Image, ImageFilter, ImageOps
from src.utils.file_utils import save_image

def apply_filter(input_path, output_path, filter_type):
    """Menerapkan filter pada gambar"""
    with Image.open(input_path) as img:
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        filtered_img = None
        
        if filter_type == 'blur':
            filtered_img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'contour':
            filtered_img = img.filter(ImageFilter.CONTOUR)
        elif filter_type == 'detail':
            filtered_img = img.filter(ImageFilter.DETAIL)
        elif filter_type == 'edge_enhance':
            filtered_img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'emboss':
            filtered_img = img.filter(ImageFilter.EMBOSS)
        elif filter_type == 'sharpen':
            filtered_img = img.filter(ImageFilter.SHARPEN)
        elif filter_type == 'smooth':
            filtered_img = img.filter(ImageFilter.SMOOTH)
        elif filter_type == 'grayscale':
            filtered_img = ImageOps.grayscale(img)
            if img.mode == 'RGBA':
                gray_data = filtered_img.getdata()
                alpha_data = img.getchannel('A').getdata()
                filtered_img = Image.new('RGBA', img.size)
                new_data = []
                for i, value in enumerate(gray_data):
                    new_data.append((value, value, value, alpha_data[i]))
                filtered_img.putdata(new_data)
        elif filter_type == 'sepia':
            sepia_data = []
            img_data = img.getdata()
            for pixel in img_data:
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    r, g, b = min(255, tr), min(255, tg), min(255, tb)
                    if len(pixel) == 4:
                        sepia_data.append((r, g, b, pixel[3]))
                    else:
                        sepia_data.append((r, g, b))
                else:
                    sepia_data.append(pixel)
            filtered_img = Image.new(img.mode, img.size)
            filtered_img.putdata(sepia_data)
        elif filter_type == 'invert':
            filtered_img = ImageOps.invert(img)
        elif filter_type == 'solarize':
            filtered_img = ImageOps.solarize(img, threshold=128)
        elif filter_type == 'posterize':
            filtered_img = ImageOps.posterize(img, bits=2)
        elif filter_type == 'equalize':
            filtered_img = ImageOps.equalize(img)
        else:
            raise ValueError(f"Filter type '{filter_type}' not supported")
        
        return save_image(filtered_img, output_path)