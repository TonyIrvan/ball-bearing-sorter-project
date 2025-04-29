import logging
import time
import config
import vision
import camera
import motor_control
from sensor_motor import SensorMotorSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        logger = logging.getLogger(__name__)
        logger.info("Starting material sorting system with sensor-based rotation")
        
        sorter = SensorMotorSystem()

        while True:
            # Wait for magnet detection and stop at a valid position
            sorter.wait_for_next_position()

            # Take picture and classify
            material, avg_rgb, filename = vision.capture_and_process()

            if material:
                logger.info(f"Identified {material} from {filename}")
                sorter.sort_material(material)
            else:
                logger.warning("No material identified")

            time.sleep(config.PROCESSING_DELAY)

    except KeyboardInterrupt:
        logger.info("Shutting down system...")

    finally:
        motor_control.cleanup()
        sorter.cleanup()
        camera.camera_system.release()

if __name__ == "__main__":
    main()
