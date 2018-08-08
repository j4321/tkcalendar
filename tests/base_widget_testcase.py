import unittest
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


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
