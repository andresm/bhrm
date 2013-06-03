#! /usr/bin/python
# -*- coding: utf-8 *-*

# This file is part of the Beurer HRM python interface.
# Copyright (C) 2013 Andres Moreno

# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

# This file interpret the raw data read from the heart rate monitor
import sys
import getopt
import logging

from report import HRMReport
from exception import HRMException
from lap import Lap

__VERSION__ = 0.1


class Parser(object):

    """Interpret the raw data from the HRM."""

    def __init__(self, stream):
        """Initializes the object"""
        super(Parser, self).__init__()
        self.report = HRMReport()
        position = 0
        buffer_ = map(ord, stream.read())
        i = 0

        while i < 6:
            if (buffer_[position] >> 4) == 1:
                position = self._parse_header(buffer_, position)

            if (buffer_[position] >> 4) == 2:
                position = self._parse_results(buffer_, position)

            if (buffer_[position] >> 4) == 3:
                position = self._parse_fitness(buffer_, position)

            if (buffer_[position] >> 4) == 4:
                position = self._parse_heart_rates(buffer_, position)

            if (buffer_[position] >> 4) == 5:
                position = self._parse_speed(buffer_, position)

            if (buffer_[position] >> 4) == 6:
                position = self._parse_lap_results(buffer_, position)

            i += 1
        self.report.dump()

    def _parse_header(self, buffer_, position):
        """Parse the data header."""
        logging.info('Parsing header section.')
        if not self._checkchecksum(buffer_, position):
            raise HRMException('Checksum is not correct.')

        # Gender
        self.report.gender = (buffer_[position + 3] >> 7)
        self.report.age = (buffer_[position + 3] & 0x7F)
        self.report.weight = (buffer_[position + 4])
        self.report.height = (buffer_[position + 5])
        self.report.hr_hlimit = (buffer_[position + 6])
        self.report.hr_llimit = buffer_[position + 7]
        self.report.hr_maximun = buffer_[position + 8]
        return position + buffer_[position + 1] + 4

    def _parse_fitness(self, buffer_, position):
        """Parse fitness section."""
        logging.info('Parsing fitness test section.')
        base_year = 2000
        self.report.fitness_flag = buffer_[position + 2]
        self.report.min = self._bcd2hex(buffer_[position + 3])
        self.report.hr = self._bcd2hex(buffer_[position + 4])
        self.report.day = self._bcd2hex(buffer_[position + 5])
        self.report.month = self._bcd2hex(buffer_[position + 6])
        self.report.year = self._bcd2hex(buffer_[position + 7]) + base_year
        self.report.fitness = buffer_[position + 8]
        self.report.vo2max = buffer_[position + 9]
        return position + buffer_[position + 1] + 4

    def _parse_results(self, buffer_, position):
        """Parse the results section."""
        logging.info('Parsing global results section.')
        self.report.kcal = buffer_[position + 4]
        self.report.fat = buffer_[position + 6]
        self.report.tr_intime_seg = self._bcd2hex(buffer_[position + 8])
        self.report.tr_intime_min = self._bcd2hex(buffer_[position + 9])
        self.report.tr_intime_hr = self._bcd2hex(buffer_[position + 10])
        self.report.tr_ltime_seg = self._bcd2hex(buffer_[position + 11])
        self.report.tr_ltime_min = self._bcd2hex(buffer_[position + 12])
        self.report.tr_ltime_hr = self._bcd2hex(buffer_[position + 13])
        self.report.tr_htime_seg = self._bcd2hex(buffer_[position + 14])
        self.report.tr_htime_min = self._bcd2hex(buffer_[position + 15])
        self.report.tr_htime_hr = self._bcd2hex(buffer_[position + 16])
        self.report.tr_hrmax = buffer_[position + 17]
        self.report.tr_hravg = buffer_[position + 18]
        return position + buffer_[position + 1] + 4

    def _parse_heart_rates(self, buffer_, position):
        """Parses the heart rates section."""
        logging.info('Parsing heart rates section.')
        datalen = (buffer_[position + 2] << 4) + buffer_[position + 1]
        self.report.hr_data_hour = buffer_[position + 4]
        self.report.hr_data_min = buffer_[position + 5]
        hr_offset = 6
        while hr_offset < datalen + 3:
            self.report.hr_data.append(buffer_[position + hr_offset])
            hr_offset = hr_offset + 1

        return position + buffer_[position + 1] + 4

    def _parse_speed(self, buffer_, position):
        """Parses the heart rates section."""
        # Distance?
        logging.info('Parsing distance section.')
        return position + buffer_[position + 1] + 4

    def _parse_lap_results(self, buffer_, position):
        """Parse the lap result section."""
        logging.info('Parsing lap results section.')
        len_ = buffer_[position + 1] + 4
        lap_offset = 10
        id_ = 0
        while lap_offset < len_ - 1:
            lap = Lap(id_)
            lap.seg = self._bcd2hex(buffer_[position + lap_offset])
            lap.min = self._bcd2hex(buffer_[position + lap_offset + 1])
            lap.hour = self._bcd2hex(buffer_[position + lap_offset + 2])
            lap.hr = buffer_[position + lap_offset + 3]
            self.report.laps.append(lap)
            lap_offset = lap_offset + 7
            id_ = id_ + 1

        return position + buffer_[position + 1] + 4

    def _checkchecksum(self, buffer_, position):
        """Checks the data chunk checksum."""
        length = buffer_[position + 1] + 2
        accumulator = 0
        for i in range(length):
            accumulator += buffer_[position + i]

        return True

    def _bcd2hex(self, byte):
        """Returns byte value of a BCD byte."""
        low = byte & 0xF
        high = (byte >> 4) & 0xF
        return low + high * 10


def _show_help():
    """Show the help message."""
    print 'Beurer Heart Rate Monitor Parser version: %s' % __VERSION__
    print 'This software interprets the data read from the Beurer HRMs'
    print 'If no input file is given, then the data is read from stdin'
    print ''
    print 'Use:'
    print ''
    print '  parser.py [-h] [-i inputfile]'
    print ''
    print '  -h,        Display this help message'
    print '  -i,        Input file'
    print '  -v level,  Set the verbose level'
    print '             1: Debug level'
    print '             2: Info level'


if __name__ == '__main__':
    inputfile = sys.stdin

    # Parser command line options
    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "hi:v:")

        for option in opts:
            if option[0] == '-i':
                inputfile = open(option[1], 'r')

            elif option[0] == '-h':
                _show_help()
                exit(0)

            elif option[0] == '-v':
                if option[1] == '1':
                    level = logging.DEBUG

                elif option[1] == '2':
                    level = logging.INFO

                logging.basicConfig(level=level)

    except getopt.GetoptError:
        _show_help()
        sys.exit(2)

    parser = Parser(inputfile)
    inputfile.close()
    exit(0)