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
# along with Starker.  If not, see <http://www.gnu.org/licenses/>.

# This file interpret the raw data read from the heart rate monitor
import sys

from report import HRMReport
from exception import HRMException


class Parser(object):

    """Interpret the raw data from the HRM."""

    def __init__(self, stream):
        """Initializes the object"""
        super(Parser, self).__init__()
        self.report = HRMReport()
        position = 0
        buffer_ = map(ord, stream.read())
        i = 0

        while i < 3:
            if (buffer_[position] >> 4) == 1:
                position = self._parse_header(buffer_, position)

            if (buffer_[position] >> 4) == 2:
                position = self._parse_results(buffer_, position)

            if (buffer_[position] >> 4) == 3:
                position = self._parse_fitness(buffer_, position)

            i += 1
        self.report.dump()

    def _parse_header(self, buffer_, position):
        """Parse the data header."""
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
        print buffer_[position]
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

if __name__ == '__main__':
    data_source = sys.stdin
    parser = Parser(data_source)
