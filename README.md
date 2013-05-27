bhrm
====

Python class to access Beurer's heart rate monitors training data under linux

This projects is not supported nor developed by Beurer. The aim for this
project is to provide a way to access the training data recorded by the
Beurer's heart rate monitors and interpret the data. It does not and
will not provide a gui.


Use
---
To dump the heart rate monitor data on a file:

  ./beurer.py -o outputile

To intepret the dumped data:

  ./parser.py < inputfile

License
-------
GPL v2 or v3

Todo
----
 - Finish the interpretation of section 6 Laps results
 - Interpret the speed section (5)
 - Complete de help displayed when the main file is called with -h
 - Add the option to delete the data after reading it
 - Check the number of bytes recieved

Bugs
----

There is a bug where the program hangs when there is too much data.

