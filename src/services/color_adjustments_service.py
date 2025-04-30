from PIL import Image, ImageEnhance
import numpy as np
import colorsys
from src.utils.file_utils import save_image

def adjust_brightness(input_path, output_path, factor):
    """Mengubah kecerahan gambar"""
    with Image.open(input_path) as img:
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        enhancer = ImageEnhance.Brightness(img)
        brightened_img = enhancer.enhance(factor)
        return save_image(brightened_img, output_path)

def adjust_contrast(input_path, output_path, factor):
    """Mengubah kontras gambar"""
    with Image.open(input_path) as img:
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        enhancer = ImageEnhance.Contrast(img)
        contrasted_img = enhancer.enhance(factor)
        return save_image(contrasted_img, output_path)

def adjust_saturation(input_path, output_path, factor):
    """Mengubah saturasi gambar"""
    with Image.open(input_path) as img:
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        enhancer = ImageEnhance.Color(img)
        saturated_img = enhancer.enhance(factor)
        return save_image(saturated_img, output_path)

def adjust_hue_saturation_lightness(input_path, output_path, hue_shift=0, saturation_factor=1.0, lightness_factor=1.0):
    """Mengubah hue, saturasi dan kecerahan (HSL) secara terpisah"""
    with Image.open(input_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        data = np.array(img)
        h, w, d = data.shape
        data = data.reshape(h * w, d)
        
        rgb_data = data / 255.0
        hsl_data = []
        
        for pixel in rgb_data:
            h, l, s = colorsys.rgb_to_hls(pixel[0], pixel[1], pixel[2])
            h = (h + hue_shift) % 1.0
            s = max(0.0, min(1.0, s * saturation_factor))
            l = max(0.0, min(1.0, l * lightness_factor))
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            hsl_data.append([r, g, b])
        
        processed_data = np.array(hsl_data) * 255
        processed_data = processed_data.astype('uint8').reshape(img.height, img.width, 3)
        processed_img = Image.fromarray(processed_data, 'RGB')
        
        if img.mode == 'RGBA':
            alpha = img.getchannel('A')
            processed_img.putalpha(alpha)
        
        return save_image(processed_img, output_path)

def apply_color_temperature(input_path, output_path, temperature):
    """Mengubah suhu warna gambar (cool/warm)"""
    with Image.open(input_path) as img:
        has_alpha = img.mode == 'RGBA'
        if has_alpha:
            alpha = img.getchannel('A')
            img = img.convert('RGB')
        
        kelvin_table = {
            1000: (255, 56, 0),
            2000: (255, 109, 0),
            3000: (255, 137, 18),
            4000: (255, 161, 72),
            5000: (255, 180, 107),
            6000: (255, 196, 137),
            7000: (255, 209, 163),
            8000: (255, 219, 186),
            9000: (255, 228, 206),
            10000: (255, 236, 224)
        }
        
        temperature = max(1000, min(10000, temperature))
        lower_kelvin = max([k for k in kelvin_table.keys() if k <= temperature])
        upper_kelvin = min([k for k in kelvin_table.keys() if k >= temperature])
        
        if lower_kelvin == upper_kelvin:
            r, g, b = kelvin_table[lower_kelvin]
        else:
            ratio = (temperature - lower_kelvin) / (upper_kelvin - lower_kelvin)
            r = kelvin_table[lower_kelvin][0] + ratio * (kelvin_table[upper_kelvin][0] - kelvin_table[lower_kelvin][0])
            g = kelvin_table[lower_kelvin][1] + ratio * (kelvin_table[upper_kelvin][1] - kelvin_table[lower_kelvin][1])
            b = kelvin_table[lower_kelvin][2] + ratio * (kelvin_table[upper_kelvin][2] - kelvin_table[lower_kelvin][2])
        
        r, g, b = r/255, g/255, b/255
        matrix = (
            r, 0, 0, 0,
            0, g, 0, 0,
            0, 0, b, 0
        )
        
        temp_img = img.convert('RGB', matrix)
        
        if has_alpha:
            temp_img = temp_img.convert('RGBA')
            temp_img.putalpha(alpha)
        
        return save_image(temp_img, output_path)