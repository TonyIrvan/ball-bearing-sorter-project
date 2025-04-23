# Trapdoor Motor PCA9685 Channels, Hall Effect Sensor (GPIO), & Lagging Motor (PCA)
MOTORS = {
    "brass": 1,
    "nylon": 0
}

HALL_SENSOR_PIN = 23           # Stays GPIO
LAGGING_MOTOR_PIN = 13          # PCA9685 channel

CONTINUOUS_MOTOR1 = 14          # PCA9685 channel - horizontal screws
CONTINUOUS_MOTOR2 = 15          # PCA9685 channel - vert screw and cement mixer

# Motor PWM signal values
FAST_CW = 64000
FAST_CCW = 17000
SLOW_CW = 54000
SLOW_CCW = 45500
MOTOR_ZERO = 0

CEMENT_MIXER = 57500
R_LAGGING_MOTOR = 45500

SERVO_ZERO = 7864
SERVO_OPEN = 1700

# Camera Settings (for camera.py)
CAMERA_INDEX = 0
CAMERA_WIDTH = 480   # 640x480 is typically fastest
CAMERA_HEIGHT = 480

# Timing Settings
MOTOR_ACTIVATION_TIME = 2.0      # Seconds (from motor_control.py)
LAGGING_DELAY = 8.0              # Seconds (from lagging_system.py)
PROCESSING_DELAY = 1.0
HALL_EFFECT_DELAY = 2.0

# Per-material motor timing (in seconds)
CONVEYOR_DELAY = {
    "nylon": 2.5,  # seconds to reach nylon trapdoor
    "brass": 4.1,  # seconds to reach brass trapdoor
    # no entry for chrome = no trapdoor
}

# Fallback if material not found
DEFAULT_ACTIVATION_TIME = 1.0

# Vision Processing Settings
PROCESS_CENTER_ONLY = True  # Only process center of image
CENTER_REGION_RATIO = 0.3   # Use center 30% of image
BW_TOLERANCE = 10  # tweak this if you want to be more/less strict


# Predefined RGB Ranges for Material Identification
# NOT ACTUAL DATA
COLOR_RANGES = {
    "chrome": [(180, 180, 180), (255, 255, 255)],
    "brass": [(160, 100, 60), (230, 190, 140)],
    "nylon": [(200, 200, 200), (240, 240, 240)]
}
