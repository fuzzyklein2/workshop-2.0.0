#!/usr/bin/env python3

"""
@file hw.py
@version 1.0.1
@brief Defines the class that runs the module as a program.


For more information, see:

    https://github.com/fuzzyklein2/workshop-0.0.1b
"""

import os
from pathlib import Path
import sys

from rich.columns import Columns
from rich.console import Console

from pygnition.files import File
from pygnition.filter import Filter
from pygnition.lumberjack import debug

console = Console()

class LSD(Filter):
    def __init__(self):
        super().__init__()
        if not self.paths:
            self.paths = [Path.cwd()]
        self.files = list()

    def process_file(self, p:Path):
        debug(f'Processing file: {str(p)} ...')
        self.files.append(File(p).output())

    def process_directory(self, p:Path):
        debug(f'Processing directory: {str(p)} ...')
        if self.recursive:
            warn(f'Directory walk is under construction!{CONSTRUCTION_PICT}')
            os.chdir(p)
            t = Table('Root', 'Directories', 'Files')
            for root, dirs, files in os.walk(os.curdir):
                if root == os.curdir:
                    root = p.name
                # if
                t.add_row(f'{root}', f'{pformat(dirs)}', f'{pformat(files)}')
                t.add_row('','','')
            rp(t)
            os.chdir(self.cwd)
        else:
            self.files = sorted(os.listdir(p))
            self.files = ['[blue bold]' + f + '[/blue bold]' if (p / f).is_dir() else f for f in self.files]
            console.print(f"\n📁  Files in [cyan bold]{str(p)}[/cyan bold]:")
            console.print(Columns(self.files, expand=True, equal=True))
            print()
#             old_stdout = sys.stdout
#             sys.stdout = StringIO()
#             Cmd().columnize(self.files)
#             columns = sys.stdout.getvalue()
#             sys.stdout = old_stdout
            
#             rp(f"""{FOLDER_PICT}Files in [cyan bold]{str(p)}[/cyan bold]:
        
# {columns}""")

    def run(self):
        super().run()


if __name__ == '__main__':
    rp(f"{WARNING_PICT}[yellow bold]WARNING[/yellow bold]: {PROGRAM_NAME} is under construction! {CONSTRUCTION_PICT}")
    ListDirectory().run()
