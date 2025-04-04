import motor_control
import time

materials = ["chrome", "brass", "nylon"]

try:
    for material in materials:
        print(f"Testing motor for {material}...")
        motor_control.activate_motor(material)
        time.sleep(1)

finally:
    motor_control.cleanup()
