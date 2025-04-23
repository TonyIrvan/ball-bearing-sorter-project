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

# Queue of (material, trigger_time)
material_queue = []

def set_servo_position(channel, duty):
    pca.channels[channel].duty_cycle = duty
    time.sleep(0.5)
    pca.channels[channel].duty_cycle = config.MOTOR_ZERO

def activate_motor(material):
    if material not in config.MOTORS:
        logger.info(f"No motor for '{material}', skipping.")
        return

    try:
        ch = config.MOTORS[material]
        activation_time = config.MOTOR_ACTIVATION_TIME.get(material, 1.0)

        set_servo_position(ch, config.SERVO_OPEN)
        time.sleep(activation_time)
        set_servo_position(ch, config.SERVO_ZERO)

        logger.info(f"Trapdoor activated for {material}")
    except Exception as e:
        logger.error(f"Motor activation failed: {e}")

def process_signal(material):
    material_queue.append(material)

    if len(material_queue) < 3:
        return

    delayed_material = material_queue.pop(0)

    if delayed_material in config.CONVEYOR_DELAY:
        # Delay by conveyor travel time
        time.sleep(config.CONVEYOR_DELAY[delayed_material])
        activate_motor(delayed_material)


def update_queue():
    now = time.time()
    ready = [entry for entry in material_queue if entry[1] <= now]
    remaining = [entry for entry in material_queue if entry[1] > now]

    for material, _ in ready:
        activate_motor(material)

    material_queue[:] = remaining  # Update in-place

def cleanup():
    for ch in config.MOTORS.values():
        set_servo_position(ch, config.SERVO_ZERO)
    logger.info("Motors cleaned up")
