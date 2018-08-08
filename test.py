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


import unittest
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
import locale
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from pynput.mouse import Controller, Button

locale.setlocale(locale.LC_ALL, '')


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.window = tk.Toplevel()
        self.window.update()

    def tearDown(self):
        self.window.update()
        self.window.destroy()


class TestEvent:
    """Fake event for testing."""
    def __init__(self, **kwargs):
        self._prop = kwargs

    def __getattr__(self, attr):
        if attr not in self._prop:
            raise AttributeError("TestEvent has no attribute %s." % attr)
        else:
            return self._prop[attr]


class TestCalendar(BaseWidgetTest):
    def test_calendar_init(self):
        widget = Calendar(self.window)
        widget.pack()
        self.window.update()
        widget.destroy()
        widget = Calendar(self.window, font="Arial 14", selectmode='day',
                          cursor="hand1", year=2018, month=2, day=5)
        widget.pack()
        self.window.update()
        self.assertEqual(widget.selection_get(), date(2018, 2, 5))
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

        widget = Calendar(self.window, selectmode='none', locale=None,
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
        widget.selection_set(datetime(2018, 12, 31).strftime('%x'))
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
        var = tk.StringVar(self.window,)
        widget = Calendar(self.window, selectmode='day', locale=None,
                          year=2015, month=1, day=3, textvariable=var)
        widget.pack()
        self.window.update()
        self.assertEqual(datetime(2015, 1, 3).strftime('%x'), var.get())
        self.assertEqual(datetime(2015, 1, 3).strftime('%x'), widget.get_date())
        widget.selection_set(datetime(2018, 11, 21))
        self.window.update()
        self.assertEqual(datetime(2018, 11, 21).strftime('%x'), var.get())
        self.assertEqual(datetime(2018, 11, 21).strftime('%x'), widget.get_date())
        widget.selection_set(None)
        self.window.update()
        self.assertEqual('', widget.get_date())
        self.assertEqual('', var.get())
        var.set(datetime(2014, 3, 2).strftime('%x'))
        self.window.update()
        self.assertEqual(datetime(2014, 3, 2), widget.selection_get())
        self.assertEqual(datetime(2014, 3, 2).strftime('%x'), var.get())
        self.assertEqual(datetime(2014, 3, 2).strftime('%x'), widget.get_date())
        try:
            var.set('a')
        except tk.TclError:
            # some versions of python raise an error because of the exception
            # raised inside the trace
            pass
        self.window.update()
        self.assertEqual(datetime(2014, 3, 2), widget.selection_get())
        self.assertEqual(datetime(2014, 3, 2).strftime('%x'), var.get())
        self.assertEqual(datetime(2014, 3, 2).strftime('%x'), widget.get_date())
        var.set('')
        self.window.update()
        self.assertIsNone(widget.selection_get())
        self.assertEqual('', var.get())
        self.assertEqual('', widget.get_date())

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
                   'disableddayforeground']
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
        dic = {op: "yellow" for op in options[7:]}
        widget.configure(**dic)
        self.window.update()
        for op in options[7:]:
            self.assertEqual(widget.cget(op), "yellow")


class TestDateEntry(BaseWidgetTest):
    def test_dateentry_init(self):
        widget = DateEntry(self.window, width=12, background='darkblue',
                           foreground='white', borderwidth=2)
        widget.pack()
        self.window.update()
        widget.destroy()
        widget = DateEntry(self.window, year=2012)
        widget.pack()
        self.window.update()
        widget.destroy()

    def test_dateentry_drop_down(self):
        """Check whether drop down opens on click."""
        widget = DateEntry(self.window)
        widget.pack()
        self.window.update()
        x, y = widget.winfo_rootx(), widget.winfo_rooty()
        w = widget.winfo_width()
        mouse_controller = Controller()
        mouse_controller.position = (x + w - 2, y + 2)
        self.window.update()
        mouse_controller.press(Button.left)
        self.window.update()
        mouse_controller.release(Button.left)
        self.window.update()
        self.assertTrue(widget._top_cal.winfo_ismapped())

    def test_dateentry_get_set(self):
        widget = DateEntry(self.window, width=12, background='darkblue',
                           foreground='white', borderwidth=2, font='Arial 9')
        widget.pack()
        self.window.update()

        keys = ['exportselection',
                'invalidcommand',
                'justify',
                'show',
                'cursor',
                'style',
                'state',
                'takefocus',
                'textvariable',
                'validate',
                'validatecommand',
                'width',
                'xscrollcommand']
        keys.extend(widget._calendar.keys())
        self.assertEqual(sorted(list(set(keys))), sorted(widget.keys()))

        self.assertEqual(widget["background"], 'darkblue')
        self.assertEqual(widget.cget("width"), 12)

        widget["borderwidth"] = 5
        self.window.update()
        self.assertEqual(widget["borderwidth"], 5)

        widget.config(font="Arial 20 bold")
        self.window.update()
        self.assertEqual(widget["font"], "Arial 20 bold")

        widget.config(style="my.TEntry")
        self.window.update()
        self.assertEqual(widget["style"], "my.TEntry")

    def test_dateentry_functions(self):
        widget = DateEntry(self.window, width=12, background='darkblue',
                           foreground='white', borderwidth=2)
        widget.pack()
        self.window.update()

        widget.set_date(datetime(2018, 12, 31).strftime('%x'))
        self.assertEqual(widget.get_date(), date(2018, 12, 31))
        with self.assertRaises(ValueError):
            widget.set_date("ab")
        widget.set_date(datetime(2015, 12, 31))
        self.assertEqual(widget.get_date(), date(2015, 12, 31))
        self.assertEqual(widget.get(), datetime(2015, 12, 31).strftime("%x"))

        widget.delete(0, "end")
        widget.insert(0, "abc")
        self.window.focus_force()
        self.assertEqual(widget.get_date(), date(2015, 12, 31))

        widget._on_motion(TestEvent(x=10, y=20))
        widget._on_b1_press(TestEvent(x=10, y=20))
        widget._on_b1_press(TestEvent(x=widget.winfo_width() - 2, y=2))
        widget._on_focus_out_cal(TestEvent(x=10, y=20))

        widget.state(("disabled",))
        self.window.update()
        self.assertIn("disabled", widget.state())

        widget.drop_down()
        self.window.update()
        widget._select()
        self.window.update()
        widget.drop_down()
        self.window.update()
        widget.drop_down()
        self.window.update()

        widget.configure(state='readonly')
        self.window.update()
        widget._select()
        self.assertIn('readonly', widget.state())
