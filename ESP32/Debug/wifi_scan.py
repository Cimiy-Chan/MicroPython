"""
WiFi scan demo for ESP32
The network part is copied frp WiFi scan example for Arduino RP2040 Connect

"""
import machine, time, network
from machine import UART
import os


class FuncWifi:

    def __init__(self, counter):
        self.counter = counter
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.uart = UART(2)
        self.uart.init(baudrate=9600, bits=8, stop=1, parity=None)
        #Above: Use UART2 for ESP32. Warning: If wrong UART number (for example use UART0), it will be hang up and cannot
        #enter REPL mode and need to re-flash the firmware again.
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.led.off()
        self.system_info = os.uname()

    def display(self, msg):
        print (msg)
        self.uart.write(msg)
        self.uart.write('\r\n')

    def led_blink(self):
        self.led.on()
        time.sleep_ms(50)
        self.led.off()
        time.sleep_ms(50)

    def wifi_scan (self):
        while self.counter !=0:
            scan_result = self.wlan.scan()
            for ap in scan_result: #ap content is (ssid, bssid, ch, rssi, security, hidden)
                ssid = str(ap[0], 'utf-8')
                security = 'Unknown'
                hidden =''
                if ap[4] == 0: # Micropython doesn't support match-cas statement
                    security = 'Open'
                elif ap[4] == 1:
                    security = 'WEP'
                elif ap[4] == 2:
                    security = 'WPA-PSK'
                elif ap[4] == 3:
                    security = 'WPA2-PSK'
                elif ap[4] == 4:
                    security = 'WPA/WPA2-PSK'
                if ap[5]:
                    hidden = 'Yes'
                else:
                    hidden = 'No'
                self.display(f'SSID = {ssid}, RSSI = {ap[3]}dBm, ch = {ap[2]}, Security = {security}, Hidden = {hidden}')
                self.led_blink() # This provide 100ms delay
            self.counter = self.counter - 1
            self.display(f'Counter = {self.counter}')
            self.led_blink()
            time.sleep_ms(1000)
        self.display('End of Wifi Scan...')

# Main entry point
if __name__ == '__main__':
    obj_wifi_scan = FuncWifi(1)
    obj_wifi_scan.display(f'**** Board: {obj_wifi_scan.system_info[4]}, MicroPython: {obj_wifi_scan.system_info[3]} ****')
    obj_wifi_scan.wifi_scan()

