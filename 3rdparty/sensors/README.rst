=========
PySensors
=========

:author: Marc 'BlackJack' Rintsch
:date: 2014-08-17

Python bindings for ``libsensors.so`` from the `lm-sensors`_ project via
`ctypes`. Supports API version 4, i.e. `libsensors` version 3.x.

==========
Modified for Psistats
==========

Some modifications were done for the Psistats project. The project seems
dead. These changes include the pull request for py3 support.

Motivation
==========

Motivation for this package are shortcomings of scraping the output of
the ``sensors`` command by different shell scripts.  Some had problems when
labels changed, others could not cope with too many matches of their
overly broad regular expressions, and so on.  Those scripts and thus
this package are used at `RebeIT`_ for monitoring servers.  The needs of
that task are the driving force behind this implementation.

Requirements
============

* Python â‰¥2.6 and < 3
* ``libsensors.so`` from `lm-sensors`_ version 3.x (API 4)

The package is pure Python, so any implementation with the `ctypes` module
should work.  Tested so far with `CPython`_ and `PyPy`_.

.. TODO: Test with Jython.

Installation
============

The usual ``python setup.py install`` from within the source distribution.

Links
=====

================= =================================================
PyPi Entry        http://pypi.python.org/pypi/PySensors/
Source repository https://bitbucket.org/blackjack/pysensors/
Bugtracker        https://bitbucket.org/blackjack/pysensors/issues/
================= =================================================

Example
=======

The following example prints all detected sensor chips, their adapter, and the features with their â€mainâ€ value for each chip::

  import sensors
  
  sensors.init()
  try:
      for chip in sensors.iter_detected_chips():
          print '%s at %s' % (chip, chip.adapter_name)
          for feature in chip:
              print '  %s: %.2f' % (feature.label, feature.get_value())
  finally:
      sensors.cleanup()

Example output of the code above::

  k8temp-pci-00c3 at PCI adapter
    Core0 Temp: 16.00
    Core0 Temp: 11.00
    Core1 Temp: 28.00
    Core1 Temp: 19.00
  w83627ehf-isa-0290 at ISA adapter
    Vcore: 1.10
    in1: 1.10
    AVCC: 3.30
    VCC: 3.31
    in4: 1.68
    in5: 1.68
    in6: 1.86
    3VSB: 3.30
    Vbat: 3.06
    in9: 1.55
    Case Fan: 1231.00
    CPU Fan: 2410.00
    Aux Fan: 0.00
    fan5: 0.00
    Sys Temp: 39.00
    CPU Temp: 31.50
    AUX Temp: 30.50
    cpu0_vid: 0.00

.. _CPython: http://www.python.org/
.. _lm-sensors: http://www.lm-sensors.org/
.. _PyPy: http://pypy.org/
.. _RebeIT: http://www.rebeit.de/

