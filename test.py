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

Test
"""


import unittest
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import locale
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

import sys

locale.setlocale(locale.LC_ALL, '')


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        sys.stdout = open('/tmp/tmp.log', 'a')
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
        self.assertEqual(widget.selection_get(), datetime(2018, 12, 31))
        with self.assertRaises(ValueError):
            widget.selection_set("ab")
        widget.selection_set(None)
        self.assertIsNone(widget.selection_get())
        widget.selection_set(datetime(2015, 12, 31))
        self.assertEqual(widget.selection_get(), datetime(2015, 12, 31))

        widget.config(selectmode='none')
        self.assertIsNone(widget.selection_get())

        l = ttk.Label(widget, text="12")
        widget._on_click(TestEvent(widget=l))

    def test_calendar_get_set(self):
        widget = Calendar(self.window, foreground="red")
        widget.pack()
        self.window.update()

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
        with self.assertRaises(AttributeError):
            widget.config(locale="en_US.UTF-8")
        with self.assertRaises(AttributeError):
            widget.config(test="test")
        dic = {op: "yellow" for op in options[5:]}
        widget.configure(**dic)
        self.window.update()
        for op in options[5:]:
            self.assertEqual(widget.cget(op), "yellow")


class TestDateEntry(BaseWidgetTest):
    def test_dateentry_init(self):
        widget = DateEntry(self.window, width=12, background='darkblue',
                           foreground='white', borderwidth=2)
        widget.pack()
        self.window.update()

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

        widget.config(style="my.TEntry")
        self.window.update()
        self.assertEqual(widget["style"], "my.TEntry")

    def test_dateentry_functions(self):
        widget = DateEntry(self.window, width=12, background='darkblue',
                           foreground='white', borderwidth=2)
        widget.pack()
        self.window.update()

        widget.set_date(datetime(2018, 12, 31).strftime('%x'))
        self.assertEqual(widget.get_date(), datetime(2018, 12, 31))
        with self.assertRaises(ValueError):
            widget.set_date("ab")
        widget.set_date(datetime(2015, 12, 31))
        self.assertEqual(widget.get_date(), datetime(2015, 12, 31))
        self.assertEqual(widget.get(), datetime(2015, 12, 31).strftime("%x"))

        widget.delete(0, "end")
        widget.insert(0, "abc")
        self.window.focus_force()
        self.assertEqual(widget.get_date(), datetime(2015, 12, 31))

        widget._on_motion(TestEvent(x=10, y=20))
        widget._on_b1_press(TestEvent(x=10, y=20))
        widget._on_b1_press(TestEvent(x=widget.winfo_width() - 2, y=2))
        widget._on_b1_release(TestEvent(x=10, y=20))
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
