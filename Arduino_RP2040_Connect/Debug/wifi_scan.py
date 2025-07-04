"""
WiFi scan example for Arduino RP2040 Connect
Since there is out dated firmware NNA module (Ver: 1.4.8), only
older version of MicroPython ver 1.18 is used.

Newer MicroPython version will make board hang up at the function of wlan.active(True)
"""
import machine, time, network
import led_define
import os


class FuncWifi:

    def __init__(self, counter):
        self.counter = counter
        self.led = machine.Pin(led_define.LEDR, machine.Pin.OUT)
        self.uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1)) #Use UART 0 for PyCharm, 1 for Thonny
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.led.off()
        self.system_info = os.uname()

    def display(self, msg):
        print (msg)
        self.uart.write(msg)
        self.uart.write('\r\n')

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
                self.led.toggle()
                time.sleep_ms(100)
            self.counter = self.counter - 1
            self.display(f'Counter = {self.counter}')
            self.led.off()
            time.sleep_ms(1000)
        self.display('End of Wifi Scan...')

# Main entry point
if __name__ == '__main__':
    obj_wifi_scan = FuncWifi(1)
    obj_wifi_scan.display(f'**** Board: {obj_wifi_scan.system_info[4]}, MicroPython: {obj_wifi_scan.system_info[3]}')
    obj_wifi_scan.wifi_scan()

