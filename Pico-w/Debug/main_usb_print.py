# USB as serial
from machine import Pin
import time
import select
import sys


bi_led = Pin('LED', Pin.OUT)
led_val = bi_led.value()

poll_obj = select.poll()
poll_obj.register(sys.stdin, 1)

if __name__ == '__main__':

    while True:
        if poll_obj.poll(0):
            ch = sys.stdin.read(2)
            print (f'CH: {ch}')
            if ch == 'ty':
                bi_led.value(not bi_led.value())
                print ('LED toggle')
        time.sleep(0.5)

