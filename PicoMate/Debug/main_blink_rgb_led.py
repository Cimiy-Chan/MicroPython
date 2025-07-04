"""
Deski PicoMate has a WS2812 RGB LED pre-wiored to GP22 on the Pico.
We can use the NeoPixel library to blink the TGB LED.
"""

import time
from neopixel import Neopixel

R = (50, 0, 0)
G = (0, 50, 0)
B = (0, 0, 50)
COLORS = (R, G, B)

DATA_PIN = 22
rgb_led = Neopixel(1, 0, DATA_PIN, 'RGB')
rgb_led.brightness(50)

while True:
    for color in COLORS:
        rgb_led.set_pixel(0, color)
        rgb_led.show()
        time.sleep(0.5)
        rgb_led.clear()