HowTos
======

Widget styling
--------------

.. rubric:: Calendar

All styling is done using options, see the :ref:`documentation <doc>`.

.. rubric:: DateEntry

:class:`~tkcalendar.DateEntry` inherits from :class:`ttk.Entry` therefore the styling is done using
a ttk style:

.. code:: python

    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        import Tkinter as tk
        import ttk

    from tkcalendar import DateEntry

    style = ttk.Style()
    # style.theme_use('clam')  # -> uncomment this line if the styling does not work
    style.configure('my.DateEntry',
                    fieldbackground='light green',
                    background='dark green',
                    foreground='dark blue',
                    arrowcolor='white')

    dateentry = DateEntry(style='my.DateEntry')
    dateentry.pack()

    tk.mainloop()

If the style of the :class:`~tkcalendar.DateEntry` does not change, then it might be because of the
used ttk theme. Changing the theme with ``style.theme_use('clam')`` should solve
the issue.

PyInstaller
-----------

When bundling an application with `PyInstaller <http://www.pyinstaller.org/>`_,
there is an issue (`#32 <https://github.com/j4321/tkcalendar/issues/32>`_)
with the detection of the babel dependency of tkcalendar.
This can be fixed by using the ``--hidden-import`` option:

::

    $ pyinstaller --hidden-import babel.numbers myscript.py


or by editing the *.spec* file:


::

    hiddenimports=["babel.numbers"]


Custom date formatting 
----------------------

When using the "en_US" locale, the default date formatting in the :class:`~tkcalendar.DateEntry`, 
or when getting the selected date from the :class:`~tkcalendar.Calendar` as a string 
is :obj:`M/d/yy`, i.e. July 4, 2019 will give "7/4/19". 
If you want to get "07/04/2019" instead, you can pass "MM/dd/yyyy" to 
the *date_pattern* option of the :class:`~tkcalendar.Calendar` or :class:`~tkcalendar.DateEntry`.

.. code:: python

    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        import Tkinter as tk
        import ttk

    from tkcalendar import DateEntry
    
    DateEntry(locale='en_US').pack()
    DateEntry(locale='en_US', date_pattern='MM/dd/yyyy').pack()
    
    tk.mainloop()

