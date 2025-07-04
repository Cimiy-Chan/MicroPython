# I2C Scanner MicroPython
from machine import Pin, SoftI2C

def iic_scan():
    # You can choose any other combination of I2C pins
    i2c = SoftI2C(scl=Pin(7), sda=Pin(6)) #Seed:SCL=GPIO7, SDA=GPIO6

    print('I2C SCANNER')
    devices = i2c.scan()

    if len(devices) == 0:
        print('No i2c device !')
    else:
        print(f'i2c devices found: {len(devices)}')

    for each_device in devices:
         print (f'I2C Hex address: {hex(each_device)}')

#Run program here
if __name__ == '__main__':
    iic_scan()