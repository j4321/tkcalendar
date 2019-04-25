# -*- coding: utf-8 -*-
"""
tkcalendar - Calendar and DateEntry widgets for Tkinter
Copyright 2017-2018 Juliette Monsel <j_4321@protonmail.com>

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

Test
"""


from tests import BaseWidgetTest, TestEvent, tk, ttk, format_date
from tkcalendar import Calendar
from datetime import date, datetime


class TestCalendar(BaseWidgetTest):
    def test_calendar_init(self):
        widget = Calendar(self.window)
        widget.pack()
        self.window.update()
        widget.destroy()
        widget = Calendar(self.window, showweeknumbers=False)
        self.window.update()
        widget.destroy()
        today = format_date(date.today(), 'short')
        var = tk.StringVar(self.window, today)
        widget = Calendar(self.window, textvariable=var, month=3, year=2011, day=10)
        self.window.update()
        self.assertEqual(var.get(), today)
        self.assertEqual(widget.selection_get(), date.today())
        widget.destroy()
        widget = Calendar(self.window, font="Arial 14", selectmode='day',
                          cursor="hand1", year=2018, month=2, day=5)
        widget.pack()
        self.window.update()
        self.assertEqual(widget.selection_get(), date(2018, 2, 5))
        self.assertEqual(widget.get_displayed_month(), (2, 2018))
        w, d = widget._get_day_coords(date(2018, 2, 5))
        self.assertEqual(widget._calendar[w][d].cget('text'), '5')
        widget.destroy()

        widget = Calendar(self.window, year=2011, month=2, day=35)
        widget.pack()
        self.window.update()
        self.assertIsNone(widget.selection_get())
        self.assertEqual(widget._date, date(2011, 2, 1))
        widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, month=23)
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, borderwidth="e")
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(TypeError):
            widget = Calendar(self.window, weekenddays=7)
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, weekenddays="e")
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, weekenddays=[1])
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, weekenddays=['a', 'b'])
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, weekenddays=[12, 3])
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(TypeError):
            widget = Calendar(self.window, maxdate="e")
            widget.pack()
            self.window.update()
            widget.destroy()

        widget = Calendar(self.window, mindate=datetime(2013, 5, 22, 10, 5),
                          maxdate=datetime.today())
        widget.pack()
        self.window.update()
        widget.destroy()

        with self.assertRaises(TypeError):
            widget = Calendar(self.window, mindate="e")
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, mindate=date(2018, 4, 5),
                              maxdate=date(2018, 4, 4))
            widget.pack()
            self.window.update()
            widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, firstweekday="e")
            widget.pack()
            self.window.update()
            widget.destroy()

        widget = Calendar(self.window, font="Arial 14", selectmode='day',
                          cursor="hand1", year=2018, month=2, day=5)
        widget.pack()
        self.window.update()
        widget.destroy()

        widget = Calendar(self.window, selectmode='none',
                          year=2015, month=1, background="black",
                          foreground="white", key="a")
        widget.pack()
        self.window.update()
        self.assertIsNone(widget.selection_get())
        self.assertEqual(widget._date, date(2015, 1, 1))
        widget.destroy()

        with self.assertRaises(ValueError):
            widget = Calendar(self.window, selectmode='wrong')
            widget.pack()
            self.window.update()
            widget.destroy()

    def test_calendar_selection(self):
        widget = Calendar(self.window, month=3, year=2011, day=10,
                          maxdate=date(2013, 1, 1), mindate=date(2010, 1, 1))
        widget.pack()
        self.assertEqual(widget.selection_get(), date(2011, 3, 10))

        widget.selection_set(date(2012, 4, 11))
        self.assertEqual(widget.selection_get(), date(2012, 4, 11))
        self.assertEqual(widget._date, date(2012, 4, 1))
        widget.selection_set(datetime(2012, 5, 11))
        self.assertEqual(widget.selection_get(), date(2012, 5, 11))
        self.assertNotIsInstance(widget.selection_get(), datetime)
        self.assertIsInstance(widget.selection_get(), date)
        widget.selection_set(datetime(2012, 5, 21).strftime('%x'))
        self.assertEqual(widget.selection_get(), date(2012, 5, 21))
        self.assertNotIsInstance(widget.selection_get(), datetime)
        self.assertIsInstance(widget.selection_get(), date)

        widget.selection_set(date(2018, 4, 11))
        self.assertEqual(widget.selection_get(), date(2013, 1, 1))
        widget.selection_set(date(2001, 4, 11))
        self.assertEqual(widget.selection_get(), date(2010, 1, 1))
        widget.selection_clear()
        self.assertIsNone(widget.selection_get())

    def test_calendar_buttons_functions(self):
        widget = Calendar(self.window)
        widget.pack()
        widget._prev_month()
        widget._next_month()
        widget._prev_year()
        widget._next_year()
        widget._remove_selection()
        widget.selection_set(format_date(date(2018, 12, 31), 'short'))
        self.assertEqual(widget.selection_get(), date(2018, 12, 31))
        with self.assertRaises(ValueError):
            widget.selection_set("ab")
        widget.selection_set(None)
        self.assertIsNone(widget.selection_get())
        widget.selection_set(date(2015, 12, 31))
        self.assertEqual(widget.selection_get(), date(2015, 12, 31))

        widget.config(selectmode='none')
        self.assertIsNone(widget.selection_get())
        l = ttk.Label(widget, text="12")
        widget._on_click(TestEvent(widget=l))
        self.assertIsNone(widget.selection_get())
        self.window.update()
        widget.config(selectmode='day')
        l = ttk.Label(widget, text="12")
        widget._on_click(TestEvent(widget=l))
        self.window.update()
        self.assertEqual(widget.selection_get(), date(2015, 12, 12))
        widget.config(state='disabled')
        l = ttk.Label(widget, text="14")
        widget._on_click(TestEvent(widget=l))
        self.window.update()
        self.assertEqual(widget.selection_get(), date(2015, 12, 12))
        widget.config(state='normal')
        self.assertEqual(widget._date, date(2015, 12, 1))
        widget.see(date(2017, 3, 11))
        self.window.update()
        self.assertEqual(widget._date, date(2017, 3, 1))

    def test_calendar_textvariable(self):
        var = tk.StringVar(self.window)
        widget = Calendar(self.window, selectmode='day',
                          year=2015, month=1, day=3, textvariable=var)
        widget.pack()
        self.window.update()
        self.assertEqual('', var.get())
        self.assertEqual('', widget.get_date())
        self.assertEqual(date(2015, 1, 1), widget._date)
        widget.selection_set(date(2018, 11, 21))
        self.window.update()
        self.assertEqual(format_date(date(2018, 11, 21), 'short'), var.get())
        self.assertEqual(format_date(date(2018, 11, 21), 'short'), widget.get_date())
        widget.selection_set(None)
        self.window.update()
        self.assertEqual('', widget.get_date())
        self.assertEqual('', var.get())
        var.set(format_date(date(2014, 3, 2), 'short'))
        self.window.update()
        self.assertEqual(date(2014, 3, 2), widget.selection_get())
        self.assertEqual(format_date(date(2014, 3, 2), 'short'), var.get())
        self.assertEqual(format_date(date(2014, 3, 2), 'short'), widget.get_date())
        try:
            var.set('a')
        except tk.TclError:
            # some versions of python raise an error because of the exception
            # raised inside the trace
            pass
        self.window.update()
        self.assertEqual(date(2014, 3, 2), widget.selection_get())
        self.assertEqual(format_date(date(2014, 3, 2), 'short'), var.get())
        self.assertEqual(format_date(date(2014, 3, 2), 'short'), widget.get_date())
        var.set('')
        self.window.update()
        self.assertIsNone(widget.selection_get())
        self.assertEqual('', var.get())
        self.assertEqual('', widget.get_date())

        var2 = tk.StringVar(widget, format_date(date(2011, 1, 21), 'short'))
        widget['textvariable'] = var2
        self.window.update()
        self.assertEqual(widget.get_date(), var2.get())
        self.assertEqual('', var.get())

    def test_calendar_get_set(self):
        widget = Calendar(self.window, foreground="red")
        widget.pack()
        self.window.update()

        options = ['cursor',
                   'font',
                   'borderwidth',
                   'state',
                   'selectmode',
                   'textvariable',
                   'locale',
                   'mindate',
                   'maxdate',
                   'firstweekday',
                   'weekenddays',
                   'showweeknumbers',
                   'showothermonthdays',
                   'selectbackground',
                   'selectforeground',
                   'disabledselectbackground',
                   'disabledselectforeground',
                   'normalbackground',
                   'normalforeground',
                   'background',
                   'foreground',
                   'bordercolor',
                   'disabledbackground',
                   'disabledforeground',
                   'othermonthforeground',
                   'othermonthbackground',
                   'othermonthweforeground',
                   'othermonthwebackground',
                   'weekendbackground',
                   'weekendforeground',
                   'headersbackground',
                   'headersforeground',
                   'disableddaybackground',
                   'disableddayforeground',
                   'tooltipbackground',
                   'tooltipforeground',
                   'tooltipalpha',
                   'tooltipdelay']

        self.assertEqual(sorted(widget.keys()), sorted(options))

        with self.assertRaises(AttributeError):
            widget.cget("test")

        self.assertEqual(widget["foreground"], "red")
        widget["foreground"] = "blue"
        self.window.update()
        self.assertEqual(widget["foreground"], "blue")

        widget.config(cursor="watch")
        self.window.update()
        self.assertEqual(widget["cursor"], "watch")
        self.assertTrue(widget["showweeknumbers"])
        self.assertNotEqual(widget._week_nbs[0].grid_info(), {})
        widget.config(showweeknumbers=False)
        self.window.update()
        self.assertFalse(widget["showweeknumbers"])
        self.assertEqual(widget._week_nbs[0].grid_info(), {})
        self.assertFalse(widget._week_nbs[0].winfo_ismapped())
        self.assertNotEqual(widget._calendar[-1][-1].cget('text'), '')
        self.assertTrue(widget["showothermonthdays"])
        widget.config(showothermonthdays=False)
        self.window.update()
        self.assertFalse(widget["showothermonthdays"])
        self.assertEqual(widget._calendar[-1][-1].cget('text'), '')
        widget.config(font="Arial 20 bold")
        self.window.update()
        self.assertEqual(widget["font"], "Arial 20 bold")
        widget.config(borderwidth=5)
        self.window.update()
        self.assertEqual(widget["borderwidth"], 5)
        with self.assertRaises(ValueError):
            widget.config(borderwidth="a")
        widget.config(firstweekday='sunday')
        self.window.update()
        self.assertEqual(widget["firstweekday"], 'sunday')
        with self.assertRaises(ValueError):
            widget.config(firstweekday="a")

        widget.config(weekenddays=[5, 7])
        self.window.update()
        we_style = 'we.%s.TLabel' % widget._style_prefixe
        normal_style = 'normal.%s.TLabel' % widget._style_prefixe
        for i in range(7):
            self.assertEqual(widget._calendar[0][i].cget('style'), we_style if (i + 1) in [5, 7] else normal_style)

        widget["mindate"] = datetime(2018, 9, 10)
        self.assertEqual(widget["mindate"], date(2018, 9, 10))
        widget.selection_set(date(2018, 9, 23))
        self.window.update()
        i, j = widget._get_day_coords(date(2018, 9, 2))
        self.assertIn('disabled', widget._calendar[i][j].state())
        i, j = widget._get_day_coords(date(2018, 9, 21))
        self.assertNotIn('disabled', widget._calendar[i][j].state())
        self.assertIn('disabled', widget._l_month.state())
        self.assertIn('disabled', widget._l_year.state())
        with self.assertRaises(TypeError):
            widget.config(mindate="a")
        self.assertEqual(widget["mindate"], date(2018, 9, 10))
        widget["mindate"] = None
        self.window.update()
        self.assertIsNone(widget["mindate"])
        i, j = widget._get_day_coords(date(2018, 9, 2))
        self.assertNotIn('disabled', widget._calendar[i][j].state())
        self.assertNotIn('disabled', widget._l_month.state())
        self.assertNotIn('disabled', widget._l_year.state())

        widget["maxdate"] = datetime(2018, 9, 10)
        self.assertEqual(widget["maxdate"], date(2018, 9, 10))
        widget.selection_set(date(2018, 9, 2))
        self.window.update()
        i, j = widget._get_day_coords(date(2018, 9, 22))
        self.assertIn('disabled', widget._calendar[i][j].state())
        i, j = widget._get_day_coords(date(2018, 9, 4))
        self.assertNotIn('disabled', widget._calendar[i][j].state())
        self.assertIn('disabled', widget._r_month.state())
        self.assertIn('disabled', widget._r_year.state())
        with self.assertRaises(TypeError):
            widget.config(maxdate="a")
        self.assertEqual(widget["maxdate"], date(2018, 9, 10))
        widget["maxdate"] = None
        self.window.update()
        self.assertIsNone(widget["maxdate"])
        i, j = widget._get_day_coords(date(2018, 9, 22))
        self.assertNotIn('disabled', widget._calendar[i][j].state())
        self.assertNotIn('disabled', widget._r_month.state())
        self.assertNotIn('disabled', widget._r_year.state())

        widget.config(selectmode="none")
        self.window.update()
        self.assertEqual(widget["selectmode"], "none")
        widget.config(selectmode="day")
        self.window.update()
        self.assertEqual(widget["selectmode"], "day")
        with self.assertRaises(ValueError):
            widget.config(selectmode="a")
        self.assertEqual(widget.cget('state'), tk.NORMAL)
        with self.assertRaises(ValueError):
            widget.config(state="test")
        with self.assertRaises(AttributeError):
            widget.config(locale="en_US.UTF-8")
        with self.assertRaises(AttributeError):
            widget.config(test="test")
        dic = {op: "yellow" for op in options[12:-4]}
        widget.configure(**dic)
        self.window.update()
        for op in options[12:-4]:
            self.assertEqual(widget.cget(op), "yellow")
        widget.config(tooltipalpha=0.5)
        self.assertEqual(widget["tooltipalpha"], 0.5)
        self.assertEqual(widget.tooltip_wrapper["alpha"], 0.5)
        widget.config(tooltipdelay=1000)
        self.assertEqual(widget["tooltipdelay"], 1000)
        self.assertEqual(widget.tooltip_wrapper["delay"], 1000)
        widget.config(tooltipforeground='black')
        self.assertEqual(widget["tooltipforeground"], 'black')
        widget.config(tooltipbackground='cyan')
        self.assertEqual(widget["tooltipbackground"], 'cyan')

    def test_calevents(self):
        widget = Calendar(self.window)
        widget.pack()
        self.window.update()
        evdate = date.today() + widget.timedelta(days=2)
        widget.calevent_create(evdate, 'Hello World', 'message')
        widget.calevent_create(evdate, 'Reminder 2', 'reminder')
        widget.calevent_create(evdate + widget.timedelta(days=-2), 'Reminder 1', 'reminder')
        widget.calevent_create(evdate + widget.timedelta(days=3), 'Message', 'message')

        widget.tag_config('reminder', background='red', foreground='yellow')
        widget.tag_config('test', background='blue', foreground='white')

        # get_calevents
        self.assertEqual(widget.get_calevents(), tuple(i for i in range(4)))
        self.assertEqual(widget.get_calevents(date=evdate), (0, 1))
        self.assertEqual(widget.get_calevents(date=evdate + widget.timedelta(days=-5)), ())
        self.assertEqual(widget.get_calevents(tag='message'), (0, 3))
        self.assertEqual(widget.get_calevents(tag='message', date=evdate), (0,))
        self.assertEqual(widget.get_calevents(tag='message',
                                              date=evdate + widget.timedelta(days=-2)), ())
        with self.assertRaises(TypeError):
            widget.get_calevents(date='12/12/2012')

        # cget / configure
        self.assertEqual(widget.calevent_cget(1, 'tags'), ['reminder'])
        self.assertEqual(widget.calevent_cget(0, 'text'), 'Hello World')
        self.assertEqual(widget.calevent_cget(2, 'date'), evdate + widget.timedelta(days=-2))
        widget.calevent_configure(1, tags=['reminder', 'new'])
        self.assertEqual(widget.calevent_cget(1, 'tags'), ['reminder', 'new'])
        widget.calevent_configure(1, tags='reminder')
        self.assertEqual(widget.calevent_cget(1, 'tags'), ['reminder'])
        widget.calevent_configure(0, text='Hi')
        self.assertEqual(widget.calevent_cget(0, 'text'), 'Hi')
        self.assertNotIn(evdate + widget.timedelta(days=5), widget._calevent_dates)
        widget.calevent_configure(3, date=evdate + widget.timedelta(days=5, minutes=2))
        self.assertEqual(widget.calevent_cget(3, 'date'), evdate + widget.timedelta(days=5))
        self.assertIn(evdate + widget.timedelta(days=5), widget._calevent_dates)
        widget.calevent_configure(2, date=evdate)
        self.assertEqual(widget.calevent_cget(2, 'date'), evdate)
        with self.assertRaises(ValueError):
            widget.calevent_cget(1, 'arg')
        with self.assertRaises(ValueError):
            widget.calevent_cget(5, 'date')
        with self.assertRaises(ValueError):
            widget.calevent_configure(5, text='a')
        with self.assertRaises(KeyError):
            widget.calevent_configure(1, test='a')
        with self.assertRaises(TypeError):
            widget.calevent_configure(1, date='a')

        # lower / raise
        self.assertEqual(widget._calevent_dates[evdate], [0, 1, 2])
        widget.calevent_lower(0)
        self.assertEqual(widget._calevent_dates[evdate], [1, 2, 0])
        widget.calevent_lower(1, 2)
        self.assertEqual(widget._calevent_dates[evdate], [2, 1, 0])
        widget.calevent_raise(0)
        self.assertEqual(widget._calevent_dates[evdate], [0, 2, 1])
        widget.calevent_raise(1, 2)
        self.assertEqual(widget._calevent_dates[evdate], [0, 1, 2])
        with self.assertRaises(ValueError):
            widget.calevent_raise(4)
        with self.assertRaises(ValueError):
            widget.calevent_raise(1, 4)
        with self.assertRaises(ValueError):
            widget.calevent_lower(4)
        with self.assertRaises(ValueError):
            widget.calevent_lower(1, 4)

        # tags
        self.assertEqual(set(widget.tag_names()), set(('new', 'message', 'reminder', 'test')))
        self.assertEqual(widget.tag_cget('test', 'foreground'), 'white')
        self.assertEqual(widget.tag_cget('test', 'background'), 'blue')
        with self.assertRaises(ValueError):
            widget.tag_cget('hello', 'background')
        with self.assertRaises(ValueError):
            widget.tag_cget('test', 'text')
        with self.assertRaises(ValueError):
            widget.tag_delete('birthday')
        widget.tag_delete('message')
        self.assertEqual(set(widget.tag_names()), set(('new', 'reminder', 'test')))
        self.assertEqual(widget.calevent_cget(0, 'tags'), [])

        # remove
        widget.calevent_remove(0)
        self.assertEqual(widget.get_calevents(), tuple(i for i in range(1, 4)))
        widget.calevent_remove(date=evdate + widget.timedelta(days=3))
        self.assertEqual(widget.get_calevents(), tuple(i for i in range(1, 4)))
        widget.calevent_remove(date=evdate + widget.timedelta(days=5))
        self.assertEqual(widget.get_calevents(), tuple(i for i in range(1, 3)))
        widget.calevent_remove(tag='reminder')
        self.assertEqual(widget.get_calevents(), ())
        widget.calevent_create(evdate, 'Hello World', 'message')
        widget.calevent_create(evdate, 'Reminder 2', 'reminder')
        widget.calevent_create(evdate + widget.timedelta(days=-2), 'Reminder 1', 'reminder')
        widget.calevent_create(evdate + widget.timedelta(days=3), 'Message', 'message')
        self.window.update()
        self.assertEqual(widget.get_calevents(), tuple(i for i in range(4)))
        widget.calevent_remove(tag='reminder', date=evdate)
        self.assertEqual(widget.get_calevents(), (0, 2, 3))
        widget.calevent_remove(3, tag='reminder', date=evdate)
        self.assertEqual(widget.get_calevents(), (0, 2))
        widget.calevent_remove('all')
        self.assertEqual(widget.get_calevents(), ())

    def test_calendar_virtual_events(self):
        widget = Calendar(self.window)
        widget.pack()
        self.window.update()

        self.event_triggered = False

        def binding(event):
            self.event_triggered = True

        widget.bind('<<CalendarSelected>>', binding)
        widget._on_click(TestEvent(widget=widget._calendar[2][1]))
        self.window.update()
        self.assertTrue(self.event_triggered)

        widget.bind('<<CalendarMonthChanged>>', binding)
        self.event_triggered = False
        widget._l_month.invoke()
        self.window.update()
        self.assertTrue(self.event_triggered)
        self.event_triggered = False
        widget._r_month.invoke()
        self.window.update()
        self.assertTrue(self.event_triggered)
        self.event_triggered = False
        widget._l_year.invoke()
        self.window.update()
        self.assertTrue(self.event_triggered)
        self.event_triggered = False
        widget._r_year.invoke()
        self.window.update()
        self.assertTrue(self.event_triggered)
