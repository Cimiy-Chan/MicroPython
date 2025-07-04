"""
DeskPi PicoMate has a Digital PIR sensor pre-wired to GP28 on the Pico.
The digital PIR sensor allows you to share sens motion, almost used to detect whether a human has
moved in or out of the sensors range
"""

from machine import Pin
from neopixel import Neopixel

DATA_PIN = 22
rgb_led = Neopixel(1, 0, DATA_PIN, 'RGB')
rgb_led.brightness(20)

pir_sensor = Pin(28, Pin.PULL_DOWN, Pin.IN)

previous_pir_value = pir_sensor.value()

while True:
    if pir_sensor.value():
        rgb_led.set_pixel(0, (255, 0, 0))
        rgb_led.show()
    else:
        rgb_led.set_pixel(0, (0, 255, 0))
        rgb_led.show()
    rgb_led.clear()