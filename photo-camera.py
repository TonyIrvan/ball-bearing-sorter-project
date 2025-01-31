import RPi.GPIO as GPIO
from picamera import PiCamera
from PIL import Image  # For image processing
import numpy as np  # For numerical operations
from time import sleep
import datetime
import os

# GPIO setup
TRIGGER_PIN = 17  # GPIO pin connected to the sensor/button
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Camera setup
camera = PiCamera()
camera.resolution = (1024, 768)  # Set resolution


# Function to capture image
def capture_image():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"/home/pi/images/{timestamp}.jpg"  # Save images in a folder
    camera.capture(image_path)
    print(f"Image saved: {image_path}")
    return image_path

# Function to calculate average RGB values
def calculate_average_rgb(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)
    # Convert the image to a numpy array for easy calculations
    image_array = np.array(image)
    # Calculate the average RGB values
    average_rgb = np.mean(image_array, axis=(0, 1))  # Average over all pixels
    return average_rgb

try:
    print("Waiting for trigger...")
    while True:
        if GPIO.input(TRIGGER_PIN) == GPIO.HIGH:  # Check if the pin is HIGH (triggered)
            print("Trigger detected! Capturing image...")
            image_path = capture_image()
            # Calculate the average RGB values
            average_rgb = calculate_average_rgb(image_path)
            print(f"Average RGB values: R={average_rgb[0]:.2f}, G={average_rgb[1]:.2f}, B={average_rgb[2]:.2f}")
            sleep(1)  # Debounce delay to avoid multiple triggers
        sleep(0.1)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Exiting...")

finally:
    camera.stop_preview()
    GPIO.cleanup()
