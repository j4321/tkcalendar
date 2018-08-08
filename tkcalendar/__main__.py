from tkcalendar import Calendar, DateEntry, EventCalendar
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
import datetime

#def example1():
#    def print_sel():
#        print(cal.selection_get())
#
#    top = tk.Toplevel(root)
#    top.grab_set()
#
#    cal = Calendar(top, font="Arial 14", selectmode='day',
#                   cursor="hand1", year=2018, month=2, day=5)
#
#    cal.pack(fill="both", expand=True)
#    ttk.Button(top, text="ok", command=print_sel).pack()
#
#
#def example2():
#    top = tk.Toplevel(root)
#    top.grab_set()
#
#    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
#
#    cal = DateEntry(top, width=12, background='darkblue',
#                    foreground='white', borderwidth=2, year=2010)
#    cal.pack(padx=10, pady=10)
#
#
#root = tk.Tk()
#ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
#ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)
#
#root.mainloop()
root = tk.Tk()

cal = EventCalendar(root)
cal.pack()
date = datetime.date.today() + datetime.timedelta(days=2)
print(date)
cal.add_event(date, 'Test', 'red', 'white')
cal.add_event(date, 'Test 2', 'blue', 'yellow')

root.mainloop()