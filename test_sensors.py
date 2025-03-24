import RPi.GPIO as GPIO
import time
import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(config.HALL_SENSOR_PIN) == GPIO.LOW:
            print("Magnet detected!")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
