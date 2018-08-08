from tests import BaseWidgetTest, TestEvent
from tkcalendar import DateEntry
from datetime import datetime, date
from pynput.mouse import Controller, Button


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
