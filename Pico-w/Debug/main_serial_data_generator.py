"""
Controller unit for serial data generator (SDG)

Hardware configuration:
4x4 Keypad: GP0-GP7
320 x 240 TFT display:-
    SCK = GPIO10
    MISO = GPIO8
    MOSI = GPIO11
    DC = GPIO18
    RST = GPIO19
UART serial port:-
    TX = GP12
    RX = GP13
"""
import os
#import uos
from machine import Pin, UART, SPI
import st7789lib as st7789
# from fonts import vga2_8x8 as font1 # Use at Debug folder
# from fonts import vga1_16x32 as font2 #Use at Debug folder
import vga1_8x16 as small_font
import vga1_16x16 as big_font
from time import sleep_ms
from keypad_4x4 import Keypad


class FuncSerialDataGen:
    """
    Class containing functions of Serial Data Generator
    """
    def __init__(self, lcd_width, lcd_height, rotation, lcd_dc, lcd_rst):
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

    def main_menu(self, refresh_screen = False):
        """
        Show main menu at display
        Optional: if refresh_screen = True, it will refresh the whole screen but the time is slower
        :return: Nil
        """
        if refresh_screen:
            self.display.fill(st7789.BLACK)
        self.display.text_line(big_font, 'SDG Main Menu', color=st7789.color565(0,255,0))
        self.display.text_line(small_font, '1. Single shot', 2)
        self.display.text_line(small_font, '2. Continue shot', 3)
        self.display.text_line(small_font, '4. Serial data - 1 (Default)', 4)
        self.display.text_line(small_font, '5. Serial data - 2', 5)
        self.display.text_line(small_font, '6. Serial data - 3', 6)
        self.display.text_line(small_font, '*. System information', 7)

    def serial_send_str (self, string_message: str):
        """
        Send a serial text message to UART. During sending also LED is flash
        :param string_message:
        :return:
        """
        self.uart1.write(string_message)
        self.led.on()
        sleep_ms(100)
        self.led.off()

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
        self.display.text_line(small_font, ' ' * len(f'Message Loaded...'), 9)
        self.display.text_line(small_font, ' ' * len(txt_message), 10)

# Main Program Entry
if __name__ == '__main__':
    st7789_dc =18
    st7789_res = 19
    LCD_WIDTH = 240
    LCD_HEIGHT = 320
    count = 0
    is_serialized = False
    serial_message_1 = 'This is test\r\n'
    serial_message_2 = 'Item,1,2,4.5\r\n'
    serial_message_3 = f'Item,2.3,4,Unit\r\n'
    # The CS pin should hard-wire to GND
    obj_sdg = FuncSerialDataGen(LCD_WIDTH, LCD_HEIGHT, rotation=2, lcd_rst=st7789_res, lcd_dc=st7789_dc)
    # rotation: 0-Portrait, 1-Landscape, 2-Inverted Portrait, 3-Inverted Landscape

    obj_sdg.main_menu()

    serial_message = serial_message_1
    text_message = f'Message:{serial_message_1}'

    while True:
        key_pad_val = obj_sdg.keypad.read_keypad_char()
        if key_pad_val == '1':
            if is_serialized:
                msg_send = f'Line:{count},{serial_message}'
            else:
                msg_send = serial_message
            obj_sdg.display.text_line(small_font, 'Single shoot...', 9, color=st7789.color565(255,0,0))
            obj_sdg.display.text_line(small_font, text_message, 10)
            obj_sdg.serial_send_str(msg_send)
            sleep_ms(100)
            #Blank the lines
            obj_sdg.display.text_line(small_font, ' ' * len('Single shoot...'), 9)
            obj_sdg.display.text_line(small_font, ' ' * len(text_message), 10)
            if is_serialized: count +=1

        if key_pad_val == '2':
            obj_sdg.display.text_line(small_font, 'Continuous shot', 9, color=st7789.color565(255,0,0))
            obj_sdg.display.text_line(small_font, text_message, 10)
            obj_sdg.display.text_line(small_font, 'Press # to stop', 12)
            while obj_sdg.keypad.read_keypad() !='#':
                if is_serialized:
                    msg_send = f'Line:{count},{serial_message}'
                else:
                    msg_send = serial_message
                obj_sdg.serial_send_str(msg_send)
                if is_serialized: count += 1
                sleep_ms(100)
            #Blank the lines
            obj_sdg.display.text_line(small_font, ' ' * len('Continuous shot'), 9)
            obj_sdg.display.text_line(small_font, ' ' * len(text_message), 10)
            obj_sdg.display.text_line(small_font, ' ' * len('Press # to stop'), 12)


        if key_pad_val == '4':
            serial_message = serial_message_1
            text_message = f'Message:{serial_message_1}'
            obj_sdg.message_load(text_message, 500)
            is_serialized = False

        if key_pad_val == '5':
            serial_message = serial_message_2
            text_message = f'Message:{serial_message_2}'
            obj_sdg.message_load(text_message, 500)
            is_serialized = False

        if key_pad_val == '6':
            serial_message = serial_message_3
            text_message = f'Message:{serial_message_3}'
            obj_sdg.message_load(text_message, 500)
            is_serialized = True


        if key_pad_val == '*':
            obj_sdg.display.fill(st7789.BLACK)
            obj_sdg.display.text_line(small_font, f'System: {os.uname()[0]}', 1)
            obj_sdg.display.text_line(small_font, f'MicroPython Ver: {os.uname()[2]}', 2)
            obj_sdg.display.text_line(small_font, f'Machine: {os.uname()[4][:17] + '...'}', 3)
            obj_sdg.display.text_line(small_font, f'{os.uname()[4][18:]}', 4)
            obj_sdg.display.text_line(small_font, 'Written by: Cimiy Chan', 6, st7789.GREEN)
            obj_sdg.display.text_line(small_font, 'Version 1.0', 7, st7789.GREEN)
            obj_sdg.display.text_line(small_font, 'Press # to Main Menu...', 9, st7789.GREEN)
            while obj_sdg.keypad.read_keypad_char() != '#': #Form a dead-loop until key # is pressed
                pass
            obj_sdg.main_menu(refresh_screen=True)
