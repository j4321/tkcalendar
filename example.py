#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:47:14 2018

@author: juliette
"""

from tkcalendar import Calendar
import tkinter as tk
import datetime


root = tk.Tk()

cal = Calendar(root)
cal2 = Calendar(root)
cal.pack()
cal2.pack()
date = datetime.date.today() + datetime.timedelta(days=2)
date2 = datetime.date.today() + datetime.timedelta(days=-2)
print(date)
cal.calevent_create(date, 'Test', 'holiday')
cal.calevent_create(date, 'Test 2', 'birthday')
cal2.calevent_create(date, 'Test', 'holiday')
cal2.calevent_create(date, 'Test 2', 'birthday')
cal.calevent_create(date, 'Test 3', ['a', 'b'])
cal.calevent_create(date2, 'Test 4', 'birthday')
cal.tag_config('holiday', foreground='white', background='green')
cal.tag_config('birthday', foreground='yellow', background='red')
cal.tag_config('a', foreground='black', background='light green')
cal.tag_config('b', foreground='black', background='light blue')
