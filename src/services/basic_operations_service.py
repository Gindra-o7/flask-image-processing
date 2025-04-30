from PIL import Image
from src.utils.file_utils import save_image

def crop_image(input_path, output_path, crop_box):
    """Memotong gambar sesuai dengan koordinat yang diberikan"""
    with Image.open(input_path) as img:
        # Pastikan crop_box berada dalam batas gambar
        width, height = img.size
        x1, y1, x2, y2 = crop_box
        
        # Batasi nilai koordinat ke ukuran gambar
        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))
        
        if x1 >= x2 or y1 >= y2:
            raise ValueError("Invalid crop coordinates")
        
        # Lakukan crop
        cropped_img = img.crop((x1, y1, x2, y2))
        return save_image(cropped_img, output_path)

def rotate_image(input_path, output_path, angle, expand=True):
    """Memutar gambar sesuai dengan sudut yang diberikan"""
    with Image.open(input_path) as img:
        # Putar gambar, expand=True agar semua konten tetap terlihat
        rotated_img = img.rotate(angle, expand=expand, resample=Image.BICUBIC)
        return save_image(rotated_img, output_path)

def resize_image(input_path, output_path, size, maintain_aspect=True):
    """Mengubah ukuran gambar"""
    with Image.open(input_path) as img:
        width, height = size
        
        if maintain_aspect:
            # Hitung rasio aspek dan ukuran baru
            img_width, img_height = img.size
            aspect = img_width / img_height
            
            if width == 0:
                # Jika width=0, hitung berdasarkan height
                width = int(height * aspect)
            elif height == 0:
                # Jika height=0, hitung berdasarkan width
                height = int(width / aspect)
            else:
                # Jika keduanya diisi, gunakan yang menghasilkan ukuran lebih kecil
                new_aspect = width / height
                if new_aspect > aspect:
                    width = int(height * aspect)
                else:
                    height = int(width / aspect)
        
        # Resize gambar
        resized_img = img.resize((width, height), Image.LANCZOS)
        return save_image(resized_img, output_path)

def flip_image(input_path, output_path, direction):
    """Membalik gambar secara horizontal atau vertikal"""
    with Image.open(input_path) as img:
        if direction == 'horizontal':
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
        
        return save_image(flipped_img, output_path)