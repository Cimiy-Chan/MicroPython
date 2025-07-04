"""
For flashing the file into device, filename must be "main.py"
Other filename cannot be flashed into the Pico-W device.

Communication with PC <--> Pico-W

|------|         |----|
|      |         |    |
|      |         |    |
|Pico-W|<------->|USB |<---->PC
|      |         |UART|
|      |         |    |
|----- |         |----|
"""

from machine import Pin, UART
import time

class Pico_Func:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

    def blink_led(self):
        """
        - Blinking LED
        - LED location: Built-in at Pico-W
        """
        self.led.on()
        time.sleep(0.1)
        self.led.off()
        time.sleep(0.5)

    def msg_write(self, msg) -> None:
        """
        - Write a message to UART
        :param msg:
        :return:
        """
        self.uart1.write(msg)

    def timer_delay(self, time_val) -> None:
        """
        - Delay a while
        :param time_val:
        :return:
        """
        time.sleep(time_val)


if __name__ == '__main__':
    apps_pico_w = Pico_Func()
    while True:
        apps_pico_w.blink_led()
        apps_pico_w.msg_write('Test only\n\r')
        apps_pico_w.timer_delay(1)