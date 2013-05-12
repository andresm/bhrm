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
        # General information
        self.gender = True
        self.age = 0
        self.weight = 0
        self.height = 0
        self.hr_llimit = 0
        self.hr_hlimit = 0
        self.hr_maximun = 0
        # Fitness information
        self.fitness_flag = 0
        self.min = 0
        self.hr = 0
        self.day = 0
        self.month = 0
        self.year = 0
        self.fitness = 0
        self.vo2max = 0
        # Results information
        self.fat = 0
        self.kcal = 0
        self.tr_hrmax = 0
        self.tr_ltime_seg = 0
        self.tr_ltime_min = 0
        self.tr_ltime_hr = 0
        self.tr_intime_seg = 0
        self.tr_intime_min = 0
        self.tr_intime_hr = 0
        self.tr_htime_hr = 0
        self.tr_htime_hr = 0
        self.tr_htime_hr = 0

    def dump(self):
        """Dumps the report data."""
        print 'Heart Rate Monitor Report'
        print '-------------------------'
        print 'Gender: %s' % (self.gender and 'M' or 'F')
        print 'Age: %s' % self.age
        print 'Weight: %s' % self.weight
        print 'Height: %s' % self.height
        print 'Heart rate high limit: %s' % self.hr_hlimit
        print 'Heart rate low limit: %s' % self.hr_llimit
        print 'Heart rate maximun: %s' % self.hr_maximun
        print 'Fitness flag: %s' % self.fitness_flag
        print 'Updated on : %s-%s-%s %s:%s' % (self.year, self.month, self.day,
                                        self.hr, self.min)
        print 'Fitness: %s' % self.fitness
        print 'Vo2 Max: %s' % self.vo2max
        print 'Fat: %s' % self.fat
        print 'Kcal: %s' % self.kcal
        print 'Training Max HR: %s' % self.tr_hrmax
        print 'Training AVG HR: %s' % self.tr_hravg
        print 'Training time below target HR: %s:%s:%s' % (self.tr_ltime_hr,
                                                            self.tr_ltime_min,
                                                            self.tr_ltime_seg)
        print 'Training time in target HR: %s:%s:%s' % (self.tr_intime_hr,
                                                            self.tr_intime_min,
                                                            self.tr_intime_seg)
        print 'Training time over target HR: %s:%s:%s' % (self.tr_htime_hr,
                                                            self.tr_htime_min,
                                                            self.tr_htime_seg)