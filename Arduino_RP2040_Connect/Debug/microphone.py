"""
Demo program for running solid state microphone ST34DT05A
Notes:
    1. No other hardware is running in-between the PDM function because it runs as state-machine inside the
    MCU.
    2. At the irq_handler(), try-exception statement is added to avoid system hang up due to run-time error
       (possible runtime error: Schedule buffer full)
    3. Due to some firmware outdated issue, only MircoPython version 1.18.0 can be used. See os.uname() list as below

(sysname='rp2', nodename='rp2', release='1.18.0', version='v1.18 on 2022-01-17 (GNU 11.2.0 MinSizeRel)',
machine='Arduino Nano RP2040 Connect with RP2040')

However, under this old version, it doesn't support RGB LED at board.
"""


import time
from led_define import LED_BUILDIN
from wavsimple import wav
from machine import Pin, UART
import st34dt05a as pdm
import uos

class FuncAudio:
    def __init__(self, counter, filename):
        self.counter = counter
        self.filename = filename
        self.pcm_rate = 8_000 # Hz - default is 12kHz i.e. 3.072MHz bit-sample rate
        pdm.bit_sample_freq = self.pcm_rate * 300
        self.pdm_clk = Pin(23)
        self.pdm_data = Pin(22)

        self.led = Pin(LED_BUILDIN, Pin.OUT)
        self.uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), timeout=1000)
        self.record_flag = False
        self.led.off()

    def buffer_handler(self, inactive_buf):
        global record_flag
        if self.record_flag:
            self.obj_wav.write(pdm.get_buffer(inactive_buf))

    def display(self, msg, is_return = True):
        print(msg)
        self.uart.write(msg)
        if is_return:
            self.uart.write('\r\n')

    def led_blink (self):
        """
        LED blink - Added by Cimiy
        :return:
        """
        self.led.toggle()
        time.sleep_ms(50)
        self.led.toggle()
        time.sleep_ms(50)

    def audio_sampling(self, sample_len):
        self.obj_wav = wav(self.filename, SampleRate=self.pcm_rate)
        pdm.init(self.pdm_clk, self.pdm_data, handler=self.buffer_handler)
        pdm.start()
        time.sleep(1)  # wait whilst StateMachine inits
        self.record_flag = True
        time.sleep(sample_len)
        self.display('End of sampling...')
        self.record_flag = False
        self.obj_wav.close()
        file_status = uos.stat(self.filename)
        self.display(f'Wavefile: "{self.filename}" Size:{file_status[6]} Bytes')
        time.sleep(1)
        pdm.stop()

    def delay_with_blink (self):
        self.counter = self.counter * 10 - 1 # Each loop contain around 0.1 second

        while self.counter != 0:
            self.led_blink() # Each led_blink use 0.1 sec
            self.counter = self.counter - 1

    def user_input(self):
        self.display('\r\nPress "S" or "s" to start sampling ')
        is_wait = True
        decoded_str = ''
        while is_wait:
            self.display('In while loop....')
            uart_reading = self.uart.read(1)
            if uart_reading != None:
                self.display(f'Result={uart_reading.decode('utf-8')}')
                decoded_str = uart_reading.decode('utf-8')
            if decoded_str == 's' or decoded_str == 'S':
                self.display(f'Process now...')
                is_wait = False



if __name__== '__main__':
    sample_len = 10 #Len in second
    no_of_trial = 1
    counter = 0
    obj_func_audio = FuncAudio(sample_len, 'output.wav')
    obj_func_audio.display('******* Welcome to use Arduino RP2040 Connect MicroPhone Demo *******')
    obj_func_audio.display(f'The application will sample audio {no_of_trial} trial/s with {sample_len} secs each trial\r\n')

    while counter < no_of_trial:
        #obj_func_audio.user_input()
        obj_func_audio.led_blink()
        time.sleep(0.5)
        obj_func_audio.display(f'Start audio sampling with {sample_len} seconds for trial {counter + 1} ')
        obj_func_audio.audio_sampling(sample_len)
        counter = counter + 1
        obj_func_audio.led_blink()
    obj_func_audio.display('End of application...')
