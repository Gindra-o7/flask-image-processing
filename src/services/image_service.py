from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import os
import numpy as np
from flask import current_app
import math
import colorsys

def allowed_file(filename):
    """Cek apakah ekstensi file diizinkan"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(img, output_path):
    """Menyimpan gambar dengan format yang sesuai"""
    format_mapping = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.webp': 'WEBP'
    }
    
    file_ext = os.path.splitext(output_path)[1].lower()
    save_format = format_mapping.get(file_ext, 'JPEG')
    
    # Tambahkan opsi kualitas jika format mendukung
    if save_format == 'JPEG':
        img.save(output_path, format=save_format, quality=current_app.config['DEFAULT_JPEG_QUALITY'])
    elif save_format == 'PNG':
        img.save(output_path, format=save_format, compress_level=current_app.config['DEFAULT_PNG_COMPRESS_LEVEL'])
    else:
        img.save(output_path, format=save_format)
    
    return output_path

def generate_preview(input_path, output_path, max_size=(800, 800)):
    """Membuat preview dengan ukuran yang lebih kecil dari gambar asli"""
    with Image.open(input_path) as img:
        img.thumbnail(max_size)
        save_image(img, output_path)
    return output_path

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

def adjust_brightness(input_path, output_path, factor):
    """Mengubah kecerahan gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB jika format tidak mendukung
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        # Gunakan ImageEnhance.Brightness untuk mengubah kecerahan
        enhancer = ImageEnhance.Brightness(img)
        brightened_img = enhancer.enhance(factor)
        return save_image(brightened_img, output_path)

def adjust_contrast(input_path, output_path, factor):
    """Mengubah kontras gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB jika format tidak mendukung
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        # Gunakan ImageEnhance.Contrast untuk mengubah kontras
        enhancer = ImageEnhance.Contrast(img)
        contrasted_img = enhancer.enhance(factor)
        return save_image(contrasted_img, output_path)

def adjust_saturation(input_path, output_path, factor):
    """Mengubah saturasi gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB jika format tidak mendukung
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        # Gunakan ImageEnhance.Color untuk mengubah saturasi
        enhancer = ImageEnhance.Color(img)
        saturated_img = enhancer.enhance(factor)
        return save_image(saturated_img, output_path)

def apply_filter(input_path, output_path, filter_type):
    """Menerapkan filter pada gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB jika format tidak mendukung
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        filtered_img = None
        
        # Implementasi berbagai filter
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
            # Jika gambar asli memiliki mode RGBA, kita perlu mengembalikan ke RGBA
            if img.mode == 'RGBA':
                # Konversi grayscale ke RGBA dengan alpha channel asli
                gray_data = filtered_img.getdata()
                alpha_data = img.getchannel('A').getdata()
                filtered_img = Image.new('RGBA', img.size)
                new_data = []
                for i, value in enumerate(gray_data):
                    new_data.append((value, value, value, alpha_data[i]))
                filtered_img.putdata(new_data)
        elif filter_type == 'sepia':
            # Implementasi filter sepia
            sepia_data = []
            img_data = img.getdata()
            for pixel in img_data:
                if len(pixel) >= 3:  # RGB or RGBA
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    # Pastikan nilai tidak melebihi 255
                    r, g, b = min(255, tr), min(255, tg), min(255, tb)
                    
                    # Jika gambar memiliki alpha channel
                    if len(pixel) == 4:
                        sepia_data.append((r, g, b, pixel[3]))
                    else:
                        sepia_data.append((r, g, b))
                else:
                    sepia_data.append(pixel)  # Kasus untuk format gambar lain
            
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

def add_text(input_path, output_path, text, position, font_size=24, color='black'):
    """Menambahkan teks pada gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB atau RGBA jika format tidak mendukung drawing
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        # Buat objek drawing
        draw = ImageDraw.Draw(img)
        
        # Coba dapatkan font, gunakan default jika tidak ditemukan
        try:
            # Untuk aplikasi production, gunakan folder fonts terpisah
            # font_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'arial.ttf')
            # font = ImageFont.truetype(font_path, font_size)
            
            # Untuk development, gunakan default
            font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # Tambahkan teks
        draw.text(position, text, fill=color, font=font)
        
        return save_image(img, output_path)

def add_border(input_path, output_path, border_width, color='black'):
    """Menambahkan border pada gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB atau RGBA jika format tidak mendukung
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        # Tambahkan border
        img_with_border = ImageOps.expand(img, border=border_width, fill=color)
        
        return save_image(img_with_border, output_path)

# Tambahan fungsi edit gambar lanjutan

def adjust_hue_saturation_lightness(input_path, output_path, hue_shift=0, saturation_factor=1.0, lightness_factor=1.0):
    """Mengubah hue, saturasi dan kecerahan (HSL) secara terpisah"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Ambil data pixel
        data = np.array(img)
        
        # Reshape untuk pemrosesan lebih mudah
        h, w, d = data.shape
        data = data.reshape(h * w, d)
        
        # Konversi RGB ke HSL
        rgb_data = data / 255.0  # Normalisasi ke range 0-1
        hsl_data = []
        
        for pixel in rgb_data:
            h, l, s = colorsys.rgb_to_hls(pixel[0], pixel[1], pixel[2])
            
            # Terapkan perubahan
            h = (h + hue_shift) % 1.0  # Hue dalam range 0-1
            s = max(0.0, min(1.0, s * saturation_factor))
            l = max(0.0, min(1.0, l * lightness_factor))
            
            # Konversi kembali ke RGB
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            hsl_data.append([r, g, b])
        
        # Konversi kembali ke format yang dapat diproses oleh PIL
        processed_data = np.array(hsl_data) * 255
        processed_data = processed_data.astype('uint8').reshape(img.height, img.width, 3)
        
        # Buat gambar baru
        processed_img = Image.fromarray(processed_data, 'RGB')
        
        # Jika gambar asli memiliki alpha channel, tambahkan kembali
        if img.mode == 'RGBA':
            alpha = img.getchannel('A')
            processed_img.putalpha(alpha)
        
        return save_image(processed_img, output_path)

