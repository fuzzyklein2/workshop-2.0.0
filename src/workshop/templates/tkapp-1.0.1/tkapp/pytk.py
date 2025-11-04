#!/usr/bin/env python
# --*-- coding: utf-8 --*--
""" main.py
    v0.0.0c

    This program runs an empty `tkinter` application.
"""

import tkinter as tk

from application import Application
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.master.title("Worksheet")
    app.mainloop()
