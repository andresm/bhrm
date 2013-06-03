bhrm
====

Python class to access Beurer's heart rate monitors training data under linux
this software was tested using a PM 70 model.

This projects is not supported nor developed by Beurer. The aim for this
project is to provide a way to access the training data recorded by the
Beurer's heart rate monitors and interpret the data. It does not and
will not provide a gui.


Use
---
To dump the heart rate monitor data on a file:

  ./beurer.py -o outputile

To intepret the dumped data:

  ./parser.py -i inputfile


License
-------
GPL v2 or v3


Hacking
-------

Theres a file named HACKING with insructions on how to help with the data
that is not yet interpreted


Todo
----
 - Interpret the Speed section (5)
 - Interpret the Height section (?)
 - Correct the main parser bucle to stop after trying all data
 

Bugs
----

 - There is a bug where the  program sometimes hangs when there is too
   much  data.  However, I  have not  been able  to reproduce  it, and
   there is no data loss

