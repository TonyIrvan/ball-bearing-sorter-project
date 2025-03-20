from gpiozero import Button

hall_sensor = Button(17) #gpio pin

while True:
    if hall_sensor.is_pressed:
        print("Magnet detected")
