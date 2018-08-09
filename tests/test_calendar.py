from tests import BaseWidgetTest, TestEvent, tk, ttk, format_date
from tkcalendar import Calendar
from datetime import date


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
        self.assertEqual(format_date(date(2015, 1, 3), 'short'), var.get())
        self.assertEqual(format_date(date(2015, 1, 3), 'short'), widget.get_date())
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
