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

from pathlib import Path
import shutil
import subprocess
from urllib.parse import urlparse

from pygnition.configure import config
from pygnition.tools import cwd

def https_to_ssh(url: str) -> str:
    """
    Convert a GitHub HTTPS URL to SSH format.
    Example: https://github.com/user/repo.git -> git@github.com:user/repo.git
    """
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return url  # Already SSH or something else

    # Remove leading '/' from path
    path = parsed.path.lstrip('/')
    return f"git@{parsed.netloc}:{path}"

def repo_exists(ssh_url: str) -> bool:
    """
    Check if a GitHub repository exists using the gh CLI.
    """
    # Extract user and repo name from SSH URL
    try:
        user_repo = ssh_url.split(":")[1].replace(".git", "")
    except IndexError:
        raise ValueError(f"Invalid SSH URL: {ssh_url}")
    
    try:
        subprocess.run(
            ["gh", "repo", "view", user_repo],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def create_repo(ssh_url: str) -> None:
    """
    Create a new GitHub repository using the gh CLI.
    """
    user_repo = ssh_url.split(":")[1].replace(".git", "")
    subprocess.run(["gh", "repo", "create", user_repo, "--public", "--confirm"], check=True)

def ensure_repo_exists(
    repo_url: str,
    template_repo_url: str | None = None,
    prefs_dir: Path | None = None,
    local_only: bool = False
) -> Path:
    """
    Ensure a project repository exists.

    Behavior:
    - If template_repo_url is a local directory → copy it, initialize a new Git repo
    - If template_repo_url is remote → create GitHub repo from template
    - If template_repo_url is None → create new empty repo

    Returns:
        Path to the local repository (even for remote, path is ~/projects/<repo_name> by default)
    """
    repo_name = Path(repo_url).name
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    # Default local path
    local_path = cwd() / repo_name
    local_path.mkdir(parents=True, exist_ok=True)

    # --- LOCAL TEMPLATE CASE ---
    if template_repo_url and Path(template_repo_url).exists():
        src = Path(template_repo_url).expanduser().resolve()
        if local_path.exists() and any(local_path.iterdir()):
            print(f"⚠️  Destination already exists and is not empty: {local_path}")
        else:
            print(f"📁 Copying template {src} → {local_path}")
            shutil.copytree(src, local_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
            # Initialize new Git repo
            subprocess.run(["git", "init"], cwd=local_path, check=True)
            subprocess.run(["git", "add", "."], cwd=local_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit from template"], cwd=local_path, check=True)
            print(f"✅ Local repository initialized at {local_path}")
        return local_path

    # --- REMOTE GITHUB CASE ---
    if not local_only:
        if not prefs_dir:
            raise ValueError("data_dir is required for GitHub operations")
        gh_user = config(prefs_dir / "config.ini")["GITHUB_USERNAME"]
        full_repo = f"{gh_user}/{repo_name}"
        ssh_url = https_to_ssh(repo_url)

        # Check if repo exists remotely
        try:
            subprocess.run(
                ["gh", "repo", "view", full_repo],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"✅ GitHub repo already exists: {full_repo}")
        except subprocess.CalledProcessError:
            cmd = ["gh", "repo", "create", full_repo, "--public", "--confirm"]
            if template_repo_url:
                cmd.extend(["--template", template_repo_url])
            print(f"🌐 Creating GitHub repository {full_repo}...")
            subprocess.run(cmd, check=True)
            print(f"✅ GitHub repository created: {full_repo}")

    # --- Ensure local repo exists ---
    if not local_path.exists() or not any(local_path.iterdir()):
        local_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init"], cwd=local_path, check=True)
        print(f"✅ Local repository created at {local_path}")

    return local_path
