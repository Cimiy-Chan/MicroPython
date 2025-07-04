"""
"""
import time
from machine import Pin
from MAX9814 import MAX9814
from neopixel import Neopixel

if __name__ == '__main__':
    obj_max9814 = MAX9814(sma_buffer_size=20)
    led_pixel = Neopixel(8, 0, 22, 'RGB')
    led = Pin("LED", Pin.OUT)
    led.on()
    led_ext = Pin(3, Pin.OUT)
    button = Pin(2, Pin.IN, Pin.PULL_DOWN)
    button_current_state: int = 0
    button_next_state: int = 0
    led_pixel.brightness(20)

    is_first_time: bool = True
    no_of_pixel_display: int = 0

    while True:
        led.on()
        #no_of_pixel_display: int = obj_max9814.audio_indicator(8)
        print(f'No. of pixel: {no_of_pixel_display}')  # Debug use
        if 0 < no_of_pixel_display <= 3:
            print ('Line')
            led_pixel.set_pixel_line(0,no_of_pixel_display, (0, 255, 0) )
        if 3 < no_of_pixel_display <=7:
            print ('Gradient')
            led_pixel.set_pixel_line_gradient(0, no_of_pixel_display, (0,255,0), (255, 0, 0))
        led_pixel.show()
        if no_of_pixel_display == 0:
            led_pixel.show()
            time.sleep_ms(1)
            led_pixel.clear()
            time.sleep(1)

        else:
            time.sleep(1)
            led_pixel.clear()
            #time.sleep(1)
        no_of_pixel_display += 1
        if no_of_pixel_display > 7:
            no_of_pixel_display = 0
        button_current_state = button.value()
        if button_current_state != button_next_state:
            led_pixel.show()
            time.sleep_ms(1)
            led_pixel.clear()
            time.sleep(10)
            print ('End of application...')
            break
    led_ext.on()
    led.off()
    time.sleep(1)

    led_ext.off()
    #End of program