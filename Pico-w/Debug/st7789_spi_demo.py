"""
Demo for ST7789 SPI display

SCK = GPIO10
MISO = GPIO8
MOSI = GPIO11
DC = GPIO18
RST = GPIO19
"""

import uos
import machine
import st7789lib as st7789
# from fonts import vga2_8x8 as font1 # Use at Debug folder
# from fonts import vga1_16x32 as font2 #Use at Debug folder
import vga1_8x16 as small_font
import vga1_16x16 as big_font
from time import sleep_ms

#Debug entry point
if __name__ == '__main__':
    st7789_dc =18
    st7789_res = 19
    # The CS pin should hard-wire to GND

    WIDTH = 240
    HEIGHT = 320

    print (f'Machine name: {uos.uname()[4]}')
    spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
    #Default SPI config: baudrate=24000000, polarity=1, phase=0, bits=8, sck=10, mosi=11, miso=8
    #Pin definition of sck, mosi and miso no need to re-define. Default: SCK=10, MOSI=11, MISC=8
    print(f'SPI config: {spi1}')
    set_rotation = 2 #0-Portrait, 1-Landscape, 2-Inverted Portrait, 3-Inverted Landscape
    display = st7789.ST7789(spi1, WIDTH, HEIGHT,
                            reset=machine.Pin(st7789_res, machine.Pin.OUT),
                            dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                            xstart=0, ystart=0, rotation=set_rotation)

    #width and height at display.fill is depending on rotation
    #if set_rotation == 1 or set_rotation == 3: #If yes, swap width <-> height
        #rotation_width = disp_height
        #rotation_height = disp_width

    CENTER_Y = int(display.height / 2) #Define circle center position
    CENTER_X = int(display.width / 2)


    #Fill rectangle demo
    """
    display.fill(st7789.color565(255, 0, 0))
    sleep_ms(1000)
    r_width = display.width - 20
    r_height = display.height - 20
    display.fill_rect(10, 10, r_width, r_height, st7789.color565(0, 255, 0))
    sleep_ms(1000)
    r_width = display.width - 40
    r_height = display.height - 40
    display.fill_rect(20, 20, r_width, r_height, st7789.color565(0, 0, 255))
    r_width = display.width - 60
    r_height = display.height - 60
    display.fill_rect(30, 30, r_width, r_height, st7789.color565(255, 255, 255))
    sleep_ms(1000)
    r_width = display.width - 80
    r_height = display.height - 80
    display.fill_rect(40, 40, r_width, r_height, st7789.color565(0,0,0))
    sleep_ms(1000)
    r_width = display.width - 150
    r_height = display.height - 150
    display.fill_rect(75, 75, r_width, r_height, st7789.color565(255, 255, 0))
    sleep_ms(1000)
    """
    # Text font demo
    display.fill(st7789.BLACK)
    """
    display.text(small_font, "vga1 8x16 line 1", 10, 0)
    display.text(small_font, "vga1 8x16 line 2", 10, 22)
    display.text(small_font, "vga1 8x16 line 3", 10, 44)
    #display.text(big_font, "vga2 16x16", 10, 40)
    """
    for i in range (100):
        display.text_line(big_font, "This is title line", 1)
        display.text_line(big_font, f'C: {i}', 2)
        sleep_ms(100)

    """
    # Fill circle demo
    display.fill_circle(CENTER_X, CENTER_Y, 100)
    sleep_ms(500)
    display.fill_circle(CENTER_X, CENTER_Y, 30, st7789.color565(255, 0, 0))
    sleep_ms(500)
    display.fill_circle(CENTER_X, CENTER_Y, 50, st7789.color565(0, 255, 0))
    sleep_ms(500)
    display.fill_circle(CENTER_X, CENTER_Y, 70, st7789.color565(0, 0, 255))
    sleep_ms(500)
    """

    print("- bye-")