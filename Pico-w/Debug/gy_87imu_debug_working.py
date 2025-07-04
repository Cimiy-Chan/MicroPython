# I2C Scanner MicroPython
import time
from machine import Pin, I2C

def iic_scan():
    # You can choose any other combination of I2C pins
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)

    # Unlock the HMC5883L IIC address
    buf = bytearray(2)
    buf[0]=2
    i2c.writeto_mem(0x68, 0x37, buf)
    buf[0]=0
    i2c.writeto_mem(0x68, 0x6A, buf)

    #I2C Scanner
    devices = i2c.scan()

    if len(devices) == 0:
        print('No i2c device !')
    else:
        print(f'i2c devices found: {len(devices)}')

    for each_device in devices:
        print(f'I2C Hex address: {hex(each_device)}')

if __name__ == '__main__':
    iic_scan()