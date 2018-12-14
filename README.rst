##########
tkcalendar
##########

|Release| |Travis| |Appveyor| |Codecov| |Windows| |Linux| |Mac| |License| |Doc|

tkcalendar is a python module that provides the Calendar and DateEntry widgets for Tkinter.
The DateEntry widget is similar to a Combobox, but the drop-down is not a list but a Calendar to select a date.
Events can be displayed in the Calendar with custom colors and a tooltip displays the event list for a given day.
tkcalendar is compatible with both Python 2 and Python 3.
It supports many locale settings (e.g. 'fr_FR', 'en_US', ..) and the colors are customizable.

The documentation is also available here: https://tkcalendar.readthedocs.io

.. contents:: Table of Contents

Requirements
============

- Linux, Windows, OSX
- Python 2 or 3 with tkinter + ttk (default for Windows but not for Linux) and babel


Installation
============

- Ubuntu: use the PPA `ppa:j-4321-i/ppa <https://launchpad.net/~j-4321-i/+archive/ubuntu/ppa>`__

    ::

        $ sudo add-apt-repository ppa:j-4321-i/ppa
        $ sudo apt-get update
        $ sudo apt-get install python(3)-tkcalendar

- Archlinux:

    The package is available on `AUR <https://aur.archlinux.org/packages/python-tkcalendar>`__

- With pip:

    ::

        $ pip install tkcalendar


Documentation
=============

Calendar widget
---------------

Syntax
~~~~~~

    ::

        Calendar(master=None, **kw)

Widget keyword options
~~~~~~~~~~~~~~~~~~~~~~

* Standard options

    cursor : str
        cursor to display when the pointer is in the widget

    font : str such as "Arial 20 bold" or a Tkinter Font instance
        font of the calendar

    borderwidth : int
        width of the border around the calendar

    state : str
        "normal" or "disabled" (unresponsive widget)

* Widget-specific options:

    year : int
        intinitially displayed year, default is current year.

    month : int
        initially displayed month, default is current month.

    day : int
        initially selected day, if month or year is given but not day, no initial selection, otherwise, default is today.

    firstweekday : "monday" or "sunday"
        first day of the week

    showweeknumbers : bool (default is True)
        whether to display week numbers.

    showothermonthdays : bool (default is True)
        whether to display the last days of the previous month and the first of the next month.

    locale : str
        locale to use, e.g. 'en_US'

    selectmode : "none" or "day" (default)
        whether the user can change the selected day with a mouse click.

    textvariable : StringVar
        connect the currently selected date to the variable.

* Style options:

    background :
        background color of calendar border and month/year name

    foreground :
        foreground color of month/year name

    bordercolor :
        day border color

    headersbackground :
        background color of day names and week numbers

    headersforeground :
        foreground color of day names and week numbers

    selectbackground :
        background color of selected day

    selectforeground :
        foreground color of selected day

    disabledselectbackground :
        background color of selected day in disabled state

    disabledselectforeground :
        foreground color of selected day in disabled state

    normalbackground :
        background color of normal week days

    normalforeground :
        foreground color of normal week days

    weekendbackground :
        background color of week-end days

    weekendforeground :
        foreground color of week-end days

    othermonthforeground :
        foreground color of normal week days belonging to the previous/next month

    othermonthbackground :
        background color of normal week days belonging to the previous/next month

    othermonthweforeground :
        foreground color of week-end days belonging to the previous/next month

    othermonthwebackground :
        background color of week-end days belonging to the previous/next month

    disableddaybackground :
        background color of days in disabled state

    disableddayforeground :
        foreground color of days in disabled state

* Tooltip options (for calevents):

    tooltipforeground :
        tooltip text color

    tooltipbackground :
        tooltip background color

    tooltipalpha : float
        tooltip opacity between 0 and 1

    tooltipdelay : int
        delay in ms before displaying the tooltip

Virtual Events
~~~~~~~~~~~~~~

    * A ``<<CalendarSelected>>`` event is generated each time the user selects a day with the mouse.

    * A ``<<CalendarMonthChanged>>`` event is generated each time the user changes the displayed month.

