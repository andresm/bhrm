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

# This file show the data read from the heart rate monitor using matplotlib
import getopt
from matplotlib import use
use('AGG')
from matplotlib import pyplot as plt
from matplotlib.pylab import *
from matplotlib import dates
from PySide import QtGui
import datetime

from parser import Parser

__VERSION__ = 0.1


class Visualizer(object):

    """Show the heart rate data in a window using Qt."""

    def __init__(self):
        """Initializes the object."""

    def _get_data(self, stream):
        """Get the necessary data to plot."""
        parser = Parser()
        report = parser.parse(stream)
        hr_data = report.hr_data
        start_time = datetime.datetime(report.lr_data_year,
                                       report.lr_data_month,
                                       report.lr_data_day,
                                       report.hr_data_hour,
                                       report.hr_data_min)
        delta_time = datetime.timedelta(minutes=1)
        time_data = []
        for i in range(len(hr_data)):
            time_data.append(start_time + delta_time * i)

        time_data = dates.date2num(time_data)

        return (hr_data, time_data)

    def plot(self, stream):
        """Plot the HR data."""
        (hr_data, time_data) = self._get_data(stream)
        self._plot(hr_data, time_data)

    def _plot(self, hr_data, time_data):
        """Plot the data into the window"""
        plot(time_data, hr_data, linewidth=2, linestyle='-',
             marker=r'$\dot$', markersize=5, label='Heart rates')
        grid(True)
        plt.xticks(rotation='vertical')
        legend(loc='upper left')
        plt.subplots_adjust(bottom=.2)
        date_format = dates.DateFormatter('%m/%d %H:%M')

        figure = gcf()
        ax = figure.add_subplot(111)
        ax.xaxis.set_major_formatter(date_format)

        figure.canvas.draw()
        stringBuffer = figure.canvas.buffer_rgba(0, 0)
        l, b, w, h = figure.bbox.bounds

        # Get it into Qt
        app = QtGui.QApplication(sys.argv)
        qImage = QtGui.QImage(stringBuffer, w, h, QtGui.QImage.Format_ARGB32)
        scene = QtGui.QGraphicsScene()
        view = QtGui.QGraphicsView(scene)
        pixmap = QtGui.QPixmap.fromImage(qImage)
        pixmapItem = QtGui.QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmapItem)
        view.show()

        app.exec_()


def _show_help():
    """Show the help message."""
    print 'Beurer Heart Rate Monitor Visualizer version: %s' % __VERSION__
    print 'This software shows the heart rate data'
    print ''
    print 'Use:'
    print ''
    print '  beurer.py [-h] [-i inputfile]'
    print ''
    print '  -h,        Display this help message'
    print '  -i file,   Read data from file'


if __name__ == '__main__':
    inputfile = sys.stdin

    # Parser command line options
    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "hi:")

        for option in opts:
            if option[0] == '-i':
                inputfile = open(option[1], 'r')

            elif option[0] == '-h':
                _show_help()
                exit(0)

    except getopt.GetoptError:
        _show_help()
        sys.exit(2)

    v = Visualizer()
    v.plot(inputfile)
    inputfile.close()