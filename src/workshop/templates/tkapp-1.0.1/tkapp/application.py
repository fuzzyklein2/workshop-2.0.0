#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
"""
    Define the Application class.
"""

# IMPORTS
import os
# from pathlib import Path
import pdb
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

# MODULES -- These have to be in the same directory as this file or in a directory contained in sys.path.
# from setup import HOMEDIR
# from worktext import WorkText
# from help import showhelp

from constants import HOMEDIR
from worktext import WorkText

def showhelp():
    pass

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master # Added. A better solution should be found. I'm not sure if None is a good default argument.
        self.pack(side='top', fill='both', expand='true')
        self.createWidgets()

    def alert (self, s) :
        showinfo ("About Workshop", s)

    def about (self) :
        self.alert ("This is Workshop v1.0.0a")

# TODO: Move the menu data to a spreadsheet or a config file(s) that can be edited by the user. Make sure to handle errors in such files without exiting if at all possible.
    def createWidgets(self):
        """ Seems to be where all the action takes place. """
        menubar = Menu(self)
        menubar.ICONSDIR = os.path.join (HOMEDIR, "icons", "16x16")
        menubar.empty_img = PhotoImage (file = os.path.join(menubar.ICONSDIR, "empty.png"))
        file_menu = Menu(self)
        file_menu.new_img = PhotoImage (file = os.path.join(menubar.ICONSDIR, "new.png"))
        file_menu.add_command (label="New", command=self.new_file, accelerator="Ctrl+N", compound="left", image=file_menu.new_img, underline=0)
        file_menu.open_img = PhotoImage(file = os.path.join(menubar.ICONSDIR, "open.png"))
        file_menu.add_command (label="Open", command=self.open_file, accelerator="Ctrl+O", underline=0, compound="left", image=file_menu.open_img)
        file_menu.save_img = PhotoImage(file = os.path.join(menubar.ICONSDIR, "save.png"))
        file_menu.add_command (label="Save", command=self.save_file, accelerator="Ctrl+S", underline=0, compound="left", image=file_menu.save_img)
        file_menu.add_command (label="Save As...", command=self.save_as, accelerator="Ctrl+Shift+S", underline=5, compound="left", image=menubar.empty_img)
        file_menu.add_command (label="Close", command=self.close_file, accelerator="Ctrl+W", underline=0, compound="left", image=menubar.empty_img)
        file_menu.add_separator()
        file_menu.add_command (label="Page Setup...", command=self.page_setup, accelerator="Ctrl+Shift+P", underline = 2, compound="left", image=menubar.empty_img)
        file_menu.print_img = PhotoImage ( file=os.path.join(menubar.ICONSDIR,"print.png"))
        file_menu.add_command (label="Print...", command=self.print_file, accelerator="Ctrl+P", underline=0, compound="left", image=file_menu.print_img)
        file_menu.add_separator()
        file_menu.add_command (label="Quit", command=self.master.destroy, accelerator="Ctrl+Q", underline=0, compound="left", image=menubar.empty_img)
        menubar.add_cascade(label="File", menu=file_menu, underline=0)

# Edit Menu
        edit_menu = Menu(self)
        edit_menu.undo_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "undo.png"))
        edit_menu.add_command (label="Undo", command=self.edit_undo, accelerator="Ctrl+Z", underline=0, compound="left", image=edit_menu.undo_img)
        edit_menu.redo_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "redo.png"))
        edit_menu.add_command (label="Redo", command=self.edit_redo, accelerator="Ctrl+Y", underline=2, compound="left", image=edit_menu.redo_img)
        edit_menu.add_separator()
        edit_menu.cut_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "cut.png"))
        edit_menu.add_command (label="Cut", command=self.edit_cut, accelerator="Ctrl+X", underline=2, compound="left", image=edit_menu.cut_img)
        edit_menu.copy_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "copy.png"))
        edit_menu.add_command (label="Copy", command=self.edit_copy, accelerator="Ctrl+C", underline=0, compound="left", image=edit_menu.copy_img)
        edit_menu.paste_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "paste.png"))
        edit_menu.add_command (label="Paste", command=self.edit_paste, accelerator="Ctrl+V", underline=0, compound="left", image=edit_menu.paste_img)
#        edit_menu.add_separator()
        edit_menu.add_command (label="Clear", command=self.edit_clear, underline=1, compound="left", image=menubar.empty_img)
        edit_menu.add_command (label="Select All", command=self.select_all, accelerator="Ctrl+A", underline=7, compound="left", image=menubar.empty_img)
        edit_menu.add_separator()
        edit_menu.find_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "find.png"))
        edit_menu.add_command (label="Find...", command=self.edit_find, accelerator="Ctrl+F", underline=0, compound="left", image=edit_menu.find_img)
        edit_menu.add_command (label="Replace...", command=self.edit_replace, accelerator="Ctrl+R", underline=0, compound="left", image=edit_menu.find_img)
        menubar.add_cascade(label="Edit", menu=edit_menu, underline=0)

# Help Menu
        help_menu = Menu(self)
        help_menu.about_img = PhotoImage (file=os.path.join(menubar.ICONSDIR, "about.png"))
        help_menu.add_command (label="Help...", command=self.help, accelerator="Ctrl+?", compound="left", image=help_menu.about_img, underline=0)
        help_menu.add_command (label="About...", command=self.about, underline=0, compound="left", image=menubar.empty_img)
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        self.master.config(menu=menubar)

