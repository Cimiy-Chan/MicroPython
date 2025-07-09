# VfsFat use real time? - scruss, 2022-10
# sd card (Maker Pi Pico)
#  wired SCK on GP10, TX on GP11, RX on GP12, CS on GP1*5*

from machine import Pin, SPI, RTC
from time import localtime, mktime
from uos import VfsFat, mount, stat
# get the new sdcard.py from micropython-lib repo
from sdcard import SDCard

# file existence check routine
def file_or_dir_exists(filename):
    try:
        stat(filename)
        return True
    except OSError:
        return False

# init sd card
sd_spi = SPI(1, sck=Pin(10, Pin.OUT), mosi=Pin(11, Pin.OUT),
             miso=Pin(12, Pin.OUT))
sd = SDCard(sd_spi, Pin(15, Pin.OUT))
vfs = VfsFat(sd)
mount(vfs, "/sd")

# get current time, perhaps set by Thonny
rtc = RTC()
now = rtc.datetime()
print("current RTC time:", now)
ts = mktime(now)
print("Timestamp of now / s:", ts)

# create trivial file on sd card
f = open("/sd/now.txt", "w")
f.write(str(now)+"\n")
f.close()

# get file details
status = stat("/sd/now.txt")
print("os.stat of /sd/now.txt:", status)
print("Iffy file timestamp:", status[7])
offset = status[7] - ts
print("VfsFat time offset / s:", offset, end='')
print(" (or roughly", round(offset / (60 * 60 * 24 * 365.25)), "years)")
print("Corrected file date:", localtime(status[7] - offset))
print()

# compare with a LittleFS file, if it exists
if file_or_dir_exists("/boot.py"):
    print("/boot.py file date:", localtime(stat("/boot.py")[7]))
else:
    print("/boot.py doesn't exist, can't compare")