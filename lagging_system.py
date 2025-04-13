import RPi.GPIO as GPIO
import time
import board
import busio
from adafruit_pca9685 import PCA9685

import config

# Setup I2C and PCA9685 for lagging motor control
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Start motor
    pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0xFFFF

    def hall_callback(channel):
        print("Magnet detected - pausing system")
        pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0
        time.sleep(config.LAGGING_DELAY)
        pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0xFFFF

    GPIO.add_event_detect(config.HALL_SENSOR_PIN, GPIO.FALLING,
                          callback=hall_callback, bouncetime=200)

def cleanup():
    pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = 0
