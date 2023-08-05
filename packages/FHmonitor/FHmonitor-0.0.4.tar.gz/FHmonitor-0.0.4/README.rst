=========
FHmonitor
=========


.. image:: https://img.shields.io/pypi/v/FHmonitor.svg
        :target: https://pypi.python.org/pypi/FHmonitor

.. image:: https://img.shields.io/travis/bitknitting/FHmonitor.svg
        :target: https://travis-ci.com/bitknitting/FHmonitor

.. image:: https://readthedocs.org/projects/FHmonitor/badge/?version=latest
        :target: https://FHmonitor.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

FHmonitor (FitHome monitor):

* Is a Python Package written for the `FitHome Experience. <https://github.com/BitKnitting/FitHome/wiki>`_
* Assumes the package is running on a Raspberry Pi.
* Reads the active and reactive power registers of the atm90e32 and stores the readings into a mongo database.





* Free software: MIT license
* Documentation: https://FHmonitor.readthedocs.io.


Features
--------

* Implements the Monitor class to easily:
        * access current, active and reactive power readings obtained from an `atm90e32's registers <http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-46003-SE-M90E32AS-Datasheet.pdf>`_
        * store readings into a mongo database.
* Built to work best on a Raspberry Pi model 3 B and above communicating over SPI to `Circuit Setup's Split Single Phase Real Time Whole House Energy Meter (v 1.4) <https://circuitsetup.us/>`_

Credits
-------

Our code stands on the shoulders of Tisham Dhar's work. In particular the `atm90e26 Arduino library <https://github.com/whatnick/ATM90E26_Arduino>`_.

Another package we learned from was Circuit Setup's `atm90e32 Arduino library <https://github.com/CircuitSetup/Split-Single-Phase-Energy-Meter/tree/master/Software/libraries/ATM90E32>`_.

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`_ project template.
