'''
Demo application for SD card for Seeed Xiao (RP2040) + Seed Xiao expansion board
'''
from machine import Pin, SPI
import time
import sdcard
import uos

SD_CS = 28
SD_SCK = 2
SD_MOSI = 3
SD_MISO = 4

RGB_R = 17
RGB_G = 16
RGB_B = 25

led_r = Pin(RGB_R, Pin.OUT)
led_g = Pin(RGB_G, Pin.OUT)
led_b = Pin(RGB_B, Pin.OUT)

# Active low: on() -> LED off
led_r.on()
led_g.on()
led_b.on()



mount_point = '/sd' #Mount point = directory of SD card


def check_sd_card (sd_obj, sd_mount_point):
    try:
        # Mount filesystem
        vfs = uos.VfsFat(sd_obj)
        uos.mount(vfs, sd_mount_point)
        return [True, 'Card Detected']
    except Exception as e:
        return [False, f'Error: {e}']



if __name__ == '__main__':
    counter: int = 0
    # Assign chip select (CS) pin (and start it high)
    cs = Pin(SD_CS, Pin.OUT)

    # Initial SPI peripheral (start with 1 MHz)
    spi = SPI(0,
              baudrate=1000000,
              polarity=0,
              phase=0,
              bits=8,
              firstbit=SPI.MSB,
              sck=SD_SCK,
              mosi=SD_MOSI,
              miso=SD_MISO)

    # Check SD card
    sd_obj = sdcard.SDCard(spi, cs)
    sd_detect = check_sd_card(sd_obj, mount_point)

    while True:
        if sd_detect[0]:
            led_g.off()
            print ('SD detect')
            with open("/sd/test03.txt", "a+") as file:
                file.write(f'This is a test - line {counter}\r\n')
                file.close()
                counter += 1
            time.sleep_ms(500)
            led_g.on()
            time.sleep_ms(500)
        else:
            led_r.off()
            time.sleep_ms(500)
            led_r.on()
            time.sleep_ms(500)


