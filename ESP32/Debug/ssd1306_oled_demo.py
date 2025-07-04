"""
Demo application for OLED display board used with ESP32 system
Pin configuration of OLED
SCL = GPIO22
SDA = GPIO21
Buildin LED = GPIO2 for Ideaspark ESP32 board with OLED + Buildin LED

This OLED is dividing the color into two parts
1. Yellow color at height=0 to 15
2. Blue color at height=16 to 63

Note that the text cell is occupying 8x8 pixel and there is no way to change the text size.
"""

from machine import Pin,I2C, UART
import time
import ssd1306

class OLED_Demo:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.i2c=I2C(sda=Pin(21), scl=Pin(22))
        self.display = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
        self.led = Pin(2, Pin.OUT)
        self.led.off()
        self.uart2 = UART(2)
        self.uart2.init(baudrate = 9600, bits = 8, stop = 1, parity = None)


    def pixel_running(self):

        for pixel_width_pos in range(0, 50):
            self.display.pixel(pixel_width_pos, 0, 1)
            self.display.show()
            #time.sleep_ms(50)
            self.display.pixel(pixel_width_pos,0,0)
            self.display.show()

    #Draw micropython logo
    def mp_log(self, y_offset):
        self.display.fill(0)
        # Text display at yellow area (y=0 to 15)
        self.display.text('MP logo show',0,0)
        self.display.text('By Cimiy Chan', 0, 8)
        # MicroPython logo show at blue area (y=16 to 63)
        self.display.fill_rect(0, 0 + y_offset, 32, 32, 1)
        self.display.fill_rect(2, 2 + y_offset, 28, 28, 0)
        self.display.vline(9, 8 + y_offset, 22, 1)
        self.display.vline(16, 2 + y_offset, 22, 1)
        self.display.vline(23, 8 + y_offset, 22, 1)
        self.display.fill_rect(26, 24 + y_offset, 2, 4, 1)
        self.display.text('MicroPython', 40, 0 + y_offset, 1)
        self.display.text('SSD1306', 40, 12 + y_offset, 1)
        self.display.text('OLED 128x64', 40, 24 + y_offset, 1)
        self.display.show()

    def led_blink(self):
        self.led.on()
        time.sleep_ms(300)
        self.led.off()
        time.sleep_ms(300)

    def uart_write(self, msg):
        self.uart2.write(f'{msg}\r\n')




#Main entry point
if __name__ == '__main__':
    obj_oled_demo = OLED_Demo(128, 64)
    #obj_oled_demo.pixel_running()
    obj_oled_demo.uart_write('Demo to show MicroPython Logo')
    obj_oled_demo.mp_log(16)
    for dummy in range(0,2):
        obj_oled_demo.led_blink()
