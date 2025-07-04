"""
Simple demo program to show the interface between Nextion LCD touch panel with the board
This application should be used together with the Nextion HMI file: TBD

"""

from machine import Pin, UART
import time
import max7219


class SysIoT:
    def __init__(self):
        self.led_display = max7219.Max7219API()  # Init MAX7219 driver object
        self.panel_uart = UART(0)  # Time out in ms
        self.panel_uart.init(115200)  # The serial port of LCD panel is set to 115200
        # Define LED pin assignment
        self.led_builtin = Pin(48, Pin.OUT)
        self.led_green_inv = Pin(0, Pin.OUT)  # This LED is inverted. That is Off is ON
        self.led_red_inv = Pin(46, Pin.OUT)
        self.led_blue_inv = Pin(45, Pin.OUT)
        self.led_builtin.off()
        self.led_red_inv.on()  # Inverted ON is off
        self.led_green_inv.on()  # Inverted ON is off
        self.led_blue_inv.on()  # Inverted ON is off
        self.id_suffix = b'\xff\xff\xff'
        # Define rotary switch (rs) digital pin assignment
        self.rs_clk = Pin(17, Pin.IN, Pin.PULL_UP) #D8 = GPIO17
        self.rs_dt = Pin (18, Pin.IN, Pin.PULL_UP) #D9 = GPIO18
        self.rs_sw = Pin (21, Pin.IN, Pin.PULL_UP) #D10 = GPIO21


    def red_led_on(self):
        """
        Turn Red LED ON. This is only one statement but it makes life more easier.
        :return:
        """
        self.led_red_inv.off()

    def red_led_off(self):
        """
        Turn Red LED ON. This is only one statement but it makes life more easier.
        :return:
        """
        self.led_red_inv.on()

    def green_led_on(self):
        """
        Turn Green LED ON. This is only one statement but it makes life more easier.
        :return:
        """
        self.led_green_inv.off()

    def green_led_off(self):
        """
        Turn Green LED ON. This is only one statement but it makes life more easier.
        :return:
        """
        self.led_green_inv.on()

    def blue_led_on(self):
        """
        Turn Blue LED ON. This is only one statement but it makes life more easier.
        :return:
        """
        self.led_blue_inv.off()

    def blue_led_off(self):
        """
        Turn Blue LED ON. This is only one statement but it makes life more easier.
        :return:
        """
        self.led_blue_inv.on()

    def nextion_write(self, cmd):
        """
        UART write to command string to Nextion LCD panel.
        Note that the cmd should be byte string. For example: cmd = b'textbox.txt='
        :param cmd:
        :return: N/A
        """
        self.panel_uart.write(cmd + self.id_suffix)

    def nextion_multi_write(self, cmd_list):
        """
        UART multiple write command string to Nextion LCD panel
        :param cmd_list:
        :return:
        """
        for each_cmd_no in range(0, len(cmd_list)):
            # print (f'Each cmd: {cmd_list[each_cmd_no]}')
            self.nextion_write(cmd_list[each_cmd_no])
            time.sleep_ms(5)


    def panel_comm_setup(self):
        """
        - This is used to set up the communication between LCD panel and system
        :return:
        """
        buffer = None
        time_out_counter = 0
        setup_status = 0  # 0=Not setup, 1=setup at stage 1, 2=setup at stage 2

        while setup_status != 2:  # Trying to communicate and connect with Nextion LCD panel
            setup_status = 0
            while setup_status == 0:
                time.sleep_ms(50)
                buffer = self.panel_uart.read()
                # print (f'Stage {setup_status}: {buffer}')
                if buffer == b'NEXTION_REQ':
                    self.nextion_write(b'var1.txt="ESP32"')  # Send ack message to Nextion
                    setup_status = 1
                    buffer = None
            while setup_status == 1 and time_out_counter < 10:
                time.sleep_ms(50)
                buffer = self.panel_uart.read()
                # print (f'Stage {setup_status}: {buffer}, counter={time_out_counter}')
                time_out_counter += 1
                if buffer == b'NEXTION_OK':
                    self.nextion_write(
                        b'var0.txt="CONNECT"')  # Confirm connection to Nextion LCD self.nextion_write(b'var0.txt="CONNECT"')  # Confirm connection to Nextion LCD
                    setup_status = 2
                    time_out_counter = 10  # Force while loop break
            time_out_counter = 0
        # print ('End of communication')

    def led_init(self):
        self.led_display.max7219_normal_operation()
        self.led_display.max7219_scan_limit(0x07)
        self.led_display.max7219_code_b_mode_4()
        self.led_display.max7219_intensity_adjust(0x05)
        self.led_display.max7219_display_test_mode(is_test_mode=False)

    def seven_segment_display(self, num_val):
        """
        - To display two digits seven segment display on board. Num_val should be in range
        - 00 to 99.
        :param num_val:
        :return: True if num_val is in the range of 0 to 99 inclusive otherwise return false
        """
        epsilon = 0.001  # Small value to compensate the floating point truncation error

        if 0 <= num_val <= 99:
            num_val = num_val / 10.0
            dig_10 = int(num_val)
            dig_1 = int((num_val - int(num_val)) * 10.0 + epsilon)

            # Put it to the seven segment hardware
            # print (f'Dig_10={dig_10}, Dig_1={dig_1}')
            self.led_display.max7219_digit_write(1, dig_1)
            self.led_display.max7219_digit_write(2, dig_10)
            return True
        else:
            self.led_display.max7219_digit_write(1, 0x0b)  # Display EE as Error
            self.led_display.max7219_digit_write(2, 0x0b)

    def counter_down_timer(self, count_down_val, duration):
        """
        - Count_down_val should be in range 0 to 99
        - Duration in ms. Min. value is 100. That is 100ms.
        :param count_down_val:
        :param duration:
        :return:
        """

        if 0 <= count_down_val <= 99 and duration >= 100:
            while count_down_val >= 1:
                buffer = self.panel_uart.read()
                if buffer == b'RESET': # RESET button press
                    count_down_val = 0
                    duration = 1
                self.seven_segment_display(count_down_val)
                count_down_val -= 1
                time.sleep_ms(duration)
        else:
            self.led_display.max7219_digit_write(1, 0x0a)  # Display as '--'
            self.led_display.max7219_digit_write(2, 0x0a)

    def check_comm (self):
        """
        It is used to check the status of communication between Nextion and ESP32
        :return: True is link is OK.
        """

        # Send variable value request to Nextion
        buffer = None
        self.nextion_write(b'get page0.var0.txt')
        time.sleep_ms(20)
        read_buffer = self.panel_uart.read()
        # print (f'Check comm: {read_buffer}')
        if read_buffer is not None and b'CONNECT' in read_buffer:
            return True
        else:
            return False

    def get_nextion_cmd (self):
        """
        Get cmd string from Nextion LCD display
        :return: cmd_list if command caught. NULL if no command is found.
        """
        cmd_list = [b'SET_0099S']
        self.nextion_write(b'get page0.cmd.txt')
        time.sleep_ms(10)
        read_buffer = self.panel_uart.read() #Read cmd.txt content
        # print (f'Get nextion cmd: {read_buffer}')
        if read_buffer is not None:
            for cmd_no in range (0,len(cmd_list)):
                if cmd_list[cmd_no] in read_buffer:
                    self.nextion_write(b'page0.cmd.txt="NULL"') # O Overwrite the read command to avoid cmd repeat
                    return cmd_list[cmd_no]
        return b'NULL'

    def start_0099s(self):
        """
        Timer function manually adjusting count down time from 00 to 99 sec.
        :return:
        """
        self.nextion_write(b'get page1.n0.val') #Get value of object n0. That is the number dial value
        time.sleep_ms(30)
        read_buffer = self.panel_uart.read() #Read cd_val content
        # print (f'Read buffer start_0099s:{read_buffer}')
        return list(read_buffer)[1] # Timer value is location at 2nd position of array

    def rotary_encode(self):
        """
        Function for rotary encoder. This function will go to dead loop until the user rotate the encoder either in clockwise, anticlockwise or push a button
        :return:0=pin push button pushed. 1=clockwise, 2 = anticlockwise
        """
        previous_dt_state = obj_func.rs_dt.value()
        while True:
            sw_val = self.rs_sw.value()
            time.sleep_ms(5) # Note: This delay time is critical.
            dt_val = self.rs_dt.value()
            if sw_val == 0:
                return 0
            elif dt_val != previous_dt_state:
                if self.rs_clk.value() != dt_val:
                    return 1
                else:
                    return 2
            previous_dt_state = dt_val


if __name__ == '__main__':
    obj_func = SysIoT()
    obj_func.led_display.max7219_display_clear()
    obj_sys_iot = SysIoT()
    obj_sys_iot.led_init()
    obj_func.seven_segment_display(88)
    time.sleep_ms(500)
    obj_func.seven_segment_display(0)
    time.sleep_ms(500)

    counter = 0
    previous_dt_state = obj_func.rs_dt.value()
    while True:
        rotary_encode_state = obj_func.rotary_encode()
        if rotary_encode_state == 0:
            obj_func.seven_segment_display(0)
            counter = 0
        else:
            if rotary_encode_state == 1 and counter <=98:
                counter += 1
                obj_func.seven_segment_display(counter)
            elif rotary_encode_state == 2 and counter >=1:
                counter -= 1
                obj_func.seven_segment_display(counter)
        obj_func.green_led_on()
        time.sleep_ms(20)
        obj_func.green_led_off()


        time.sleep_ms(20)
