#from machine import Pin, SoftI2C, RTC
from machine import Pin, I2C, RTC
from ds1307 import DS1307
import time


if __name__ == '__main__':
    is_set_clock: bool = False
    # full test code
    #i2c0 = SoftI2C(scl=Pin(15), sda=Pin(14), freq=100000)
    i2c0 = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)

    #Create object RTC of pico
    pico_rtc = RTC()

    iic_address = i2c0.scan()[0]
    ds1307rtc = DS1307(i2c0, iic_address)

    # set and read disable_oscillator property
    #ds1307rtc.disable_oscillator = True
    #print("disable_oscillator = ", ds1307rtc.disable_oscillator)
    #ds1307rtc.disable_oscillator = False
    #print("disable_oscillator = ", ds1307rtc.disable_oscillator,"\n")

    print(f'Current Date/Time')
    print(ds1307rtc.date_time_format(ds1307rtc.datetime))
    print()

    if is_set_clock:
        # set time (year, month, day, hours. minutes, seconds, weekday: integer: 0-6 )
        ds1307rtc.datetime = (2024, 6, 5, 15, 48, 0, 4, None)
        # read time
        dt = ds1307rtc.datetime
        print ('Set Date/Time')
        print (ds1307rtc.date_time_format(dt))
        print()
        pico_rtc.datetime(ds1307rtc.datetimeRTC)
        print(f'set pico clock')
        print(ds1307rtc.date_time_format(time.localtime()))
