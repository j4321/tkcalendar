HowTos
======

This section answers some questions that were asked about tkcalendar.

Widget styling
--------------

.. rubric:: Calendar

All styling is done using options, see the :ref:`documentation <doc>`.

.. rubric:: DateEntry

``DateEntry`` inherits from ``ttk.Entry`` therefore the styling is done using
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
    style.configure('my.DateEntry',
                    fieldbackground='light green',
                    background='dark green',
                    foreground='dark blue',
                    arrowcolor='white')

    dateentry = DateEntry(style='my.DateEntry')
    dateentry.pack()

    tk.mainloop()


PyInstaller
-----------

When bundling an application with `PyInstaller <http://www.pyinstaller.org/>`_,
some of tkcalendar's dependencies are not detected so it is necessary to use
the ``--hidden-import`` option to specify them:

.. rubric:: Python 3

::

    $ pyinstaller --hidden-import tkinter.ttk --hidden-import tkinter.font myscript.py

.. rubric:: Python 2

::

    $ pyinstaller --hidden-import ttk --hidden-import tkFont myscript.py

Or this can be done inside the *.spec* file with

.. rubric:: Python 3

::

    hiddenimports=["tkinter.ttk", "tkinter.font"]

.. rubric:: Python 2

::

    hiddenimports=["ttk", "tkFont"]

    
