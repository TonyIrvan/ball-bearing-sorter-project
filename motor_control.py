import RPi.GPIO as GPIO
import time
import config

GPIO.setmode(GPIO.BCM)
for pin in config.MOTORS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def activate_motor(material):
    if material in config.MOTORS:
        GPIO.output(config.MOTORS[material], GPIO.HIGH)
        time.sleep(config.MOTOR_ACTIVATION_TIME)
        GPIO.output(config.MOTORS[material], GPIO.LOW)

def cleanup():
    GPIO.cleanup()