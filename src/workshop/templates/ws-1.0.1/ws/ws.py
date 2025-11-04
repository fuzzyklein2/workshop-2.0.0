#!/usr/bin/env python3

"""
@file ws.py
@version 0.0.1b
@brief Defines the class that runs the module as a program.


For more information, see:

    https://github.com/fuzzyklein2/workshop-0.0.1b
"""

from pathlib import Path
import sys

from rich import print as rp

# DEBUG = not __debug__

# LOCATION_PATH = Path.home() / '.pygnition.location.txt'
# IGNITION_PATH = LOCATION_PATH.read_text().strip()

# sys.path.insert(0, str(IGNITION_PATH))
from pygnition.driver import Driver
from pygnition.lumberjack import debug
from pygnition.picts import *
from pygnition.tools import get_func_name

class WS(Driver):
    def __init__(self):
        super().__init__()        
        self.projects_file = self.user_data / 'var/projects.json'
        if not self.projects_file.exists():
            mkdir(self.projects_file.parent)
            d = dict()
            self.projects_file.write_text(json.dumps(d))
        
        self.packages = self.user_data / 'etc/packages.txt'
        if not self.packages.exists():
            mkdir(self.packages.parent)
            touch(self.packages)
        
        self.project = None
        # self.current_cmd = None

        # if self.debug: self.dump()

    class Create(Driver.Command):
        def __init__(self, name, line):
            super().__init__(name, line)
            debug('What the fuck?')

        def run(self):
            debug(f'Running {self.name}')

    class Compile(Driver.Command):
        def __init__(self, name, line):
            super().__init__(name, line)
            debug(f'Initializing {self.__class__.__name__} object ...')

        def run(self):
            debug(f'Running {self.name} ...')

    @get_func_name
    def do_create(self, line:str):
        self.command(self.current_cmd, line)

    @get_func_name
    def do_compile(self, line:str):
        self.command(self.current_cmd, line)
        
    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, p : Path | None = None):
        self._project = p
        
    @project.deleter
    def project(self):
        del self._project
            
if __name__ == '__main__':
    rp(f"{WARNING_PICT}[yellow bold]WARNING[/yellow bold]: {PROGRAM_NAME} is under construction! {CONSTRUCTION_PICT}")
    ws = WS()
    ws.dump()
    ws.run()
