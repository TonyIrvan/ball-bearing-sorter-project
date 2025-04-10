from PIL import Image
import numpy as np
import config
import logging
import camera  # Import the camera module

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def capture_and_process():
    """
    Combined function to capture image and process it
    Returns: (material, avg_rgb, filename) or (None, None, None) on failure
    """
    try:
        # Capture new image
        success, filename = camera.camera_system.capture_image()
        if not success:
            logger.error("Image capture failed")
            return None, None, None

        # Process the image
        avg_rgb = calculate_average_rgb(filename)
        material = identify_material(avg_rgb)

        logger.info(f"Processed {filename}: Material={material}, RGB={avg_rgb}")
        return material, avg_rgb, filename

    except Exception as e:
        logger.error(f"Vision processing failed: {str(e)}")
        return None, None, None


def calculate_average_rgb(image_path):
    """Calculate average RGB values from an image file"""
    try:
        image = Image.open(image_path)
        image_array = np.array(image)

        # Only process center region if needed (for more consistent readings)
        if config.PROCESS_CENTER_ONLY:
            h, w = image_array.shape[:2]
            margin = int(min(h, w) * config.CENTER_REGION_RATIO)
            image_array = image_array[
                          margin:h - margin,
                          margin:w - margin
                          ]

        average_rgb = np.mean(image_array, axis=(0, 1))
        return tuple(map(int, average_rgb))

    except Exception as e:
        logger.error(f"RGB calculation failed: {str(e)}")
        return 0, 0, 0  # Return black on error


def identify_material(avg_rgb):
    """Identify material based on RGB values"""
    try:
        for material, (low, high) in config.COLOR_RANGES.items():
            if all(low[i] <= avg_rgb[i] <= high[i] for i in range(3)):
                return material
        logger.warning(f"No material matched for RGB {avg_rgb}")
        return None

    except Exception as e:
        logger.error(f"Material identification failed: {str(e)}")
        return None