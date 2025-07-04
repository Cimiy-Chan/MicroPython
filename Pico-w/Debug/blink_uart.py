"""
For flashing the file into device, filename must be "main.py"
Other filename cannot be flashed into the Pico-W device.

Two UARTs at Pico-W
UART0 - GPIO 0/1, 12/13 and 16/17 (Internal use)
UART1 - GPIO 4/5, 8/9

Only one timer at RP2040
"""

from machine import Pin, Timer, UART

led = Pin("LED", Pin.OUT)
timer0 = Timer() #No need to specify the timer id (ignore yellow snake)
uart1 = UART(0, baudrate=9600, tx=Pin(4), rx=Pin(5)) #ID=0 for pico-W

is_blink = True
msg = 'Serial message from Pico-W PyCharm'
counter = 0

def blink_led(self):
    global is_blink, msg, counter
    if is_blink:
        led.off()
        is_blink = False
    else:
        led.on()
        is_blink = True
        uart1.write(f'{msg}: {counter}\r\n')
        counter = counter + 1



timer0.init(period=200, mode=Timer.PERIODIC, callback=blink_led)