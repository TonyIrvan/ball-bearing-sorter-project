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
    """Calculate average RGB values, excluding near-black and near-white pixels"""
    try:
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)

        # Flatten to 2D array: (pixels, 3)
        pixels = image_array.reshape(-1, 3)

        # Define tolerance to filter near-black and near-white
        tolerance = getattr(config, 'BW_TOLERANCE', 10)

        # Filter out near-black or near-white pixels
        filtered_pixels = np.array([
            p for p in pixels
            if not (all(p <= tolerance) or all(p >= 255 - tolerance))
        ])

        if len(filtered_pixels) == 0:
            logger.warning("All pixels were black/white or image is empty")
            return 0, 0, 0

        return tuple(map(int, np.mean(filtered_pixels, axis=0)))

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