def apply_vignette(input_path, output_path, intensity=1.0):
    """Menambahkan efek vignette (tepi gelap) pada gambar"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB atau RGBA
        has_alpha = img.mode == 'RGBA'
        if has_alpha:
            img_rgb = img.convert('RGB')
            alpha = img.getchannel('A')
        else:
            img_rgb = img.convert('RGB')
        
        # Buat mask vignette
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
        
        # Terapkan mask
        vignette_img = img_rgb.copy()
        vignette_img.putalpha(mask)
        vignette_img = Image.composite(vignette_img, Image.new('RGB', img.size, (0, 0, 0)), mask)
        
        # Jika gambar asli memiliki alpha channel, tambahkan kembali
        if has_alpha:
            vignette_img = vignette_img.convert('RGBA')
            vignette_img.putalpha(alpha)
        
        return save_image(vignette_img, output_path)

def apply_color_temperature(input_path, output_path, temperature):
    """Mengubah suhu warna gambar (cool/warm)"""
    with Image.open(input_path) as img:
        # Konversi ke mode RGB
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        # Tetapkan alpha channel jika ada
        has_alpha = img.mode == 'RGBA'
        if has_alpha:
            alpha = img.getchannel('A')
            img = img.convert('RGB')
        
        # Buat gambar baru
        kelvin_table = {
            1000: (255, 56, 0),    # Sangat hangat
            2000: (255, 109, 0),   # Hangat
            3000: (255, 137, 18),  # Sedikit hangat
            4000: (255, 161, 72),  # Netral hangat
            5000: (255, 180, 107), # Netral
            6000: (255, 196, 137), # Netral sejuk
            7000: (255, 209, 163), # Sedikit sejuk
            8000: (255, 219, 186), # Sejuk
            9000: (255, 228, 206), # Sangat sejuk
            10000: (255, 236, 224) # Ultra sejuk
        }
        
        # Cari nilai kelvin terdekat
        temperature = max(1000, min(10000, temperature))
        lower_kelvin = max([k for k in kelvin_table.keys() if k <= temperature])
        upper_kelvin = min([k for k in kelvin_table.keys() if k >= temperature])
        
        if lower_kelvin == upper_kelvin:
            r, g, b = kelvin_table[lower_kelvin]
        else:
            # Interpolasi nilai
            ratio = (temperature - lower_kelvin) / (upper_kelvin - lower_kelvin)
            r = kelvin_table[lower_kelvin][0] + ratio * (kelvin_table[upper_kelvin][0] - kelvin_table[lower_kelvin][0])
            g = kelvin_table[lower_kelvin][1] + ratio * (kelvin_table[upper_kelvin][1] - kelvin_table[lower_kelvin][1])
            b = kelvin_table[lower_kelvin][2] + ratio * (kelvin_table[upper_kelvin][2] - kelvin_table[lower_kelvin][2])
        
        r, g, b = r/255, g/255, b/255
        
        # Terapkan temperatur warna
        matrix = (
            r, 0, 0, 0,
            0, g, 0, 0,
            0, 0, b, 0
        )
        
        temp_img = img.convert('RGB', matrix)
        
        # Kembalikan alpha channel jika ada
        if has_alpha:
            temp_img = temp_img.convert('RGBA')
            temp_img.putalpha(alpha)
        
        return save_image(temp_img, output_path)

def create_collage(image_paths, output_path, layout='grid', spacing=10, background_color='white'):
    """Membuat kolase dari beberapa gambar"""
    images = [Image.open(path) for path in image_paths]
    
    if layout == 'grid':
        # Hitung jumlah baris dan kolom yang optimal
        count = len(images)
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)
        
        # Cari ukuran terbesar untuk setiap gambar dalam grid
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        
        # Buat gambar baru untuk kolase
        result_width = cols * max_width + (cols + 1) * spacing
        result_height = rows * max_height + (rows + 1) * spacing
        result = Image.new('RGB', (result_width, result_height), background_color)
        
        # Tempatkan gambar dalam grid
        for i, img in enumerate(images):
            row = i // cols
            col = i % cols
            x = col * (max_width + spacing) + spacing
            y = row * (max_height + spacing) + spacing
            
            # Tempatkan gambar di tengah sel
            img_x = x + (max_width - img.width) // 2
            img_y = y + (max_height - img.height) // 2
            result.paste(img, (img_x, img_y))
    
    elif layout == 'horizontal':
        # Sejajarkan gambar secara horizontal
        total_width = sum(img.width for img in images) + (len(images) + 1) * spacing
        max_height = max(img.height for img in images)
        result = Image.new('RGB', (total_width, max_height + 2 * spacing), background_color)
        
        x = spacing
        for img in images:
            y = spacing + (max_height - img.height) // 2  # Tengah vertikal
            result.paste(img, (x, y))
            x += img.width + spacing
    
    elif layout == 'vertical':
        # Sejajarkan gambar secara vertikal
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images) + (len(images) + 1) * spacing
        result = Image.new('RGB', (max_width + 2 * spacing, total_height), background_color)
        
        y = spacing
        for img in images:
            x = spacing + (max_width - img.width) // 2  # Tengah horizontal
            result.paste(img, (x, y))
            y += img.height + spacing
    
    else:
        raise ValueError(f"Layout '{layout}' tidak didukung")
    
    return save_image(result, output_path)