import array, time
from random import random, randrange

from machine import Pin
import rp2
import random

# PIO state machine for RGB. Pulls 24 bits (rgb -> 3 * 8bit) automatically
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    """
    Note that the following codings are the RP2040 assembly language which is not supported by PyCharm IDE.
    Therefore, there will be the "read-snake" error appeared. We con ignore this error
    :return:
    """
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop().side(0)                       [T2 - 1]
    wrap()

# PIO state machine for RGBW. Pulls 32 bits (rgbw -> 4 * 8bit) automatically
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=32)
def sk6812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Delay here is the reset time. You need a pause to reset the LED strip back to the initial LED
# however, if you have quite a bit of processing to do before the next time you update the strip
# you could put in delay=0 (or a lower delay)
#
# Class supports different order of individual colors (GRB, RGB, WRGB, GWRB ...). In order to achieve
# this, we need to flip the indexes: in 'RGBW', 'R' is on index 0, but we need to shift it left by 3 * 8bits,
# so in it's inverse, 'WBGR', it has exactly right index. Since micropython doesn't have [::-1] and recursive rev()
# isn't too efficient we simply do that by XORing (operator ^) each index with 3 (0b11) to make this flip.
# When dealing with just 'RGB' (3 letter string), this means same but reduced by 1 after XOR!.
# Example: in 'GRBW' we want final form of 0bGGRRBBWW, meaning G with index 0 needs to be shifted 3 * 8bit ->
# 'G' on index 0: 0b00 ^ 0b11 -> 0b11 (3), just as we wanted.
# Same hold for every other index (and - 1 at the end for 3 letter strings).

def get_rgb_data_decorator(func):
    """
    This is the decorator for set_pixel_line_gradient()
    :return:
    """
    def wrapper(self, pixel1, pixel2, left_rgb_w, right_rgb_w, how_bright = None):
        if self.is_display_gradient_pixel == True: #This is declared at Class instantiation
            func(self, pixel1, pixel2, left_rgb_w, right_rgb_w, how_bright = None)

        #Additonal codes to get the value of RGB values
        right_pixel = max(pixel1, pixel2)
        left_pixel = min(pixel1, pixel2)
        self.rgb_val.clear()

        for i in range(right_pixel - left_pixel + 1):
            fraction = i / (right_pixel - left_pixel)
            green = round((right_rgb_w[0] - left_rgb_w[0]) * fraction + left_rgb_w[0])
            red = round((right_rgb_w[1] - left_rgb_w[1]) * fraction + left_rgb_w[1])
            blue = round((right_rgb_w[2] - left_rgb_w[2]) * fraction + left_rgb_w[2])
            self.rgb_val.append((green, red, blue)) #Store rgb val tuple into the array.
            # if it's (r, g, b, w)
    return wrapper



