import time
import logging
import board
import busio
from adafruit_pca9685 import PCA9685

import config

logger = logging.getLogger(__name__)

# Setup I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

class MotorController:
    def __init__(self):
        self.motor_channels = config.MOTORS
        for ch in self.motor_channels.values():
            self._set_servo_angle(ch, 0)  # Initialize closed position
        logger.info("Trapdoor motors initialized")

    def _angle_to_duty(self, angle):
        # Converts 0-180° to duty cycle for PCA9685 (16-bit)
        min_duty = 1500   # ~2.5%
        max_duty = 8000   # ~12.5%
        return int((angle / 180) * (max_duty - min_duty) + min_duty)

    def _set_servo_angle(self, channel, angle):
        duty = self._angle_to_duty(angle)
        pca.channels[channel].duty_cycle = duty
        time.sleep(0.5)
        pca.channels[channel].duty_cycle = 0  # Stop signal

    def activate_motor(self, material):
        if material not in self.motor_channels:
            logger.error(f"Invalid material: {material}")
            return

        try:
            ch = self.motor_channels[material]
            self._set_servo_angle(ch, 90)  # Open trapdoor
            time.sleep(config.MOTOR_ACTIVATION_TIME)
            self._set_servo_angle(ch, 0)   # Close trapdoor
            logger.info(f"Trapdoor opened for {material}")
        except Exception as e:
            logger.error(f"Motor activation failed: {e}")

    def cleanup(self):
        for ch in self.motor_channels.values():
            self._set_servo_angle(ch, 0)
        logger.info("MotorController cleaned up")

# Singleton instance
motor_controller = MotorController()
