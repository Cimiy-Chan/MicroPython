
from machine import Pin, Timer, UART

led = Pin(4, Pin.OUT)
timer_0 = Timer(0)
uart2 = UART(2)
uart2.init(baudrate = 9600, bits = 8, stop = 1, parity = None)

is_blink = False
msg = 'Message from ESP32 - PyCharm'
counter = 0

def led_blink (self): #Key word self MUST be used
    global msg, counter, is_blink
    if not is_blink:
        led.on()
        is_blink = True
    else:
        led.off()
        is_blink = False
    uart2.write(f'{msg} :{counter}\r\n')
    counter = counter + 1

timer_0.init(period=800, mode=Timer.PERIODIC, callback=led_blink) #Period in ms
