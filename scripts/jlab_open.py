#!/usr/bin/env python3
"""
Open one or more files in an existing Jupyter Lab session,
or start one automatically if none is running.

Usage:
    python jlab_open.py file1.ipynb file2.py ...
"""

import sys
import time
import webbrowser
import subprocess
from pathlib import Path
import requests
from urllib.parse import urljoin, quote
from jupyter_server import serverapp


def get_running_server():
    """Return the first running Jupyter server’s info dict, or None."""
    servers = list(serverapp.list_running_servers())
    return servers[0] if servers else None


def start_jupyter_lab(root: Path):
    """Start Jupyter Lab in the background and wait for it to be ready."""
    print(f"🚀 Starting Jupyter Lab in {root} ...")
    subprocess.Popen(
        ["jupyter", "lab", "--no-browser", "--notebook-dir", str(root)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait for Jupyter to start (up to 15 seconds)
    for _ in range(30):
        time.sleep(0.5)
        server = get_running_server()
        if server:
            print("✅ Jupyter Lab started.")
            return server
    sys.exit("❌ Failed to start Jupyter Lab.")


def ensure_server_for_file(file_path: Path):
    """Return a running server that can access the given file."""
    abs_file = Path(file_path).resolve()
    server = get_running_server()

    if not server:
        # Start a new Jupyter Lab instance in the file's directory
        return start_jupyter_lab(abs_file.parent)

    root = Path(server["root_dir"]).resolve()
    if not abs_file.is_relative_to(root):
        print(f"⚠️  {abs_file} is outside the Lab root ({root}). Restarting server...")
        return start_jupyter_lab(abs_file.parent)

    return server


def open_in_lab(file_paths):
    # Use first file to decide if we need to start Lab
    first_file = Path(file_paths[0]).resolve()
    server = ensure_server_for_file(first_file)

    base_url = server["url"]
    token = server.get("token")
    root = Path(server["root_dir"]).resolve()
    headers = {"Authorization": f"token {token}"} if token else {}

    # Notify backend for each file (optional, improves UX)
    workspace_url = urljoin(base_url, "lab/api/workspaces/default")

    opened_urls = []
    for file_path in file_paths:
        abs_path = Path(file_path).resolve()
        try:
            rel_path = abs_path.relative_to(root)
        except ValueError:
            print(f"⚠️  Skipping {abs_path} (outside Lab root {root})")
            continue

        tree_url = urljoin(base_url, f"lab/tree/{quote(str(rel_path))}")
        if token:
            tree_url += f"?token={token}"

        payload = {"data": {"type": "file", "path": str(rel_path)}}
        try:
            requests.post(workspace_url, headers=headers, json=payload, timeout=3)
        except Exception:
            pass

        opened_urls.append(tree_url)
        print(f"🌐 Queued for opening: {rel_path}")

    if opened_urls:
        # Open first URL in the browser (Jupyter will open the rest in tabs)
        webbrowser.open(opened_urls[0])
    else:
        print("⚠️  No valid files to open.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python jlab_open.py file1 [file2 ...]")
        sys.exit(1)

    open_in_lab(sys.argv[1:])


if __name__ == "__main__":
    main()
