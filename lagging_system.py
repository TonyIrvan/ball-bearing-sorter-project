import RPi.GPIO as GPIO
import config
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(config.LAGGING_MOTOR_PIN, GPIO.OUT)
GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)  # Motor runs by default

def hall_sensor_callback(channel):
    print("Magnet detected! Stopping motor.")
    GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.LOW)  # Stop motor
    time.sleep(8)  # Wait for camera to take a picture
    print("Resuming motor.")
    GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)  # Resume motor

GPIO.add_event_detect(config.HALL_SENSOR_PIN, GPIO.FALLING, callback=hall_sensor_callback, bouncetime=200)

def cleanup():
    GPIO.cleanup()
