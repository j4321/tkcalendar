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
there seem to be an issue (`#32 <https://github.com/j4321/tkcalendar/issues/32>`_)
with the detection of the babel dependency of tkcalendar.
This can be fixed by using the ``--hidden-import`` option:

::

    $ pyinstaller --hidden-import babel.numbers myscript.py


or by editing the *.spec* file:


::

    hiddenimports=["babel.numbers"]
