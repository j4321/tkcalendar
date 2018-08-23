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

Standard options
^^^^^^^^^^^^^^^^

    cursor : str
        cursor to display when the pointer is in the widget

    font : str such as "Arial 20 bold" or a Tkinter Font instance
        font of the calendar, can be a

    borderwidth : int
        width of the border around the calendar

    state : str
        "normal" or "disabled" (unresponsive widget)

Widget-specific options
^^^^^^^^^^^^^^^^^^^^^^^

    year : int
        intinitially displayed year, default is current year.

    month : int
        initially displayed month, default is current month.

    day : int
        initially selected day, if month or year is given but not day, no initial selection, otherwise, default is today.

    firstweekday : "monday" or "sunday"
        first day of the week

    showweeknumbers : boolean (default is True)
        whether to display week numbers.

    locale : str
        locale to use, e.g. 'en_US'

    selectmode : "none" or "day" (default)
        whether the user can change the selected day with a mouse click.

    textvariable : StringVar
        connect the currently selected date to the variable.

Style options
^^^^^^^^^^^^^

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

Tooltip options (for calevents)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

    A ``<<CalendarSelected>>`` event is generated each time the user selects a day with the mouse.

Widget methods
~~~~~~~~~~~~~~

Standard methods
^^^^^^^^^^^^^^^^

    - methods common to all tkinter widgets
      (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html>`__)

    - methods common to all ttk widgets
      (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Widget.html>`__)

Widget-Specific methods
^^^^^^^^^^^^^^^^^^^^^^^

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

    Keyword options of ``Calendar`` to configure the drop-down calendar

    Keyword options of ``ttk.Entry``

        By default, 'validate' is set to 'focusout' and 'validatecommand' is configured so that each
        time the widget looses focus, if the content is not a valid date (in locale format '%x'),
        it is reset to the previous valid date.

        The widget style is set to 'DateEntry'. A custom style inheritting from 'DateEntry'
        can be created by naming it  '<style name>.DateEntry'

Virtual Events
~~~~~~~~~~~~~~

    A ``<<DateEntrySelected>>`` event is generated each time the user selects a date.

Widget methods
~~~~~~~~~~~~~~

Standard methods
^^^^^^^^^^^^^^^^

    - methods common to all tkinter widgets
      (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html>`__)

    - methods common to all ttk widgets
      (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Widget.html>`__)

    - methods of the ``Entry`` widget
      (more details `here <http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/entry.html>`__)

Widget-Specific methods
^^^^^^^^^^^^^^^^^^^^^^^

    drop_down() :
        Display or withdraw the drop-down calendar depending on its current state.

    get_date() :
        Return the selected date as a ``datetime.date`` instance.

    set_date(self, date) :
        Set the value of the DateEntry to *date* where *date* can be either a ``datetime.date``
        instance or a string corresponding to the date format `"%x"` in the `Calendar` locale.
