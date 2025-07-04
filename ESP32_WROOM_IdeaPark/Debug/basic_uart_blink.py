
from machine import Pin, Timer, UART

led = Pin(2, Pin.OUT)
timer_0 = Timer(0)
uart2 = UART(2)
uart2.init(baudrate = 9600, bits = 8, stop = 1, parity = None)

is_blink = False
msg = 'Message from ESP32 - PyCharm'
counter = 0
timer_period = 500

def led_blink (self): #Key word self MUST be used
    global msg, counter, is_blink, timer_period
    if not is_blink:
        led.on()
        is_blink = True
    else:
        led.off()
        is_blink = False
    uart2.write(f'{msg} :{counter}\r\n')
    if counter == 10:
        timer_0.init(period=-1)
    else:
        counter = counter + 1

timer_0.init(period=timer_period, mode=Timer.PERIODIC, callback=led_blink) #Period in ms, if period = -1 --> timer disable
