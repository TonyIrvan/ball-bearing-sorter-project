# Trapdoor Motor PCA9685 Channels, Hall Effect Sensor (GPIO), & Lagging Motor (PCA)
MOTORS = {
    "chrome": 0,
    "brass": 1,
    "nylon": 2
}

HALL_SENSOR_PIN = 23           # Stays GPIO
LAGGING_MOTOR_PIN = 13          # PCA9685 channel

CONTINUOUS_MOTOR1 = 14          # PCA9685 channel - horizontal screws
CONTINUOUS_MOTOR2 = 15          # PCA9685 channel - vert screw and cement mixer

# Motor PWM signal values
FAST_CW = 64000
FAST_CCW = 17000
SLOW_CW = 54000
SLOW_CCW = 45000
MOTOR_ZERO = 52000

SERVO_OPEN = 7864
SERVO_ZERO = 1700

# Camera Settings (for camera.py)
CAMERA_INDEX = 0
CAMERA_WIDTH = 640   # 640x480 is typically fastest
CAMERA_HEIGHT = 480

# Timing Settings
MOTOR_ACTIVATION_TIME = 2.0      # Seconds (from motor_control.py)
LAGGING_DELAY = 8.0              # Seconds (from lagging_system.py)
PROCESSING_DELAY = 1.0
HALL_EFFECT_DELAY = 5.0
PRE_HALL_EFFECT_ADJUSTMENT = 0.5 # Seconds (from hall_effect.py)

# Vision Processing Settings
PROCESS_CENTER_ONLY = True  # Only process center of image
CENTER_REGION_RATIO = 0.3   # Use center 30% of image

# Predefined RGB Ranges for Material Identification
# NOT ACTUAL DATA
COLOR_RANGES = {
    "chrome": [(180, 180, 180), (255, 255, 255)],
    "brass": [(160, 100, 60), (230, 190, 140)],
    "nylon": [(200, 200, 200), (240, 240, 240)]
}
