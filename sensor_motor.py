import RPi.GPIO as GPIO
import time
import config
import motor_control
import vision
import logging
import threading
from collections import deque

import board
import busio
from adafruit_pca9685 import PCA9685

logger = logging.getLogger(__name__)

# Setup I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50


class SensorMotorSystem:
    def __init__(self):
        self.current_position = 1  # Positions 1-4
        self.material_queue = deque()
        self.position_lock = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Start motor using PCA
        pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0xFFFF
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
                # Stop motor
                pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0
                self.current_position = (self.current_position % 4) + 1
                logger.info(f"Position updated to {self.current_position}")

                if self.current_position == 2:
                    material, _, _ = vision.capture_and_process()
                    if material:
                        self.material_queue.append((material, 2))
                        logger.info(f"Queued {material} for processing")

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
                pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0xFFFF

    def cleanup(self):
        pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0
        GPIO.cleanup()


# Singleton instance
sensor_motor_system = SensorMotorSystem()
