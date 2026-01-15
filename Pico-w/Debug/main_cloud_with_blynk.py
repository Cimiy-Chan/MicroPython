"""
This is demo application for communicating the Pico RPI 2 W with Blynk 2.0 App
For detail setup, pls go to link: https://how2electronics.com/iot-led-control-using-blynk-2-0-raspberry-pi-pico-w/

Note that, with using the old BlynkLib.py, the MicroPython firmware version should be 1.22 or lower.

Hardware configuration:-
RPI Pico W
320 x 240 TFT display with SPI interface
4x4 Keypad
"""

import os
#import uos
from machine import Pin, UART, SPI, SoftI2C
import st7789lib as st7789
# from fonts import vga2_8x8 as font1 # Use at Debug folder
# from fonts import vga1_16x32 as font2 #Use at Debug folder
import vga1_8x16 as small_font
import vga1_16x16 as big_font
from time import sleep_ms
from keypad_4x4 import Keypad
import network
from BMP180 import BMP180
import BlynkLib # Should be used with MicroPython firmware version 1.22 or lower.


class FuncHardware:
    """
    Class containing functions of Serial Data Generator
    """
    def __init__(self, lcd_width, lcd_height, rotation, lcd_dc, lcd_rst):
        MAX_LINE_DISPLAY = 10
        spi1 = SPI(1, baudrate=40000000, polarity=1)
        self.display = st7789.ST7789(spi1, lcd_width, lcd_height,
                                reset=Pin(lcd_rst, Pin.OUT),
                                dc=Pin(lcd_dc, Pin.OUT),
                                xstart=0, ystart=0, rotation=rotation)
        self.uart1 = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13)) #ID=0 for pico-W GPIO8=Tx, GPIO9=Rx
        self.user_led = Pin(9)
        self.builtin_led = 'LED' #Build in LED at Pico Pi W
        self.led = Pin(self.user_led, Pin.OUT)
        self.led.off()
        self.bool_blink_toggle = True
        self.line_written = ['']* MAX_LINE_DISPLAY
        self.no_of_line_written = 0

        # Define GPIO pins for rows
        column_pins = [Pin(0), Pin(1), Pin(2), Pin(3)]

        # Define GPIO pins for columns
        row_pins = [Pin(4), Pin(5), Pin(6), Pin(7)]

        # Define keypad layout
        keys = [
            ['D', 'C', 'B', 'A'],
            ['#', '9', '6', '3'],
            ['0', '8', '5', '2'],
            ['*', '7', '4', '1']]

        self.keypad = Keypad(row_pins, column_pins, keys)

        i2c = SoftI2C(sda = Pin(20), scl = Pin(21)) # i2c for BMP180 sensor (temperature and pressure)
        self.bmp = BMP180(i2c)
        self.bmp.oversample = 2 # 0, 1, 2, 3 = ultra low power, standard, high, ultra-high resolution
        self.bmp.sealevel = 1019 # Need to be adjusted per location. In HKG, link: https://www.hko.gov.hk/en/wxinfo/ts/display_element_pp.htm

    def func_led_blink(self, bool_blink, blink_time_ms=100):
        """
        This is a simple code for testing the hardware healthiness.
        It will make use of internal timer for build-in LED blinking
        :param bool_blink: 0 = not blink, LED is on. 1 = blink with time blink_time_ms
        :param blink_time_ms: Blinking time
        :return: NIL
        """

    def blink_led(self, t): # t is dummy for timer callback use
        if self.bool_blink_toggle:
            self.led.off()
            self.bool_blink_toggle = False
        else:
            self.led.on()
            self.bool_blink_toggle = True

    def write_one_line(self, txt_msg, line_number, color = st7789.WHITE):
        """
        Write one line on display with fix small font one by one
        The line starts with line 1, line 2 for next one and so on.
        When it is written, it will overwrite the previous one.

        :param color:
        :param txt_msg: Text message input
        :param line_number: line no (1-10) that the line is located
        :return: True if a line has normally been written. False otherwise
        """

        if line_number <= 0 or line_number > 10:
            return False
        else:
            if len(self.line_written[line_number-1]) == 0: # If yes, no line is written on this line before
                self.line_written[line_number-1] = txt_msg
                self.display.text_line(small_font, txt_msg, line=line_number, color=color)
            else: # If yes, this line has been written before
                self.display.text_line(small_font, ' ' * len(self.line_written[line_number-1]), line=line_number)  # For erasing the message
                self.display.text_line(small_font, txt_msg, line=line_number, color=color)
            return True


    def main_menu(self, refresh_screen = False):
        """
        Show main menu at display
        Optional: if refresh_screen = True, it will refresh the whole screen but the time is slower
        :return: Nil
        """
        if refresh_screen:
            self.display.fill(st7789.BLACK)
        self.display.text_line(small_font, 'IoT Blynk Main Menu', color=st7789.color565(0,255,0))
        #self.display.text_line(small_font, '1. LED Blink', 2)
        #self.display.text_line(small_font, '2. LED ON/OFF', 3)
        #self.display.text_line(small_font, '*. System information', 4)

    def message_load (self, txt_message, delay_time):
        """
        Load message and display at time delay_time
        :param txt_message:
        :param delay_time:
        :return:
        """
        self.display.text_line(small_font, f'Message Loaded...', 9, color=st7789.RED)
        self.display.text_line(small_font, txt_message, 10, color=st7789.RED)
        sleep_ms(delay_time)
        self.display.text_line(small_font, ' ' * len(f'Message Loaded...'), 9) # For erasing the message
        self.display.text_line(small_font, ' ' * len(txt_message), 10)

