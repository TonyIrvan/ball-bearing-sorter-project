from components import vision, motor_control, lagging_system, camera, hall_effect
import config
import time
import logger
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    try:
        logger.info("Starting material sorting system")

        while True:
            # Capture and process in one call
            material, avg_rgb, filename = vision.capture_and_process()

            if material:
                logger.info(f"Identified {material} from {filename}")
                motor_control.activate_motor(material)
            else:
                logger.warning("No material identified")

            time.sleep(config.PROCESSING_DELAY)

    except KeyboardInterrupt:
        logger.info("Shutting down system...")
    finally:
        motor_control.cleanup()
        lagging_system.cleanup()
        camera.camera_system.release()


if __name__ == "__main__":
    main()