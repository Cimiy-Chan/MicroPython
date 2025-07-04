"""
Put this code into the main.py
Display result on both REPL terminal and UART serial port
"""
import time
from lsm6dsox import LSM6DSOX
from machine import Pin, I2C, UART

class FuncMain:
    def __init__(self):
        # Initialize the LSM6DSOX sensor with I2C interface
        self.lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))
        self.led = Pin(6, Pin.OUT)
        self.uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) #Use UART 0 for PyCharm, 1 for Thonny

        self.led.off() # Off initially
        self.counter = 100 #For debugging use. Limit the loop

    def display(self, msg):
        print (msg)
        self.uart.write(msg)
        self.uart.write('\r\n')

    def get_data(self):
        while self.counter != 0: # Limit to run 10 times to quite
            # Read accelerometer values
            accel_values = self.lsm.acceleration()
            self.display('Accelerometer: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*accel_values))

            # Read gyroscope values
            gyro_values = self.lsm.gyro()
            self.display('Gyroscope: x:{:>8.3f} y:{:>8.3f} z:{:>8.3f}'.format(*gyro_values))

            self.display(f'Remain: {self.counter}')
            self.led.toggle()
            time.sleep_ms(500)
            self.counter = self.counter - 1
            self.led.toggle()
            time.sleep_ms(500)
        self.display('\r\n')
        self.display('Ending....')

if __name__ == '__main__':
    obj_main = FuncMain()
    obj_main.get_data()