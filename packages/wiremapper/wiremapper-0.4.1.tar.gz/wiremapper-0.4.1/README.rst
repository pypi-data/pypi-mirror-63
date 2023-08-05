Wiremapper
==========

This is a python GTK3 application that uses the pockethernet library
to run various network tests using the Pockethernet hardware (a bluetooth
connected network diagnostics tool)

Features
--------

* Quicktest feature which is a single-button test-everything sensible mode.
  If you have a wiremap inserted it will run a wiremap and otherwise it
  will run link/poe tests

* Pair the pockethernet once with your regular bluetooth menu and
  Wiremapper will deal with connecting for you. There's a dropdown
  in the header to switch between paired pockethernets if you have
  multiple (showing bluetooth device aliases set in the regular bluetooth
  menu)

* Run a custom test with multiple result "slots", this is mainly for testing
  a complete office building and exporting a .csv file with the results for
  each ethernet outlet in the building.

* Responsive application that should work on any phone/tablet/laptop/desktop

Installation
------------

You can install Wiremapper with ``pip3 install wiremapper``. I haven't figured out
how to correctly package a launcher yet but you can start it by running ``wiremapper``

Screenshots
-----------

.. image:: data/screenshot-wiremap.png

.. image:: data/screenshot-link.png

.. image:: data/screenshot-loopback.png

.. image:: data/screenshot-custom.png