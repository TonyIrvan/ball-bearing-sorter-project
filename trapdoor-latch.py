import RPi.GPIO as GPIO
import time

servo_pin = 18  # GPIO pin connected to the signal wire

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance with 50Hz frequency
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop sending signal

# Rotate 90 degrees
set_angle(90)

# Cleanup
pwm.stop()
GPIO.cleanup()