Widget methods
~~~~~~~~~~~~~~

    * Standard methods:

        - methods common to all tkinter widgets
          (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html>`__)

        - methods common to all ttk widgets
          (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Widget.html>`__)

    * Widget-Specific methods:

        calevent_cget(ev_id, option) :
            Return value of given option for the event *ev_id*.

        calevent_configure(ev_id, \*\*kw) :
            Return value of given option for the event *ev_id*.

        calevent_create(date, text, tags=[]) :
            Add new event in calendar and return event id.

            Options:

                *date*: datetime.date or datetime.datetime instance.

                *text*: text to put in the tooltip associated to date.

                *tags*: list of tags to apply to the event. The last tag determines the way the event is displayed.
                If there are several events on the same day, the lowest one (on the tooltip list)
                which has tags determines the colors of the day.

        calevent_lower(ev_id, below=None) :
            Lower event *ev_id* in tooltip event list.

                *below*: put event below given one, if below is None, put it at the bottom of tooltip event list.

            The day's colors are determined by the last tag of the lowest event which has tags.

        calevent_raise(ev_id, above=None) :
            Raise event *ev_id* in tooltip event list.

                *above*: put *ev_id* above given one, if above is None, put it on top of tooltip event list.

            The day's colors are determined by the last tag of the lowest event which has tags.

        calevent_remove(\*ev_ids, \*\*kw) :
            Remove events from calendar.

                Arguments: event ids to remove or 'all' to remove them all.

                Keyword arguments: *tag*, *date*. They are taken into account only if no id is given.
                Remove all events with given tag on given date. If only date is given,
                remove all events on date and if only tag is given, remove all events with tag.

        get_date() :
            If selectmode is 'day', return the string corresponding to the selected date in the
            ``Calendar`` locale, otherwise return ``""``.

        get_calevents(date=None, tag=None) :
            Return event ids of events with given tag and on given date.

                If only *date* is given, return event ids of all events on date.

                If only *tag* is given, return event ids of all events with tag.

                If both options are None, return all event ids.

        get_displayed_month() :
            Return the currently displayed month in the form of a (month, year) tuple.

        selection_get() :
            If selectmode is 'day', return the selected date as a ``datetime.date``
            instance, otherwise return ``None``.

        selection_set(self, date) :
            If selectmode is 'day', set the selection to *date* where *date* can be either a ``datetime.date``
             instance or a string corresponding to the date format ``"%x"`` in the ``Calendar``
             locale. Does nothing if selectmode is ``"none"``.

        tag_cget(tag, option) :
            Return the value of the tag's option.

        tag_config(self, tag, \*\*kw) :
            Configure *tag*.

                Keyword options: *foreground*, *background* (of the day in the calendar)

        tag_delete(tag) :
            Delete given tag and remove it from all events.

        tag_names() :
            Return tuple of existing tags.



DateEntry widget
----------------

Date selection entry with drop-down calendar.


Syntax
~~~~~~

    ::

        DateEntry(master=None, **kw)

Widget keyword options
~~~~~~~~~~~~~~~~~~~~~~

    * Keyword options of ``Calendar`` to configure the drop-down calendar

    * Keyword options of ``ttk.Entry``

        By default, 'validate' is set to 'focusout' and 'validatecommand' is configured so that each
        time the widget looses focus, if the content is not a valid date (in locale format '%x'),
        it is reset to the previous valid date.

        The widget style is set to 'DateEntry'. A custom style inheritting from 'DateEntry'
        can be created by naming it  '<style name>.DateEntry'

    * Virtual Events

        A ``<<DateEntrySelected>>`` event is generated each time the user selects a date.

