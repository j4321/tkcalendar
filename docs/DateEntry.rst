DateEntry
=========

Class
-----

.. autoclass:: tkcalendar.DateEntry
    :members:
    :show-inheritance:

    .. py:method:: __init__(master=None, **kw)

       Create an entry with a drop-down calendar to select a date.

       When the entry looses focus, if the user input is not a valid date,
       the entry content is reset to the last valid date.

       **Keyword Options**

       - ``ttk.Entry`` options:
       
           class, cursor, style, takefocus, xscrollcommand, exportselection, justify, show, state, textvariable, width.
           
       - ``Calendar`` options: see the :ref:`documentation <doc>`.


Virtual Events
--------------

A ``<<DateEntrySelected>>`` event is generated each time the user selects a date.