# Toolbar
        self.toolbar = Frame(self, height=25)
        self.toolbar.ICONSDIR = os.path.join (HOMEDIR, "icons", "22x22")
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "new.png"))
        button = Button(self.toolbar, image=image, command=self.new_file)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "open.png"))
        button = Button(self.toolbar, image=image, command=self.open_file)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "save.png"))
        button = Button(self.toolbar, image=image, command=self.save_file)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "print.png"))
        button = Button(self.toolbar, image=image, command=self.print_file)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "cut.png"))
        button = Button(self.toolbar, image=image, command=self.edit_cut)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "copy.png"))
        button = Button(self.toolbar, image=image, command=self.edit_copy)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "paste.png"))
        button = Button(self.toolbar, image=image, command=self.edit_paste)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "undo.png"))
        button = Button(self.toolbar, image=image, command=self.edit_undo)
        button.image = image
        button.pack(side=LEFT)
        image = PhotoImage(file=os.path.join(self.toolbar.ICONSDIR, "redo.png"))
        button = Button(self.toolbar, image=image, command=self.edit_redo)
        button.image = image
        button.pack(side=LEFT)


        self.toolbar.pack( expand=NO, fill=X)

        self.work_text = WorkText(self)
        self.work_text.configure (setgrid='true')

        self.master.bind('<Control-N>', self.new_file)
        self.master.bind('<Control-n>', self.new_file)
        self.master.bind('<Control-O>', self.open_file)
        self.master.bind('<Control-o>', self.open_file)
        self.master.bind('<Control-s>', self.save_file)
        self.master.bind('<Control-S>', self.save_as)
        self.master.bind('<Control-P>', self.page_setup)
        self.master.bind('<Control-p>', self.print_file)
        self.master.bind('<Control-Q>', self.quit_app)
        self.master.bind('<Control-q>', self.quit_app)
        self.master.bind('<Control-A>', self.select_all)
        self.master.bind('<Control-a>', self.select_all)
        self.master.bind('<Control-F>', self.edit_find)
        self.master.bind('<Control-f>', self.edit_find)
        self.master.bind('<Control-R>', self.edit_replace)
        self.master.bind('<Control-r>', self.edit_replace)
        self.master.bind('<KeyPress-F1>', self.help)

        self.work_text.pack (side='bottom', expand='true', fill='both')
        self.pack (expand='true')

#        self.work_text.insert(END,"Hello, Tkinter!")

    def new_file(self, event=None):
        """ Create a new file. Ideally, in a new tab or window. """
        self.master.title("Untitled")
        self.work_text.filename = None
        self.work_text.delete(1.0, END)

    def open_file(self, event=None):
        """ Open a file and display its contents. """
        self.work_text.filename = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),("Text Documents","*.txt")])
        if self.work_text.filename == "":
            self.work_text.filename = None
        else:
            self.master.title(os.path.basename(self.work_text.filename) + " - Workshop")
        self.work_text.delete(1.0, END)
        with (open(self.work_text.filename,"r")) as f :
            self.work_text.insert(1.0,f.read())

    def save_file(self, event=None):
        """ Save the current buffer to the current file. """
        try:
            with (open(self.work_text.filename,'w')) as f :
                f.write (self.work_text.get(1.0,'end'))
        except TypeError:
            self.save_as()

    def save_as(self, event=None):
        """ Save the current buffer to a new file. """
        try:
            response = asksaveasfilename (initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Doecuments","*.txt")])
            if (response) :
                self.work_text.filename = response
                self.save_file()
                self.master.title(os.path.basename(self.work_text.filename))
        except:
            pass

    def close_file(self, event=None): pass
    def page_setup(self, event=None): pass
    def print_file(self, event=None): pass

    def quit_app(self, event=None) :
        self.master.destroy()

    def edit_undo(self, event=None):
        self.work_text.edit_undo()

    def edit_redo(self, event=None):
        self.work_text.edit_redo()

    def edit_cut(self, event=None):
        self.work_text.event_generate("<<Cut>>")

    def edit_copy(self, event=None):
        self.work_text.event_generate("<<Copy>>")

    def edit_paste(self, event=None):
        self.work_text.event_generate("<<Paste>>")

    def edit_clear(self, event=None): pass

    # Since the re package exists this could probably be done more easily with regular expressions, even though it amounts to about the same thing either way.
    def edit_find(self, event=None):
        t2 = Toplevel(self.master)
        t2.title('Find')
        t2.geometry('{0}x65+200+250'.format(246 if os.name=='nt' else 320))
        t2.transient(self.master) # TODO: See if all dialogs can be loaded in memory at startup and displayed or hidden as needed. This speeds them up.
        Label(t2, text="Find All:").grid(row=0, column=0, sticky='w')
        v=StringVar()
        e=Entry(t2, width=25, textvariable=v)
        e.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        e.focus_set()
        c=IntVar()

        def search_for (needle, cssnstv, t2, e) :
            self.work_text.tag_remove('match', '1.0', END)
            count=0
            if needle:
                pos='1.0'
                while True:
                    pos = self.work_text.search(needle, pos, nocase=cssnstv, stopindex=END)
                    if not pos: break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    self.work_text.tag_add('match', pos, lastpos)
                    count+=1
                    pos=lastpos
                self.work_text.tag_config('match', foreground='red', background='yellow')
                e.focus_set()
                t2.title('%d matches found' %count)

        def close_search():
            self.work_text.tag_remove('match', '1.0', END)
            t2.destroy()

        # pdb.set_trace()
        def search():
            search_for(v.get(), c.get(), t2, e)

        Button(t2, text="Find", underline=0, command=search).grid(row=0, column=2, sticky='e', padx=2, pady=2)
        Checkbutton(t2, text="Ignore Case", variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
        t2.protocol ('WM_DELETE_WINDOW', close_search)

    def edit_replace(self, event=None): pass

    def select_all(self, event=None):
        self.work_text.tag_add('sel', '1.0', 'end')

    def help(self, event=None):
        showhelp()

if __name__ == "__main__":
    pass
