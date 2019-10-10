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

       - :class:`ttk.Entry` options:
       
           class, cursor, style, takefocus, xscrollcommand, exportselection, justify, show, state, textvariable, width.
           
       - :class:`Calendar` options: see the :ref:`documentation <doc>`. 
       
           The Calendar option *cursor* has been renamed *calendar_cursor* to avoid name clashes with the corresponding :class:`ttk.Entry` option.


Virtual Events
--------------

A :obj:`\<\<DateEntrySelected\>\>` event is generated each time the user selects a date.
