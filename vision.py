from PIL import Image
import numpy as np
import config
import logging
import camera

logger = logging.getLogger(__name__)

def capture_and_process():
    """Capture an image and identify its material based on average RGB"""
    try:
        success, filename = camera.camera_system.capture_image()
        if not success:
            logger.error("Image capture failed")
            return None, None, None

        avg_rgb = calculate_average_rgb(filename)
        material = identify_material(avg_rgb)

        logger.info(f"Processed {filename}: Material={material}, RGB={avg_rgb}")
        return material, avg_rgb, filename

    except Exception as e:
        logger.error(f"Vision processing failed: {e}")
        return None, None, None

def calculate_average_rgb(image_path):
    """Calculate average RGB values, optionally using only the center region"""
    try:
        image_array = np.array(Image.open(image_path))
        if config.PROCESS_CENTER_ONLY:
            h, w = image_array.shape[:2]
            m = int(min(h, w) * config.CENTER_REGION_RATIO)
            image_array = image_array[m:h - m, m:w - m]

        return tuple(map(int, np.mean(image_array, axis=(0, 1))))

    except Exception as e:
        logger.error(f"RGB calculation failed: {e}")
        return 0, 0, 0

def identify_material(avg_rgb):
    """Classify material based on configured RGB ranges"""
    try:
        for material, (low, high) in config.COLOR_RANGES.items():
            if all(low[i] <= avg_rgb[i] <= high[i] for i in range(3)):
                return material
        logger.warning(f"No material matched for RGB {avg_rgb}")
        return None

    except Exception as e:
        logger.error(f"Material identification failed: {e}")
        return None
