"""
Demo program of Pico-W for WiFi-Scan
"""

import machine, time, network, rp2

led = machine.Pin("LED", machine.Pin.OUT)
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))
wlan = network.WLAN()
wlan.active(True)

uart.write('Scanning\r\n')
uart.write(f'Status = {wlan.status()}')
while True:
    led.on()
    scan_result = wlan.scan()
    uart.write(f'Scan_result = {scan_result}\r\n')

    #for ap in scan_result:
    #uart.write('Channel: %d RSSI: %d Auth:%d BSSID:%s SSID: %s')

    uart.write('Message from ...MicroPython\r\n')
    time.sleep(1)
    led.off()
    time.sleep(0.1)