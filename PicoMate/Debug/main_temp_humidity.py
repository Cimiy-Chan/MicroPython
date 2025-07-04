"""
DeskPi PicoMate has a temperature and humidity sensor (SHT30-DIS),
which is pre-wired to the Pico using I2C1 with the device address 0x44

Pin connection: SCL=Pin15, SDA=Pin14
"""

import time
from machine import Pin, I2C
import sht31d
import ssd1306

def display_text(str, line):
    display.text(str, 0, (line % 8) * 8, 1)

if __name__ == '__main__':

    bi_led = Pin ('LED', Pin.OUT)
    i2c_sht31d = I2C(1, scl=Pin(15), sda=Pin(14))
    i2cf_oled = I2C(0, scl=Pin(17), sda=Pin(16))
    sensor = sht31d.SHT31(i2c_sht31d, addr=0x44)
    display=ssd1306.SSD1306_I2C(128, 64, i2cf_oled)

    while True:
        bi_led.on()
        temperature, humidity = sensor.get_temp_humi()
        display.fill(0) #Blank to refresh
        display_text('SHT31D Demo', 0)
        display_text(f'Temp: {temperature}C', 2)
        display_text(f'Humi: {humidity}%',3)
        display.show()
        time.sleep(0.3)
        bi_led.off()
        time.sleep(0.2)
