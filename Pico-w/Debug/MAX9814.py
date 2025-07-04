import time
from machine import Pin, I2C, ADC

class MAX9814:
    def __init__(self, sma_buffer_size = 10):
        self.adc = ADC(Pin(26))
        self.volt_min: float = 0.0
        self.volt_max: float = 0.0
        self.sma_buffer_size = sma_buffer_size
        self.sma_buffer: list = []

    def simple_moving_average_float(self, val: float, array_list: list) -> float:
        """
        Moving average
        :param val:
        :param array_list:
        :return:
        """

        sum_val: float = 0.0
        # Buffer element filling
        if len(array_list) > self.sma_buffer_size:
            return 0.0
        elif len(array_list) == self.sma_buffer_size: # Buffer full
            array_list.pop(0) # Remove the first element
            array_list.append(val)
        else:
            array_list.append(val)

        for each_element in range(0, len(array_list)):
            sum_val += array_list[each_element]

        return (sum_val / len(array_list)) * 1.0 # multiplied by 1.0 to convert to float

    def find_min_max(self, no_of_trial: int = 10) -> None:
        """
        :param no_of_trial:
        :return:
        """
        is_first_time: bool = True

        if no_of_trial >= 10:
            while no_of_trial >= 0:
                adc_res:float = ((self.adc.read_u16())/65535.0) * 3.3
                if is_first_time:
                    self.volt_min = adc_res
                    self.volt_max = adc_res
                    is_first_time = False
                else:
                    if adc_res > self.volt_max:
                        self.volt_max = adc_res
                        print (f'Volt_min: {self.volt_min}, Volt_max: {self.volt_max}')
                    if adc_res < self.volt_min:
                        volt_min = adc_res
                        print(f'Volt_min: {volt_min}, Volt_max: {self.volt_max}')

    """
    def audio_indicator (self, no_of_pixel: int) -> int:

        sma_gain: float = 1.0

        if no_of_pixel < 1:
            return 0
        else:
            adc_res: float = abs(((self.adc.read_u16()) / 65535.0) * 3.3 - 1.25)
            sma_avg: float = self.simple_moving_average_float(adc_res, self.sma_buffer)
            sma_avg = sma_avg * sma_gain
            no_of_pixel_display: int = int((sma_avg/0.54) * (no_of_pixel - 1))
            #print (f'No. of pixel: {no_of_pixel_display}, ADC value (SMA): {sma_avg}V') #Debug use
            if no_of_pixel_display > 7:
                no_of_pixel_display = 7
            if no_of_pixel_display < 0:
                no_of_pixel_display = 0

        return no_of_pixel_display
    """

