# -*- coding: utf-8 -*-
"""
tkcalendar - Calendar and DateEntry widgets for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

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


tkcalendar module providing Calendar and DateEntry widgets
"""

import calendar
import locale
from sys import platform
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.font import Font
except ImportError:
    import Tkinter as tk
    import ttk
    from tkFont import Font


def _unbind(widget, seq, funcid):
    """Unbind callback to funcid on seq (workaround fixing bug in widget.unbind)."""
    bindings = {x.split()[1][3:]: x for x in widget.bind(seq).splitlines() if x.strip()}
    try:
        del bindings[funcid]
    except KeyError:
        raise tk.TclError('Binding "%s" not defined.' % funcid)
    widget.bind(seq, '\n'.join(list(bindings.values())))


class Calendar(ttk.Frame):
    """Calendar widget."""
    date = calendar.datetime.date
    timedelta = calendar.datetime.timedelta
    strptime = calendar.datetime.datetime.strptime

    def __init__(self, master=None, **kw):
        """
        Construct a Calendar with parent master.

        STANDARD OPTIONS

            cursor, font, borderwidth

        WIDGET-SPECIFIC OPTIONS

            year, month: initially displayed month, default is current month
            day: initially selected day, if month or year is given but not
                day, no initial selection, otherwise, default is today
            locale: locale to use, e.g. 'fr_FR.utf-8'
                    (the locale need to be installed, otherwise it will
                     raise 'locale.Error: unsupported locale setting')
            selectmode: "none" or "day" (default) define whether the user
                        can change the selected day with a mouse click
            background: calendar border and month/year name background color
            foreground: month/year name foreground color
            bordercolor: day border color
            selectbackground: selected day background color
            selectforeground: selected day foreground color
            normalbackground: normal week days background color
            normalforeground: normal week days foreground color
            othermonthforeground: foreground color for normal week days
                                  belonging to the previous/next month
            othermonthbackground: background color for normal week days
                                  belonging to the previous/next month
            othermonthweforeground: foreground color for week-end days
                                    belonging to the previous/next month
            othermonthwebackground: background color for week-end days
                                    belonging to the previous/next month
            weekendbackground: week-end days background color
            weekendforeground: week-end days foreground color
            headersbackground: day names and week numbers background color
            headersforeground: day names and week numbers foreground color

        VIRTUAL EVENTS

            A <<CalendarSelected>> event is generated each time the user
            selects a day with the mouse.
        """

        curs = kw.pop("cursor", "")
        font = kw.pop("font", "Liberation\ Sans 9")
        classname = kw.pop('class_', "Calendar")
        name = kw.pop('name', None)
        ttk.Frame.__init__(self, master, class_=classname, cursor=curs, name=name)
        self._style_prefixe = str(self)
        ttk.Frame.configure(self, style=self._style_prefixe + '.main.TFrame')

        self._font = Font(self, font)
        prop = self._font.actual()
        prop["size"] += 1
        self._header_font = Font(self, **prop)

        try:
            bd = int(kw.pop('borderwidth', 2))
        except ValueError:
            raise ValueError('expected integer for the borderwidth option.')

        # --- date
        today = self.date.today()

        if (("month" in kw) or ("year" in kw)) and ("day" not in kw):
            month = kw.pop("month", today.month)
            year = kw.pop('year', today.year)
            self._sel_date = None  # selected day
        else:
            day = kw.pop('day', today.day)
            month = kw.pop("month", today.month)
            year = kw.pop('year', today.year)
            self._sel_date = self.date(year, month, day)  # selected day
        self._date = self.date(year, month, 1)  # (year, month) displayed by the calendar

        # --- selectmode
        selectmode = kw.pop("selectmode", "day")
        if selectmode not in ("none", "day"):
            raise ValueError("'selectmode' option should be 'none' or 'day'.")
        # --- locale
        locale = kw.pop("locale", '')

        if locale is None:
            self._cal = calendar.TextCalendar(calendar.MONDAY)
        else:
            self._cal = calendar.LocaleTextCalendar(calendar.MONDAY, locale)

        # --- style
        self.style = ttk.Style(self)
        active_bg = self.style.lookup('TEntry', 'selectbackground', ('focus',))

        # --- properties
        options = ['cursor',
                   'font',
                   'borderwidth',
                   'selectmode',
                   'locale',
                   'selectbackground',
                   'selectforeground',
                   'normalbackground',
                   'normalforeground',
                   'background',
                   'foreground',
                   'bordercolor',
                   'othermonthforeground',
                   'othermonthbackground',
                   'othermonthweforeground',
                   'othermonthwebackground',
                   'weekendbackground',
                   'weekendforeground',
                   'headersbackground',
                   'headersforeground']

        keys = list(kw.keys())
        for option in keys:
            if option not in options:
                del(kw[option])

        self._properties = {"cursor": curs,
                            "font": font,
                            "borderwidth": bd,
                            "locale": locale,
                            "selectmode": selectmode,
                            'selectbackground': active_bg,
                            'selectforeground': 'white',
                            'normalbackground': 'white',
                            'normalforeground': 'black',
                            'background': 'gray30',
                            'foreground': 'white',
                            'bordercolor': 'gray70',
                            'othermonthforeground': 'gray45',
                            'othermonthbackground': 'gray93',
                            'othermonthweforeground': 'gray45',
                            'othermonthwebackground': 'gray75',
                            'weekendbackground': 'gray80',
                            'weekendforeground': 'gray30',
                            'headersbackground': 'gray70',
                            'headersforeground': 'black'}
        self._properties.update(kw)

        # --- init calendar
        # --- *-- header: month - year
        header = ttk.Frame(self, style=self._style_prefixe + '.main.TFrame')

        f_month = ttk.Frame(header,
                            style=self._style_prefixe + '.main.TFrame')
        l_month = ttk.Button(f_month,
                             style=self._style_prefixe + '.L.TButton',
                             command=self._prev_month)
        self._header_month = ttk.Label(f_month, width=10, anchor='center',
                                       style=self._style_prefixe + '.main.TLabel', font=self._header_font)
        r_month = ttk.Button(f_month,
                             style=self._style_prefixe + '.R.TButton',
                             command=self._next_month)
        l_month.pack(side='left', fill="y")
        self._header_month.pack(side='left', padx=4)
        r_month.pack(side='left', fill="y")

        f_year = ttk.Frame(header, style=self._style_prefixe + '.main.TFrame')
        l_year = ttk.Button(f_year, style=self._style_prefixe + '.L.TButton',
                            command=self._prev_year)
        self._header_year = ttk.Label(f_year, width=4, anchor='center',
                                      style=self._style_prefixe + '.main.TLabel', font=self._header_font)
        r_year = ttk.Button(f_year, style=self._style_prefixe + '.R.TButton',
                            command=self._next_year)
        l_year.pack(side='left', fill="y")
        self._header_year.pack(side='left', padx=4)
        r_year.pack(side='left', fill="y")

        f_month.pack(side='left', fill='x')
        f_year.pack(side='right')

        # --- *-- calendar
        self._cal_frame = ttk.Frame(self,
                                    style=self._style_prefixe + '.cal.TFrame')

        ttk.Label(self._cal_frame,
                  style=self._style_prefixe + '.headers.TLabel').grid(row=0,
                                                                      column=0,
                                                                      sticky="eswn")

        for i, d in enumerate(self._cal.formatweekheader(3).split()):
            self._cal_frame.columnconfigure(i + 1, weight=1)
            ttk.Label(self._cal_frame,
                      font=self._font,
                      style=self._style_prefixe + '.headers.TLabel',
                      anchor="center",
                      text=d, width=4).grid(row=0, column=i + 1,
                                            sticky="ew", pady=(0, 1))
        self._week_nbs = []
        self._calendar = []
        for i in range(1, 7):
            self._cal_frame.rowconfigure(i, weight=1)
            wlabel = ttk.Label(self._cal_frame, style=self._style_prefixe + '.headers.TLabel',
                               font=self._font, padding=2,
                               anchor="e", width=2)
            self._week_nbs.append(wlabel)
            wlabel.grid(row=i, column=0, sticky="esnw", padx=(0, 1))
            self._calendar.append([])
            for j in range(1, 8):
                label = ttk.Label(self._cal_frame, style=self._style_prefixe + '.normal.TLabel',
                                  font=self._font, anchor="center")
                self._calendar[-1].append(label)
                label.grid(row=i, column=j, padx=(0, 1), pady=(0, 1), sticky="nsew")
                if selectmode is "day":
                    label.bind("<1>", self._on_click)

        # --- *-- pack main elements
        header.pack(fill="x", padx=2, pady=2)
        self._cal_frame.pack(fill="both", expand=True, padx=bd, pady=bd)

        # --- bindings
        self.bind('<<ThemeChanged>>', self._setup_style)

        self._setup_style()
        self._display_calendar()

    def __getitem__(self, key):
        """Return the resource value for a KEY given as string."""
        try:
            return self._properties[key]
        except KeyError:
            raise AttributeError("Calendar object has no attribute %s." % key)

    def __setitem__(self, key, value):
        if key not in self._properties:
            raise AttributeError("Calendar object has no attribute %s." % key)
        elif key is "locale":
            raise AttributeError("This attribute cannot be modified.")
        else:
            if key is "selectmode":
                if value is "none":
                    for week in self._calendar:
                        for day in week:
                            day.unbind("<1>")
                elif value is "day":
                    for week in self._calendar:
                        for day in week:
                            day.bind("<1>", self._on_click)
                else:
                    raise ValueError("'selectmode' option should be 'none' or 'day'.")
            elif key is 'borderwidth':
                try:
                    bd = int(value)
                    self._cal_frame.pack_configure(padx=bd, pady=bd)
                except ValueError:
                    raise ValueError('expected integer for the borderwidth option.')
            elif key is "font":
                font = Font(self, value)
                prop = font.actual()
                self._font.configure(**prop)
                prop["size"] += 1
                self._header_font.configure(**prop)
                size = max(prop["size"], 10)
                self.style.configure(self._style_prefixe + '.R.TButton', arrowsize=size)
                self.style.configure(self._style_prefixe + '.L.TButton', arrowsize=size)
            elif key is "normalbackground":
                self.style.configure(self._style_prefixe + '.cal.TFrame', background=value)
                self.style.configure(self._style_prefixe + '.normal.TLabel', background=value)
                self.style.configure(self._style_prefixe + '.normal_om.TLabel', background=value)
            elif key is "normalforeground":
                self.style.configure(self._style_prefixe + '.normal.TLabel', foreground=value)
            elif key is "bordercolor":
                self.style.configure(self._style_prefixe + '.cal.TFrame', background=value)
            elif key is "othermonthforeground":
                self.style.configure(self._style_prefixe + '.normal_om.TLabel', foreground=value)
            elif key is "othermonthbackground":
                self.style.configure(self._style_prefixe + '.normal_om.TLabel', background=value)
            elif key is "othermonthweforeground":
                self.style.configure(self._style_prefixe + '.we_om.TLabel', foreground=value)
            elif key is "othermonthwebackground":
                self.style.configure(self._style_prefixe + '.we_om.TLabel', background=value)
            elif key is "selectbackground":
                self.style.configure(self._style_prefixe + '.sel.TLabel', background=value)
            elif key is "selectforeground":
                self.style.configure(self._style_prefixe + '.sel.TLabel', foreground=value)
            elif key is "weekendbackground":
                self.style.configure(self._style_prefixe + '.we.TLabel', background=value)
                self.style.configure(self._style_prefixe + '.we_om.TLabel', background=value)
            elif key is "weekendforeground":
                self.style.configure(self._style_prefixe + '.we.TLabel', foreground=value)
            elif key is "headersbackground":
                self.style.configure(self._style_prefixe + '.headers.TLabel', background=value)
            elif key is "headersforeground":
                self.style.configure(self._style_prefixe + '.headers.TLabel', foreground=value)
            elif key is "background":
                self.style.configure(self._style_prefixe + '.main.TFrame', background=value)
                self.style.configure(self._style_prefixe + '.main.TLabel', background=value)
                self.style.configure(self._style_prefixe + '.R.TButton', background=value,
                                     bordercolor=value,
                                     lightcolor=value, darkcolor=value)
                self.style.configure(self._style_prefixe + '.L.TButton', background=value,
                                     bordercolor=value,
                                     lightcolor=value, darkcolor=value)
            elif key is "foreground":
                self.style.configure(self._style_prefixe + '.R.TButton', arrowcolor=value)
                self.style.configure(self._style_prefixe + '.L.TButton', arrowcolor=value)
                self.style.configure(self._style_prefixe + '.main.TLabel', foreground=value)
            elif key is "cursor":
                ttk.Frame.configure(self, cursor=value)
            self._properties[key] = value

    def _setup_style(self, event=None):
        """Configure style."""
        self.style.layout(self._style_prefixe + '.L.TButton',
                          [('Button.focus',
                            {'children': [('Button.leftarrow', None)]})])
        self.style.layout(self._style_prefixe + '.R.TButton',
                          [('Button.focus',
                            {'children': [('Button.rightarrow', None)]})])
        active_bg = self.style.lookup('TEntry', 'selectbackground', ('focus',))

        sel_bg = self._properties.get('selectbackground')
        sel_fg = self._properties.get('selectforeground')
        cal_bg = self._properties.get('normalbackground')
        cal_fg = self._properties.get('normalforeground')
        hd_bg = self._properties.get("headersbackground")
        hd_fg = self._properties.get("headersforeground")
        bg = self._properties.get('background')
        fg = self._properties.get('foreground')
        bc = self._properties.get('bordercolor')
        om_fg = self._properties.get('othermonthforeground')
        om_bg = self._properties.get('othermonthbackground')
        omwe_fg = self._properties.get('othermonthweforeground')
        omwe_bg = self._properties.get('othermonthwebackground')
        we_bg = self._properties.get('weekendbackground')
        we_fg = self._properties.get('weekendforeground')

        self.style.configure(self._style_prefixe + '.main.TFrame', background=bg)
        self.style.configure(self._style_prefixe + '.cal.TFrame', background=bc)
        self.style.configure(self._style_prefixe + '.main.TLabel', background=bg, foreground=fg)
        self.style.configure(self._style_prefixe + '.headers.TLabel', background=hd_bg,
                             foreground=hd_fg)
        self.style.configure(self._style_prefixe + '.normal.TLabel', background=cal_bg,
                             foreground=cal_fg)
        self.style.configure(self._style_prefixe + '.normal_om.TLabel', background=om_bg,
                             foreground=om_fg)
        self.style.configure(self._style_prefixe + '.we_om.TLabel', background=omwe_bg,
                             foreground=omwe_fg)
        self.style.configure(self._style_prefixe + '.sel.TLabel', background=sel_bg,
                             foreground=sel_fg)
        self.style.configure(self._style_prefixe + '.we.TLabel', background=we_bg,
                             foreground=we_fg)
        size = max(self._header_font.actual()["size"], 10)
        self.style.configure(self._style_prefixe + '.R.TButton', background=bg,
                             arrowcolor=fg, arrowsize=size, bordercolor=bg,
                             relief="flat", lightcolor=bg, darkcolor=bg)
        self.style.configure(self._style_prefixe + '.L.TButton', background=bg,
                             arrowsize=size, arrowcolor=fg, bordercolor=bg,
                             relief="flat", lightcolor=bg, darkcolor=bg)

        self.style.map(self._style_prefixe + '.R.TButton', background=[('active', active_bg)],
                       bordercolor=[('active', active_bg)],
                       relief=[('active', 'flat')],
                       darkcolor=[('active', active_bg)],
                       lightcolor=[('active', active_bg)])
        self.style.map(self._style_prefixe + '.L.TButton', background=[('active', active_bg)],
                       bordercolor=[('active', active_bg)],
                       relief=[('active', 'flat')],
                       darkcolor=[('active', active_bg)],
                       lightcolor=[('active', active_bg)])

    def _display_calendar(self):
        """Display the days of the current month (the one in self._date)."""
        year, month = self._date.year, self._date.month

        # update header text (Month, Year)
        header = self._cal.formatmonthname(year, month, 0, False)
        self._header_month.configure(text=header.title())
        self._header_year.configure(text=str(year))

        # update calendar shown dates
        cal = self._cal.monthdatescalendar(year, month)

        m = month + 1
        y = year
        if m == 13:
            m = 1
            y += 1
        if len(cal) < 6:
            if cal[-1][-1].month == month:
                i = 0
            else:
                i = 1
            cal.append(self._cal.monthdatescalendar(y, m)[i])
            if len(cal) < 6:
                cal.append(self._cal.monthdatescalendar(y, m)[i + 1])

        week_days = {i: '.normal' for i in range(7)}
        week_days[5] = '.we'
        week_days[6] = '.we'
        prev_m = (month - 2) % 12 + 1
        months = {month: '.TLabel', m: '_om.TLabel', prev_m: '_om.TLabel'}

        week_nb = self._date.isocalendar()[1]

        for i_week in range(6):
            self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % 52 + 1))
            for i_day in range(7):
                style = self._style_prefixe + week_days[i_day] + months[cal[i_week][i_day].month]
                txt = str(cal[i_week][i_day].day)
                self._calendar[i_week][i_day].configure(text=txt,
                                                        style=style)
        self._display_selection()

    def _display_selection(self):
        """Highlight selected day."""
        if self._sel_date is not None:
            year = self._sel_date.year
            if year == self._date.year:
                _, w, d = self._sel_date.isocalendar()
                w -= self._date.isocalendar()[1]
                w %= 52
                if 0 <= w and w < 6:
                    self._calendar[w][d - 1].configure(style=self._style_prefixe + ".sel.TLabel")

    def _remove_selection(self):
        """Remove highlight of selected day."""
        if self._sel_date is not None:
            year, month = self._sel_date.year, self._sel_date.month
            if year == self._date.year:
                _, w, d = self._sel_date.isocalendar()
                w -= self._date.isocalendar()[1]
                w %= 52
                if w >= 0 and w < 6:
                    if month == self._date.month:
                        if d < 6:
                            self._calendar[w][d - 1].configure(style=self._style_prefixe + ".normal.TLabel")
                        else:
                            self._calendar[w][d - 1].configure(style=self._style_prefixe + ".we.TLabel")
                    else:
                        if d < 6:
                            self._calendar[w][d - 1].configure(style=self._style_prefixe + ".normal_om.TLabel")
                        else:
                            self._calendar[w][d - 1].configure(style=self._style_prefixe + ".we_om.TLabel")

    # --- callbacks
    def _next_month(self):
        """Display the next month."""
        year, month = self._date.year, self._date.month
        self._date = self._date + \
            self.timedelta(days=calendar.monthrange(year, month)[1])
