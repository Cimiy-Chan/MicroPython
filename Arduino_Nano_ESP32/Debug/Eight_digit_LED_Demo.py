from machine import Pin
import time, math
import max7219


class SysIoT:
    def __init__(self):
        self.led_display = max7219.Max7219API()  # Init MAX7219 driver object

    def led_init(self):
        self.led_display.max7219_normal_operation()
        self.led_display.max7219_scan_limit(0x07)
        self.led_display.max7219_code_b_mode_4()
        self.led_display.max7219_intensity_adjust(0x05)
        self.led_display.max7219_display_test_mode(is_test_mode=False)

    def seven_segment_display (self, num_val):
        """
        - To display two digits seven segment display on board. Num_val should be in range
        - 00 to 99.
        :param num_val:
        :return: True if num_val is in the range of 0 to 99 inclusive otherwise return false
        """
        epsilon = 0.001 # Small value to compensate the floating point truncation error


        if 0<= num_val <= 99:
            num_val = num_val / 10.0
            dig_10 = int(num_val)
            dig_1 = int ((num_val-int(num_val))*10.0 + epsilon)

            #Put it to the seven segment hardware
            #print (f'Dig_10={dig_10}, Dig_1={dig_1}')
            self.led_display.max7219_digit_write(1, dig_1)
            self.led_display.max7219_digit_write(2, dig_10)
            return True
        else:
            self.led_display.max7219_digit_write(1, 0x0b) #Display EE as Error
            self.led_display.max7219_digit_write(2, 0x0b)


    def counter_down_timer(self, count_down_val, duration):
        """
        Count down function
        :param count_down_val:
        :return:
        """
        if 0<= count_down_val <=99 and duration >=100:
            while count_down_val >= 0:
                self.seven_segment_display(count_down_val)
                count_down_val -= 1
                time.sleep_ms(duration)
        else:
            self.led_display.max7219_digit_write(1, 0x0a) # Display as '--'
            self.led_display.max7219_digit_write(2, 0x0a)



if __name__ == '__main__':
    obj_sys_iot = SysIoT()
    obj_sys_iot.led_init()
    obj_sys_iot.led_display.max7219_display_clear()
    obj_sys_iot.counter_down_timer(35, 500)
