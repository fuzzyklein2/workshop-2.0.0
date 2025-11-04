#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
    Define the WorkText class.
"""
import tkinter
from tkinter.scrolledtext import ScrolledText

class WorkText (ScrolledText) :
    """ The main text area of a (the) Worksheet window. """
    def __init__(self, master):
        ScrolledText.__init__(self, master, undo=True)
        # self.undo=True

