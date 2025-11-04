#!/usr/bin/env python3

from pathlib import Path

from .startmeup import *

MODULE_NAME = Path(__file__).stem

__doc__ = f"""Python IDE for the command line.

========== ⚠️ WARNING! ⚠️ ==========
This project is currently under construction.
Stay tuned for updates.

Module: {PACKAGE_NAME}.{MODULE_NAME}
Version: {VERSION}
Author: {AUTHOR}
Date: {str(last_saved_datetime(__file__).date()).split('.')[0]}

## Description

This module defines the Workshop class.

## Typical Use
```python
app = Workshop()
app.run()

Notes
-----
You can include implementation notes, dependencies, or version-specific
details here.

## [GitHub]({get_upstream_url()})

## Sample Output

New Project parameters:

'author': 'Fuzzy Klein',
'description': 'File filtering tool.',
'github': 'https://github.com/fuzzyklein2/lsd-1.3.git',
'license': 'MIT',
'name': 'lsd',
'path': '/home/fuzzy/.workshop/temp/lsd-1.2/lsd-1.3',
'requirements': 'pygnition',
'type': 'Script',
'version': '1.3',
'visibility': 'public'

"""

from pprint import pformat, pprint as pp

from rich import print as rp

from pygnition.constants import HYPHEN
from pygnition.driver import Driver
from pygnition.files import File
from pygnition.picts import *
from pygnition.lumberjack import debug, error, info, stop, warn
from pygnition.strings import is_valid_module_name
from pygnition.tools import cwd
from pygnition.where import USER_PREFS_DIR

from .constants import KEY_PROMPTS
from .ghtools import *
from .new_project_dialog import new_project_dialog
from .projects import Project # probably don't really need to except for type hints and such

class Workshop(Driver):
    def __init__(self, *args, **kwargs):
        Driver.__init__(*args, **kwargs)
        print(self.args[0])
        self.current_project = Project(cwd())
        self.prompt = 'ws'

    class Open(Driver.Command):
        """ Open a project by `cd`'ing to its root directory. """
        def __init__(self, name, line, **kwargs):
            super().__init__(name, line, **kwargs)

            # pp(self.args)

            self.log.debug(f'{DEBUG_PICT}Running `{self.cmd_name}`')

        def run(self):
            if self.args:
                p = Project(self.args[0])
                self.driver.current_project = p
                self.log.info(f'{INFO_PICT}Opened {p.describe()}')
            else:
                self.log.warning(f'{WARNING_PICT}open command requires an argument.')

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
    
    class Compile(Driver.Command):
        def __init__(self, name, line):
            super().__init__(name, line)
            debug(f'Initializing {self.__class__.__name__} object ...')

    def __init__(self):
        super().__init__()

    def test(self):
        warn(f'{self.name} is under construction!')
        if self.testing: self.dump()

    def run(self):
        print(f'Hello, {GLOBE_AMERICA_PICT.strip()} !')
        super().run()

if __name__ == '__main__':
    p = Workshop()
    if p.testing:
        p.test()
    p.run()
