'''
Demo program for Seeed Xiao RP2040 + Seded Xiao Expansion board (RTC)
It is embedded at Seed Xiao Expansion board with the following hardware
#
#
Seeed Xiao Board RP2040
1. USER_LED: R(GPIO17), G(GPIO16), B(GPIO25). Active low: led.off() #LED light on
2. RGB KED (DIN=GPIO12, VCC=NEO_PWR=GPIO11)
#
#
Expansion board
1. RTC PCF8563 (0x51, SCL=GPIO7, SDA=GPIO6)
2. OLED 0.96" display (0x3C, SCL=GPIO7, SDA=GPIO6)
3. Buzzer: (GPIO29)
4. User button: (GPIO27)
5. UART: ID=1, Tx=0, Rx=1
'''

import pcf8563
from machine import Pin, I2C
import time
day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

if __name__ == '__main__':
    RTC_sda = 6
    RTC_scl = 7
    i2c = I2C(1, sda=Pin(RTC_sda), scl=Pin(RTC_scl)) #ID=1 for Seed
    rtc = pcf8563.PCF8563(i2c) #Instiate rtc object

    #Check critical time boundary at Date: 2024/12/31 Time:23/59/50 after 10 seconds
    rtc.set_datetime((24, 12, 31, 23, 59, 50, 6)) #Format: (Year, Month, Date, Hour, Min, Sec, Day)
    while True:
        datetime_value = rtc.datetime()
        print (f'Date: {datetime_value[0]+2000:04d}/{datetime_value[1]:02d}/{datetime_value[2]:02d}  '
               f'Time: {datetime_value[3]:02d}:{datetime_value[4]:02d}:{datetime_value[5]:02d} {day[datetime_value[6]]}')
        time.sleep(1)
