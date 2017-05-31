tkcalendar
==========

tkcalendar is a calendar widget for Tkinter. It is compatible with both Python 2
and Python 3. It support all locale setting supported by the system and the colors
are customizable.


Requirements
------------

- Linux, Windows, Mac
- Python 2 or 3 with tkinter + ttk (default for Windows but not for Linux)


Installation
------------
- Ubuntu:

::

    $ dpkg -i python(3)-tkcalendar_x.y.z-1_all.deb

- Archlinux: the package is available on `AUR <https://aur.archlinux.org/packages/python-tkcalendar>`__

- With pip:

::

    $ pip install tkcalendar


Documentation
-------------

Syntax:

::

    Calendar(master=None, **kw)

Widget keyword options:

* Standard options

    cursor: cursor to display when the pointer is in the widget
    
    font: font of the calendar, can be a string such as "Arial 20 bold" or a Tkinter Font instance


* Widget-Specific Options

    year, month: initially displayed month, default is current month

    day: initially selected day, if month or year is given but not day, no initial selection, otherwise, default is today

    locale: locale to use, e.g. "fr_FR" for a French calendar

    selectmode: "none" or "day" (default) define whether the user can change the selected day with a mouse click

    background: border and month/year name background color
    
    foreground: border and month/year name foreground color

    selectbackground: selected day background color
    
    selectforeground: selected day foreground color

    normalbackground: normal week days background color
    
    normalforeground: normal week days foreground color

    othermonthforeground: foreground color for days belonging to the previous/next month

    weekendbackground: week-end days background color
    
    weekendforeground: week-end days foreground color

    headersbackground: day names and week numbers background color
    
    headersforeground: day names and week numbers foreground color


* Virtual Events

    A `<<CalendarSelected>>` event is generated each time the selected day changes.


Changelog
---------

- tkcalendar 1.0.0
    * Initial version

Example
=======

.. code:: python

    try:
        from tkinter import Tk, Button
    except ImportError:
        from Tkinter import Tk, Button
    from tkcalendar import Calendar

    def print_sel():
        print(cal.selection_get())

    root = Tk()

    cal = Calendar(root, locale="fr_FR.UTF-8",
                   font="Arial 12",
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    Button(root, text="ok", command=print_sel).pack()

    root.mainloop()
