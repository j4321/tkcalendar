# -*- coding: utf-8 -*-
"""
tkcalendar - Calendar and DateEntry widgets for Tkinter
Copyright 2017-2018 Juliette Monsel <j_4321@protonmail.com>
with contributions from:
  - Neal Probert (https://github.com/nprobert)
  - arahorn28 (https://github.com/arahorn28)

tkcalendar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcalendar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


EventCalendar widget
"""

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from tkcalendar.calendar_ import Calendar
from tkcalendar.tooltip import TooltipWrapper
import datetime


class EventCalendar(Calendar):
    def __init__(self, master=None, selectmode='none', **kw):
        self.events = {}
        Calendar.__init__(self, master, selectmode=selectmode, **kw)

        self._next_event_id = 0  # to give each event a different id

        self.style = ttk.Style(self)

        self.tooltip_wrapper = TooltipWrapper(self)
        self.bind('<FocusOut>', lambda e: self.tooltip_wrapper.tooltip.withdraw())

    def _display_calendar(self):
        """Display the days of the current month (the one in self._date)."""
        year, month = self._date.year, self._date.month

        # update header text (Month, Year)
        header = self._cal.formatmonthname(year, month, 0, False)
        self._header_month.configure(text=header.title())
        self._header_year.configure(text=str(year))

        # update calendar shown dates
        cal = self._cal.monthdatescalendar(year, month)

        next_m = month + 1
        y = year
        if next_m == 13:
            next_m = 1
            y += 1
        if len(cal) < 6:
            if cal[-1][-1].month == month:
                i = 0
            else:
                i = 1
            cal.append(self._cal.monthdatescalendar(y, next_m)[i])
            if len(cal) < 6:
                cal.append(self._cal.monthdatescalendar(y, next_m)[i + 1])

        week_days = {i: 'normal' for i in range(7)}
        week_days[5] = 'we'
        week_days[6] = 'we'
        prev_m = (month - 2) % 12 + 1
        months = {month: '.%s.TLabel' % self._style_prefixe,
                  next_m: '_om.%s.TLabel' % self._style_prefixe,
                  prev_m: '_om.%s.TLabel' % self._style_prefixe}

        week_nb = self._date.isocalendar()[1]
        modulo = max(week_nb, 52)
        for i_week in range(6):
            self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
            for i_day in range(7):
                style = week_days[i_day] + months[cal[i_week][i_day].month]
                txt = str(cal[i_week][i_day].day)
                self._calendar[i_week][i_day].configure(text=txt,
                                                        style=style)
                if cal[i_week][i_day] in self.events:
                    date = cal[i_week][i_day]
                    label = self._calendar[i_week][i_day]
                    last = max(self.events[date])
                    background = self.events[date][last]['background']
                    foreground = self.events[date][last]['foreground']
                    self.style.configure('%s.TLabel' % label, background=background,
                                         foreground=foreground)
                    label.configure(style='%s.TLabel' % label)
                    text = '\n'.join(['➢ {}'.format(ev['text']) for ev in self.events[date].values()])
                    self.tooltip_wrapper.remove_tooltip(label)
                    self.tooltip_wrapper.add_tooltip(label, text)

        self._display_selection()

    def _reset_day(self, date):
        """Restore usual week day colors."""
        year, month = date.year, date.month
        if year == self._date.year:
            _, w, d = date.isocalendar()
            wn = self._date.isocalendar()[1]
            w -= wn
            w %= max(52, wn)
            if w >= 0 and w < 6:
                self.tooltip_wrapper.remove_tooltip(self._calendar[w][d - 1])
                if month == date.month:
                    if d < 6:
                        self._calendar[w][d - 1].configure(style='normal.%s.TLabel' % self._style_prefixe)
                    else:
                        self._calendar[w][d - 1].configure(style='we.%s.TLabel' % self._style_prefixe)
                else:
                    if d < 6:
                        self._calendar[w][d - 1].configure(style='normal_om.%s.TLabel' % self._style_prefixe)
                    else:
                        self._calendar[w][d - 1].configure(style='we_om.%s.TLabel' % self._style_prefixe)

    def _remove_selection(self):
        """Remove highlight of selected day."""
        if self._sel_date is not None:
            if self._sel_date in self.events:
                self._show_event(self._sel_date)
            else:
                year, month = self._sel_date.year, self._sel_date.month
                if year == self._date.year:
                    _, w, d = self._sel_date.isocalendar()
                    wn = self._date.isocalendar()[1]
                    w -= wn
                    w %= max(52, wn)
                    if w >= 0 and w < 6:
                        if month == self._date.month:
                            if d < 6:
                                self._calendar[w][d - 1].configure(style='normal.%s.TLabel' % self._style_prefixe)
                            else:
                                self._calendar[w][d - 1].configure(style='we.%s.TLabel' % self._style_prefixe)
                        else:
                            if d < 6:
                                self._calendar[w][d - 1].configure(style='normal_om.%s.TLabel' % self._style_prefixe)
                            else:
                                self._calendar[w][d - 1].configure(style='we_om.%s.TLabel' % self._style_prefixe)

    def _show_event(self, date):
        if date.year == self._date.year:
            _, w, d = date.isocalendar()
            wn = self._date.isocalendar()[1]
            w -= wn
            w %= max(52, wn)
            if w >= 0 and w < 6:
                label = self._calendar[w][d - 1]
                last = max(self.events[date])
                background = self.events[date][last]['background']
                foreground = self.events[date][last]['foreground']
                self.style.configure('%s.TLabel' % label, background=background,
                                     foreground=foreground)
                label.configure(style='%s.TLabel' % label)
                text = '\n'.join(['➢ {}'.format(ev['text']) for ev in self.events[date].values()])
                self.tooltip_wrapper.remove_tooltip(label)
                self.tooltip_wrapper.add_tooltip(label, text)

    def add_event(self, date, text, background='royal blue', foreground='white'):
        """
        Add event in calendar at given date, with given color and
        with a tooltip displaying the text. Return event id (for edit and deletion purposes).
        """
        if isinstance(date, datetime.datetime):
            date = date.date()
        ev_id = self._next_event_id
        if date not in self.events:
            self.events[date] = {ev_id: {'text': text, 'background': background,
                                         'foreground': foreground}}
        else:
            self.events[date][ev_id] = {'text': text, 'background': background,
                                        'foreground': foreground}
        self._show_event(date)
        self._next_event_id += 1
        return ev_id

    def del_event(self, date, ev_id=None):
        if ev_id is None:
            del self.events[date]
            self._reset_day(date)
        else:
            del self.events[date][ev_id]
            if not self.events[date]:
                del self.events[date]
                self._reset_day(date)
            else:
                self._show_event(date)

    def edit_event(self, date, ev_id, **kw):
        try:
            ev = self.events[date][ev_id]
        except KeyError:
            raise KeyError("Event %i on the %s does not exists" % (ev_id, date))
        else:
            keys = set(ev.keys())
            keys.union(set(kw.keys()))
            if len(keys) > 3:
                raise KeyError("Invalid keyword option, valid options are text, foreground and background.")
            else:
                ev.update(kw)
                self._show_event(date)

