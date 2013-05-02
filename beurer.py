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

# This file connects to Beurer Heart Rate monitors using the USB port
# to get the trainig data.
#
# If you are experiencing problems with your HRM not beign detecte under
# linux, be sure to add it to udev rules
#
import usb.core
import usb.util

# TODO: Command line interface
# TODO: Complete the switch case for baud rates
# TODO: Separate delete data function
# TODO: Check number of bytes recieved


class HRMException(Exception):

    """Exceptions thrown by the HRM"""
    def __init__(self, msg):
        """Initialize object."""
        super(HRMException, self).__init__()
        self.msg = msg

    def __str__(self):
        """Returns error message."""
        return self.msg


class HeartRateMonitor():

    """Beurar Heart Rate Monitor Interface class."""

    def __init__(self):
        """Initialize the heart rate monitor.

        This function sets the initial parameters previous to any
        communication.

        """
        self.id_vendor = 0x0e6a  # MegaWin
        self.id_product = 0x0101  # Usb Bridge
        self.device = None

    def open(self):
        """Open connection to device"""
        self.device = usb.core.find(idVendor=self.id_vendor,
                                    idProduct=self.id_product)
        if self.device is None:
            raise HRMException("Heart Rate Monitor not found!")

        self.device.set_configuration()

    def close(self):
        """Close the device."""
        self.device.close()

    def download_data(self):
        """Connect and get all the training data from device"""
        self.open()
        self.set_baud_rate(9600)
        self.set_time_out(0xD0)
        self._get_all_data()
        self.close()

    def _recieve_command_data(self):
        """Get data from a command sent to the device."""
        bm_request_type = 0xC0
        b_request = 0x4
        value = 0x5002
        index = 0x0
        length = 0xFA0
        timeout = 10000
        response = self.device.ctrl_transfer(bm_request_type, b_request, value,
                                            index, length, timeout)
        return response

    def _recieve_checksum(self):
        """Returns a single recieved message checksum."""
        bm_request_type = 0xC0
        b_request = 0x4
        value = 0x500D
        index = 0x0
        length = 0x2
        timeout = 1000
        response = self.device.ctrl_transfer(bm_request_type, b_request, value,
                                            index, length, timeout)
        return response

    def send_message(self, msg):
        """Send a single control message."""
        bm_request_type = 0x40
        b_request = 0x4
        value = 0x5001
        index = 0x0
        timeout = 1000
        response = self.device.ctrl_transfer(bm_request_type, b_request,
                                            value, index, msg, timeout)
        return response

    def _check_msg_checksum(self, msg, checksum):
        """Check recieved message checksum."""
        valid = False
        accumulator = 0x0
        for byte in msg[:-1]:
            accumulator += byte

        valid = (accumulator & 0x0FF) == msg[-1]
        return valid

    def _get_all_data(self):
        """Get all the training data."""
        msg = '\x91\x01\x00\x01\x93'  # Initial message
        while True:
            if ord(msg[3]) == 0:
                break

            self.send_message(msg)
            response = self._recieve_command_data()
            print response
            checksum = self._recieve_checksum()
            if not self._check_msg_checksum(response, checksum):
                raise HRMException('Transmission error, bad checksum.')

            msg = self._next_message(response)

    def _next_message(self, last_message):
        """Returns next message.

        Messages to be send to the HRM are dependant on the last response
        from the HRM, this function generates the next message to be send
        from the last message recieved.

        """
        msg = ''
        msg += chr((last_message[0] & 0x0F) - 0x60 & 0xFF)
        msg += chr(0x01)
        msg += chr(0x00)
        msg += chr(last_message[0] >> 4)  # Key byte (stop byte)
        msg += chr(self._checksum(msg))
        return msg

    def _checksum(self, msg):
        """Generate messaages checksum byte."""
        accumulator = 0x0
        for byte in msg:
            accumulator += ord(byte)

        return accumulator & 0x0FF

    def set_baud_rate(self, rate):
        """Set device baud rate."""
        if self.device is None:
            raise HRMException("Device not connected (Opened)")

        if rate == 9600:
            msg = '\x10'

        self.device.ctrl_transfer(0x40, 0xC, 0x5003, 0xF0, msg)

    def set_time_out(self, timeout):
        """Set device timeout"""
        if self.device is None:
            raise HRMException("Device not connected (Opened)")

        msg = chr(timeout)
        self.device.ctrl_transfer(0x40, 0xC, 0x5003, 0xFFFF, msg)

if __name__ == '__main__':
    try:
        hrt = HeartRateMonitor()
        hrt.download_data()
        exit(0)

    except HRMException as error:
        print error.msg
        exit(1)
