#!/usr/bin/env python3

from pathlib import Path

from ..startmeup import *

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


# from __future__ import annotations
import os, re, subprocess, logging
from enum import Enum, auto
from pathlib import Path
from types import SimpleNamespace

from pygnition._data_tools import is_valid_data_line
from pygnition.constants import HYPHEN
from pygnition.files import File, Folder
from pygnition._git_tools import get_github_username
from pygnition.user_tools import get_full_name

class Project(Folder):
    """A folder representing a Python project."""

    PRJ_TYPE_STRS = [
        'script', 'module', 'program', 'filter', 'driver',
        'cgi', 'tkapp', 'gtkapp', 'webapp'
    ]

    class Types(Enum):
        SCRIPT  = auto()
        MODULE  = auto()
        PACKAGE = auto()
        PROGRAM = auto()
        FILTER  = auto()
        DRIVER  = auto()
        CGI     = auto()
        TK      = auto()
        GTK     = auto()
        WEBKIT  = auto()
        DEFAULT = SCRIPT

    GH_TEMPLATES = {
        'script': None,
        'module': None,
        'package': None,
        'program': None,
        'filter': None,
        'driver': None,
        'cgi': None,
        'tkapp:': None,
        'gtkapp': None,
        'webapp': None
    }

    # ──────────────────────────────────────────────
    # Subclass registry and auto-dispatch
    # ──────────────────────────────────────────────
    _registry: dict[str, type[Project]] = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator for subclasses to self-register under a type name.
        Example:
            @Project.register("script")
            class Script(Project): ...
        """
        def decorator(subclass):
            cls._registry[name] = subclass
            return subclass
        return decorator

    def __new__(cls, p):
        """Return the proper subclass (Script, Program, etc.) if detected."""
        if cls is not Project:
            # Already constructing a subclass — skip re-dispatch
            return super().__new__(cls)

        path = Path(p)
        try:
            project_type = cls._detect_type_static(path)
            subclass = cls._registry.get(project_type, cls)
            if subclass is not cls:
                return super(Project, subclass).__new__(subclass)
        except Exception as e:
            print(f"DEBUG: Project type detection failed: {e}")

        return super().__new__(cls)

    @staticmethod
    def _detect_type_static(path: Path) -> str:
        """
        Lightweight static detection used during __new__.
        Avoids side effects — only checks file structure.
        """
        src = path / "src"
        name = path.name
        package = src / name
        main_py = package / "__main__.py"
        module_py = package / f"{name}.py"

        if package.exists():
            if main_py.exists():
                return "program"
            if module_py.exists():
                return "module"

        if (src / "index.html").exists():
            return "cgi"

        if len(list(path.glob("*.py"))) == 1:
            return "script"

        return "default"

    # ──────────────────────────────────────────────
    # Normal Project initialization
    # ──────────────────────────────────────────────
    def __init__(self, p):
        super().__init__(p)
        print(f"DEBUG Project.__init__ called for {p}")
        self.name, self.version = self._parse_name_version()
        self.source = self.path / "src" if (self.path / "src").exists() else None
        self.package = self.source / self.name if self.source else None
        self.data = self.source / 'data' if self.source else None
        self.requirements = self.read_requirements()
        self.github = self.deduce_github()
        self.type = self.detect_type()
        self.context = self.detect_context()

    # ──────────────────────────────────────────────
    # Utility methods
    # ──────────────────────────────────────────────
    def deduce_github(self):
        if self.name and self.version:
            return f'https://github.com/{get_github_username()}/{self.name}-{self.version}.git'
        elif self.name:
            return f"https://github.com/{get_github_username()}/{self.name}.git"
        else:
            return ''
            
    def detect_type(self):
        main_py = self.package / '__main__.py'
        module_py = self.package / f'{self.name}.py'

        if self.package.exists():
            target_files = [main_py, module_py]
            for f in target_files:
                if f.exists():
                    text = f.read_text(errors="ignore")
    
                    # Subclass-based detection
                    if re.search(r"class\s+\w+\(.*Filter.*\):", text):
                        return self.Types.FILTER
                    if re.search(r"class\s+\w+\(.*Driver.*\):", text):
                        return self.Types.DRIVER
    
                    # GUI imports
                    if re.search(r"\bimport\s+tkinter\b|\bfrom\s+tkinter\b", text):
                        return self.Types.TK
                    if re.search(r"\bimport\s+gi\b.*Gtk", text):
                        return self.Types.GTK
    
            if main_py.exists():
                return self.Types.PROGRAM
    
        if (self.source / "index.html").exists():
            return self.Types.CGI
    
        if len(list(self.path.glob("*.py"))) == 1:
            return self.Types.SCRIPT
    
        return self.Types.DEFAULT

    def get_author(self):
        AUTHOR_FILE = self.data / 'author.txt'
        if AUTHOR_FILE.exists():
            return AUTHOR_FILE.read_text()
        else:
            try:
                author = subprocess.run(
                    ["git", "config", "user.name"],
                    capture_output=True,
                    text=True,
                    check=True
                ).stdout.strip()
            except Exception:
                author = None
        
            if not author:
                try:
                    author = get_full_name()
                except Exception:
                    author = os.getenv("USER", "")

        return author or ''

    def get_description(self):
        DESC_FILE = self.data / 'description.txt'
        if DESC_FILE.exists():
            return DESC_FILE.read_text()
        return ''

    def read_requirements(self):
        for filename in ("requirements.txt", "requirements.in"):
            path = self.path / filename
            if path.exists():
                lines = path.read_text().splitlines()
                valid = [s.strip() for s in lines if is_valid_data_line(s)]
                return " ".join(valid)
        return ""

    def detect_context(self) -> dict[str, str | bool]:
        return {
            'project_name': self.name,
            'version': self.version,
            'is_update': True,
            'is_git_repo': (self.path / '.git').exists(),
            'author': self.get_author(),
            'description': self.get_description(),
            'class_name': '',
            'requirements': self.requirements,
            'github': self.github,
        }

    def _parse_name_version(self):
        m = re.match(r"^(.*?)-v?(\d+(?:\.\d+){0,4}[a-z]?)$", self.path.name)
        if m:
            return m.group(1), m.group(2)
        return self.path.name, None

    def __repr__(self):
        return f"Project(name={self.name!r}, version={self.version!r}, path={self.path!s})"

    def describe(self):
        parts = [f"[bold]{self.name}[/bold]"]
        if self.version:
            parts.append(f"[cyan]{self.version}[/cyan]")
        if self.source:
            parts.append("[green]src/[/green]")
        return " ".join(parts)

# Register this type with File (unchanged)
File.register_folder(lambda p: (p / "src").exists())(Project)
