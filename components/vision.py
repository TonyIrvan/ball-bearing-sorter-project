from PIL import Image
import numpy as np
import config

def calculate_average_rgb(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)
    average_rgb = np.mean(image_array, axis=(0, 1))
    return tuple(map(int, average_rgb))

def identify_material(avg_rgb):
    for material, (low, high) in config.COLOR_RANGES.items():
        if all(low[i] <= avg_rgb[i] <= high[i] for i in range(3)):
            return material
    return None