#        if month == 12:
#            # don't increment year
#            self._date = self._date.replace(year=year)
        self._display_calendar()

    def _prev_month(self):
        """Display the previous month."""
        self._date = self._date - self.timedelta(days=1)
        self._date = self._date.replace(day=1)
        self._display_calendar()

    def _next_year(self):
        """Display the next year."""
        year = self._date.year
        self._date = self._date.replace(year=year + 1)
        self._display_calendar()

    def _prev_year(self):
        """Display the previous year."""
        year = self._date.year
        self._date = self._date.replace(year=year - 1)
        self._display_calendar()

    # --- bindings
    def _on_click(self, event):
        """Select the day on which the user clicked."""
        label = event.widget
        day = label.cget("text")
        style = label.cget("style")
        if style in [self._style_prefixe + ".normal_om.TLabel", self._style_prefixe + ".we_om.TLabel"]:
            if label in self._calendar[0]:
                self._prev_month()
            else:
                self._next_month()
        if day:
            day = int(day)
            year, month = self._date.year, self._date.month
            self._remove_selection()
            self._sel_date = self.date(year, month, day)
            self._display_selection()
            self.event_generate("<<CalendarSelected>>")

    # --- selection handling
    def selection_get(self):
        """
        Return currently selected date (datetime.date instance).
        Always return None if selectmode is "none".
        """
        if self._properties.get("selectmode") is "day":
            return self._sel_date
        else:
            return None

    def selection_set(self, date):
        """
        Set the selection to date.

        date can be either a datetime.date
        instance or a string corresponding to the date format "%x"
        in the Calendar locale.

        Do nothing if selectmode is "none".
        """
        if self._properties.get("selectmode") is "day":
            if date is None:
                self._remove_selection()
                self._sel_date = None
            else:
                if isinstance(date, self.date):
                    self._sel_date = date
                else:
                    try:
                        self._sel_date = self.strptime(date, "%x")
                    except Exception as e:
                        raise type(e)("%r is not a valid date." % date)
                self._date = self._sel_date.replace(day=1)
                self._display_calendar()
                self._display_selection()

    # --- other methods
    def keys(self):
        """Return a list of all resource names of this widget."""
        return list(self._properties.keys())

    def cget(self, key):
        """Return the resource value for a KEY given as string."""
        return self[key]

    def configure(self, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        for item, value in kw.items():
            self[item] = value

    def config(self, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        for item, value in kw.items():
            self[item] = value


class DateEntry(ttk.Entry):
    """Date selection entry with drop-down calendar."""

    entry_kw = {'exportselection': 1,
                'invalidcommand': '',
                'justify': 'left',
                'show': '',
                'cursor': 'xterm',
                'style': '',
                'state': 'normal',
                'takefocus': 'ttk::takefocus',
                'textvariable': '',
                'validate': 'none',
                'validatecommand': '',
                'width': 20,
                'xscrollcommand': ''}

    def __init__(self, master=None, **kw):
        """
        Create an entry with a drop-down calendar to select a date.

        When the entry looses focus, if the user input is not a valid date,
        the entry content is reset to the last valid date.

        KEYWORDS OPTIONS

            usual ttk.Entry options and Calendar options

        VIRTUAL EVENTS

            A <<DateEntrySelected>> event is generated each time
            the user selects a date.
        """
        # sort keywords between entry options and calendar options
        kw['selectmode'] = 'day'
        entry_kw = {}

        for key in self.entry_kw:
            entry_kw[key] = kw.pop(key, self.entry_kw[key])
        entry_kw['font'] = kw.get('font', None)

        # set locale to have the right date format
        loc = kw.get('locale', '')
        locale.setlocale(locale.LC_ALL, loc)

        ttk.Entry.__init__(self, master, **entry_kw)
        # down arrow button bbox (to detect if it was clicked upon)
        self._down_arrow_bbox = [0, 0, 0, 0]

        # drop-down calendar
        self._top_cal = tk.Toplevel(self)
        self._top_cal.withdraw()
        if platform == "linux":
            self._top_cal.attributes('-type', 'DROPDOWN_MENU')
        self._top_cal.overrideredirect(True)
        self._calendar = Calendar(self._top_cal, **kw)
        self._calendar.pack()

        # style
        self.style = ttk.Style(self)
        self._setup_style()
        self.configure(style='DateEntry')

        # add validation to Entry so that only date in the locale '%x' format
        # are accepted
        validatecmd = self.register(self._validate_date)
        self.configure(validate='focusout',
                       validatecommand=validatecmd)

        # initially selected date
        self._date = self._calendar.selection_get()
        if self._date is None:
            self._date = self._calendar.date.today()
        self.insert(0, self._date.strftime('%x'))

        # --- bindings
        # reconfigure style if theme changed
        self.bind('<<ThemeChanged>>',
                  lambda e: self.after(10, self._setup_style))
        # determine new downarrow button bbox
        self.bind('<Configure>', self._determine_bbox)
        self.bind('<Map>', self._determine_bbox)
        # hide drop-down calendar when window is moved
        master = self.master
        while not (isinstance(master, tk.Toplevel) or isinstance(master, tk.Tk)):
            master = master.master
        funcid = master.bind('<Configure>', self._on_move, True)
        self.bind('<Destroy>', lambda e: _unbind(master, '<Configure>', funcid))
        # handle appearence to make the entry behave like a Combobox but with
        # a drop-down calendar instead of a drop-down list
        self.bind('<Leave>', lambda e: self.state(['!active']))
        self.bind('<Motion>', self._on_motion)
        self.bind('<ButtonPress-1>', self._on_b1_press)
        self.bind('<ButtonRelease-1>', self._on_b1_release)
        # update entry content when date is selected in the Calendar
        self._calendar.bind('<<CalendarSelected>>', self._select)
        # hide calendar if it looses focus
        self._calendar.bind('<FocusOut>', self._on_focus_out_cal)

    def __getitem__(self, key):
        """Return the resource value for a KEY given as string."""
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _setup_style(self, event=None):
        """Style configuration."""
        self.style.layout('DateEntry', self.style.layout('TCombobox'))
        fieldbg = self.style.map('TCombobox', 'fieldbackground')
        self.style.map('DateEntry', fieldbackground=fieldbg)

    def _determine_bbox(self, event=None):
        """Determine downarrow button bbox."""
        if self.winfo_ismapped():
            self.update_idletasks()
            h = self.winfo_height()
            w = self.winfo_width()
            y = h // 2
            x = 0
            if self.identify(x, y):
                while x < w and self.identify(x, y) != 'downarrow':
                    x += 1
                if x < w:
                    self._down_arrow_bbox = [x, 0, w, h]
            else:
                self.after(10, self._determine_bbox)

    def _on_motion(self, event):
        """Set widget state depending on mouse position to mimic Combobox behavior."""
        x, y = event.x, event.y
        x1, y1, x2, y2 = self._down_arrow_bbox
        if 'disabled' not in self.state():
            if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                self.state(['active'])
                self.configure(cursor='arrow')
            else:
                self.state(['!active'])
                if 'readonly' not in self.state():
                    self.configure(cursor='xterm')

    def _on_b1_press(self, event):
        """Trigger self.drop_down on downarrow button press and set widget state to ['pressed', 'active']."""
        x, y = event.x, event.y
        x1, y1, x2, y2 = self._down_arrow_bbox
        if (('disabled' not in self.state()) and
                x >= x1 and x <= x2 and y >= y1 and y <= y2):
            self.state(['pressed', 'active'])
            self.drop_down()

    def _on_b1_release(self, event):
        """Remove 'pressed' from widget's states when the downarrow button is released."""
        x, y = event.x, event.y
        x1, y1, x2, y2 = self._down_arrow_bbox
        if (('disabled' not in self.state()) and
                x >= x1 and x <= x2 and y >= y1 and y <= y2):
            self.state(['!pressed', 'active'])

    def _on_move(self, event):
        """Withdraw drop-down calendar if window is moved."""
        self._top_cal.withdraw()

    def _on_focus_out_cal(self, event):
        """Withdraw drop-down calendar when it looses focus."""
        if self.focus_get() is not None:
            if self.focus_get() == self:
                x, y = event.x, event.y
                x1, y1, x2, y2 = self._down_arrow_bbox
                if (type(x) != int or type(y) != int or
                        not (x >= x1 and x <= x2 and y >= y1 and y <= y2)):
                    self._top_cal.withdraw()
            else:
                self._top_cal.withdraw()

    def _validate_date(self):
        """Date entry validation: only dates in locale '%x' format are accepted."""
        try:
            self._date = self._calendar.strptime(self.get(), '%x')
            return True
        except ValueError:
            self.delete(0, 'end')
            self.insert(0, self._date.strftime('%x'))
            return False

    def _select(self, event=None):
        """Display the selected date in the entry and hide the calendar."""
        date = self._calendar.selection_get()
        if date is not None:
            if 'readonly' in self.state():
                readonly = True
                self.state(('!readonly',))
            else:
                readonly = False
            self.delete(0, 'end')
            self.insert(0, date.strftime('%x'))
            self.event_generate('<<DateEntrySelected>>')
            if readonly:
                self.state(('readonly',))
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self._calendar.strptime(self.get(), '%x')
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date.date())

    def state(self, *args):
        """
        Modify or inquire widget state.

        Widget state is returned if statespec is None, otherwise it is
        set according to the statespec flags and then a new state spec
        is returned indicating which flags were changed. statespec is
        expected to be a sequence.
        """
        if args:
            # change cursor depending on state to mimic Combobox behavior
            states = args[0]
            if 'disabled' in states or 'readonly' in states:
                self.configure(cursor='arrow')
            elif '!disabled' in states or '!readonly' in states:
                self.configure(cursor='xterm')
        return ttk.Entry.state(self, *args)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = list(self.entry_kw)
        keys.extend(self._calendar.keys())
        return list(set(keys))

    def cget(self, key):
        """Return the resource value for a KEY given as string."""
        if key in self.entry_kw:
            return ttk.Entry.cget(self, key)
        else:
            return self._calendar.cget(key)

    def configure(self, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        entry_kw = {}
        keys = list(kw.keys())
        for key in keys:
            if key in self.entry_kw:
                entry_kw[key] = kw.pop(key)
        font = kw.get('font', None)
        if font is not None:
            entry_kw['font'] = font
        ttk.Entry.configure(self, **entry_kw)
        self._calendar.configure(**kw)

    def config(self, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        self.configure(**kw)

    def set_date(self, date):
        """
        Set the value of the dateentry to date.

        date can be a datetime.date, a datetime.datetime or a string
        in locale '%x' format.
        """
        try:
            txt = date.strftime('%x')
        except AttributeError:
            txt = str(date)
            try:
                self._calendar.strptime(txt, '%x')
            except Exception as e:
                raise type(e)("%r is not a valid date." % date)
        self.delete(0, 'end')
        self.insert(0, txt)

    def get_date(self):
        """Return the content of the dateentry as a datetime.datetime instance."""
        self._validate_date()
        date = self.get()
        return self._calendar.strptime(date, '%x')


if __name__ == "__main__":

    def example1():
        def print_sel():
            print(cal.selection_get())

        top = tk.Toplevel(root)

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def example2():
        top = tk.Toplevel(root)
        top.grab_set()

        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)

    root = tk.Tk()
    s = ttk.Style(root)
    s.theme_use('clam')

    ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
    ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)

    root.mainloop()
