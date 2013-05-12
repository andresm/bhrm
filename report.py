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

# This file provides a class to encapsulate the interpreted data read from
# the heart rate monitor


class HRMReport(object):

    """Encapsulation of HRM report data interpretation."""

    def __init__(self):
        """Initialize data."""
        super(HRMReport, self).__init__()
        self.gender = True
        self.height = 0
        self.hr_llimit = 0
        self.hr_hlimit = 0
        self.hr_maximun = 0
        self.fitness_flag = 0
        self.min = 0
        self.hr = 0
        self.day = 0
        self.month = 0
        self.year = 0
        self.fitness = 0
        self.vo2max = 0

    def dump(self):
        """Dumps the report data."""
        print 'Heart Rate Monitor Report'
        print '-------------------------'
        print 'Gender: %s' % (self.gender and 'M' or 'F')
        print 'Height: %s' % self.height
        print 'Heart rate high limit: %s' % self.hr_hlimit
        print 'Heart rate low limit: %s' % self.hr_llimit
        print 'Heart rate maximun: %s' % self.hr_maximun
        print 'Fitness flag: %s' % self.fitness_flag
        print 'Updated on : %s-%s-%s %s:%s' % (self.year, self.month, self.day,
                                        self.hr, self.min)
        print 'Fitness: %s' % self.fitness
        print 'Vo2 Max: %s' % self.vo2max