# Main Program Entry
if __name__ == '__main__':

    st7789_dc =18
    st7789_res = 19
    LCD_WIDTH = 240
    LCD_HEIGHT = 320
    WIFI_SSID = 'ASUS_98'
    WIFI_PW = 'Ebenezer1e3'
    BLYNK_AUTH = 'yZxhY6QAXjsGmzXETdmP0SIXb4O1IaWc'

    obj_hw = FuncHardware(LCD_WIDTH, LCD_HEIGHT, rotation=2, lcd_rst=st7789_res, lcd_dc=st7789_dc)
    # rotation: 0-Portrait, 1-Landscape, 2-Inverted Portrait, 3-Inverted Landscape
    obj_hw.main_menu()
    obj_hw.led.on()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PW)
    counter = 0
    # Connect network
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        obj_hw.write_one_line('Waiting for connection...', 2, color=st7789.YELLOW)
        #print('waiting for connection...')
        sleep_ms(1000)

    # Handle connection error
    if wlan.status() != 3:
        obj_hw.write_one_line('Network connection failed', 2, color=st7789.RED)
        raise RuntimeError('network connection failed')

    else:
        obj_hw.write_one_line(' ',2)
        obj_hw.write_one_line('Connected...', 3, color=st7789.GREEN)
        ip = wlan.ifconfig()[0]
        obj_hw.write_one_line(f'IP: {ip}', 4, color=st7789.GREEN)

    #"Connection to Blynk"
    # Initialize Blynk
    blynk = BlynkLib.Blynk(BLYNK_AUTH)

    # Register virtual pin handler
    @blynk.on("V0")  # virtual pin V0
    def v0_write_handler(value):  # read the value
        if int(value[0]) == 1:
            obj_hw.led.on()  # turn the led on
            obj_hw.write_one_line(f'LED ON....', 10, color=st7789.GREEN)
        else:
            obj_hw.led.off()  # turn the led off
            obj_hw.write_one_line(f'LED OFF...', 10, color=st7789.GREEN)


    while True:
        temp_c = obj_hw.bmp.temperature
        pres_hPa = obj_hw.bmp.pressure
        #alt_m = round(obj_hw.bmp.altitude, 2)
        alt_m = 48.2

        obj_hw.write_one_line(f'Temperature: {temp_c}C', line_number=6)
        obj_hw.write_one_line(f'Pressure: {pres_hPa}hPa', line_number=7)
        obj_hw.write_one_line(f'Altitude: {alt_m}:.2dm', line_number=8)
        #obj_hw.write_one_line(f'Counter: {counter}', 8)
        counter += 1
        sleep_ms(1000)

        # Run blynk
        blynk.run()



    '''
    st7789_dc =18
    st7789_res = 19
    LCD_WIDTH = 240
    LCD_HEIGHT = 320
    count = 0
    bool_timer_enable_toggle = False
    bool_led_on_off_toggle = False
    serial_message_1 = 'This is test\r\n'
    # The CS pin should hard-wire to GND
    obj_hw = FuncHardware(LCD_WIDTH, LCD_HEIGHT, rotation=2, lcd_rst=st7789_res, lcd_dc=st7789_dc)
    # rotation: 0-Portrait, 1-Landscape, 2-Inverted Portrait, 3-Inverted Landscape

    obj_hw.main_menu()

    serial_message = serial_message_1
    text_message = f'Message:{serial_message_1}'
    timer0 = Timer()  # No need to specify the timer id (ignore yellow snake)

    while True:
        key_pad_val = obj_hw.keypad.read_keypad_char()
        if key_pad_val == '1' and bool_timer_enable_toggle == False:
            timer0.init(period=100, mode=Timer.PERIODIC, callback=obj_hw.blink_led)
            bool_timer_enable_toggle = True
            obj_hw.message_load('LED Blink', 1000)
        elif key_pad_val == '1' and bool_timer_enable_toggle == True:
            timer0.deinit()
            bool_timer_enable_toggle = False
            obj_hw.led.off()
            obj_hw.message_load('LED off', 1000)

        if key_pad_val == '2' and bool_led_on_off_toggle == False:
            bool_timer_enable_toggle = False
            timer0.deinit()
            obj_hw.led.on()
            bool_led_on_off_toggle = True
        elif key_pad_val == '2' and bool_led_on_off_toggle == True:
            bool_timer_enable_toggle = False
            timer0.deinit()
            obj_hw.led.off()
            bool_led_on_off_toggle = False

        # Display system information
        if key_pad_val == '*':
            obj_hw.display.fill(st7789.BLACK)
            obj_hw.display.text_line(small_font, f'System: {os.uname()[0]}', 1)
            obj_hw.display.text_line(small_font, f'MicroPython Ver: {os.uname()[2]}', 2)
            obj_hw.display.text_line(small_font, f'Machine: {os.uname()[4][:17] + '...'}', 3)
            obj_hw.display.text_line(small_font, f'{os.uname()[4][18:]}', 4)
            obj_hw.display.text_line(small_font, 'Written by: Cimiy Chan', 6, st7789.GREEN)
            obj_hw.display.text_line(small_font, 'Version 1.0', 7, st7789.GREEN)
            obj_hw.display.text_line(small_font, 'Press # to Main Menu...', 9, st7789.GREEN)
            while obj_hw.keypad.read_keypad_char() != '#': #Form a dead-loop until key # is pressed
                pass
            obj_hw.main_menu(refresh_screen=True)
        '''