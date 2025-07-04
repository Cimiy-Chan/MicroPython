"""
Demo application for Ideaspark Board which includes WiFi, OLED and LED (blue) indicator.

This application is the demonstration of WiFi scan, display SSID message on OLED, display more detail
message at console and UART.

This applies on the Ideaspark board + OLED (pixel: 128 x 64) in which has the following configuration :-

Yellow region:
1. Locate at the top region
2. Coordination: (0,0), (127,0), (0,15), (127, 15)

Blue region:
1. Locate at the remain region
2. Coordination: (0, 16), (127, 16), (0, 63), (127, 63)
"""

from machine import Pin, SoftI2C,UART
import time, ssd1306, os, network

class IdeaBoardFunc:
    """
    Class for member functions to manipulate OLED functions.
    """
    def __init__ (self, oled_width, oled_height):
        self.oled_width = oled_width
        self.oled_height = oled_height
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)
        self.msg_line_index = 0 #Indicate current line of msg
        self.msg_ypos_offset = [16, 32, 48]
        self.msg_list = []
        self.led = Pin(2, Pin.OUT)
        self.uart = UART(2)
        self.uart.init(baudrate=9600, bits=8, stop=1, parity=None)
        # Above: Use UART2 for ESP32. Warning: If wrong UART number (for example use UART0), it will be hang up and cannot
        # enter REPL mode and need to re-flash the firmware again.
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.led.off()
        self.system_info = os.uname()

    def header_lines (self, h1, h2):
        self.oled.text(h1, 0, 0)
        self.oled.text(h2, 0, 9)

    def display_text (self, h1, h2):
        self.oled.fill(0) # Uncomment for debugging
        for i in range(0, len(self.msg_list)):
            self.oled.text(self.msg_list[i], 0, self.msg_ypos_offset[i])

        #Header text always stick on line1 and line2
        self.header_lines(h1, h2)
        self.oled.show() # Uncomment for debugging

    def scroll_one_text_line (self, h1, h2):
        """
        Scroll down one text line. One text line define as 16 pixel (Text cell + space)
        :return:
        """
        for i in range(0, 16):
            self.oled.fill(0)
            for j in range(0, len(self.msg_list)):
                self.oled.text(self.msg_list[j], 0, self.msg_ypos_offset[j] + i)
            self.header_lines(h1, h2)
            self.oled.show()

    def write_msg_scroll (self, msg, header1, header2): #Speed = 300ms
        """
        Write a text message to the blue region.
        :param msg:
        :param header1, header2:
        :return:
        """
        #Insert msg into the msg_list
        str_len = len(self.msg_list)
        if str_len == 0:
            self.msg_list.insert(0, msg)
            self.display_text(header1, header2)
        if 1 <= str_len <= 2:
            self.scroll_one_text_line(header1, header2)
            self.msg_list.insert(0, msg)
            self.display_text(header1, header2)
        if str_len == 3:
            self.scroll_one_text_line(header1, header2)
            self.msg_list.pop()  # Remove one element
            self.msg_list.insert(0, msg)
            self.display_text(header1, header2)

    def display(self, msg):
        print (msg)
        self.uart.write(msg)
        self.uart.write('\r\n')

    def led_blink(self):
        self.led.on()
        time.sleep_ms(50)
        self.led.off()
        time.sleep_ms(50)

    def wifi_scan (self):
        scan_result = self.wlan.scan()
        for ap in scan_result: #ap content is (ssid, bssid, ch, rssi, security, hidden)
            ssid = str(ap[0], 'utf-8')
            security = 'Unknown'
            hidden =''
            if ap[4] == 0: # Micropython doesn't support match-cas statement
                security = 'Open'
            elif ap[4] == 1:
                security = 'WEP'
            elif ap[4] == 2:
                security = 'WPA-PSK'
            elif ap[4] == 3:
                security = 'WPA2-PSK'
            elif ap[4] == 4:
                security = 'WPA/WPA2-PSK'
            if ap[5]:
                hidden = 'Yes'
            else:
                hidden = 'No'
            self.display(f'SSID = {ssid}, RSSI = {ap[3]}dBm, ch = {ap[2]}, Security = {security}, Hidden = {hidden}')
            self.write_msg_scroll(f'SSID:{ssid}', 'WiFi Scan Demo', '') #Only show SSID at OLED due to size limitation
            self.led_blink() # This provide 100ms delay
        self.led_blink()
        time.sleep_ms(1000)
        self.display('End of Wifi Scan...')

#Main entry point
if __name__ == '__main__':
    obj_board = IdeaBoardFunc(128, 64)
    obj_board.write_msg_scroll('Start Scanning...', 'WiFi Scan Demo', '')
    obj_board.wifi_scan()
    obj_board.write_msg_scroll('...', 'End scan', '')



