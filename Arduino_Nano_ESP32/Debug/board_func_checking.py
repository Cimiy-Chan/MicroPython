"""
Demo program for checking the board hardware
Board: Arduino Nano ESP32
Notes:
    1. MicroPython doesn't support Pin.toggle() function
    2. Use serial0 (i.e. UART(0)) for external UART port access
    3. This will be use with OLED display with driver SSD1306 with IIC at pin11-SDA and pin12-SCL
"""

from machine import Pin, UART, SoftI2C
import time,os, ssd1306


class BoardFunc:
    def __init__ (self, width, height):
        #LED port definition
        LED_BUILDIN = 48
        LEDR = 46 # Inverted signal for RGB-LED
        LEDG = 0
        LEDB = 45

        self.led_builtin = Pin(LED_BUILDIN, Pin.OUT)
        self.ledr = Pin(LEDR, Pin.OUT)
        self.ledg = Pin(LEDG, Pin.OUT)
        self.ledb = Pin(LEDB, Pin.OUT)

        #Init led states
        self.led_builtin.off()
        self.ledr.on() # Inverted stat
        self.ledg.on()
        self.ledb.on()

        #Init UART
        self.uart = UART(0) # Use serial0 for Arduino Nano ESP32 for external access
        self.uart.init(baudrate=9600, bits=8, stop=1, parity=None)

        #get board information
        self.machine_info = os.uname()

        self.width = width
        self.height = height
        self.i2c = SoftI2C(sda=Pin(11), scl=Pin(12))
        self.display = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)

    def led_blink(self, blink_time):
        #Build in LED
        self.led_builtin.on()
        time.sleep(blink_time)
        self.led_builtin.off()
        time.sleep(blink_time)
        # Red LED
        self.ledr.off()
        time.sleep(blink_time)
        self.ledr.on()
        time.sleep(blink_time)
        #Green LED
        self.ledg.off()
        time.sleep(blink_time)
        self.ledg.on()
        time.sleep(blink_time)
        #Blue LED
        self.ledb.off()
        time.sleep(blink_time)
        self.ledb.on()
        time.sleep(blink_time)

    def display_msg (self, msg):
        print (msg) # Display message at REPL console
        self.uart.write(f'{msg}\r\n')

    def display_oled_text(self, msg):
        self.display.fill(0)
        self.display.text (msg, 0,0)
        self.display.show()

#Main entry point
if __name__ == '__main__':
    obj_board_func = BoardFunc(128, 64)
    no_of_trial = 1
    while no_of_trial !=0:
        obj_board_func.led_blink(0.1)
        obj_board_func.display_msg(f'Machine: {obj_board_func.machine_info[4]}')
        obj_board_func.display_msg(f'MicroPython ver: {obj_board_func.machine_info[3]}')
        obj_board_func.display_oled_text('OLED display')
        no_of_trial = no_of_trial - 1
