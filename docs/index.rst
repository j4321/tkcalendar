.. tkcalendar documentation master file, created by
   sphinx-quickstart on Fri Aug 17 00:37:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tkcalendar
==========

|Release| |Linux| |Travis| |Codecov| |License| |Doc|

tkcalendar is a python module that provides the Calendar and DateEntry widgets for Tkinter.
The DateEntry widget is similar to a Combobox, but the drop-down is not a list but a Calendar to select a date.
Events can be displayed in the Calendar with custom colors and a tooltip displays the event list for a given day.
tkcalendar is compatible with both Python 2 and Python 3.
It supports many locale settings (e.g. 'fr_FR', 'en_US', ..) and the colors are customizable.

Project page: https://github.com/j4321/tkcalendar

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   installation
   example
   documentation
   changelog


.. |Release| image:: https://badge.fury.io/py/tkcalendar.svg
    :alt: Latest Release
    :target: https://pypi.org/project/tkcalendar/
.. |Linux| image:: https://img.shields.io/badge/platform-Linux-blue.svg
    :alt: Platform
.. |Windows| image:: https://img.shields.io/badge/platform-Windows-blue.svg
    :alt: Platform
.. |Mac| image:: https://img.shields.io/badge/platform-Mac-blue.svg
    :alt: Platform
.. |Travis| image:: https://travis-ci.org/j4321/tkcalendar.svg?branch=master
    :target: https://travis-ci.org/j4321/tkcalendar
    :alt: Travis CI Build Status
.. |Appveyor| image::  https://ci.appveyor.com/api/projects/status/9a5bi9ewvccdmo3a/branch/master?svg=true
    :target: https://ci.appveyor.com/project/j4321/tkcalendar/branch/master
    :alt: Appveyor Build Status
.. |Codecov| image:: https://codecov.io/gh/j4321/tkcalendar/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/j4321/tkcalendar
    :alt: Code coverage
.. |License| image:: https://img.shields.io/github/license/j4321/tkcalendar.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License
.. |Doc| image:: https://readthedocs.org/projects/tkcalendar/badge/?version=latest
    :target: https://tkcalendar.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
