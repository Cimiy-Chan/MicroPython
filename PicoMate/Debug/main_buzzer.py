"""
DeskPi PicoMate has a buzzer pre-wired to GP27 on the Pico.
To control the buzzer from MicroPython, we will use ots builts in PWM, pulse-width modulation, signal generation capabilities.
"""
import time
import random
from random import randrange

from machine import PWM, Pin
from neopixel import Neopixel

Pin_rgb_led = 22
Pin_Buzzer = 27
Pin_Button = 26

TONE_FREQ = [
    1047, 1047, 1568, 1568, 1760, 1760, 1568, 0,0,
    1397, 1397, 1319, 1319, 1175, 1175, 1047, 0,0,
    1568, 1568, 1397, 1397, 1319, 1319, 1175, 0,0,
    1568, 1568, 1397, 1397, 1319, 1319, 1175, 0,0,
    1047, 1047, 1568, 1568, 1760, 1760, 1568, 0,0,
    1397, 1397, 1319, 1319, 1175, 1175, 1047, 0,0,
]


buzzer = PWM(Pin_Buzzer, freq=1000, duty_u16=0)
rgb_led = Neopixel(1, 0, Pin_rgb_led, 'RGB')
rgb_led.brightness(50)
button = Pin(Pin_Button, Pin.IN, Pin.PULL_UP)

while True:
    for note in TONE_FREQ:
        if note:
            buzzer.duty_u16(32768)
            buzzer.freq(note)
            rgb_led.set_pixel(0, (randrange(0,256), randrange(0, 256), randrange(0, 256)))
            rgb_led.show() #Flase the light
            time.sleep_ms(100)
            rgb_led.clear()
            rgb_led.show()
            buzzer.duty_u16(0) #Stop the buzzer bee
        time.sleep_ms(200)
    while True:
        rgb_led.set_pixel(0, (0, 255, 0))
        rgb_led.show()
        time.sleep_ms(50)
        rgb_led.clear()
        rgb_led.show()
        time.sleep_ms(1000)
        if button.value() == 0:
            break
