import RPi.GPIO as GPIO
import time
import config
import vision
import motor_control

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(config.LAGGING_MOTOR_PIN, GPIO.OUT)

# Start with motor running
GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)


def magnet_detected(channel):
    # Pause motor
    time.sleep(config.PRE_HALL_EFFECT_ADJUSTMENT)
    GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.LOW)

    # Capture and process image
    material, _, _ = vision.capture_and_process()

    # Activate sorting if material found
    if material:
        motor_control.activate_motor(material)

    # Wait before resuming
    time.sleep(config.HALL_EFFECT_DELAY)

    # Restart motor
    GPIO.output(config.LAGGING_MOTOR_PIN, GPIO.HIGH)


# Detect falling edge with debounce
GPIO.add_event_detect(config.HALL_SENSOR_PIN, GPIO.FALLING,
                      callback=magnet_detected, bouncetime=100)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()