HowTos
======

This section answers some questions that were asked about tkcalendar.

PyInstaller
-----------

When bundling an application with `PyInstaller <http://www.pyinstaller.org/>`_,
some of tkcalendar's dependencies are not detected so it is necessary to use
the ``--hidden-import`` option to specify them:

- Python 3

    ::

        $ pyinstaller --hidden-import tkinter.ttk --hidden-import tkinter.font myscript.py

- Python 2

    ::

        $ pyinstaller --hidden-import ttk --hidden-import tkFont myscript.py

Or this can be done inside the *.spec* file with

- Python 3

    ::

        hiddenimports=["tkinter.ttk", "tkinter.font"]

- Python 2

    ::

        hiddenimports=["ttk", "tkFont"]

    