class Neopixel:
    """
    Class containing member functions of controlling the LED matrix with WS2812B chip
    """
    def __init__(self, num_leds, state_machine, pin, mode="RGB", delay=0.0001):
        self.pixels = array.array("I", [0 for _ in range(num_leds)])
        self.mode = set(mode)   # set for better performance
        if 'W' in self.mode:
            # RGBW uses different PIO state machine configuration
            self.sm = rp2.StateMachine(state_machine, sk6812, freq=8000000, sideset_base=Pin(pin))
            # dictionary of values required to shift bit into position (check class desc.)
            self.shift = {'R': (mode.index('R') ^ 3) * 8, 'G': (mode.index('G') ^ 3) * 8,
                          'B': (mode.index('B') ^ 3) * 8, 'W': (mode.index('W') ^ 3) * 8}
        else:
            self.sm = rp2.StateMachine(state_machine, ws2812, freq=8000000, sideset_base=Pin(pin))
            self.shift = {'R': ((mode.index('R') ^ 3) - 1) * 8, 'G': ((mode.index('G') ^ 3) - 1) * 8,
                          'B': ((mode.index('B') ^ 3) - 1) * 8, 'W': 0}
        self.sm.active(1)
        self.num_leds = num_leds
        self.delay = delay
        self.brightnessvalue = 255
        self.rgb_val = [] # rbg_val getting from function set_pixel_line_gradient()
        self.is_display_gradient_pixel = True

    def pixel_para_random(self, no_of_pixel=1):
        """
        Random (but in range) pixel parameter generation in group. After running this function, the following
        pixel paremeters:-
        xy: tuple (x_pos, y_pos) where x_pos/y_pos in range (0, 7)
        rgb: color parameter in tuple form (red, green, blue), (0,255) for each color
        brightness: (0, 100)
        :parm no_of_pixel:
        :return: pixel_parm [x,y, rgb(), brightness]
        """

        if no_of_pixel < 1:
            return

        pixel_parm=[[]] * no_of_pixel
        for each_parm in range (0, no_of_pixel):
            x_pos = randrange(0, 8) # x position
            y_pos = randrange(0, 8) # y position
            xy_pos = (x_pos, y_pos)
            red = randrange(0, 256)
            green = randrange(0, 256)
            blue = randrange(0, 256)
            rgb = (red, green, blue) # rgb in tuple
            br=randrange(0, 100)
            pixel_parm[each_parm] = [xy_pos, rgb, br]

        return pixel_parm

    def brightness(self, brightness=None):
        """
        # Set the overal value to adjust brightness when updating leds
        :param brightness:
        :return:
        """
        if brightness == None:
            return self.brightnessvalue
        else:
            if brightness < 1:
                brightness = 1
        if brightness > 255:
            brightness = 255
        self.brightnessvalue = brightness

    # Create a gradient with two RGB colors between "pixel1" and "pixel2" (inclusive)
    # Function accepts two (r, g, b) / (r, g, b, w) tuples

    @get_rgb_data_decorator
    def set_pixel_line_gradient(self, pixel1, pixel2, left_rgb_w, right_rgb_w, how_bright = None):
        if pixel2 - pixel1 == 0:
            return
        right_pixel = max(pixel1, pixel2)
        left_pixel = min(pixel1, pixel2)

        for i in range(right_pixel - left_pixel + 1):
            fraction = i / (right_pixel - left_pixel)
            green = round((right_rgb_w[0] - left_rgb_w[0]) * fraction + left_rgb_w[0])
            red = round((right_rgb_w[1] - left_rgb_w[1]) * fraction + left_rgb_w[1])
            blue = round((right_rgb_w[2] - left_rgb_w[2]) * fraction + left_rgb_w[2])
            # if it's (r, g, b, w)
            if len(left_rgb_w) == 4 and 'W' in self.mode:
                white = round((right_rgb_w[3] - left_rgb_w[3]) * fraction + left_rgb_w[3])
                self.set_pixel(left_pixel + i, (green, red, blue, white), how_bright)
            else:
                self.set_pixel(left_pixel + i, (green, red, blue), how_bright)

    # Set an array of pixels starting from "pixel1" to "pixel2" (inclusive) to the desired color.
    # Function accepts (r, g, b) / (r, g, b, w) tuple
    def set_pixel_line(self, pixel1, pixel2, rgb_w, how_bright = None):
        for i in range(pixel1, pixel2 + 1):
            self.set_pixel(i, rgb_w, how_bright)

    # Set red, green and blue value of pixel on position <pixel_num>
    # Function accepts (r, g, b) / (r, g, b, w) tuple
    def set_pixel(self, pixel_num, rgb_w, how_bright = None):
        if how_bright == None:
            how_bright = self.brightness()
        pos = self.shift

        green = round(rgb_w[0] * (how_bright / 255))
        red = round(rgb_w[1] * (how_bright / 255))
        blue = round(rgb_w[2] * (how_bright / 255))
        white = 0
        # if it's (r, g, b, w)
        if len(rgb_w) == 4 and 'W' in self.mode:
            white = round(rgb_w[3] * (how_bright / 255))

        self.pixels[pixel_num] = white << pos['W'] | blue << pos['B'] | red << pos['R'] | green << pos['G']

    def set_pixel_pos(self, xy_pos, rbg, how_bright = None):
        """
        Enable specific pixel position (x, y). The position is specified as the following:-
        Top-Left=(0,0), Top-Right=(0,7), Bottom-Left=(7,0), Bottom-Right=(7,7)
        :param xy_pos in tuple (x, y)
        :param rbg:
        :param how_bright:
        :return:
        """

        if xy_pos[0] > 7 or xy_pos[1] > 7:
            return
        else:
            led_pos = xy_pos[1] * 8 + xy_pos[0]
            self.set_pixel(led_pos, rbg, how_bright)


    def pixel_group_flash (self, no_of_pixel, xy_pos_array_tuple, rgb_array_tuple, bright_min, bright_max, duration_ms=100):
        """
        pixel flash in group with specific positions.
        :param no_of_pixel: Min = 1
        :param xy_pos_array_tuple:
        :param rgb_array_tuple:
        :param bright_min:
        :param bright_max:
        :param duration_ms:
        :return:
        """
        if no_of_pixel < 1 or bright_min < 0 or bright_max > 100 or (bright_max - bright_min) <= 0 or duration_ms < 50 or duration_ms > 1000:
            return

        # Create no. of steps for brightness
        no_of_step = int((duration_ms / 2.0) / 5.0)
        brightness_array = []
        for brightness_step in range(0, no_of_step):
            brightness_array.append(int((bright_max - bright_min) * (brightness_step / no_of_step) + bright_min))

        # Fade in
        for each_brightness in range(0, len(brightness_array)):
            self. brightness(brightness_array[each_brightness])
            for each_pixel_index in range(0, no_of_pixel):
                self.set_pixel_pos(xy_pos_array_tuple[each_pixel_index], rgb_array_tuple[each_pixel_index], how_bright=brightness_array[each_brightness])
            time.sleep_ms(5)
            self.show()
        # Fade out
        for each_brightness in range(1, len(brightness_array)):  # Start from 1 to remove the max bright value
            self.brightness(brightness_array[len(brightness_array) - each_brightness - 1])
            for each_pixel_index in range(0, no_of_pixel):
                self.set_pixel_pos(xy_pos_array_tuple[each_pixel_index], rgb_array_tuple[each_pixel_index], how_bright=brightness_array[len(brightness_array) - each_brightness - 1])
            time.sleep_ms(5)
            self.show()


    # Converts HSV color to rgb tuple and returns it
    # Function accepts integer values for <hue>, <saturation> and <value>
    # The logic is almost the same as in Adafruit NeoPixel library:
    # https://github.com/adafruit/Adafruit_NeoPixel so all the credits for that
    # go directly to them (license: https://github.com/adafruit/Adafruit_NeoPixel/blob/master/COPYING)
    def colorHSV(self, hue, sat, val):
        if hue >= 65536:
            hue %= 65536

        hue = (hue * 1530 + 32768) // 65536
        if hue < 510:
            b = 0
            if hue < 255:
                r = 255
                g = hue
            else:
                r = 510 - hue
                g = 255
        elif hue < 1020:
            r = 0
            if hue < 765:
                g = 255
                b = hue - 510
            else:
                g = 1020 - hue
                b = 255
        elif hue < 1530:
            g = 0
            if hue < 1275:
                r = hue - 1020
                b = 255
            else:
                r = 255
                b = 1530 - hue
        else:
            r = 255
            g = 0
            b = 0

        v1 = 1 + val
        s1 = 1 + sat
        s2 = 255 - sat

        r = ((((r * s1) >> 8) + s2) * v1) >> 8
        g = ((((g * s1) >> 8) + s2) * v1) >> 8
        b = ((((b * s1) >> 8) + s2) * v1) >> 8

        return r, g, b


    # Rotate <num_of_pixels> pixels to the left
    def rotate_left(self, num_of_pixels):
        if num_of_pixels == None:
            num_of_pixels = 1
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]

    # Rotate <num_of_pixels> pixels to the right
    def rotate_right(self, num_of_pixels):
        if num_of_pixels == None:
            num_of_pixels = 1
        num_of_pixels = -1 * num_of_pixels
        self.pixels = self.pixels[num_of_pixels:] + self.pixels[:num_of_pixels]

    # Update pixels
    def show(self):
        # If mode is RGB, we cut 8 bits of, otherwise we keep all 32
        cut = 8
        if 'W' in self.mode:
            cut = 0
        for i in range(self.num_leds):
            self.sm.put(self.pixels[i], cut)
        time.sleep(self.delay)

    # Set all pixels to given rgb values
    # Function accepts (r, g, b) / (r, g, b, w)
    def fill(self, rgb_w, how_bright = None):
        for i in range(self.num_leds):
            self.set_pixel(i, rgb_w, how_bright)

    # Clear the strip
    def clear(self):
        self.pixels = array.array("I", [0 for _ in range(self.num_leds)])