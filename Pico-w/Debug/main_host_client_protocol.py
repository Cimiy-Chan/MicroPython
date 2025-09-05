"""
Basic of host (PC) and client (IoT) protocol.
This is proprietary protocol.

This is built in the hardware of
Controller unit for serial data generator (SDG)

The setup file is defined at JSON file dev_config.json

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

import time
from machine import Pin, UART, SPI
import st7789lib as st7789
# from fonts import vga2_8x8 as font1 # Use at Debug folder
# from fonts import vga1_16x32 as font2 #Use at Debug folder
import vga1_8x16 as small_font
import vga1_16x16 as big_font
from time import sleep_ms
import json

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
        self.uart1 = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))  # ID=0 for pico-W GPIO8=Tx, GPIO9=Rx
        self.user_led = Pin(9)
        self.builtin_led = 'LED'  # Build in LED at Pico Pi W
        self.led = Pin(self.user_led, Pin.OUT)
        self.led.off()
        self.msg_cr_request = ''  # Message request from host (Connection request)
        self.msg_dcr_request = ''  # Message request from host (Disconnect request)
        self.msg_ack = ''  # Message for ack to host

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

    def load_config(self) -> tuple:
        """
        Load json file which is located at the same directory of main.py file
        :return:
        """
        # Load configuration
        try:
            with open('dev_config.json', 'r') as file:
                data = json.load(file)

            self.msg_ack = f'ACK_{data['Machine_name']}'.upper()
            self.msg_cr_request = f'CR_{data['Host_name']}'.upper()
            self.msg_dcr_request = f'DCR_{data['Host_name']}'.upper()
            return True, "JSON file load successfully"

        except Exception as e:
            return False, f"Error: {e}"

        """
        except FileNotFoundError:
            return False, "FileNotFoundError"
        except json.JSONDecodeError:
            return False, "JSONDecodeError"

        except Exception as e:
            #return False, f"AnUnexpectedError: {e}"
            return False, f"AnUnexpectedError"
        """

    def main_menu(self, refresh_screen=False):
        """
        Show main menu at display
        Optional: if refresh_screen = True, it will refresh the whole screen but the time is slower
        :return: Nil
        """
        if refresh_screen:
            self.display.fill(st7789.BLACK)
        self.display.text_line(big_font, 'SDG Main Menu', color=st7789.color565(0, 255, 0))
        self.display.text_line(small_font, '1. Single shot', 2)
        self.display.text_line(small_font, '2. Continue shot', 3)
        self.display.text_line(small_font, '4. Serial data - 1 (Default)', 4)
        self.display.text_line(small_font, '5. Serial data - 2', 5)
        self.display.text_line(small_font, '6. Serial data - 3', 6)
        self.display.text_line(small_font, '*. System information', 7)

    def serial_send_str(self, string_message: str, is_led_flash=False):
        """
        Send a serial text message to UART. During sending also LED is flash
        :param string_message:
        :param is_led_flash: True for debugging use
        :return:
        """
        self.uart1.write(string_message)
        if is_led_flash:
            self.led.on()
            sleep_ms(100)
            self.led.off()

    def serial_read_str(self, max_no_bytes_read):
        """
        Read a serial string from UART
        :return:
        """
        str_read = None
        while str_read == None:
            str_read = self.uart1.read(50)
            # time.sleep_ms(100)
        return str_read

    def line_clear_small_font(self, line=1):
        """
        Clear a line at TFT display with small font size
        :param line:
        :return:
        """
        self.display.text_line(small_font, 50 * ' ', line=line)

    def line_clear_big_font(self, line=1):
        """
        Clear a line at TFT display with big font size
        :param line:
        :return:
        """
        self.display.text_line(big_font, 50 * ' ', line=line)

    def message_load(self, txt_message, delay_time):
        """
        Load message and display
        :param txt_message:
        :param delay_time:
        :return:
        """
        self.display.text_line(small_font, f'Message Loaded...', 9, color=st7789.RED)
        self.display.text_line(small_font, txt_message, 10, color=st7789.RED)
        sleep_ms(delay_time)
        self.display.text_line(small_font, ' ' * len(f'Message Loaded...'), 9)
        self.display.text_line(small_font, ' ' * len(txt_message), 10)

    def wait_for_connection_request(self, wait_before_ack=100) -> tuple:
        """
        Routine for waiting request message from host
        :param wait_before_ack: Wait time before ack (ms)
        :return: True = connection request received and ACK is sent. False: Wrong/garble msg received.
        """

        read_from_uart = str(obj_sdg.serial_read_str(50), 'utf-8')
        if read_from_uart == obj_sdg.msg_cr_request:  # Check if connection request invoked
            time.sleep_ms(wait_before_ack)
            obj_sdg.serial_send_str(obj_sdg.msg_ack)  # Send back ack message to host
            return True, 'Request confirm and ack'
        else:
            return False, 'Request failure'

        # key_pad_val = obj_sdg.keypad.read_keypad_char()
        # print (key_pad_val)
        # time.sleep(1)


# Main Program Entry
if __name__ == '__main__':
    st7789_dc = 18
    st7789_res = 19
    LCD_WIDTH = 240
    LCD_HEIGHT = 320
    count = 0
    # The CS pin should hard-wire to GND
    obj_sdg = FuncSerialDataGen(LCD_WIDTH, LCD_HEIGHT, rotation=2, lcd_rst=st7789_res, lcd_dc=st7789_dc)
    # rotation: 0-Portrait, 1-Landscape, 2-Inverted Portrait, 3-Inverted Landscape

    obj_sdg.display.fill(st7789.BLACK)
    load_json_status = obj_sdg.load_config()
    wait_status = (False, '')

    if load_json_status[0]:
        # print (obj_sdg.msg_ack)
        # print (obj_sdg.msg_cr_request)
        # print (obj_sdg.msg_dcr_request)

        while True:
            obj_sdg.display.text_line(small_font, 'Wait for REQ..........', line=1)
            wait_status = obj_sdg.wait_for_connection_request()
            print(wait_status)
            if wait_status[0]:
                print(wait_status[1])
            else:
                print(wait_status[1])
                break


    else:
        obj_sdg.line_clear_small_font(3)
        obj_sdg.display.text_line(small_font, load_json_status[1], line=3, color=st7789.RED)
        time.sleep(5)
        # obj_sdg.display.text_line(small_font, 50 * ' ', line=3)
        obj_sdg.display.text_line(small_font, 'Please check JSON file', line=5, color=st7789.RED)






