Changelog
=========

tkcalendar 1.3.0
----------------

* No longer set locale globally to avoid conflicts between several instances, use babel module instead
* Add option showwekknumbers to show/hide week numbers
* Add option firstweekday to choose first week day between 'monday' and 'sunday'
* Make DateEntry compatible with more ttk themes, especially OSX default theme
* Add possibility to display special events (like birthdays, ..) in the calendar.
  The events are displayed with colors defined by tags and the event description is displayed in a tooltip
  (see documentation).

tkcalendar 1.2.1
----------------

* Fix ``ValueError`` in DateEntry with Python 3.6.5

tkcalendar 1.2.0
----------------

* Add textvariable option to Calendar
* Add state ('normal' or 'disabled') option to Calendar
* Add options disabledselectbackground, disabledselectforeground,
  disableddaybackground and disableddayforeground to configure colors
  when Calendar is disabled
* Fix DateEntry behavior in readonly mode
* Make Calendar.selection_get always return a ``datetime.date``

tkcalendar 1.1.5
----------------

* Fix endless triggering of ``<<ThemeChanged>>`` event in DateEntry

tkcalendar 1.1.4
----------------

* Fix error in january due to week 53
* Fix DateEntry for ttk themes other than 'clam'

tkcalendar 1.1.3
----------------

* Make DateEntry support initialisation with partial dates (e.g. just year=2010)
* Improve handling of wrong year-month-day combinations

tkcalendar 1.1.2
----------------

* Fix bug after destroying a DateEntry
* Fix bug in style and font

tkcalendar 1.1.1
----------------

* Fix bug when content of DateEntry is not a valid date

tkcalendar 1.1.0
----------------

* Bug fix:

    + Fix display of the first days of the next month

    + Increment year when going from december to january

* New widget:

    + DateEntry, date selection entry with drop-down calendar

* New options in Calendar:

    + borderwidth: width of the border around the calendar (integer)

    + othermonthbackground: background color for normal week days belonging to the previous/next month

    + othermonthweforeground: foreground color for week-end days belonging to the previous/next month

    + othermonthwebackground: background color for week-end days belonging to the previous/next month


tkcalendar 1.0.0
----------------

* Initial version
