#!/usr/bin/env python3

"""
@file compile.py
@version 1.2.3
@brief Compiles a project. Supports only C++ for now.

This module:

    * Parses arguments.
    * Sets up logging.
    * Imports config files.

    For more information, see:
    https://github.com/fuzzyklein2/workshop-0.0.1b
"""

from enum import auto, Enum
from glob import glob
import logging
import os
from pathlib import Path
from pprint import pformat
from subprocess import run
import sys

from arguments import parse_arguments
from lumberjack import *
from ws import *

    
class Builder(Enum):
    CPP = auto()
    MAKE = auto()
    CMAKE = auto()
    MESON = auto()

class Compiler():
    def __init__(self, project, directory):
        info(f'Initializing {self.__class__.__name__}...')
        self.project = project
        self.directory = directory
        self.std = 20
        self.cmd_lines = list()
        self.cwd = CWD
        self.exe_path = f'bin/{self.project}'

    def compile(self):
        error("Can't call `compile` from Compiler base class!")
        exit()
    
    def finish(self):
        os.chdir(self.cwd)

    def build(self):
        os.chdir(self.directory)
        self.src_files = glob('src/*')
        info(f"""Source files:
{pformat(self.src_files)}
""")
        self.compile()
        self.finish()

    def run(self):
        for line in self.cmd_lines:
            p = run_cmd(line, check=True)
            if p.stderr:
                print(p.stderr)
                error('`make` raised an exception!')
            if p.stdout:
                print(p.stdout)

class CPPBuilder(Compiler):
    # warn("CPPBuilder not yet implemented.")
    def __init__(self, project, directory):
        super().__init__(project, directory)
        self.std_opt = f'-std=c++{self.std}'
        self.command = 'g++'

    def compile(self):
        info(f'Compiling {PROJECT}...')
        p = run_cmd(['bash', f'{WORKSHOP}/scripts/pkg-tool.sh'])
        if p.stderr:
            error(p.stderr)
        if p.stdout:
            info(p.stdout)

        PKG_CONFIG_ARGS = Path(f'data/pkg-config.out').read_text().strip().split()

        debug(f"""`pkg-config` arguments:
{pformat(PKG_CONFIG_ARGS)}
        """)

        CMD_LINE = [self.command,
                    *self.src_files,
                    '-o',
                    self.exe_path,
                    f'-Iinc',
                    *PKG_CONFIG_ARGS,
                    self.std_opt
                   ]

        debug(f"""Command line:
{pformat(CMD_LINE)}
""")
        p = run_cmd(CMD_LINE)
        if p.stdout:
            print(p.stdout)
        if p.stderr:
            error(p.stderr)
        
class MakeBuilder(CPPBuilder):
    def __init__(self, project, directory):
        super().__init__(project, directory)
        # warn("MakeBuilder not yet implemented!")
        self.cmd_lines = [['make', 'clean'], ['make']]

    def build(self):
        info(f'Compiling {self.project}...')

        if not self.cwd.samefile(self.directory):
            os.chdir(self.directory)
        
        # for line in self.cmd_lines:
        #     p = run(line, encoding='utf-8', capture_output=True, check=True)
        #     if p.stderr:
        #         print(p.stderr)
        #         error('`make` raised an exception!')
        #     if p.stdout:
        #         print(p.stdout)

        self.run()
        os.chdir(self.cwd)

                          
class CMakeBuilder():
    def __init__(self, project, directory):
        super().__init__(project, directory)
        self.cmd_lines = [['cmake', '..'],
                          ['cmake', '--build', '.']]

    def build():
        build_dir = Path(self.directory) / 'build'
        if not build_dir.exists():
            build_dir.mkdir()
        os.chdir(build_dir)
        self.run()
        os.chdir(self.cwd)
        

def MesonBuilder():
    warn("Meson not yet implemented.")

if __name__ == '__main__':
    ARGS = parse_arguments(CMD_LINE_ARGS_FILE,
                           PROGRAM, VERSION,
                           DESCRIPTION, EPILOG)
    
    try:
        PROJECT = ARGS.args[0]
        PROJECT_DIR = Path(PROJECT)
    except IndexError:
        # At some point this should cause the build of the current working directory.
        PROJECT = Path.cwd().stem
        warn("No project name specified!")
        info("Assuming current directory.")
        PROJECT_DIR = Path.cwd()
    
    info(f'Building project: {PROJECT}')
    info(f'Project Directory: {PROJECT_DIR}')
    ls = os.listdir(PROJECT_DIR)
    
    debug(f'{PROJECT_DIR=}')
    
    DETECTED = Builder.CPP
    if 'Makefile' in ls:
        DETECTED = Builder.MAKE
    elif 'CMakeLists.txt' in ls:
        DETECTED = Builder.CMAKE
    elif 'meson.build' in ls:
        DETECTED = Builder.MESON
    
    debug(f'{DETECTED=}')
    
    builders = { Builder.CPP: CPPBuilder,
                 Builder.MAKE: MakeBuilder,
                 Builder.CMAKE: CMakeBuilder,
                 Builder.MESON: MesonBuilder
               }
    
    builder = builders[DETECTED]
    # builder(PROJECT, PROJECT_DIR)
        
    builder(PROJECT, PROJECT_DIR).build()
