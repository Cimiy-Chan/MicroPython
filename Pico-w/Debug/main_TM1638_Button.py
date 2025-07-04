# Wemos D1 Mini
from TM1638 import TM1638
from machine import Pin
tm = TM1638(stb=Pin(20), clk=Pin(19), dio=Pin(18))

from time import sleep_ms

# press a button to illuminate the matching individual LED
# you can press multiple buttons simultaneously

print ('TM1638 LED&KEY demo... Press any key to start')
_=input()
print ('Start...Press any button on the board...')
while True:
    pressed = tm.keys()
    for i in range(8):
        tm.led(i, (pressed >> i) & 1)
    sleep_ms(10)