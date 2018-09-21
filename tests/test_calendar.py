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
from datetime import date


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
                   'firstweekday',
                   'showweeknumbers',
                   'selectbackground',
                   'selectforeground',
                   'disabledselectbackground',
                   'disabledselectforeground',
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
        widget.config(showweeknumbers=False)
        self.window.update()
        self.assertFalse(widget["showweeknumbers"])
        self.assertFalse(widget._week_nbs[0].winfo_ismapped())
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
        dic = {op: "yellow" for op in options[8:-4]}
        widget.configure(**dic)
        self.window.update()
        for op in options[8:-4]:
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

