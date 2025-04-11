import RPi.GPIO as GPIO
import config
import time
import logging

logger = logging.getLogger(__name__)

class MotorController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.motor_pins = config.MOTORS
        for pin in self.motor_pins.values():
            GPIO.setup(pin, GPIO.OUT)
            self._set_servo_angle(pin, 0)  # Initialize closed position
        logger.info("Trapdoor motors initialized")

    def _set_servo_angle(self, pin, angle):
        pwm = GPIO.PWM(pin, 50)  # 50Hz frequency
        pwm.start(0)
        duty = angle / 18 + 2
        GPIO.output(pin, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        GPIO.output(pin, False)
        pwm.stop()

    def activate_motor(self, material):
        if material not in self.motor_pins:
            logger.error(f"Invalid material: {material}")
            return

        try:
            pin = self.motor_pins[material]
            self._set_servo_angle(pin, 90)  # Open trapdoor
            time.sleep(config.MOTOR_ACTIVATION_TIME)
            self._set_servo_angle(pin, 0)   # Close trapdoor
            logger.info(f"Trapdoor opened for {material}")
        except Exception as e:
            logger.error(f"Motor activation failed: {e}")

    def cleanup(self):
        for pin in self.motor_pins.values():
            self._set_servo_angle(pin, 0)
        logger.info("MotorController cleaned up")

# Singleton instance
motor_controller = MotorController()