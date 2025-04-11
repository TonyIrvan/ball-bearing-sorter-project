import RPi.GPIO as GPIO
import config
import time

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config.LAGGING_MOTOR_PIN, GPIO.OUT)
    GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)  # Start motor

    def hall_callback(channel):
        print("Magnet detected - pausing system")
        GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.LOW)
        time.sleep(config.LAGGING_DELAY)
        GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)

    GPIO.add_event_detect(config.HALL_SENSOR_PIN, GPIO.FALLING,
                          callback=hall_callback, bouncetime=200)


def cleanup():
    GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.LOW)