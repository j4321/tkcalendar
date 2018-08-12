from tkcalendar.tooltip import Tooltip, TooltipWrapper
from tests import BaseWidgetTest, TestEvent
try:
    import ttk
except ImportError:
    from tkinter import ttk


class TestTooltip(BaseWidgetTest):
    def test_tooltip(self):
        t = Tooltip(self.window, background='white', foreground='black')
        self.window.update()
        t.configure(text='Hello', background='black', foreground='white',
                    image=None, alpha=0.75)


class TestTooltipWrapper(BaseWidgetTest):
    def test_tooltipwrapper(self):
        b1 = ttk.Button(self.window, text='Button 1')
        b2 = ttk.Button(self.window, text='Button 2')
        b3 = ttk.Button(self.window, text='Button 2')
        b1.pack()
        b2.pack()
        b3.pack()
        self.window.update()
        tw = TooltipWrapper(self.window, background='yellow', foreground='black')
        tw.add_tooltip(b1, "tooltip 1")
        tw.add_tooltip(b2, "tooltip 2")
        tw.add_tooltip(b3, "tooltip 3")
        self.window.update()
        b1.event_generate('<Enter>', x=0, y=0)
        self.window.update()
        self.assertEqual(tw.current_widget, b1)
        tw.display_tooltip()
        b1.event_generate('<Leave>', x=0, y=0)
        self.window.update()
        self.assertIsNone(tw.current_widget)
        tw.display_tooltip()
        self.window.update()
        b1.event_generate('<Leave>', x=0, y=0)
        self.window.update()
        self.assertIsNone(tw.current_widget)
        tw.remove_tooltip(self.window)
        tw.remove_tooltip(b1)
        self.window.update()
        b1.event_generate('<Enter>', x=0, y=0)
        self.window.update()
        self.assertIsNone(tw.current_widget)
        tw.remove_all()
        self.assertFalse(tw.widgets)
