
from machine import Pin, Timer

led = Pin(4, Pin.OUT)
timer_0 = Timer(0)

is_blink = False

def led_blink (self):
    global is_blink
    if not is_blink:
        led.on()
        is_blink = True
    else:
        led.off()
        is_blink = False

timer_0.init(period=150, mode=Timer.PERIODIC, callback=led_blink)








