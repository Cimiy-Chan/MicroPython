# I2C Scanner MicroPython
from machine import Pin, SoftI2C

def iic_scan():
    # You can choose any other combination of I2C pins
    i2c = SoftI2C(scl=Pin(1), sda=Pin(0))

    print('I2C SCANNER')
    devices = i2c.scan()

    if len(devices) == 0:
        print('No i2c device !')
    else:
        print(f'i2c devices found: {len(devices)}')

    for each_device in devices:
         print (f'I2C Hex address: {hex(each_device)}')

