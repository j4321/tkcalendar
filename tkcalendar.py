# -*- coding: utf-8 -*-
"""
tkcalendar - Calendar widget for Tkinter
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


Calendar
"""

import calendar
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.font import Font
except ImportError:
    import Tkinter as tk
    import ttk
    from tkFont import Font

class Calendar(ttk.Frame):
    """ Calendar widget """
    date = calendar.datetime.date
    timedelta = calendar.datetime.timedelta
    strptime = calendar.datetime.datetime.strptime

    def __init__(self, master=None, **kw):
        """
            Construct a Calendar with parent master.

            STANDARD OPTIONS

                cursor, font

            WIDGET-SPECIFIC OPTIONS

                year, month: initially displayed month, default is current month

                day: initially selected day, if month or year is given but not
                    day, no initial selection, otherwise, default is today

                locale: locale to use, e.g. "fr_FR" for a French calendar

                selectmode: "none" or "day" (default) define whether the user
                            can change the selected day with a mouse click

                background: calendar border and month/year name background color

                foreground: month/year name foreground color

                bordercolor: day border color

                selectbackground: selected day background color

                selectforeground: selected day foreground color

                normalbackground: normal week days background color

                normalforeground: normal week days foreground color

                othermonthforeground: foreground color for days belonging to
                                      the previous/next month

                weekendbackground: week-end days background color

                weekendforeground: week-end days foreground color

                headersbackground: day names and week numbers background color

                headersforeground: day names and week numbers foreground color

            VIRTUAL EVENTS

                A <<CalendarSelected>> event is generated each time the user
                selects a day with the mouse.
        """

        curs = kw.pop("cursor", "")
        font = kw.pop("font", "")
        classname = kw.pop('class_', "Calendar")
        ttk.Frame.__init__(self, master, class_=classname, cursor=curs)
        self._style_prefixe = '%s.%s' % (self.winfo_name(), self.winfo_class())
        ttk.Frame.configure(self, style=self._style_prefixe + '.main.TFrame')

        self._font = Font(self, font)
        prop = self._font.actual()
        prop["size"] += 1
        self._header_font = Font(self, **prop)

        self._properties = {"cursor": curs, "font": font}

        ### date
        today = self.date.today()

        if (("month" in kw) or ("year" in kw)) and (not "day" in kw):
            month = kw.pop("month", today.month)
            year = kw.pop('year', today.year)
            self._sel_date = None  # selected day
        else:
            day = kw.pop('day', today.day)
            month = kw.pop("month", today.month)
            year = kw.pop('year', today.year)
            self._sel_date = self.date(year, month, day)  # selected day
        self._date = self.date(year, month, 1)  # (year, month) displayed by the calendar

        ### selectmode
        self._properties["selectmode"] = selectmode = kw.get("selectmode", "day")
        if not selectmode in ("none", "day"):
            raise ValueError("'selectmode' option should be 'none' or 'day'.")

        ### locale
        self._properties["locale"] = locale = kw.get("locale", None)
        if locale is None:
            self._cal = calendar.TextCalendar(calendar.MONDAY)
        else:
            self._cal = calendar.LocaleTextCalendar(calendar.MONDAY, locale)

        ### style
        self.style = ttk.Style(self)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        self.style.layout(self._style_prefixe + '.L.TButton', arrow_layout('left'))
        self.style.layout(self._style_prefixe + '.R.TButton', arrow_layout('right'))
        active_bg = self.style.lookup('TEntry', 'selectbackground', ('focus',))
        sel_bg = kw.get('selectbackground', active_bg)
        sel_fg = kw.get('selectforeground', 'white')
        cal_bg = kw.get('normalbackground', 'white')
        cal_fg = kw.get('normalforeground', 'black')
        hd_bg = kw.get("headersbackground", "gray70")
        hd_fg = kw.get("headersforeground", "black")
        bg = kw.get('background', '#424242')
        fg = kw.get('foreground', 'white')
        bc = kw.get('bordercolor', hd_bg)
        om_fg = kw.get('othermonthforeground', 'gray')
        we_bg = kw.get('weekendbackground', 'gray80')
        we_fg = kw.get('weekendforeground', '#424242')

        self._properties.update({'selectbackground': sel_bg,
                                 'selectforeground': sel_fg,
                                 'normalbackground': cal_bg,
                                 'normalforeground': cal_fg,
                                 'background': bg,
                                 'foreground': fg,
                                 'bordercolor': bc,
                                 'othermonthforeground': om_fg,
                                 'weekendbackground': we_bg,
                                 'weekendforeground': we_fg,
                                 'headersbackground': hd_bg,
                                 'headersforeground': hd_fg})

        self.style.configure(self._style_prefixe + '.main.TFrame', background=bg)
        self.style.configure(self._style_prefixe + '.cal.TFrame', background=bc)
        self.style.configure(self._style_prefixe + '.main.TLabel', background=bg, foreground=fg)
        self.style.configure(self._style_prefixe + '.headers.TLabel', background=hd_bg,
                             foreground=hd_fg)
        self.style.configure(self._style_prefixe + '.normal.TLabel', background=cal_bg,
                             foreground=cal_fg)
        self.style.configure(self._style_prefixe + '.normal_om.TLabel', background=cal_bg,
                             foreground=om_fg)
        self.style.configure(self._style_prefixe + '.we_om.TLabel', background=we_bg,
                             foreground=om_fg)
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
                       darkcolor=[('active', active_bg)],
                       lightcolor=[('active', active_bg)])
        self.style.map(self._style_prefixe + '.L.TButton', background=[('active', active_bg)],
                       bordercolor=[('active', active_bg)],
                       darkcolor=[('active', active_bg)],
                       lightcolor=[('active', active_bg)])

        ### init calendar
        ### *-- header: month - year
        header = ttk.Frame(self, style=self._style_prefixe + '.main.TFrame')

        f_month = ttk.Frame(header, style=self._style_prefixe + '.main.TFrame')
        l_month = ttk.Button(f_month, style=self._style_prefixe + '.L.TButton',
                         command=self._prev_month)
        self._header_month = ttk.Label(f_month, width=10, anchor='center',
                                       style=self._style_prefixe + '.main.TLabel', font=self._header_font)
        r_month = ttk.Button(f_month, style=self._style_prefixe + '.R.TButton',
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

        ### *-- calendar
        cal = ttk.Frame(self, style=self._style_prefixe + '.cal.TFrame')

        ttk.Label(cal, style=self._style_prefixe + '.headers.TLabel').grid(row=0, column=0,
                                                             sticky="eswn")

        for i, d in enumerate(self._cal.formatweekheader(3).split()):
            cal.columnconfigure(i + 1, weight=1)
            ttk.Label(cal,
                      font=self._font,
                      style=self._style_prefixe + '.headers.TLabel',
                      anchor="center",
                      text=d, width=4).grid(row=0, column=i + 1,
                                            sticky="ew", pady=(0,1))
        self._week_nbs = []
        self._calendar = []
        for i in range(1,7):
            cal.rowconfigure(i, weight=1)
            wlabel = ttk.Label(cal, style=self._style_prefixe + '.headers.TLabel',
                               font=self._font, padding=2,
                               anchor="e", width=2)
            self._week_nbs.append(wlabel)
            wlabel.grid(row=i, column=0, sticky="esnw", padx=(0, 1))
            self._calendar.append([])
            for j in range(1,8):
                label = ttk.Label(cal, style=self._style_prefixe + '.normal.TLabel',
                                  font=self._font, anchor="center")
                self._calendar[-1].append(label)
                label.grid(row=i, column=j, padx=(0,1), pady=(0,1), sticky="nsew")
                if selectmode == "day":
                    label.bind("<1>", self._on_click)

        ### *-- pack main elements
        header.pack(fill="x", padx=2, pady=2)
        cal.pack(fill="both", expand=True, padx=(2, 1), pady=(2, 1))

        self._display_calendar()

    def __getitem__(self, item):
        try:
            return self._properties[item]
        except KeyError:
            raise AttributeError("Calendar object has no attribute %s." % item)

    def __setitem__(self, item, value):
        if not item in self._properties:
            raise AttributeError("Calendar object has no attribute %s." % item)
        elif item == "locale":
            raise AttributeError("This attribute cannot be modified.")
        else:
            if item == "selectmode":
                if value == "none":
                    for week in self._calendar:
                        for day in week:
                            day.unbind("<1>")
                elif value == "day":
                    for week in self._calendar:
                        for day in week:
                            day.bind("<1>", self._on_click)
                else:
                    raise ValueError("'selectmode' option should be 'none' or 'day'.")
            elif item == "font":
                font = Font(self, value)
                prop = font.actual()
                self._font.configure(**prop)
                prop["size"] += 1
                self._header_font.configure(**prop)
                size = max(prop["size"], 10)
                self.style.configure(self._style_prefixe + '.R.TButton', arrowsize=size)
                self.style.configure(self._style_prefixe + '.L.TButton', arrowsize=size)
            elif item == "normalbackground":
                self.style.configure(self._style_prefixe + '.cal.TFrame', background=value)
                self.style.configure(self._style_prefixe + '.normal.TLabel', background=value)
                self.style.configure(self._style_prefixe + '.normal_om.TLabel', background=value)
            elif item == "normalforeground":
                self.style.configure(self._style_prefixe + '.normal.TLabel', foreground=value)
            elif item == "bordercolor":
                self.style.configure(self._style_prefixe + '.cal.TFrame', background=value)
            elif item == "othermonthforeground":
                self.style.configure(self._style_prefixe + '.normal_om.TLabel', foreground=value)
                self.style.configure(self._style_prefixe + '.we_om.TLabel', foreground=value)
            elif item == "selectbackground":
                self.style.configure(self._style_prefixe + '.sel.TLabel', background=value)
            elif item == "selectforeground":
                self.style.configure(self._style_prefixe + '.sel.TLabel', foreground=value)
            elif item == "weekendbackground":
                self.style.configure(self._style_prefixe + '.we.TLabel', background=value)
                self.style.configure(self._style_prefixe + '.we_om.TLabel', background=value)
            elif item == "weekendforeground":
                self.style.configure(self._style_prefixe + '.we.TLabel', foreground=value)
            elif item == "headersbackground":
                self.style.configure(self._style_prefixe + '.headers.TLabel', background=value)
            elif item == "headersforeground":
                self.style.configure(self._style_prefixe + '.headers.TLabel', foreground=value)
            elif item == "background":
                self.style.configure(self._style_prefixe + '.main.TFrame', background=value)
                self.style.configure(self._style_prefixe + '.main.TLabel', background=value)
                self.style.configure(self._style_prefixe + '.R.TButton', background=value,
                                     bordercolor=value,
                                     lightcolor=value, darkcolor=value)
                self.style.configure(self._style_prefixe + '.L.TButton', background=value,
                                     bordercolor=value,
                                     lightcolor=value, darkcolor=value)
            elif item == "foreground":
                self.style.configure(self._style_prefixe + '.R.TButton', arrowcolor=value)
                self.style.configure(self._style_prefixe + '.L.TButton', arrowcolor=value)
                self.style.configure(self._style_prefixe + '.main.TLabel', foreground=value)
            elif item == "cursor":
                ttk.TFrame.configure(self, cursor=value)
            self._properties[item] = value

    def _display_calendar(self):
        """ Display the days of the current month (the one in self._date). """
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
            cal.append(self._cal.monthdatescalendar(y, m)[1])
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
        """ Highlight selected day. """
        if self._sel_date is not None:
           year = self._sel_date.year
           if year == self._date.year:
               _, w, d = self._sel_date.isocalendar()
               w -= self._date.isocalendar()[1]
               w %= 52
               if 0 <= w and w < 6:
                   self._calendar[w][d - 1].configure(style=self._style_prefixe + ".sel.TLabel")

    def _remove_selection(self):
        """ Remove highlight of selected day. """
        if self._sel_date is not None:
           year, month = self._sel_date.year, self._sel_date.month
           if year == self._date.year:
               _, w, d = self._sel_date.isocalendar()
               w -= self._date.isocalendar()[1]
               w %= 52
               if w >=0 and w < 6:
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

    ### callbacks
    def _next_month(self):
        """ Display the next month. """
        year, month = self._date.year, self._date.month
        self._date = self._date + \
                     self.timedelta(days=calendar.monthrange(year, month)[1])
        if month == 12:
            # don't increment year
            self._date = self._date.replace(year=year)
        self._display_calendar()

    def _prev_month(self):
        """ Display the previous month. """
        self._date = self._date - self.timedelta(days=1)
        self._date = self._date.replace(day=1)
        self._display_calendar()

    def _next_year(self):
        """ Display the next year. """
        year = self._date.year
        self._date = self._date.replace(year=year + 1)
        self._display_calendar()

    def _prev_year(self):
        """ Display the previous year. """
        year = self._date.year
        self._date = self._date.replace(year=year - 1)
        self._display_calendar()

    ### bindings
    def _on_click(self, event):
        """ Select the day on which the user clicked. """
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
            year, month = self._date.year,  self._date.month
            self._remove_selection()
            self._sel_date = self.date(year, month, day)
            self._display_selection()
            self.event_generate("<<CalendarSelected>>")

    ### selection handling
    def selection_get(self):
        """
            Return currently selected date (datetime.date instance).
            Always return None if selectmode is "none".
        """
        if self._properties.get("selectmode") == "day":
            return self._sel_date
        else:
            return None

    def selection_set(self, date):
        """
            Set the selection to date. date can be either a datetime.date
            instance or a string corresponding to the date format "%x"
            in the Calendar locale.

            Do nothing if selectmode is "none".
        """
        if self._properties.get("selectmode") == "day":
            if date is None:
                self._remove_selection()
                self._sel_date = None
            else:
                if type(date) == self.date:
                    self._sel_date = date
                else:
                    self._sel_date = self.strptime(date, "%x")
                self._date = self._sel_date.replace(day=1)
                self._display_calendar()
                self._display_selection()

    ### other methods
    def keys(self):
        """ Return a list of all resource names of this widget. """
        return list(self._properties.keys())

    def cget(self, key):
        """ Return the resource value for a KEY given as string. """
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


if __name__ =="__main__":

    def print_sel():
        print(cal.selection_get())

    root = tk.Tk()
    s = ttk.Style(root)
    s.theme_use('clam')
    cal = Calendar(root, locale="fr_FR.UTF-8",
                   font="Arial 14", selectmode='none',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(root, text="ok", command=print_sel).pack()

    root.mainloop()
