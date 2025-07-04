"""
Demo application of 8x8 NeoPixel
"""
import time, random
from random import randrange
from neopixel import Neopixel
from machine import Pin

if __name__ == '__main__':
    button = Pin(2, Pin.IN, Pin.PULL_DOWN)
    led_light = Pin(3, Pin.OUT)
    Numpix = 64
    DataPin = 22
    led = Neopixel(Numpix, 0, DataPin, 'RGB')
    led.brightness(20)
    button_current_state = 0
    button_next_state = 0

    """
    #Code for checking the LED one by one. 
    # Check single R, G and B and RGB (white) together
    while True:
        for pixel_pos in range (0, 48):
            led.set_pixel(pixel_pos, (255, 0, 0))
            led.show()
            time.sleep_ms(20)
            led.clear()
            time.sleep_ms(20)
        for pixel_pos in range (48, 0, -1):
            led.set_pixel(pixel_pos, (0, 255, 0))
            led.show()
            time.sleep_ms(20)
            led.clear()
            time.sleep_ms(20)
        for pixel_pos in range (0, 48):
            led.set_pixel(pixel_pos, (0, 0, 255))
            led.show()
            time.sleep_ms(20)
            led.clear()
            time.sleep_ms(20)
        for pixel_pos in range (48, 0, -1):
            led.set_pixel(pixel_pos, (255, 255, 255))
            led.show()
            time.sleep_ms(20)
            led.clear()
            time.sleep_ms(20)

    """

    xy_array = []
    rgb_array = []
    while True:
        no_of_pixel = randrange(5,30)
        pixel_parm = led.pixel_para_random(no_of_pixel)
        for each_parm in range(0, len(pixel_parm)):
            xy_array.append(pixel_parm[each_parm][0])
            rgb_array.append(pixel_parm[each_parm][1])
        led.pixel_group_flash(no_of_pixel, xy_array, rgb_array, 0, 50, duration_ms=100)
        xy_array.clear()
        rgb_array.clear()
        button_current_state = button.value()
        if button_current_state != button_next_state:
            break
        time.sleep_ms(50)
    led_light.on()
    time.sleep(3)
    led_light.off()
    #End of program

