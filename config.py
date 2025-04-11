﻿# Trapdoor Motor GPIO Pins, Hall Effect Sensor, & Lagging Motor
MOTORS = {
    "chrome": 17,
    "brass": 27,
    "nylon": 22
}
HALL_SENSOR_PIN = 23
LAGGING_MOTOR_PIN = 24


# Camera Settings (for camera.py)
CAMERA_INDEX = 0
CAMERA_WIDTH = 640   # 640x480 is typically fastest
CAMERA_HEIGHT = 480

# Timing Settings
MOTOR_ACTIVATION_TIME = 0.5      # Seconds (from motor_control.py)
LAGGING_DELAY = 8                # Seconds (from lagging_system.py)
PROCESSING_DELAY = 1
HALL_EFFECT_DELAY = 10
PRE_HALL_EFFECT_ADJUSTMENT = 0.5 # Seconds (from hall_effect.py)

# Vision Processing Settings
PROCESS_CENTER_ONLY = True  # Only process center of image
CENTER_REGION_RATIO = 0.3   # Use center 30% of image

# Predefined RGB Ranges for Material Identification
#NOT ACTUAL DATA
COLOR_RANGES = {
    "chrome": [(180, 180, 180), (255, 255, 255)],
    "brass": [(160, 100, 60), (230, 190, 140)],
    "nylon": [(200, 200, 200), (240, 240, 240)]
}
