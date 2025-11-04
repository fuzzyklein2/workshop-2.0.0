#!/usr/bin/env python3

"""
@file hw.py
@version 0.0.1b
@brief Defines the class that runs the module as a program.


For more information, see:

    https://github.com/fuzzyklein2/workshop-0.0.1b
"""

from pathlib import Path
import sys

# DEBUG = not __debug__

# LOCATION_PATH = Path.home() / '.pygnition.location.txt'
# IGNITION_PATH = LOCATION_PATH.read_text().strip()

# sys.path.insert(0, str(IGNITION_PATH))
# from pygnition.program import *
from pygnition.driver import *
from pygnition.server import *

PROJECT_DIR = Path(__file__).resolve().parent.parent

class HWWW(Driver):
    def __init__(self):
        super().__init__()
        self.srv = Server()

    # class Start(Driver.Command):
    #     # def __init__(self, name, line):
    #         # super().__init__(name, line)
    #     def run(self):
    #         debug(f'Running {self.name}')
    #         self.srv.start()
    
    # class Stop(Driver.Command):
    #     def run(self):
    #         debug(f'Running {self.name}')
    #         self.srv.stop()

    # @get_func_name
    def do_start(self, line:str):
        try:
            self.srv.start()
        except KeyboardInterrupt:
            # self.srv.stop()
            pass
            
    # @get_func_name
    def do_stop(self, line:str):
        # self.do_command(self.current_cmd, line)
        self.srv.stop()        

if __name__ == '__main__':
    if DEBUG:
        rp(f"{WARNING_PICT}[yellow bold]WARNING[/yellow bold]: {PROGRAM_NAME} is under construction! {CONSTRUCTION_PICT}")
        Program().run()
