Changelog
=========

tkcalendar 1.4.0
----------------

.. rubric:: New features

- ``<<CalendarMonthChanged>>`` virtual event: event generated each time the user changes the displayed month
- ``Calendar.get_displayed_month()`` method: return the currently displayed month in the form of a (month, year) tuple.

.. rubric:: New Calendar options

- *showothermonthdays*: show/hide the last and first days of the previous and next months

.. rubric:: Bug fixes

- Fix handling of *style* option in DateEntry

tkcalendar 1.3.1
----------------

.. rubric:: Bug fixes

- Fix bug in day selection when *firstweekday* is 'sunday'

tkcalendar 1.3.0
----------------

.. rubric:: New feature

- Add possibility to display special events (like birthdays, ..) in the calendar.
  The events are displayed with colors defined by tags and the event description is displayed in a tooltip
  (see :ref:`calevent`)

.. rubric:: New Calendar options

- *showwekknumbers*: show/hide week numbers
- *firstweekday*: first week day ('monday' or 'sunday')

.. rubric:: Bug fixes

- No longer set locale globally to avoid conflicts between several instances, use babel module instead
- Make DateEntry compatible with more ttk themes, especially OSX default theme

tkcalendar 1.2.1
----------------

.. rubric:: Bug fix

- Fix ``ValueError`` in DateEntry with Python 3.6.5

tkcalendar 1.2.0
----------------

.. rubric:: New Calendar options

- *textvariable*: connect the currently selected date to the given ``StringVar``
- *state*: 'normal' or 'disabled'
- *disabledselectbackground*, *disabledselectforeground*,
  *disableddaybackground* and *disableddayforeground*: configure colors
  when Calendar is disabled


.. rubric:: Bug fixes

- Fix DateEntry behavior in readonly mode
- Make Calendar.selection_get always return a ``datetime.date``

tkcalendar 1.1.5
----------------

.. rubric:: Bug fix

- Fix endless triggering of ``<<ThemeChanged>>`` event in DateEntry

tkcalendar 1.1.4
----------------

.. rubric:: Bug fixes

- Fix error in january due to week 53
- Fix DateEntry for ttk themes other than 'clam'

tkcalendar 1.1.3
----------------

.. rubric:: Bug fixes

- Make DateEntry support initialisation with partial dates (e.g. just year=2010)
- Improve handling of wrong year-month-day combinations

tkcalendar 1.1.2
----------------

.. rubric:: Bug fixes

- Fix bug after destroying a DateEntry
- Fix bug in style and font

tkcalendar 1.1.1
----------------

.. rubric:: Bug fixes

- Fix bug when content of DateEntry is not a valid date

tkcalendar 1.1.0
----------------

.. rubric:: Bug fixes

- Fix display of the first days of the next month

- Increment year when going from december to january

.. rubric:: New widget

- DateEntry, date selection entry with drop-down calendar

.. rubric:: New Calendar options

- *borderwidth*: width of the border around the calendar (integer)

- *othermonthbackground*: background color for normal week days belonging to the previous/next month

- *othermonthweforeground*: foreground color for week-end days belonging to the previous/next month

- *othermonthwebackground*: background color for week-end days belonging to the previous/next month


tkcalendar 1.0.0
----------------

Initial version
