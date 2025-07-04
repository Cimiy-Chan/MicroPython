"""
For flashing the file into device, filename must be "main.py"
Other filename cannot be flashed into the Pico-W device.

Two UARTs at Pico-W
UART0 - GPIO 0/1, 12/13 and 16/17 (Internal use)
UART1 - GPIO 4/5, 8/9

Only one timer at RP2040
"""

from machine import Pin, Timer, UART

RGB_R = 17
RGB_G = 16
RGB_B = 25

led_r = Pin(RGB_R, Pin.OUT)
led_g = Pin(RGB_G, Pin.OUT)
led_b = Pin(RGB_B, Pin.OUT)
timer0 = Timer() #No need to specify the timer id (ignore yellow snake)
uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #Seed: Tx=0, Rx=1

is_blink = True
msg = 'Serial message from Seed Xiao'
counter = 0

led_r.on()
led_g.on()
led_b.on()

def blink_led(self):
    global is_blink, msg, counter
    if is_blink:
        led_g.off()
        is_blink = False
    else:
        led_g.on()
        is_blink = True
        uart1.write(f'{msg}: {counter}\r\n')
        counter = counter + 1



timer0.init(period=100, mode=Timer.PERIODIC, callback=blink_led)