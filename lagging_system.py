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
    pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = config.SLOW_CCW

def stop_motor():
    pca.channels[config.LAGGING_MOTOR_PIN].duty_cycle = config.MOTOR_ZERO

def hall_callback(channel):
    print("Magnet detected - stopping motor and processing")
    
    stop_motor()
    
    material, _, _ = vision.capture_and_process()

    if material:
        motor_control.process_signal(material)

    time.sleep(config.HALL_EFFECT_DELAY)
    start_motor()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN)

    pca.channels[config.LED_PIN].duty_cycle = config.BRIGHTNESS


    start_motor()

    GPIO.add_event_detect(config.HALL_SENSOR_PIN, GPIO.RISING,
                          callback=hall_callback, bouncetime=150) #bounce = 90 on Left one

def cleanup():
    stop_motor()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        while True:
            motor_control.update_queue()
            time.sleep(0.1)
    except KeyboardInterrupt:
        cleanup()
