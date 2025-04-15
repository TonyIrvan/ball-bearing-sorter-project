import time
import signal
import sys
import board
import busio
from adafruit_pca9685 import PCA9685

import config

# Setup I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def setup():
    # Set motors to full speed (duty cycle max)
    pca.channels[config.CONTINUOUS_MOTOR1].duty_cycle = config.FAST_CW
    pca.channels[config.CONTINUOUS_MOTOR2].duty_cycle = config.FAST_CW
    while(True):
        pca.channels[config.CONTINUOUS_MOTOR2].duty_cycle = config.FAST_CW
        time.sleep(config.R_LAG_CYCLE)
        pca.channels[config.CONTINUOUS_MOTOR2].duty_cycle = config.MOTOR_ZERO
        time.sleep(1)


def cleanup(signal, frame):
    # Stop motors by setting duty cycle to 0
    pca.channels[config.CONTINUOUS_MOTOR1].duty_cycle = config.MOTOR_ZERO
    pca.channels[config.CONTINUOUS_MOTOR2].duty_cycle = config.MOTOR_ZERO
    print("Motors stopped. Exiting.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    setup()
    print("Motors running continuously. Press CTRL+C to stop.")
    while True:
        time.sleep(1)
