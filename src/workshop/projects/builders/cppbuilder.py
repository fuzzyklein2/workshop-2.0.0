#!/usr/bin/env python3

from pathlib import Path

from ...startmeup import *

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

import os
from pprint import pformat

from pygnition.constants import SPACE
from pygnition.lumberjack import debug, error, info, stop, warn
from pygnition._read_lines import read_lines
from pygnition.where import USER_DATA_DIR

from .builder import Builder

@Builder.register('cpp')
class CPPBuilder(Builder):
    # warn("CPPBuilder not yet implemented.")
    def __init__(self, project):
        super().__init__(project)
        self.std_opt = f'-std=c++{self.std}'
        self.command = 'g++'

    @auto_doc()
    def compile(self):
        info(f'Compiling {self.project.name}...')
        # os.environ['WORKSHOP_SCRIPT_DIRECTORY'] = str(self.project.source / 'scripts')
        # os.environ['WORKSHOP_TEMP_DIRECTORY'] = str(USER_DATA_DIR / 'temp')

        # debug("Calling pkg-tool.sh")
        # debug(f'{PACKAGE_PATH=}')
        # p = run_cmd(['bash',
        #              f'{PACKAGE_PATH}/scripts/pkg-tool.sh']
        #            )
        # if p.stderr:
        #     error(p.stderr)
        # if p.stdout:
        #     info(p.stdout)

        # PKG_CONFIG_ARGS = Path(f'{self.project.user_data}/temp/pkg-config.out').read_text().strip().split()
        PACKAGES = SPACE.join(read_lines(self.project.path / 'data/packages.txt'))
        process = subprocess.run(['pkg-config',
                          '--cflags',
                          '--libs',
                          *PACKAGES.split()],
                          encoding='utf-8',
                          capture_output=True,
                          check=False,
                          shell=False
                         )
        if process.returncode:
            error(f"pkg-config returned error code: {process.returncode}")
            error(f"""Error output:
{process.stderr}
""")
        else:
            PKG_CONFIG_ARGS = process.stdout.split()
        debug(f"""`pkg-config` arguments:
{pformat(PKG_CONFIG_ARGS)}
        """)
        # return
        CMD_LINE = [self.command,
                    *self.src_files,
                    '-o',
                    self.exe_path,
                    f'-Iinc',
                    self.std_opt
                   ]
        CMD_LINE.extend(PKG_CONFIG_ARGS)

        debug(f"""Command line:
{pformat(CMD_LINE)}
""")
        p = subprocess.run(CMD_LINE,
                           encoding='utf-8',
                           capture_output=True,
                           check=False,
                           shell=False
                          )
        if p.stdout:
            print(p.stdout)
        if p.stderr:
            error(p.stderr)
        
