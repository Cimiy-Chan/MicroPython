"""
DeskPi PicoMate has a 6-axis IMU sensor (LSM6DS3TR-C) featuring a 3D digital
accelerometer and a 3D digital gyroscope.
The sensor is pre-wired to the Pico using I2C1 with the device address 0x6A.

Pin connection: SCL=Pin15, SDA=Pin14
"""

from machine import I2C, Pin
from lsm6ds3 import LSM6DS3, NORMAL_MODE_104HZ
import ssd1306
import time

OLED_sda = 16
OLED_scl = 17
IMU_sda = 14
IMU_scl = 15

def display_text(str, line):
    display.text(str, 0, (line % 8) * 8, 1)

if __name__ == '__main__':

    # Create the I2C instance and pass that to LSM6DS3 and OLED
    i2c_imu = I2C(1, scl=Pin(IMU_scl), sda=Pin(IMU_sda)) #ID=1 for I2C1.
    sensor = LSM6DS3(i2c_imu, mode=NORMAL_MODE_104HZ)

    i2c_oled = I2C(0, sda=Pin(OLED_sda), scl=Pin(OLED_scl), freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c_oled)
    bi_led = Pin('LED', Pin.OUT)

    buildin_led = Pin('LED', Pin.OUT)

    # Grab and print the current readings once per second
    while True:
        display.fill(0)
        display_text('IMU Demo...', 0)
        ax, ay, az, gx, gy, gz = sensor.get_readings()
        display_text (f'Acce: X:{ax}', 2)
        display_text (f'      Y:{ay}', 3)
        display_text (f'      Z:{az}', 4)
        display_text (f'Gyro: X:{gx}', 5)
        display_text (f'      Y:{gy}', 6)
        display_text (f'      Z:{gz}', 7)
        display.show()
        buildin_led.on()
        time.sleep(0.2)
        buildin_led.off()
        time.sleep(0.8)