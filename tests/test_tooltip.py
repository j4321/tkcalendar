from tkcalendar.tooltip import Tooltip, TooltipWrapper
from tests import BaseWidgetTest
try:
    from tkinter import ttk
    import tkinter as tk
except ImportError:
    import Tkinter as tk
    import ttk
from pynput.mouse import Controller


class TestTooltip(BaseWidgetTest):
    def test_tooltip(self):
        t = Tooltip(self.window, text='Hi!', style='my.TLabel', alpha=0.5)
        self.window.update()
        self.assertEqual(t.keys(), ['alpha'] + ttk.Label().keys())
        self.assertEqual(str(t.cget('compound')), 'left')
        self.assertEqual(t.cget('text'), 'Hi!')
        self.assertEqual(t.cget('alpha'), 0.5)
        self.assertEqual(t.cget('style'), 'my.TLabel')

        t.configure(text='Hello', style='test.TLabel',
                    image=None, alpha=0.75, compound='right')
        self.assertEqual(str(t.cget('compound')), 'right')
        self.assertEqual(t.cget('text'), 'Hello')
        self.assertEqual(t.cget('alpha'), 0.75)
        self.assertEqual(t.cget('style'), 'test.TLabel')
        self.assertEqual(t.cget('image'), '')


class TestTooltipWrapper(BaseWidgetTest):
    def test_tooltipwrapper_init(self):
        TooltipWrapper(self.window, delay=3000)

        with self.assertRaises(ValueError):
            TooltipWrapper(self.window, delay='a')

    def test_tooltip_config(self):
        tw = TooltipWrapper(self.window)
        tw.configure(alpha=0.3, style='hello.TLabel', delay=30)
        self.assertEqual(tw['alpha'], 0.3)
        self.assertEqual(tw.tooltip['alpha'], 0.3)
        self.assertEqual(tw.cget('delay'), 30)
        self.assertEqual(tw.cget('style'), 'hello.TLabel')
        self.assertEqual(tw.tooltip.cget('style'), 'hello.TLabel')
        with self.assertRaises(ValueError):
            tw['delay'] = 's'

    def test_tooltipwrapper(self):
        b1 = ttk.Button(self.window, text='Button 1')
        b2 = tk.Button(self.window, text='Button 2')
        b1.pack()
        b2.pack()
        self.window.update()
        tw = TooltipWrapper(self.window, delay=1)
        tw.add_tooltip(b1, "tooltip 1")
        tw.add_tooltip(b2, "tooltip 2")
        self.window.update()

        mouse = Controller()

        def removal_tests():
            tw.remove_tooltip(self.window)
            tw.remove_tooltip(b1)
            self.window.update()
            b1.event_generate('<Enter>', x=0, y=0)
            self.window.update()
            self.assertIsNone(tw.current_widget)
            tw.remove_all()
            self.assertFalse(tw.widgets)

        def test_leave(button):
            x = self.window.winfo_rootx() + self.window.winfo_width() + 5
            y = self.window.winfo_rooty() + self.window.winfo_height() + 5
            mouse.position = x, y
            self.window.update()
            self.assertFalse(tw.tooltip.winfo_ismapped())
            self.assertIsNone(tw.current_widget)

        def test(button):
            mouse.position = button.winfo_rootx() + 1, button.winfo_rooty() + 1
            self.window.update()
            self.assertEqual(tw.current_widget, button)
            self.window.after(5, lambda: self.assertTrue(tw.tooltip.winfo_ismapped()))
            self.window.after(7, test_leave)

        test(b1)
        self.window.after(20, lambda: test(b2))
        self.window.after(40, removal_tests)
