"""
DeskPi PicoMate has a Digital Optical Sensor (LTR-381RGB-01) that integrates
an ambient light sensor (ALS) and a color sensor (CS). With the advanced RGB
color sensor, this sensor converts light (Red, Green, Blue, and IR) intensity
to a digital output signal capable of direct I2C interface. The ALS provides a
linear response over a wide dynamic range, which is well suited to applications
under very low or bright ambient brightness.

Pin connection: SCL=Pin15, SDA=Pin14
"""

import time
from ltr381rgb import LTR381RGB
from machine import Pin, I2C
from neopixel import Neopixel


if __name__ == '__main__':
    DATA_PIN = 22
    rgb_led = Neopixel(1, 0, DATA_PIN, 'RGB')
    rgb_led.brightness(50)
    bi_led = Pin('LED', Pin.OUT)
    i2c = I2C(1, sda=14, scl=15)
    optical_cs = LTR381RGB(i2c)
    optical_cs.ltr381rgb_init()

    """
    #Debug use
    part_id = int(optical_cs.ltr381rgb_part_id()[0])
    print(f'PART ID: {part_id}')
    main_status = optical_cs.ltr381rgb_main_status()
    print(f'Main Status: {main_status}')
    """

    while True:
        bi_led.on()
        ir, r, g, b = optical_cs.ltr381rgb_raw_data()
        if r >= 255:
            r = 255
        if g >= 255:
            g = 255
        if b >= 255:
            b = 255
        rgb_led.set_pixel(0, (r,g,b))
        rgb_led.show()
        time.sleep(0.3)
        bi_led.off()
        rgb_led.clear()
        rgb_led.show()
        time.sleep(0.2)
