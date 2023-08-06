 FHmonitor package
 =================

The FHmonitor package was written to run on a
Raspberry Pi that is communicating with an atm90e32 chip over SPI.
We use `Circuit Setup's energy meter <https://circuitsetup.us/index.php/product/split-single-phase-real-time-whole-house-energy-meter-v1-4/>`_,
which uses the atm90e32.

Example
-------
::

   from FHmonitor.monitor import Monitor

   m = Monitor()
   m.init_sensor()  # You will most likely need to adjust.
   pA, pR = m.take_reading()
   m.store_reading(pA,pR)

*Note: Make sure you understand the energy sensor initialization
parameters of :meth:`~FHmonitor.monitor.Monitor.init_sensor`.  You
could be using a different Power Transformer and/or Current Transformers.*

Monitor class
-------------

The class you will use the most is :class:`~FHmonitor.monitor.Monitor`.
This class contains methods to:

* Take an active and reactive power reading (see :meth:`~FHmonitor.monitor.Monitor.take_reading`).

   * Before taking a reading, the energy meter must be initialized (see :meth:`~FHmonitor.monitor.Monitor.init_sensor`).
* Store the reading into the mongo db running on the Raspberry Pi (see :meth:`~FHmonitor.monitor.Monitor.store_reading`).

   * Before storing readings, the mongo db must be opened (see :meth:`~FHmonitor.monitor.Monitor.open_db`).

.. automodule:: FHmonitor.monitor
   :members:
   :undoc-members:

Store class
-----------
The :class:`~FHmonitor.monitor.Monitor` class uses an implementation of the :class:`~FHmonitor.store.Store` abstract class to store power readings into a datastore.  The only data store currently available is the mongo db.  We originally started with
a Firebase DB, but decided running everything on a Raspberry Pi was much easier.  Mongo db can be run on the Raspberry Pi at no additional $ cost.


.. automodule:: FHmonitor.store
   :members:
   :undoc-members:
   :show-inheritance:








