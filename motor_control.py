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

material_queue = []

def process_signal(material):
    """Add signal and trigger motor for one two steps behind"""
    material_queue.append(material)

    if len(material_queue) > 3:
        material_queue.pop(0)  # Keep only last 3 items

    if len(material_queue) == 3:
        delayed_material = material_queue[0]
        activate_motor(delayed_material)


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

        # Allow per-material motor timings if needed
        activation_time = config.MOTOR_ACTIVATION_TIME.get(material, 1.0)

        set_servo_position(ch, config.SERVO_OPEN)  # Open trapdoor
        time.sleep(activation_time)
        set_servo_position(ch, config.SERVO_ZERO)  # Close trapdoor

        logger.info(f"Trapdoor activated for {material}")
    except Exception as e:
        logger.error(f"Motor activation failed: {e}")

def process_signal(material):
    """Add signal and trigger motor for one two steps behind"""
    material_queue.append(material)

    if len(material_queue) == 3:
        delayed_material = material_queue[0]  # The one two steps behind
        activate_motor(delayed_material)

def cleanup():
    """Reset all motors to closed"""
    for ch in config.MOTORS.values():
        set_servo_position(ch, config.SERVO_ZERO)
    logger.info("Motors cleaned up")
