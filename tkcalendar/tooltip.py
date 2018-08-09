#! /usr/bin/python3
# -*- coding:Utf-8 -*-
"""
MyNotes - System tray unread mail checker
Copyright 2016-2018 Juliette Monsel <j_4321@protonmail.com>

MyNotes is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MyNotes is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Tooltip and TooltipWrapper
"""

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from sys import platform


class Tooltip(tk.Toplevel):
    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent)
        if 'title' in kwargs:
            self.title(kwargs['title'])
        self.transient(parent)
        if platform is 'linux':
            self.attributes('-type', 'tooltip')
        self.attributes('-alpha', kwargs.get('alpha', 0.8))
        self.overrideredirect(True)
        self.configure(padx=kwargs.get('padx', 4))
        self.configure(pady=kwargs.get('pady', 4))

        self.style = ttk.Style(self)
        bg = kwargs.get('background', 'black')
        self.configure(background=bg)
        self.style.configure('tooltip.TLabel',
                             foreground=kwargs.get('foreground', 'gray90'),
                             background=bg,
                             font='TkDefaultFont 9 bold')

        self.im = kwargs.get('image', None)
        self.label = ttk.Label(self, text=kwargs.get('text', ''), image=self.im,
                               style='tooltip.TLabel',
                               compound=kwargs.get('compound', 'left'))
        self.label.pack()

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def configure(self, **kwargs):
        if 'text' in kwargs:
            self.label.configure(text=kwargs.pop('text'))
        if 'image' in kwargs:
            self.label.configure(image=kwargs.pop('image'))
        if 'background' in kwargs:
            self.style.configure('tooltip.TLabel', background=kwargs['background'])
        if 'foreground' in kwargs:
            fg = kwargs.pop('foreground')
            self.style.configure('tooltip.TLabel', foreground=fg)
        if 'alpha' in kwargs:
            self.attributes('-alpha', kwargs.pop('alpha'))
        tk.Toplevel.configure(self, **kwargs)


class TooltipWrapper:
    def __init__(self, master, **kwargs):
        self.widgets = {}
        self.bind_enter_ids = {}
        self.bind_leave_ids = {}
        if 'delay' in kwargs:
            self.delay = kwargs.pop('delay')
        else:
            self.delay = 2000
        self.kwargs = kwargs.copy()
        self._timer_id = None
        self.tooltip = Tooltip(master, **self.kwargs)
        self.tooltip.withdraw()

        self.current_widget = None

        self.tooltip.bind('<Leave>', self._on_leave_tooltip)

    def add_tooltip(self, widget, text):
        self.widgets[str(widget)] = text
        self.bind_enter_ids[str(widget)] = widget.bind('<Enter>', self._on_enter)
        self.bind_leave_ids[str(widget)] = widget.bind('<Leave>', self._on_leave)

    def set_tooltip_text(self, widget, text):
        self.widgets[str(widget)] = text

    def remove_all(self):
        for name in self.widgets:
            widget = self.tooltip.nametowidget(name)
            widget.unbind('<Enter>', self.bind_enter_ids[name])
            widget.unbind('<Leave>', self.bind_leave_ids[name])
        self.widgets.clear()
        self.bind_enter_ids.clear()
        self.bind_leave_ids.clear()

    def remove_tooltip(self, widget):
        try:
            name = str(widget)
            del self.widgets[name]
            widget.unbind('<Enter>', self.bind_enter_ids[name])
            widget.unbind('<Leave>', self.bind_leave_ids[name])
            del self.bind_enter_ids[name]
            del self.bind_leave_ids[name]
        except KeyError:
            pass

    def _on_enter(self, event):
        if not self.tooltip.winfo_ismapped():
            self._timer_id = event.widget.after(self.delay, self.display_tooltip)
            self.current_widget = event.widget

    def _on_leave(self, event):
        if self.tooltip.winfo_ismapped():
            x, y = event.widget.winfo_pointerxy()
            if not event.widget.winfo_containing(x, y) in [event.widget, self.tooltip]:
                self.tooltip.withdraw()
        else:
            try:
                event.widget.after_cancel(self._timer_id)
            except ValueError:
                pass
        self.current_widget = None

    def _on_leave_tooltip(self, event):
        x, y = event.widget.winfo_pointerxy()
        if not event.widget.winfo_containing(x, y) in [self.current_widget, self.tooltip]:
            self.tooltip.withdraw()

    def display_tooltip(self):
        if "disabled" not in self.current_widget.state():
            self.tooltip['text'] = self.widgets[str(self.current_widget)]
            self.tooltip.deiconify()
            x = self.current_widget.winfo_pointerx() + 14
            y = self.current_widget.winfo_rooty() + self.current_widget.winfo_height() + 2
            self.tooltip.geometry('+%i+%i' % (x, y))
