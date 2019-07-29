Changelog
=========

.. currentmodule:: tkcalendar

tkcalendar 1.5.0
----------------

.. rubric:: New features

- :meth:`Calendar.see` method: make sure given date is visible
- Make *locale* option editable after the creation of the :class:`Calendar`

.. rubric:: New options

- *disabledforeground* and *disabledbackground*: colors of calendar border and
  month/year name in disabled state
- *maxdate* and *mindate*: set an allowed date range for date selection
- *weekenddays*: choose the days colored as week-end days (`#37 <https://github.com/j4321/tkcalendar/issues/37>`_)
- *date_pattern*: customize the date format

.. rubric:: Bug fixes

- Make :meth:`Calendar.selection_clear` actually clear the selection
- Fix :obj:`ValueError` when retrieving default locale
- Fix date parsing error in Swedish locale and some others (`#44 <https://github.com/j4321/tkcalendar/issues/44>`_)
- Improve compliance with ttk themes by make the :class:`DateEntry` look like a :class:`ttk.Combobox` (`#42 <https://github.com/j4321/tkcalendar/issues/42>`_)
- Fix high CPU issues in Windows (`#36 <https://github.com/j4321/tkcalendar/issues/36>`_)

tkcalendar 1.4.0
----------------

.. rubric:: New features

- :obj:`\<\<CalendarMonthChanged\>\>` virtual event: event generated each time the user changes the displayed month
- :meth:`Calendar.get_displayed_month` method: return the currently displayed month in the form of a (month, year) tuple

.. rubric:: New options

- *showothermonthdays*: show/hide the last and first days of the previous and next months

.. rubric:: Bug fixes

- Fix handling of *style* option in :class:`DateEntry`
- Fix display of events for January days showing on December and conversely

tkcalendar 1.3.1
----------------

.. rubric:: Bug fixes

- Fix bug in day selection when *firstweekday* is 'sunday' (`#28 <https://github.com/j4321/tkcalendar/issues/28>`_)

tkcalendar 1.3.0
----------------

.. rubric:: New features

- Add possibility to display special events (like birthdays, ..) in the calendar.
  The events are displayed with colors defined by tags and the event description is displayed in a tooltip
  (see :ref:`calevent`) (`#19 <https://github.com/j4321/tkcalendar/issues/19>`_)

.. rubric:: New options

- *showwekknumbers*: show/hide week numbers (`#18 <https://github.com/j4321/tkcalendar/issues/18>`_)
- *firstweekday*: first week day ('monday' or 'sunday') (`#25 <https://github.com/j4321/tkcalendar/issues/25>`_)

.. rubric:: Bug fixes

- No longer set locale globally to avoid conflicts between several instances, use babel module instead (`#15 <https://github.com/j4321/tkcalendar/issues/15>`_)
- Make :class:`DateEntry` compatible with more ttk themes, especially OSX default theme (`#16 <https://github.com/j4321/tkcalendar/issues/16>`_)

tkcalendar 1.2.1
----------------

.. rubric:: Bug fixes

- Fix :obj:`ValueError` in :class:`DateEntry` with Python 3.6.5 (`#13 <https://github.com/j4321/tkcalendar/issues/13>`_)

tkcalendar 1.2.0
----------------

.. rubric:: New options

- *textvariable*: connect the currently selected date to the given :class:`StringVar` (`#6 <https://github.com/j4321/tkcalendar/issues/6>`_)
- *state*: 'normal' or 'disabled'
- *disabledselectbackground*, *disabledselectforeground*,
  *disableddaybackground* and *disableddayforeground*: configure colors
  when :class:`Calendar` is disabled

.. rubric:: Bug fixes

- Fix :class:`DateEntry` behavior in readonly mode
- Make :meth:`Calendar.selection_get` always return a :class:`datetime.date`

tkcalendar 1.1.5
----------------

.. rubric:: Bug fixes

- Fix endless triggering of :obj:`\<\<ThemeChanged\>\>` event in :class:`DateEntry` (`#9 <https://github.com/j4321/tkcalendar/issues/9>`_)

tkcalendar 1.1.4
----------------

.. rubric:: Bug fixes

- Fix error in January due to week 53
- Fix :class:`DateEntry` for ttk themes other than 'clam' (`#3 <https://github.com/j4321/tkcalendar/issues/3>`_)

tkcalendar 1.1.3
----------------

.. rubric:: Bug fixes

- Make :class:`DateEntry` support initialisation with partial dates (e.g. just year=2010)
- Improve handling of wrong year-month-day combinations

tkcalendar 1.1.2
----------------

.. rubric:: Bug fixes

- Fix bug after destroying a :class:`DateEntry`
- Fix bug in style and font

tkcalendar 1.1.1
----------------

.. rubric:: Bug fixes

- Fix bug when content of :class:`DateEntry` is not a valid date

tkcalendar 1.1.0
----------------

.. rubric:: New widget

- :class:`DateEntry`: date selection entry with drop-down calendar

.. rubric:: New options

- *borderwidth*: width of the border around the calendar (integer)

- *othermonthbackground*: background color for normal week days belonging to the previous/next month

- *othermonthweforeground*: foreground color for week-end days belonging to the previous/next month

- *othermonthwebackground*: back

.. rubric:: Bug fixes

- Fix display of the first days of the next month

- Increment year when going from December to January


tkcalendar 1.0.0
----------------

- Initial version
