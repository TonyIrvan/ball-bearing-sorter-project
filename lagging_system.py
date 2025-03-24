import RPi.GPIO as GPIO
import time

HALL_SENSOR_PIN = 23
LAGGING_MOTOR_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LAGGING_MOTOR_PIN, GPIO.OUT)
GPIO.output(LAGGING_MOTOR_PIN, GPIO.HIGH)  # Motor runs by default

def hall_sensor_callback(channel):
    print("Magnet detected! Stopping motor.")
    GPIO.output(LAGGING_MOTOR_PIN, GPIO.LOW)  # Stop motor
    time.sleep(8)  # Wait for camera to take a picture
    print("Resuming motor.")
    GPIO.output(LAGGING_MOTOR_PIN, GPIO.HIGH)  # Resume motor

GPIO.add_event_detect(HALL_SENSOR_PIN, GPIO.FALLING, callback=hall_sensor_callback, bouncetime=200)

def cleanup():
    GPIO.cleanup()
