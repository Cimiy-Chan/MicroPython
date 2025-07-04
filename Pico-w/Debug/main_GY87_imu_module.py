"""
Demo application of GY-87 IMU module
For the GY-87 Module, there are three sensors
- BMP180 (0x77) Bosh sensortec air pressure sensor
- QMC5883L (0x0D) 3-axis digital compass
- MPU6050 (0x68) Acceleerometer and gyroscope
"""
import time
import json
from MPU5060 import MPU6050
from BMP180 import BMP180
from QMC5883L import QMC5883L
from machine import Pin, I2C


if __name__ == '__main__':

    led = Pin("LED", Pin.OUT)
    led.on()
    led_ext = Pin(3, Pin.OUT)
    button = Pin(2, Pin.IN, Pin.PULL_DOWN)
    button_current_state: int = 0
    button_next_state: int = 0
    cal_data: tuple[float, float, float, float, float, float] = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)

    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    imu = MPU6050(i2c)
    bmp = BMP180(i2c)
    bmp.over_sample = 2
    bmp.sea_level = 101325

    qmc = QMC5883L(i2c, 100)
    if not qmc.is_init_qmc5883l_successful:
        print(qmc.error_msg)
        print('Application halt...')
        while True:
            time.sleep(0.01) # Create dummy dead loop
    else:
        qmc.qmc5883l_reset()
        qmc.qmc5883l_init()

    # Get QMC5883L cal data from JSON config file
    f_json = open('qmc5883l_config.json', 'r')
    qmc_cal_data = json.load(f_json)
    is_compass_calibrated: bool = qmc_cal_data['is_calibrated']
    x_offset: float = qmc_cal_data['cal_data']['x_offset']
    y_offset: float = qmc_cal_data['cal_data']['y_offset']
    z_offset: float = qmc_cal_data['cal_data']['z_offset']
    x_scale: float = qmc_cal_data['cal_data']['x_scale']
    y_scale: float = qmc_cal_data['cal_data']['y_scale']
    z_scale: float = qmc_cal_data['cal_data']['z_scale']

    while True:
        led.on()
        # Data from MPU6050
        ax=round(imu.accel.x,2)
        ay=round(imu.accel.y,2)
        az=round(imu.accel.z,2)
        gx=round(imu.gyro.x)
        gy=round(imu.gyro.y)
        gz=round(imu.gyro.z)
        tem=round(imu.temperature,2)
        print(f'MPU6050 Data: ax={ax},ay={ay},az={az}, gx={gx}, gy={gy}, gz={gz}, Temperature={tem}C')

        # Data from BMP180
        tempC = bmp.temperature        #get the temperature in degree celsius
        pres_hPa = bmp.pressure        #get the pressure in hpa
        altitude = round(bmp.altitude, 2)        #get the altitude
        print (f'BMP180 Data: temp={tempC}C, Pressure={pres_hPa}hPa, Altitude={altitude}m')

        # Data from QMC5883L
        qmc_id = qmc.qmc5883l_read_id()
        print (f'QMC5883L Device ID: 0x{qmc_id.hex()}')
        if not is_compass_calibrated:
            cal_data = qmc.qmc5883l_compass_calibration()
            is_compass_calibrated = True

        # pos =  qmc.qmc58831_compass_read_sma(cal_data=cal_data)
        pos = qmc.qmc58831_compass_read_sma(cal_data=(x_offset, y_offset, z_offset, x_scale, y_scale, z_scale)) # Manual calibration data setting
        print (f'(X,Y,Z, Heading)={pos}')

        time.sleep_ms(300)
        led.off()
        time.sleep_ms(300)
        button_current_state = button.value()
        if button_current_state != button_next_state:
            print ('End of application...')
            break
    led_ext.on()
    time.sleep(1)
    led_ext.off()
    #End of program