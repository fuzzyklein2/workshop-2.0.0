#!/usr/bin/env python3

from pathlib import Path

from pygnition import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️  WARNING! ⚠️  ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PACKAGE_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {LAST_SAVED_DATE}

## Description

This module defines the Workshop class.

## Typical Use
```python
args = parse_arguments()

## Notes

You can include implementation notes, dependencies, or version-specific
details here.

## [GitHub]({get_upstream_url()})

"""

from rich import print as rp

from pygnition.driver import Driver
from pygnition.picts import *

# from workshop.projects import Project

class Run(Driver.Command):
    """ Run the project given on the command line, the current project,
        or whatever project is represented by cwd(), if any.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def run(self):
        rp(f'{INFO_PICT}[green]Running project...[/]')
        results = list()
        project = self.driver.current_project
        if project:
            print(f"""Current project: {project.name} {project.version}""")
            results.append(project.run())
        else:
            if not self.args:
                project = Project(cwd())
                return project.run()
            else:
                results = []
                for project in self.args:
                    results.append(File(project).run())
        for p in results:
            rp(f"""[cyan]{p.args}[/cyan] results:
    
[{'red' if p.returncode else 'green'}]Return code[/]: {p.returncode}
{'[red]Error output[/]: \n' + p.stderr + '\n' if p.stderr else ''}
{'[green]Standard output[/]: \n\n' + p.stdout + '\n' if p.stdout else ''}
""")
        # return results