Widget methods
~~~~~~~~~~~~~~

    * Standard methods:

        - methods common to all tkinter widgets
          (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html>`__)

        - methods common to all ttk widgets
          (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Widget.html>`__)

        - methods of the ``Entry`` widget
          (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/entry.html>`__)

    * Widget-Specific methods:

        drop_down() :
            Display or withdraw the drop-down calendar depending on its current state.

        get_date() :
            Return the selected date as a ``datetime.date`` instance.

        set_date(self, date) :
            Set the value of the DateEntry to *date* where *date* can be either a ``datetime.date``
            instance or a string corresponding to the date format `"%x"` in the `Calendar` locale.


Changelog
=========

- tkcalendar 1.4.0

    * Add ``<<CalendarMonthChanged>>`` virtual event to the Calendar widget
    * Add ``get_displayed_month()`` method to the Calendar widget
    * Add *showothermonthdays* option to show/hide the last and first days of the previous and next months
    * Fix display of events for January days showing on December page and conversely

- tkcalendar 1.3.1

    * Fix bug in day selection when firstweekday is sunday

- tkcalendar 1.3.0

    * No longer set locale globally to avoid conflicts between several instances, use babel module instead
    * Add option showwekknumbers to show/hide week numbers
    * Add option firstweekday to choose first week day between 'monday' and 'sunday'
    * Make DateEntry compatible with more ttk themes, especially OSX default theme
    * Add possibility to display special events (like birthdays, ..) in the calendar.
      The events are displayed with colors defined by tags and the event description is displayed in a tooltip
      (see documentation).

- tkcalendar 1.2.1

    * Fix ``ValueError`` in DateEntry with Python 3.6.5

- tkcalendar 1.2.0

    * Add textvariable option to Calendar
    * Add state ('normal' or 'disabled') option to Calendar
    * Add options disabledselectbackground, disabledselectforeground,
      disableddaybackground and disableddayforeground to configure colors
      when Calendar is disabled
    * Fix DateEntry behavior in readonly mode
    * Make Calendar.selection_get always return a ``datetime.date``

- tkcalendar 1.1.5

    * Fix endless triggering of ``<<ThemeChanged>>`` event in DateEntry

- tkcalendar 1.1.4

    * Fix error in january due to week 53
    * Fix DateEntry for ttk themes other than 'clam'

- tkcalendar 1.1.3

    * Make DateEntry support initialisation with partial dates (e.g. just year=2010)
    * Improve handling of wrong year-month-day combinations

- tkcalendar 1.1.2

    * Fix bug after destroying a DateEntry
    * Fix bug in style and font

- tkcalendar 1.1.1

    * Fix bug when content of DateEntry is not a valid date

- tkcalendar 1.1.0

    * Bug fix:

        + Fix display of the first days of the next month

        + Increment year when going from december to january

    * New widget:

        + DateEntry, date selection entry with drop-down calendar

    * New options in Calendar:

        + borderwidth: width of the border around the calendar (integer)

        + othermonthbackground: background color for normal week days belonging to the previous/next month

        + othermonthweforeground: foreground color for week-end days belonging to the previous/next month

        + othermonthwebackground: background color for week-end days belonging to the previous/next month


- tkcalendar 1.0.0

    * Initial version


Example
=======

.. code:: python

    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        import Tkinter as tk
        import ttk

    from tkcalendar import Calendar, DateEntry

    def example1():
        def print_sel():
            print(cal.selection_get())

        top = tk.Toplevel(root)

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand1", year=2018, month=2, day=5)

        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()


    def example2():

        top = tk.Toplevel(root)

        cal = Calendar(top, selectmode='none')
        date = cal.datetime.today() + cal.timedelta(days=2)
        cal.calevent_create(date, 'Hello World', 'message')
        cal.calevent_create(date, 'Reminder 2', 'reminder')
        cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
        cal.calevent_create(date + cal.timedelta(days=3), 'Message', 'message')

        cal.tag_config('reminder', background='red', foreground='yellow')

        cal.pack(fill="both", expand=True)
        ttk.Label(top, text="Hover over the events.").pack()


    def example3():
        top = tk.Toplevel(root)

        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2, year=2010)
        cal.pack(padx=10, pady=10)


    root = tk.Tk()
    ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
    ttk.Button(root, text='Calendar with events', command=example2).pack(padx=10, pady=10)
    ttk.Button(root, text='DateEntry', command=example3).pack(padx=10, pady=10)

    root.mainloop()


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
