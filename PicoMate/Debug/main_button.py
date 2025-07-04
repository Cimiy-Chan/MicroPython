"""
DeskPi PicoMate has a pUsh Button pre-wired to GP26 on the Pico.
The example prints a message to the console each time the state of the button changes.
When the button is pressed, the input level of GP26 will be low (False)
"""

from machine import Pin

button = Pin(26, Pin.IN, Pin.PULL_UP)
buildin_led = Pin('LED', Pin.OUT)

last_value: int = 0

while True:
    if last_value != button.value():
        last_value = button.value()
        if last_value == 1:
            buildin_led.off() #Because, high means button not press
        else:
            buildin_led.on()
