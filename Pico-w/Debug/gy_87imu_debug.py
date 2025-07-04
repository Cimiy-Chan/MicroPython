# I2C Scanner MicroPython
import time
#from machine import Pin, SoftI2C, I2C
from machine import Pin, I2C, SoftI2C

def iic_scan():
    # You can choose any other combination of I2C pins
    i2c = SoftI2C(scl=Pin(1), sda=Pin(0))
    #i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)

    print ('Unlock the HMC5883L IIC address')
    #i2c.writeto_mem(0x68, 0x6A, b'/x00') #0x6A = dec 106
    #time.sleep(0.5)

    buf = bytearray(2)
    buf[0]=0x37
    buf[1]=0xff
    no_of_ack = i2c.writeto(0x68, buf)
    print (f'No. of ack = {no_of_ack}')


    i2c.writeto_mem(0x68, 0x68, b'/xff')
    time.sleep(1)



    who_am_i = i2c.readfrom_mem(0x68, 0x75, 1)
    print (f'Read reg 0x75, Who am i = 0x{who_am_i.hex()}')
    reg_0x37 = i2c.readfrom_mem(0x68, 0x37, 1)
    print (f'read reg 0x37, content = 0x{reg_0x37.hex()}')
    reg_0x6A = i2c.readfrom_mem(0x68, 0x6A, 1)
    print(f'read reg 0x6A, content = 0x{reg_0x6A.hex()}')
    #reg_qmc5883_id = i2c.readfrom_mem(QMC5883L_ADR, 0x0D, 1)
    #print(f'read reg_qmc5883l, content = 0x{reg_qmc5883_id.hex()}')
    reg_0x68 = i2c.readfrom_mem(0x68, 0x68, 1)
    print(f'read reg 0x68, content = 0x{reg_0x68.hex()}')

    print('I2C SCANNER')
    devices = i2c.scan()

    if len(devices) == 0:
        print('No i2c device !')
    else:
        print(f'i2c devices found: {len(devices)}')

    for each_device in devices:
        print(f'I2C Hex address: {hex(each_device)}')

if __name__ == '__main__':
    iic_scan()