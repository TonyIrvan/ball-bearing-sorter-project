import RPi.GPIO as GPIO
import time
import board
import busio
from adafruit_pca9685 import PCA9685

import config
import vision
import motor_control

# Setup I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def start_motor():
    pca.channels[config.LAGGING_PWM_CHANNEL].duty_cycle = config.FAST_CW #Might be CCW

def stop_motor():
    pca.channels[config.LAGGING_PWM_CHANNEL].duty_cycle = config.MOTOR_ZERO

def hall_callback(channel):
    print("Magnet detected - stopping motor and processing")
    
    time.sleep(config.PRE_HALL_EFFECT_ADJUSTMENT)
    stop_motor()
    
    material, _, _ = vision.capture_and_process()

    if material:
        motor_control.activate_motor(material)

    time.sleep(config.HALL_EFFECT_DELAY)
    start_motor()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    start_motor()

    GPIO.add_event_detect(config.HALL_SENSOR_PIN, GPIO.FALLING,
                          callback=hall_callback, bouncetime=200)

def cleanup():
    stop_motor()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()
