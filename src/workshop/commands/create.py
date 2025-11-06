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

from pygnition.constants import HYPHEN
from pygnition.driver import Driver
from pygnition.files import File
from pygnition.lumberjack import debug, error, info, stop, warn
from pygnition.picts import *
from pygnition.tools import cwd

from workshop.constants import KEY_PROMPTS
from workshop.new_project_dialog import new_project_dialog
from workshop.projects import Project


class Create(Driver.Command):
    def __init__(self, name, line, **kwargs):
        super().__init__(name, line, **kwargs)
        self.repo_url = None
        self.template_repo_url = None
        self.clone_dest = None
        
        if len(self.args):
            p = File(self.args[0])
        else: p = File(cwd())

        self.log.debug(f'{DEBUG_PICT}{type(p)=}')

        if type(p) is not Project:
            COMPONENTS = p.name.split(HYPHEN)

        self.log.debug(f'{DEBUG_PICT}Opening New Project dialog.')

        self.params = new_project_dialog(KEY_PROMPTS)

        if self.debug: rp(f"""{DEBUG_PICT}[red]DEBUG[/red] {DEBUG_PICT}
[cyan][bold]New Project parameters[/bold][/cyan]:

{pformat(self.params)}
""")
        if not self.params:
            self.log.info(f'{INFO_PICT}New project cancelled by user.')
            return
        else:
            self.log.info(f'{INFO_PICT}Creating {params['type']} project {params['name']} at {str(params['path'])}')

        self.log.info(f'{INFO_PICT}Creating project {str(p)}')
        if self.params:
            self.repo_url = params['github']
            self.template_repo_url = Project.GH_TEMPLATES[params['type'].lower()]
            self.clone_dest = params['path']

    def run(self):
        debug(f'Running {self.cmd_name}')
        if self.testing: debug(f'Testing {self.cmd_name} command.')
        # data = input_params_gui(key_prompts)
        # TODO: Do the dialog here and collect the data.
        # print("Collected:", data)
        """Ensure repo exists and clone it."""
        # 1. Ensure repository exists (creates if needed)
        if self.params:
            ssh_url = https_to_ssh(self.repo_url)
            
            # Use ensure_repo_exists function to create/check repo
            repo_path = ensure_repo_exists(self.repo_url, self.template_repo_url, prefs_dir = USER_PREFS_DIR)
            
            # 2. Clone the repository
            # clone_path = clone_repo(ssh_url, self.clone_dest)
            
            print(f"Repository is ready at {repo_path}")
            return repo_path
        return

