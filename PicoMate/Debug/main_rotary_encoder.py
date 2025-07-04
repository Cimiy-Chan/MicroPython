"""
DeskPi PicoMate has an incremental rotary encoder pre-wired to the Pico.
It converts the motion of the switch (clockwise or counterclockwise) into an output signal that
can be used to determine what direction the knob is being rotated.

Pin: A=GP7, B=GP6, Switch (Active high)=-GP26

Output: Light or dim the RGB LED to show the direction of the rotary switch
"""
from machine import Pin
import time

from neopixel import Neopixel

Pin_CLK = 7
Pin_DT = 6
Pin_SW = 26
Pin_rgb_led = 22

pin_clk = Pin(Pin_CLK, Pin.IN)
pin_dt = Pin(Pin_DT, Pin.IN)
pin_sw = Pin(Pin_SW, Pin.PULL_DOWN, Pin.IN)
buildin_led = Pin('LED', Pin.OUT)

counter = 0
current_state_clk = 0

rgb_led = Neopixel(1, 0, Pin_rgb_led, 'RGB')
rgb_led.brightness(50)

last_state_clk = pin_clk.value()

while True:
    current_state_clk = pin_clk.value()

    if current_state_clk != last_state_clk and current_state_clk == 1:
        buildin_led.on()
        if pin_dt.value() != current_state_clk:
            counter += 1
        else:
            counter -= 1

    #print (f'Counter: {counter}')
    if counter > 255:
        counter = 255
    if counter < 1:
        counter = 1
    rgb_led.set_pixel(0, (counter, counter, counter))
    rgb_led.show()
    last_state_clk = current_state_clk
    buildin_led.off()
    #time.sleep_ms(10) # No time delay is allowed, it will affect the inc/dec
    rgb_led.clear()

    #Detect push button
    if pin_sw.value() == 1:
        rgb_led.set_pixel(0, (255,0,0))
        rgb_led.show()
        time.sleep_ms(500)
        rgb_led.clear()

