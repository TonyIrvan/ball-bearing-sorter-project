from components import lagging_system, motor_control, vision
import time

def main():
    try:
        while True:
            image_path = "testimage1.jpg"  # Adjust if using a live camera
            avg_rgb = vision.calculate_average_rgb(image_path)
            material = vision.identify_material(avg_rgb)

            if material:
                print(f"Identified as: {material}")
                motor_control.activate_motor(material)

            time.sleep(1)  # Small delay before processing next item

    except KeyboardInterrupt:
        print("Shutting down...")
        motor_control.cleanup()
        lagging_system.cleanup()

if __name__ == "__main__":
    main()
