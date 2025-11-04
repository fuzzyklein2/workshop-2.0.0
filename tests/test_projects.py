#!/usr/bin/env python
# tests/test_projects.py

import sys
from pathlib import Path

# Add the actual pygnition source folder to sys.path

# sys.path.insert(0, '/home/fuzzy/projects/pygnition-1.2.0c/src')
# sys.path.insert(0, '/home/fuzzy/projects/workshop-2.0.0/src')


from workshop.projects import Project, looks_like_project

import pytest
from pathlib import Path


@pytest.fixture
def project():
    """Return a Project instance for the current working directory."""
    return Project(Path.cwd())


def test_folder_structure(project):
    # source, package, data
    if project.source:
        assert project.source.exists()
    if project.package:
        assert project.package.exists()
    if project.data:
        assert project.data.exists()


def test_get_author(project):
    author = project.get_author()
    assert isinstance(author, str)
    # Optional: print for manual inspection
    print("Author:", author)


def test_get_description(project):
    desc = project.get_description()
    assert isinstance(desc, str)


def test_read_requirements(project):
    reqs = project.read_requirements()
    assert isinstance(reqs, str)


def test_detect_context(project):
    ctx = project.detect_context()
    expected_keys = [
        'project_name','version','is_update','is_git_repo',
        'author','description','class_name','requirements','github'
    ]
    assert all(k in ctx for k in expected_keys)


def test_detect_type(project):
    ptype = project.detect_type()
    assert ptype in Project.Types


def test_deduce_github(project):
    url = project.deduce_github()
    assert url.startswith("https://github.com/")


def test_describe(project):
    desc = project.describe()
    assert isinstance(desc, str)
    print("Project description:", desc)


def test_parse_name_version(project):
    name, ver = project._parse_name_version()
    assert isinstance(name, str)
    assert ver is None or isinstance(ver, str)


def test_looks_like_project():
    cwd = Path.cwd()
    result = looks_like_project(cwd)
    assert result in (True, False)
