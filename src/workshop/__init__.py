#!/usr/bin/env python3

from pygnition import *

__doc__ = f"""The 🛠️  {PACKAGE_NAME} 🛠️  program is a test run for the 🔥  pygnition 🔥  project.

========== ⚠️  WARNING! ⚠️  ==========

This project is currently under construction.
Stay tuned for updates.

## Version

{VERSION}

## Author

{AUTHOR}

## Usage

`$ python -m {PACKAGE_NAME} [OPTIONS] [ARGUMENTS]`

## System Requirements

{REQUIREMENTS}

This file may re-export selected symbols from submodules for convenience.
Check the package [reference documentation](docs/markdown/index.md) for details.
"""

# from .projects.project import Project

# Force subclass registration
from workshop.projects.script import Script
from workshop.projects.module import Module
from workshop.projects.program import Program
from workshop.projects.filter import Filter
from workshop.projects.driver import Driver
from workshop.projects.cgi import Cgi
from workshop.projects.tkapp import TkApp
from workshop.projects.gtkapp import GtkApp
from workshop.projects.webapp import WebApp

from workshop.projects.builders.cppbuilder import CPPBuilder

# print(PACKAGE_NAME)