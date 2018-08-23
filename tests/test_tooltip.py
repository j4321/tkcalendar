from tkcalendar.tooltip import Tooltip, TooltipWrapper
from tests import BaseWidgetTest
try:
    from tkinter import ttk
    import tkinter as tk
except ImportError:
    import Tkinter as tk
    import ttk


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
        b3 = ttk.Button(self.window, text='Button 2')
        b1.pack()
        b2.pack()
        b3.pack()
        self.window.update()
        tw = TooltipWrapper(self.window)
        tw.add_tooltip(b1, "tooltip 1")
        tw.add_tooltip(b2, "tooltip 2")
        tw.add_tooltip(b3, "tooltip 3")
        self.window.update()
        b1.event_generate('<Enter>', x=0, y=0)
        self.window.update()
        self.assertEqual(tw.current_widget, b1)
        tw.display_tooltip()
        self.assertTrue(tw.tooltip.winfo_ismapped())
        b1.event_generate('<Leave>', x=0, y=0)
        self.window.update()
        self.assertIsNone(tw.current_widget)
        tw.display_tooltip()
        self.window.update()
        self.assertFalse(tw.tooltip.winfo_ismapped())
        b2.event_generate('<Enter>', x=0, y=0)
        self.window.update()
        self.assertEqual(tw.current_widget, b2)
        tw.display_tooltip()
        self.assertTrue(tw.tooltip.winfo_ismapped())
        tw.tooltip.event_generate('<Leave>', x=0, y=0)
        self.window.update()
        self.assertFalse(tw.tooltip.winfo_ismapped())
        b2.event_generate('<Leave>', x=0, y=0)
        self.window.update()
        tw.remove_tooltip(self.window)
        tw.remove_tooltip(b1)
        self.window.update()
        b1.event_generate('<Enter>', x=0, y=0)
        self.window.update()
        self.assertIsNone(tw.current_widget)
        tw.remove_all()
        self.assertFalse(tw.widgets)
