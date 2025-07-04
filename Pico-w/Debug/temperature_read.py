"""
For flashing the file into device, filename must be "main.py"
Other filename cannot be flashed into the Pico-W device.

Get the temperature value from built in temperature sensor
"""

from machine import Pin, ADC, UART,Timer

led = Pin("LED", Pin.OUT)
timer0 = Timer() #No need to specify the timer id (ignore yellow snake)
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
adcpin = 4
sensor = ADC(adcpin)

is_blink = True
counter = 0

def blink_led(self):
    global is_blink, msg, counter
    if is_blink:
        led.off()
        is_blink = False
    else:
        led.on()
        is_blink = True
        adc_value = sensor.read_u16()
        volt = (3.3/65535) * adc_value
        temperature = 27 - (volt - 0.706) / 0.001721
        uart1.write(f'Temperature: {round(temperature,2)}\r\n')
        counter = counter + 1

timer0.init(period=2500, mode=Timer.PERIODIC, callback=blink_led)