import board
import busio
import adafruit_pca9685
import time

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50
channel = pca.channels[0]

while True:
    for i in range (0, 7864, 100): #
        channel.duty_cycle = i
        time.sleep(0.01)
        print(i)

channel.duty_cycle = 0