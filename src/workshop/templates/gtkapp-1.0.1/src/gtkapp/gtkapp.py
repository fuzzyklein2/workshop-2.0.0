#!/usr/bin/env python3

"""
@file gtkapp.py
@version 1.0.1
@brief PyGTK app.

For more information, see:

    [GitHub](https://github.com/fuzzyklein2/workshop-0.0.1b)
"""

import os
from pathlib import Path
import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.1')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import WebKit2 as webkit
from gi.repository import GObject as gobject
from gi.repository import Pango as pango
from gi.repository import GdkPixbuf
from gi.repository import GLib

# try:
#     from pygnition.program import *
#     from pygnition.server import Server
# except (ImportError, ModuleNotFoundError):

# LOCATION_PATH = Path.home() / '.pygnition.location.txt'
# IGNITION_PATH = LOCATION_PATH.read_text().strip()

# from ignition.where import PYGNITION_DIRECTORY

# PYGNITION_DIRECTORY = os.environ["PYGNITION_DIRECTORY"]
PYGNITION_DIRECTORY = (Path.home() / '.pygnition/location.txt').read_text().strip()
print(f'Pygnition package location: {PYGNITION_DIRECTORY}')
sys.path.insert(0, PYGNITION_DIRECTORY)
print(f'First path in `sys.path`: {sys.path[0]}')

from pygnition.program import Program
from pygnition.server import Server
from pygnition.where import PYGNITION_DIRECTORY

class GTKApp(Program):
    def __init__(self):
        super().__init__()
        # debug(f'Running {PROGRAM_NAME}')
        # debug(f'{ARGS=}')
        # debug(f'{USER_DATA_DIR=}')

        self.srv = Server()
        self.srv.start()

        self.window = gtk.Window(title="Ignition Browser")
        self.window.set_default_size(800, 600)
        self.window.connect("destroy", gtk.main_quit)

        # Create WebKit2 WebView
        self.webview = webkit.WebView()
        self.window.add(self.webview)

        # Load a page
        self.webview.load_uri(f"http://{self.host}:{self.port}")

        # Show everything
        self.window.show_all()

    def shutdown(self):
        self.srv.stop()
        super().shutdown()
        
if __name__ == '__main__':
    app = GTKApp()
    gtk.main()
