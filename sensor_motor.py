import RPi.GPIO as GPIO
import time
import config
import motor_control
import vision
import logging
from collections import deque

logger = logging.getLogger(__name__)


class SensorMotorSystem:
    def __init__(self):
        self.current_position = 1  # Positions 1-4
        self.material_queue = deque()
        self.position_lock = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(config.LAGGING_MOTOR_PIN, GPIO.OUT)
        GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)
        self._setup_callbacks()

    def _setup_callbacks(self):
        GPIO.add_event_detect(
            config.HALL_SENSOR_PIN,
            GPIO.FALLING,
            callback=self._magnet_detected,
            bouncetime=200
        )

    def _magnet_detected(self, channel):
        with self.position_lock:
            try:
                # Stop motor and update position
                GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.LOW)
                self.current_position = (self.current_position % 4) + 1
                logger.info(f"Position updated to {self.current_position}")

                # Position-specific processing
                if self.current_position == 2:
                    material, _, _ = vision.capture_and_process()
                    if material:
                        self.material_queue.append((material, 2))  # Needs 2 positions to reach exit
                        logger.info(f"Queued {material} for processing")

                # Update all queued materials
                for i in reversed(range(len(self.material_queue))):
                    mat, steps = self.material_queue[i]
                    if steps <= 1:
                        motor_control.motor_controller.activate_motor(mat)
                        del self.material_queue[i]
                    else:
                        self.material_queue[i] = (mat, steps - 1)

            except Exception as e:
                logger.error(f"Processing error: {e}")
            finally:
                time.sleep(config.HALL_EFFECT_DELAY)
                GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)

    def cleanup(self):
        GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.LOW)
        GPIO.cleanup()


# Singleton instance
sensor_motor_system = SensorMotorSystem()