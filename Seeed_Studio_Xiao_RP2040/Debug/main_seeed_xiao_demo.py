'''
Demo program for Seeed Xiao RP2040 + Seded Xiao Expansion board (RTC)
It is embedded at Seed Xiao Expansion board with the following hardware
#
#
Seeed Xiao Board RP2040
1. USER_LED: R(GPIO17), G(GPIO16), B(GPIO25). Active low: led.off() #LED light on
2. RGB LED (DIN=GPIO12, VCC=NEO_PWR=GPIO11)
#
#
Expansion board
1. RTC PCF8563 (0x51, SCL=GPIO7, SDA=GPIO6)
2. OLED 0.96" display (0x3C, SCL=GPIO7, SDA=GPIO6)
3. Buzzer: (GPIO29)
4. User button: (GPIO27)
5. UART: ID=1, Tx=0, Rx=1
6. SD Card: (SCK=2, MISO=4, MOSI=3, CS=28)
'''
import machine

import pcf8563
from machine import Pin, I2C, PWM, SPI
import time
import ssd1306
import sdcard
import uos

day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
is_set_time = False
mount_point = '/sd' #Mount point = directory of SD card
datetime_value: tuple = ()

# Hardware pins to Seed Xiao RP2040 definitions
SDA = 6
SCL = 7
SD_CS = 28
SD_SCK = 2
SD_MOSI = 3
SD_MISO = 4
BUZ_PIN = 29
USER_BUTTON_PIN = 27
RGB_R = 17
RGB_G = 16
RGB_B = 25
HIGH_TONE = [784, 1047]
BEAT_TIME = [300, 200]
LOW_TONE = [1047, 784]

def display_text(str, line):
    display.text(str, 0, (line % 8) * 8, 1)

def buzzer_beep (tone_array: list, beat_arry: list):
    buzzer = PWM(BUZ_PIN, freq=1000, duty_u16=0)
    if len(tone_array) !=0 and len(tone_array) == len(beat_arry):
        for item in range(len(tone_array)):
            if tone_array[item]:
                buzzer.duty_u16(32768)
                buzzer.freq(tone_array[item])
                time.sleep_ms(beat_arry[item])
                buzzer.duty_u16(0) #Stop the buzzer

def check_sd_card (sd_obj, sd_mount_point):
    try:
        # Mount filesystem
        vfs = uos.VfsFat(sd_obj)
        uos.mount(vfs, sd_mount_point)
        return [True, 'Card Detected']
    except Exception as e:
        display_text('No SD Card', 0)
        display_text('System Halt...',2)
        display.show()
        return [False, f'Error: {e}']

def logging_info (log_type:str, log_info:str, mp:str, log_file:str):
    log_timestamp = rtc.datetime()
    timestamp_style = (f'Date: {log_timestamp[0]:04d}/{log_timestamp[1]:02d}/{log_timestamp[2]:02d} '
                      f'Time: {log_timestamp[3]:02d}:{log_timestamp[4]:02d}:{log_timestamp[5]:02d}')

    with open(mp + '/' + log_file + '.txt', 'a+') as file:
        file.write(f'{timestamp_style} [{log_type}] - {log_info}\r\n')
        file.close()

def logging_header (mp:str, log_file:str):
    with open(mp + '/' + log_file + '.txt', 'a+') as file:
        file.write('Seeed Xiao Expansion Board Demo Log file\r\n')
        file.close()

if __name__ == '__main__':
    i2c = I2C(1, sda=Pin(SDA), scl=Pin(SCL)) #ID=1 for Seed
    rtc = pcf8563.PCF8563(i2c) #Instantiate rtc object
    display = ssd1306.SSD1306_I2C(128, 64, i2c) #Instantiate oled object
    buz_pin = Pin(BUZ_PIN, Pin.OUT)
    user_button = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP) #User button: active low (Press to low state)
    cs = Pin(SD_CS, Pin.OUT)
    spi = SPI(0,
              baudrate=1000000,
              polarity=0,
              phase=0,
              bits=8,
              firstbit=machine.SPI.MSB,
              sck=SD_SCK,
              mosi=SD_MOSI,
              miso=SD_MISO)

    led_r = Pin(RGB_R, Pin.OUT)
    led_g = Pin(RGB_G, Pin.OUT)
    led_b = Pin(RGB_B, Pin.OUT)

    led_r.on() #Active low -> ledr.on() = LED OFF
    led_b.on()

    # Check SD card availability
    try:
        sd_obj = sdcard.SDCard(spi, cs)
    except Exception as e:
        display_text('No SD Card', 0)
        display_text('System Halt...',2)
        display.show()

    sd_detect = check_sd_card(sd_obj, mount_point)
    datetime_log = rtc.datetime()

    log_filename: str = (f'log_{datetime_log[0]:04d}{datetime_log[1]:02d}{datetime_log[2]:02d}'
                         f'{datetime_log[3]:02d}{datetime_log[4]:02d}{datetime_log[5]:02d}.log')

    if sd_detect[0]:
        logging_header(mount_point, log_filename)

    if is_set_time:
        rtc.set_datetime((25, 7, 4, 5, 7, 50, 00)) #Format: (Year, Month, Date, Day, Hour, Min, Sec)
    while True:
        datetime_value = rtc.datetime()
        display.fill(0)
        display_text('RTC...', 0)
        display_text(f'Date: {datetime_value[0]:04d}/{datetime_value[1]:02d}/{datetime_value[2]:02d}', 2)
        display_text(f'Time: {datetime_value[3]:02d}:{datetime_value[4]:02d}:{datetime_value[5]:02d}',3)
        display_text(f'Week: {day[datetime_value[6]]}', 4)
        display.show()
        buz_pin.on()
        led_g.off()
        time.sleep(0.5)
        buz_pin.off()
        led_g.on()
        if sd_detect[0] and datetime_value[5] == 10: # Just for demo logging, log at 10th second
            logging_info('INFO', 'Time at 10th second', mount_point, log_filename)
        if user_button.value() == 0:
            buzzer_beep(HIGH_TONE, BEAT_TIME)
            if sd_detect[0]:
                logging_info('INFO', 'User button press', mount_point, log_filename)
        else:
            time.sleep(0.5)
