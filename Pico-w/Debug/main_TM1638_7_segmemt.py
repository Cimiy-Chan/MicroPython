# Wemos D1 Mini
from TM1638 import TM1638
from machine import Pin
tm = TM1638(stb=Pin(20), clk=Pin(19), dio=Pin(18), brightness=3)

# scroll through all supported characters
tm.scroll(list())
tm.scroll(list(tm.SEGMENTS))

# 01234567
tm.clear()
tm.segments(tm.SEGMENTS[0:8])

# 89abcdef
tm.clear()
tm.segments(tm.SEGMENTS[8:16])

# ghijklmn
tm.clear()
tm.segments(tm.SEGMENTS[16:24])

# opqrstuv
tm.clear()
tm.segments(tm.SEGMENTS[24:32])

# wxyz (space) (dash) (degrees)
#tm.clear()
#tm.segments(tm.SEGMENTS[32:39])