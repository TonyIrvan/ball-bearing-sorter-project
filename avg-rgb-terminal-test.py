from PIL import Image
import numpy as np

# Function to calculate average RGB values
def calculate_average_rgb(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)
    average_rgb = np.mean(image_array, axis=(0, 1))
    return average_rgb

def display_average_color_terminal(average_rgb):
    r, g, b = average_rgb
    print(f"\033[48;2;{int(r)};{int(g)};{int(b)}m      \033[0m")  # Print a colored block
    print(f"Average Color: R={r:.2f}, G={g:.2f}, B={b:.2f}")

# Modify the test function
def test_with_static_image():
    image_path = r"C:testimage1.jpg"
    average_rgb = calculate_average_rgb(image_path)
    display_average_color_terminal(average_rgb)

test_with_static_image()