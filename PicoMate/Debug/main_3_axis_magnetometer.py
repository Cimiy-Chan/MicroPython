"""
DeskPi PicoMate has a 3-Axis Magnetometer (MMC5603NJ) that can measure magnetic fields surrounding
the device. The sensor is pre-wired to the Pico using I2C1 with the device address 0x30.

Pin connection: SCL=Pin15, SDA=Pin14 with I2C1-> id=1
"""

"""
DeskPi PicoMate has a 6-axis IMU sensor (LSM6DS3TR-C) featuring a 3D digital
accelerometer and a 3D digital gyroscope.
The sensor is pre-wired to the Pico using I2C1 with the device address 0x6A.

Pin connection: SCL=Pin15, SDA=Pin14
"""

from machine import I2C, Pin
from mmc5603 import MMC5603
import ssd1306
import time

OLED_sda = 16
OLED_scl = 17
MMC_sda = 14
MMC_scl = 15

def display_text(str, line):
    display.text(str, 0, (line % 8) * 8, 1)

if __name__ == '__main__':

    # Create the I2C instance and pass that to LSM6DS3 and OLED
    i2c_mmc = I2C(1, scl=Pin(MMC_scl), sda=Pin(MMC_sda)) #ID=1 for I2C1.
    mmc = MMC5603(i2c_mmc)
    mmc.data_rate = 10  # in Hz, from 1-255 or 1000
    mmc.continuous_mode = True


    i2c_oled = I2C(0, sda=Pin(OLED_sda), scl=Pin(OLED_scl), freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c_oled)
    bi_led = Pin('LED', Pin.OUT)

    buildin_led = Pin('LED', Pin.OUT)

    # Grab and print the current readings once per second
    while True:
        display.fill(0)
        display_text('MMC Demo...', 0)
        mag_x, mag_y, mag_z = mmc.magnetic

        #Display up to integer
        display_text(f"Mag: X:{mag_x} uT", 2)
        display_text(f"Mag: Y:{mag_y} uT", 3)
        display_text(f"Mag: Z:{mag_z} uT", 4)
        display.show()
        buildin_led.on()
        time.sleep(0.2)
        buildin_led.off()
        time.sleep(0.3)



