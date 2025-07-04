"""
Demo application for scrolling text from top to bottom at the OLED's blue region
This applies on the Ideaspark board + OLED (pixel: 128 x 64) in which has the following configuration :-

Yellow region:
1. Locate at the top region
2. Coordination: (0,0), (127,0), (0,15), (127, 15)

Blue region:
1. Locate at the remain region
2. Coordination: (0, 16), (127, 16), (0, 63), (127, 63)
"""

from machine import Pin, SoftI2C
import time, ssd1306

#ESP32 Pin assignment
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

class OLED_Func:
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

    def display_text (self):
        for i in range(0, len(self.msg_list)):
            self.oled.text(self.msg_list[i], 0, self.msg_ypos_offset[i])
        self.oled.show()

    def write_msg (self, msg):
        if len(self.msg_list) <= 2: # If yes, handle 1st line in
            self.msg_list.insert(0, msg)
            self.display_text()
        else:
            self.msg_list.pop() #Remove one element
            self.msg_list.insert(0, msg)
            self.display_text()



#Main entry point
if __name__ == '__main__':
    screen_msg = [['Msg1 -- row1', 0, 0], ['Msg2 -- row2', 0, 12], ['Msg3 -- row3', 0, 24]]
    obj_oled_func = OLED_Func(128, 64)
    obj_oled_func.write_msg('Test 1')
    time.sleep(2)
    obj_oled_func.write_msg('Test 2')
    time.sleep(2)
    obj_oled_func.write_msg('Test 3')
    time.sleep(2)
    obj_oled_func.write_msg('Test 4')
    time.sleep(2)
    obj_oled_func.write_msg('Test 5')
