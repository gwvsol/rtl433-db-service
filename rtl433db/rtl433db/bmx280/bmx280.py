from smbus2 import SMBus

from .bmx280_register import BME280_DIG_T1, BME280_DIG_T2, \
                             BME280_DIG_T3, BME280_DIG_P1, \
                             BME280_DIG_P2, BME280_DIG_P3, \
                             BME280_DIG_P4, BME280_DIG_P5, \
                             BME280_DIG_P6, BME280_DIG_P7, \
                             BME280_DIG_P8, BME280_DIG_P9, \
                             BME280_DIG_H1, BME280_DIG_H2, \
                             BME280_DIG_H3, BME280_DIG_H4, \
                             BME280_DIG_H5, BME280_DIG_H6
from .bmx280_register import BME280_CONFIG, BME280_CONFIG_SET, \
                             BME280_CONTROL_HUM, BME280_CONTROL_HUM_SET, \
                             BME280_CONTROL_MEAS, BME280_CONTROL_MEAS_SET, \
                             BME280_TEMP, BME280_PRESSURE, BME280_HUMIDITY


# BME280 default address.
BME280_I2CADDR = 0x76


class BME280(object):
    def __init__(self, port=1, address=BME280_I2CADDR):
        self.bus: SMBus = SMBus(port)
        self.address = address

        # Read calibration values
        self.dig_t1 = self.read_word(BME280_DIG_T1)  # Unsigned
        self.dig_t2 = self.read_word_sign(BME280_DIG_T2)
        self.dig_t3 = self.read_word_sign(BME280_DIG_T3)
        self.dig_p1 = self.read_word(BME280_DIG_P1)  # Unsigned
        self.dig_p2 = self.read_word_sign(BME280_DIG_P2)
        self.dig_p3 = self.read_word_sign(BME280_DIG_P3)
        self.dig_p4 = self.read_word_sign(BME280_DIG_P4)
        self.dig_p5 = self.read_word_sign(BME280_DIG_P5)
        self.dig_p6 = self.read_word_sign(BME280_DIG_P6)
        self.dig_p7 = self.read_word_sign(BME280_DIG_P7)
        self.dig_p8 = self.read_word_sign(BME280_DIG_P8)
        self.dig_p9 = self.read_word_sign(BME280_DIG_P9)

        self.dig_h1 = self.read_byte(BME280_DIG_H1)	 # unsigned char
        self.dig_h2 = self.read_word_sign(BME280_DIG_H2)
        self.dig_h3 = self.read_byte(BME280_DIG_H3)	 # unsigned char

        self.dig_h4 = (self.read_byte(BME280_DIG_H4) << 24) >> 20
        self.dig_h4 = self.dig_h4 | self.read_byte(BME280_DIG_H4+1) & 0x0F

        self.dig_h5 = (self.read_byte(BME280_DIG_H5 + 1) << 24) >> 20
        self.dig_h5 = self.dig_h5 | (self.read_byte(BME280_DIG_H5) >> 4) & 0x0F

        self.dig_h6 = self.read_byte(BME280_DIG_H6)	 # signed char
        if self.dig_h6 > 127:
            self.dig_h6 = 127 - self.dig_h6

        # Set Configuration
        self.write_byte(BME280_CONFIG, BME280_CONFIG_SET)
        self.write_byte(BME280_CONTROL_HUM, BME280_CONTROL_HUM_SET)
        self.write_byte(BME280_CONTROL_MEAS, BME280_CONTROL_MEAS_SET)

    def get_data(self):
        adc_t = self.read_adc_long(BME280_TEMP)
        adc_p = self.read_adc_long(BME280_PRESSURE)
        adc_h = self.read_adc_word(BME280_HUMIDITY)

        var1 = (adc_t/16384.0 - self.dig_t1/1024.0) * self.dig_t2
        var2 = ((adc_t/131072.0 - self.dig_t1/8192.0) *
                (adc_t/131072.0 - self.dig_t1/8192.0)) * self.dig_t3
        t_fine = (var1 + var2)
        temperature = round((t_fine / 5120.0), 2)

        var1 = (t_fine/2.0) - 64000.0
        var2 = var1 * var1 * self.dig_p6 / 32768.0
        var2 = var2 + var1 * self.dig_p5 * 2.0
        var2 = (var2/4.0)+(self.dig_p4 * 65536.0)
        var1 = (self.dig_p3 *
                var1 * var1 /
                524288.0 +
                self.dig_p2 *
                var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0)*self.dig_p1

        # Avoid exception caused by division by zero
        if (var1 == 0.0):
            return -1

        p = 1048576.0 - adc_p
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = self.dig_p9 * p * p / 2147483648.0
        var2 = p * self.dig_p8 / 32768.0
        pressure = round((p + (var1 + var2 + self.dig_p7) / 16.0), 2)
        mmhg = round(pressure / 133.3, 2)

        var_H = t_fine - 76800.0
        var_H = (adc_h -
                 (self.dig_h4 * 64.0 + self.dig_h5 / 16384.0 * var_H)) * \
                (self.dig_h2 / 65536.0 *
                 (1.0 + self.dig_h6 / 67108864.0 * var_H *
                  (1.0+self.dig_h3 / 67108864.0 * var_H)))
        humidity = round(var_H * (1.0 - self.dig_h1*var_H/524288.0), 2)

        if (humidity > 100.0):
            humidity = 100.0
        else:
            if (humidity < 0.0):
                humidity = 0.0

        return {'t': temperature, 'p': pressure, 'h': humidity, 'mmhg': mmhg}

    def get_altitude(self, pressure):
        temp = pressure/101325
        temp = 1-pow(temp, 0.19029)
        altitude = round(44330 * temp, 3)
        return altitude

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        # ATANTION! Joke from Bosch! LBS before HBS.
        # For calibration registers only!
        lbs = self.bus.read_byte_data(self.address, adr)
        hbs = self.bus.read_byte_data(self.address, adr+1)
        return (hbs << 8) + lbs

    def read_word_sign(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def read_adc_long(self, adr):
        mbs = self.bus.read_byte_data(self.address, adr)
        lbs = self.bus.read_byte_data(self.address, adr+1)
        xbs = self.bus.read_byte_data(self.address, adr+2)
        val = (mbs << 16) + (lbs << 8) + xbs
        val = (val >> 4)
        return val

    def read_adc_word(self, adr):
        mbs = self.bus.read_byte_data(self.address, adr)
        lbs = self.bus.read_byte_data(self.address, adr+1)
        val = (mbs << 8) + lbs
        return val

    def write_byte(self, adr, byte):
        self.bus.write_byte_data(self.address, adr, byte)
