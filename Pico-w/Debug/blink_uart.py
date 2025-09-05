"""
For flashing the file into device, filename must be "main.py"
Other filename cannot be flashed into the Pico-W device.

Two UARTs at Pico-W
UART0 - GPIO 0/1, 12/13 and 16/17 (Internal use)
UART1 - GPIO 4/5, 8/9

Only one timer at RP2040
"""

from machine import Pin, Timer, UART

user_led = Pin(9)
builtin_led = 'LED' #Built in LED at Pico Pi W

led = Pin(user_led, Pin.OUT)
timer0 = Timer() #No need to specify the timer id (ignore yellow snake)
#uart1 = UART(0, baudrate=9600, tx=Pin(4), rx=Pin(5)) #ID=1 for pico-W GPIO4=Tx, GPIO5=Rx
#uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)) #ID=1 for pico-W GPIO8=Tx, GPIO9=Rx
uart1 = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13)) #ID=0 for pico-W GPIO8=Tx, GPIO9=Rx

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



timer0.init(period=100, mode=Timer.PERIODIC, callback=blink_led)