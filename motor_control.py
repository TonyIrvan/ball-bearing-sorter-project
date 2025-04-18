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

def set_servo_position(channel, duty):
    """Set servo to a specific duty cycle"""
    pca.channels[channel].duty_cycle = duty
    time.sleep(0.5)
    pca.channels[channel].duty_cycle = config.MOTOR_ZERO  # Stop signal

def activate_motor(material):
    """Open and close trapdoor based on identified material"""
    if material not in config.MOTORS:
        logger.error(f"Invalid material: {material}")
        return

    try:
        ch = config.MOTORS[material]
        set_servo_position(ch, config.SERVO_OPEN)  # Open trapdoor
        time.sleep(config.MOTOR_ACTIVATION_TIME)
        set_servo_position(ch, config.SERVO_ZERO)  # Close trapdoor
        logger.info(f"Trapdoor activated for {material}")
    except Exception as e:
        logger.error(f"Motor activation failed: {e}")

def cleanup():
    """Reset all motors to closed"""
    for ch in config.MOTORS.values():
        set_servo_position(ch, config.SERVO_ZERO)
    logger.info("Motors cleaned up")
