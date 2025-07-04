"""
API for digital compass QMC5883L.
Note that it is not compatible with HMC5883L
Supports:

The following coding is transferred from the C++ API IMU_Fusion_SYC.cpp

- Getting values of XYZ axis.
- Calculating Azimuth.
- Getting 16 point Azimuth bearing direction (0 - 15).
- Smoothing of XYZ readings via rolling averaging and min / max removal.
- Optional chipset modes (see below)

FROM QST QMC5883L Datasheet [https://nettigo.pl/attachments/440]
-----------------------------------------------
 MODE CONTROL (MODE)
	Standby			0x00
	Continuous		0x01

OUTPUT DATA RATE (ODR)
	10Hz        	0x00
	50Hz        	0x04
	100Hz       	0x08
	200Hz       	0x0C

FULL SCALE (RNG)
	2G          	0x00
	8G          	0x10

OVER SAMPLE RATIO (OSR)
	512         	0x00
	256         	0x40
	128         	0x80
	64          	0xC0

"""
import time

from QMC5883L_Cofig import *
from machine import I2C
import math

class QMC5883L(object):
    """
    Module for QMC5883L. Base class implement QMC5883L digital compass (3-axis magnetic sensor)
    """

    def __init__(self, obj_i2c, sma_buffer_size = 10) -> None:
        self._qmc_i2c: object = obj_i2c
        self._buf: bytearray = bytearray(1) #Single byte reading
        self._reading: bytearray =bytearray(6) #Byte array reading
        self.is_init_qmc5883l_successful: bool = False
        self.error_msg: str = ''
        self.fill_array_buf: list = []
        self.sma_buffer_size = sma_buffer_size

        try:
            self.qmc5883l_read_id()
            self.is_init_qmc5883l_successful = True
        except Exception as e:
            if not self.is_init_qmc5883l_successful:
                self.error_msg = f'Error in connecting QML5883L: {e}'

    # read from device
    def _read(self, buf:bytearray, memaddr: int, addr: int) -> None:    # addr = I2C device address, memaddr = memory location within the I2C device
        """
        Read bytes to pre-allocated buffer Caller traps OSError.
        """
        self._qmc_i2c.readfrom_mem_into(addr, memaddr, buf)

    # write to device
    def _write(self, data: int, memaddr: int, addr: int) -> None:
        """
        Perform a memory write. Caller should trap OSError.
        """
        self._buf[0] = data
        self._qmc_i2c.writeto_mem(addr, memaddr, self._buf)

    def to_signed_init_16(self, Unint16: int)-> int:
        """
        To convert unsigned int to signed int 16 bit
        :param Unint16:
        :return:
        """

        if Unint16 < 0x8000:
            return Unint16
        else:
            return Unint16 - 0x10000

    def simple_moving_average(self, val: int, array_list: list) -> float:
        """
        Moving average
        :param val:
        :param array_list:
        :return:
        """

        sum_val = 0
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


    def qmc5883l_read_id (self) -> bytearray:
        """
        Read device ID to verify device connection
        :return:
        """
        self._read(self._buf, QMC5883L_ID_REG, QMC5883L_I2C_ADDR)
        return self._buf

    def qmc5883l_init(self) -> None:
        """
        Initialize the QMC5883L chip with the following actions:-
        SET_RESET register = 0x01
        Set the following configuration at the Mode1 register
        - Mode = Continous (0x01)
        - Output data rate (ODR) = 200Hz (0x03)
        - Field range (RNG) =  8 Gauss (0x01)
        - Over sample ration (OSR) = 512 (0x00)
        :return:
        """
        MODE_STBY = 0x00 # Standby mode
        MODE_CONT = 0x01 # Continuous mode
        ODR_10HZ = 0x00 << 2# Output data rate: 10Hz
        ODR_50HZ = 0x01 << 2
        ODR_100HZ = 0x02 << 2
        ODR_200HZ = 0x03 << 2
        RNG_2G = 0x00 << 4 #2G mode
        RNG_8G = 0x01 << 4 #8G
        OSR_512 = 0x00 << 6 # Over sample ratio: 512
        OSR_256 = 0x01 << 6  # Over sample ratio: 256
        OSR_128 = 0x02 << 6  # Over sample ratio: 128
        OSR_064 = 0x03 << 6  # Over sample ratio: 64

        self._write(0x01, QMC5883L_SET_RESET_PERIOD_REG, QMC5883L_I2C_ADDR)
        self._write(MODE_CONT|ODR_200HZ|RNG_2G|OSR_512, QMC5883L_MODE1_REG, QMC5883L_I2C_ADDR)

    def qmc5883l_reset(self) -> None:
        """
        Device reset
        :return:
        """
        self._write(0x80, QMC5883L_MODE2_REG, QMC5883L_I2C_ADDR)

    def qmc58831_compass_read_sma (self, cal_data: tuple[float, float, float, float, float, float]=(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)) -> tuple[float, float, float, float]:
        """
        Compass read data with simple moving average (sma) post data process.
        It expects to give more stable data. The configuration will set compass ODR: 200Hz and get 10 data to do the sma
        :param cal_data:
        :return:
        """

        temp_buf_x: list = []
        temp_buf_y: list = []
        temp_buf_z: list = []
        _pos_x_raw_sma: float = 0.0
        _pos_y_raw_sma: float = 0.0
        _pos_z_raw_sma: float = 0.0
        res: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)

        for each_index in range(0, self.sma_buffer_size):
            # Read raw data from QMC device
            self._read(self._reading, QMC5883L_DATA_REG_IDX, QMC5883L_I2C_ADDR)
            _pos_x_raw: int = self.to_signed_init_16(self._reading[0] | self._reading[1] * 256)
            _pos_y_raw: int = self.to_signed_init_16(self._reading[2] | self._reading[3] * 256)
            _pos_z_raw: int = self.to_signed_init_16(self._reading[4] | self._reading[5] * 256)

            #Do SMA
            _pos_x_raw_sma = self.simple_moving_average(_pos_x_raw, temp_buf_x) / 16.0
            _pos_y_raw_sma = self.simple_moving_average(_pos_y_raw, temp_buf_y) / 16.0
            _pos_z_raw_sma = self.simple_moving_average(_pos_y_raw, temp_buf_z) /16.0

        # Final calculation
        _pos_x: float = (_pos_x_raw_sma - cal_data[0]) * cal_data[3]
        _pos_y: float = (_pos_y_raw_sma - cal_data[1]) * cal_data[4]
        _pos_z: float = (_pos_z_raw_sma - cal_data[2]) * cal_data[5]
        heading: float = (math.atan2(_pos_y, _pos_x) * 180.0 / math.pi) % 360.0
        res = (_pos_x, _pos_y, _pos_z, round(heading, 2))
        return res

    def qmc5883l_compass_read(self, cal_data: tuple[float, float, float, float, float, float]=(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)) -> tuple[float, float, float, float]:
        """
        Compass read data
        :param cal_data: Calibration data with tuple format: cal_data (x_offset, y_offset, z_offset, x_scale, y_scale, z_scale)
        :return:
        """
        res: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
        self._read(self._reading, QMC5883L_DATA_REG_IDX, QMC5883L_I2C_ADDR)
        _pos_x_raw: int = self.to_signed_init_16(self._reading[0] | self._reading[1] * 256)
        _pos_y_raw: int = self.to_signed_init_16(self._reading[2] | self._reading[3] * 256)
        _pos_z_raw: int = self.to_signed_init_16(self._reading[4] | self._reading[5] * 256)

        _pos_x: float = (_pos_x_raw - cal_data[0]) * cal_data[3]
        _pos_y: float = (_pos_y_raw - cal_data[1]) * cal_data[4]
        _pos_z: float = (_pos_z_raw - cal_data[2]) * cal_data[5]
        heading: float = (math.atan2(_pos_y, _pos_x) * 180.0 / math.pi) % 360.0
        res = (_pos_x, _pos_y, _pos_z, round(heading, 2))
        return res

    def qmc5883l_compass_calibration(self) -> tuple [float, float, float, float, float, float]:
        """
        Compass calibration.
        During the calibration, it is necessary
        Return is calibration data with tuple (x_offset, y_offset, z_offset, x_scale, y_scale, z_scale)
        :return: cal_data
        """
        count_loop: int = 30
        cal_data = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        qmc_x_min: int = 0
        qmc_x_max: int = 0
        qmc_y_min: int = 0
        qmc_y_max: int = 0

        print ('Compass calibration. Please press any key to continuous:')
        _=input()

        for each_cal_loop in range(0, count_loop):
            raw_data: tuple = self.qmc58831_compass_read_sma()
            if each_cal_loop == 0:
                qmc_x_min = raw_data[0]
                qmc_x_max = raw_data[0]
                qmc_y_min = raw_data[1]
                qmc_y_max = raw_data[1]
            else:
                # Look for x min/max values
                if raw_data[0] > qmc_x_max:
                    qmc_x_max = raw_data[0]
                if raw_data[0] < qmc_x_min:
                    qmc_x_min = raw_data[0]

                # Look for y min/max values
                if raw_data[1] > qmc_y_max:
                    qmc_y_max = raw_data[1]
                if raw_data[1] < qmc_y_min:
                    qmc_y_min = raw_data[1]

            time.sleep_ms(1000)

            print (f'X_val: {raw_data[0]}, Y_val: {raw_data[1]}')
            print (f'X(min, max) = ({qmc_x_min}, {qmc_x_max}). Y(min, max) = ({qmc_y_min}, {qmc_y_max}), Loop count={each_cal_loop}')

        x_offset: float = (qmc_x_max + qmc_x_min) / 2.0
        y_offset: float = (qmc_y_max + qmc_y_min) / 2.0
        x_scale: float = (qmc_y_max - qmc_y_min) / (qmc_x_max - qmc_x_min)

        cal_data=(x_offset, y_offset, 0.0, x_scale, 1.0, 1.0)

        print (f'Cal_data = {cal_data}...Press any key to continuous')
        _=input()

        return cal_data

