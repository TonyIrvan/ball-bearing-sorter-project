import RPi.GPIO as GPIO
import time
import signal
import sys

import config

# Configuration
GPIO.setwarnings(False)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.CONTINUOUS_MOTOR1, GPIO.OUT)
    GPIO.setup(config.CONTINUOUS_MOTOR2, GPIO.OUT)
    GPIO.output(config.CONTINUOUS_MOTOR1, GPIO.HIGH)
    GPIO.output(config.CONTINUOUS_MOTOR2, GPIO.HIGH)

def cleanup(signal, frame):
    GPIO.output(config.CONTINUOUS_MOTOR1, GPIO.LOW)
    GPIO.output(config.CONTINUOUS_MOTOR2, GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    setup()
    print("Motors running continuously. Press CTRL+C to stop.")
    while True:
        time.sleep(1)  # Keep program running