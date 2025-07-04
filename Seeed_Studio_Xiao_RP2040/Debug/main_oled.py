"""
DeskPi PicoMate has a 0.96" 128x64 OLED display module, which is pre-wired to the Pico using
I2C0 with the device address 0x3C
"""
import time
from micropython import const
import ssd1306
from machine import Pin, I2C


def display_text(str, line):
    display.text(str, 0, (line % 8) * 8, 1)

if __name__ == '__main__':
    OLED_sda = 6 #Seed
    OLED_scl = 7 #Seed
    i2c = I2C(1, sda=Pin(OLED_sda), scl=Pin(OLED_scl), freq=400000) #ID=1 for Seeed
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    bi_led=Pin('LED', Pin.OUT) #Seed: 'LED' = Blue LED
    counter: int = 0

    while True:
        bi_led.on()
        display.fill(0)
        display_text('OLED Demo', 0)
        display_text('Seed Xiao', 2)
        display_text(f'Counter={counter}', 4)

        display.show()
        counter += 1
        time.sleep(0.3)
        bi_led.off()
        time.sleep(0.2)

