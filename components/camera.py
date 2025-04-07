import cv2
import time
from datetime import datetime
import config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='camera.log'
)
logger = logging.getLogger(__name__)


class CameraSystem:
    def __init__(self):
        self.camera = None
        self.last_capture_time = 0
        self.initialize_camera()

    def initialize_camera(self):
        """Initialize camera with fast capture settings"""
        try:
            self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
            if not self.camera.isOpened():
                raise RuntimeError("Could not open camera")

            # Set optimized resolution for speed (640x480 is typically fastest)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

            # Disable auto features for consistent lighting
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual exposure
            self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Disable autofocus
            self.camera.set(cv2.CAP_PROP_AUTO_WB, 0)  # Disable white balance

            logger.info(f"Camera initialized at {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")

        except Exception as e:
            logger.error(f"Camera initialization failed: {str(e)}")
            raise

    def capture_image(self, base_filename="bearing"):
        """
        Fast single image capture with timestamp
        Returns: (success, filename) tuple
        """
        try:
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{base_filename}_{timestamp}.jpg"

            # Warmup (read a couple frames first)
            for _ in range(2):
                self.camera.read()

            # Actual capture
            ret, frame = self.camera.read()
            if not ret:
                logger.warning("Capture failed - no frame received")
                return False, None

            cv2.imwrite(filename, frame)
            capture_time = time.time() - self.last_capture_time
            self.last_capture_time = time.time()

            logger.info(f"Captured {filename} in {capture_time:.2f}s")
            return True, filename

        except Exception as e:
            logger.error(f"Capture error: {str(e)}")
            return False, None

    def preview(self, duration=10):
        """Simple preview (works on Pi with GUI, optional)"""
        try:
            from threading import Thread
            preview_thread = Thread(target=self._run_preview, args=(duration,))
            preview_thread.start()
            return preview_thread
        except ImportError:
            logger.warning("Preview unavailable in headless mode")

    def _run_preview(self, duration):
        """Internal preview function"""
        end_time = time.time() + duration
        window_name = "Camera Preview (Press Q to quit)"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        while time.time() < end_time:
            ret, frame = self.camera.read()
            if ret:
                cv2.imshow(window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()

    def release(self):
        """Release camera resources"""
        if self.camera is not None:
            self.camera.release()
            logger.info("Camera resources released")


# Update config.py with these additions:
"""
# Camera Settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640   # Faster than higher resolutions
CAMERA_HEIGHT = 480
"""

# Singleton instance
camera_system = CameraSystem()


def capture_image():
    """Simple interface for main program"""
    return camera_system.capture_image()[1]


if __name__ == "__main__":
    # Test script
    try:
        print("Testing camera...")
        preview_thread = camera_system.preview()

        # Test capture speed
        test_count = 5
        start_time = time.time()

        for i in range(test_count):
            success, filename = camera_system.capture_image(f"test_{i}")
            if success:
                print(f"Captured {filename}")
            time.sleep(0.5)  # Small delay between tests

        avg_time = (time.time() - start_time) / test_count
        print(f"Average capture time: {avg_time:.2f} seconds")

        if preview_thread:
            preview_thread.join()

    finally:
        camera_system.release()