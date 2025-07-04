"""
`ltr381rgb`
================================================================================
Python LTR381RGB optical sensor library
* Author(s): Cimiy Chan
Implementation Notes
--------------------
**Software and Dependencies:**
It is written for MicroPython.
"""

from ltr381rgb_config import *
import time

class LTR381RGB(object):
    """
    Module for QMC5883L. Base class implement QMC5883L digital compass (3-axis magnetic sensor)
    """

    def __init__(self, obj_i2c, wfac: float = 1.0) -> None:
        """
        wfac = Window factor. It is used to compensate light loss due to the lower
        transmission rate from the coated-ink.
        a. WFAC = 1 for NO window / clear window glass.
        b. WFAC >1 device under tinted window glass. Calibrate under white LED.
        """
        self.wfac: float = wfac
        self._ltr_i2c: object = obj_i2c
        self._buf_1: bytearray = bytearray(1) #Single byte reading
        self._buf_12: bytearray =bytearray(12) #Byte array reading, 12 bytes read
        self.is_init_ltr381rgb_successful: bool = False
        self.error_msg: str = ''
        self.fill_array_buf: list = []
        self.gain = 1.0
        self. integration_time = 1.0


    # read from device
    def _read(self, buf:bytearray, memaddr: int, i2c_addr: int) -> None:    # addr = I2C device address, memaddr = memory location within the I2C device
        """
        Read bytes to pre-allocated buffer Caller traps OSError.
        """
        self._ltr_i2c.readfrom_mem_into(i2c_addr, memaddr, buf)

    # write to device
    def _write(self, data: int, memaddr: int, i2c_addr: int) -> None:
        """
        Perform a memory write. Caller should trap OSError.
        """
        self._buf_1[0] = data
        self._ltr_i2c.writeto_mem(i2c_addr, memaddr, self._buf_1)


    def ltr381rgb_part_id (self) -> bytearray:
        """
        Read device ID to verify device connection
        :return:
        """
        self._read(self._buf_1, LTR381RGB_PART_ID, LTR381RGB_I2C_ADDR)
        return self._buf_1

    def ltr381rgb_init(self):
        """
        Init LTR381RGB
        1. MAIN_CTRL Reg: 0x00, Data: 0x06 -> ALS Active and CS mode = CS -> All light sensor channel activated (RGB + IR + COMP)
        2. ALS_CS_MEAS_RATE Reg:0x04, Data: 0x41 -> Resolution=16 bit, Meas Rate=50ms
        3. ALS_CS_GAIN Reg: 0x05, Data: 0x00 -> Gain=1
        :return:
        """
        self._write(ALS_ACTIVE | CS_MODE, LTR381RGB_MAIN_CTRL, LTR381RGB_I2C_ADDR)
        self._write(RATE_50_MS | RESOLUTION_16_BIT, LTR381RGB_ALS_CS_MEAS_RATE, LTR381RGB_I2C_ADDR)
        self._write(GAIN_X1, LTR381RGB_ALS_CS_GAIN, LTR381RGB_I2C_ADDR)

    def ltr381rgb_main_status (self) -> bytearray:
        """
        Read MAIN_STATUS Register
        :return:
        """
        self._read(self._buf_1, LTR381RGB_MAIN_STATUS, LTR381RGB_I2C_ADDR)
        return self._buf_1

    def ltr381rgb_raw_data (self) -> tuple[int, int, int, int]:
        """
        Get Raw data from the sensor. It will get four group of sensor values:
        ir = Infra-ree
        G, R, B = Green\, Red and Blue.
        :return:
        """
        self._read(self._buf_12, LTR381RGB_CS_DATA_IR_0, LTR381RGB_I2C_ADDR)

        ir = self._buf_12[2] << 16 | self._buf_12[1] << 8 | self._buf_12[0]
        g = self._buf_12[5] << 16 | self._buf_12[4] << 8 | self._buf_12[3]
        r = self._buf_12[8] << 16 | self._buf_12[7] << 8 | self._buf_12[6]
        b = self._buf_12[11] << 16 | self._buf_12[10] << 8 | self._buf_12[9]

        return (ir, r, g, b) # Return as RGB format

    def ltr381rgb_lux (self) -> float:
        """
        It will calculate the Lux value based on the formula provided by datasheet
        :return:
        """

        ir, r, g, b = self.ltr381rgb_raw_data()
        print (f'LUX (RGB): {ir}, {r}, {g}, {b}')
        return 0.8 * g / (self.gain * self.integration_time) * (1 - 0.033 * ir / g) * self.wfac





