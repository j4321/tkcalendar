from tkcalendar.tooltip import Tooltip, TooltipWrapper
from tests import BaseWidgetTest, TestEvent
from pynput.mouse import Controller
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
        tw._on_leave_tooltip(TestEvent(widget=tw.tooltip, x=10, y=10))
        x, y = b1.winfo_rootx(), b1.winfo_rooty()
        mouse_controller = Controller()
        mouse_controller.position = (x + 10, y + 10)
        self.window.update()
        self.assertEqual(tw.current_widget, b1)
        tw.display_tooltip()
        mouse_controller.position = (x - 10, y - 10)
        self.window.update()
        print(self.window.winfo_containing(*self.window.winfo_pointerxy()))
        raise ValueError(str(self.window.winfo_containing(*self.window.winfo_pointerxy())))

#        self.assertIsNone(tw.current_widget)
#        tw.display_tooltip()
#        self.window.update()
#        mouse_controller.position = (x + 10, y + 10)
#        self.window.update()
#        mouse_controller.position = (x - 10, y - 10)
#        self.window.update()
#        self.assertIsNone(tw.current_widget)
#        tw.remove_tooltip(self.window)
#        tw.remove_tooltip(b1)
#        mouse_controller.position = (x + 10, y + 10)
#        self.window.update()
#        self.assertIsNone(tw.current_widget)
#        tw.remove_all()
#        self.assertFalse(tw.widgets)
