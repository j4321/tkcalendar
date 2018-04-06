tkcalendar
==========

tkcalendar is a python module that provides the Calendar and DateEntry widgets for Tkinter. The DateEntry widget is similar to a Combobox, but the drop-down is not a list but a Calendar to select a date.
tkcalendar is compatible with both Python 2 and Python 3.
It support all locale settings supported by the system and the colors are customizable.


Requirements
------------

- Linux, Windows, Mac
- Python 2 or 3 with tkinter + ttk (default for Windows but not for Linux)


Installation
------------

- Ubuntu: use the PPA `ppa:j-4321-i/ppa`

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
-------------

* Calendar widget

    Syntax:

    ::

        Calendar(master=None, **kw)

    Widget keyword options:

    * Standard options

        cursor: cursor to display when the pointer is in the widget

        font: font of the calendar, can be a string such as "Arial 20 bold" or a Tkinter Font instance

        borderwidth: width of the border around the calendar (integer)

        state: normal or disabled (unresponsive widget)

    * Widget-Specific Options

        year, month: initially displayed month, default is current month

        day: initially selected day, if month or year is given but not day, no initial selection, otherwise, default is today

        locale: locale to use, e.g. "fr_FR" for a French calendar

        selectmode: "none" or "day" (default) define whether the user can change the selected day with a mouse click

        textvariable: StringVar that will contain the currently selected date as str

        background: calendar border and month/year name background color

        foreground: month/year name foreground color

        bordercolor: day border color

        selectbackground: selected day background color

        selectforeground: selected day foreground color

        disabledselectbackground: selected day background color in disabled state

        disabledselectforeground: selected day foreground color in disabled state

        normalbackground: normal week days background color

        normalforeground: normal week days foreground color

        othermonthforeground: foreground color for normal week days belonging to the previous/next month

        othermonthbackground: background color for normal week days belonging to the previous/next month

        othermonthweforeground: foreground color for week-end days belonging to the previous/next month

        othermonthwebackground: background color for week-end days belonging to the previous/next month

        weekendbackground: week-end days background color

        weekendforeground: week-end days foreground color

        headersbackground: day names and week numbers background color

        headersforeground: day names and week numbers foreground color


    * Virtual Events

        A `<<CalendarSelected>>` event is generated each time the user selects a day with the mouse.


* DateEntry widget

    Date selection entry with drop-down calendar.


    Syntax:

    ::

        DateEntry(master=None, **kw)

    Widget keyword options:

    * Keyword options of Calendar to configure the drop-down calendar

    * Keyword options of ttk.Entry

        By default, 'validate' is set to 'focusout' and 'validatecommand' is configured so that each time the widget looses focus, if the content is not a valid date (in locale format '%x'), it is reset to the previous valid date.

        The widget style is set to 'DateEntry'. A custom style inheritting from 'DateEntry' can be created by naming it  '<style name>.DateEntry'

    * Virtual Events

        A <<DateEntrySelected>> event is generated each time the user selects a date.


Changelog
---------

- tkcalendar 1.2.0

    * Add textvariable option to Calendar
    * Add state ('normal' or 'disabled') option to Calendar
    * Fix DateEntry behavior in readonly mode

- tkcalendar 1.1.5

    * Fix endless triggering of `<<ThemeChanged>>` event in `DateEntry`

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

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def example2():
        top = tk.Toplevel(root)

        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)

    root = tk.Tk()
    s = ttk.Style(root)
    s.theme_use('clam')

    ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
    ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)

    root.mainloop()
