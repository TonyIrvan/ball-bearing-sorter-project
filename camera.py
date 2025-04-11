import time
from datetime import datetime
import logging
from picamera2 import Picamera2
import config

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='camera.log'
)
logger = logging.getLogger(__name__)


class CameraSystem:
    def __init__(self):
        self.picam2 = Picamera2()
        self.last_capture_time = 0
        self.configure_camera()

    def configure_camera(self):
        try:
            video_config = self.picam2.create_still_configuration(
                main={"size": (config.CAMERA_WIDTH, config.CAMERA_HEIGHT)}
            )
            self.picam2.configure(video_config)
            self.picam2.start()
            logger.info(f"Camera initialized at {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            raise

    def capture_image(self, base_filename="bearing"):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{base_filename}_{timestamp}.jpg"
            image = self.picam2.capture_array()
            self.picam2.capture_file(filename)

            capture_time = time.time() - self.last_capture_time
            self.last_capture_time = time.time()

            logger.info(f"Captured {filename} in {capture_time:.2f}s")
            return True, filename
        except Exception as e:
            logger.error(f"Capture error: {e}")
            return False, None

    def release(self):
        self.picam2.close()
        logger.info("Camera resources released")


camera_system = CameraSystem()


def capture_image():
    return camera_system.capture_image()[1]


if __name__ == "__main__":
    try:
        print("Testing camera...")
        test_count = 5
        start_time = time.time()

        for i in range(test_count):
            success, filename = camera_system.capture_image(f"test_{i}")
            if success:
                print(f"Captured {filename}")
            time.sleep(0.5)

        avg_time = (time.time() - start_time) / test_count
        print(f"Average capture time: {avg_time:.2f} seconds")

    finally:
        camera_system.release()
