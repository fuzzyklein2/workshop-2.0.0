#!/usr/bin/env bash
# ======================================================
# newproj-init.sh
# ------------------------------------------------------
# Initialize or update a Python project using setuptools-scm
# - If not in a Git repo: create one and publish it to GitHub
# - If in a Git repo: enable versioning via tags if needed
# - Ensure src/ exists or prompt user to choose one via Zenity
# - Prompt for GitHub repo visibility (Public/Private)
# ======================================================

set -euo pipefail

PROJECT_NAME=$(basename "$(pwd)")
DEFAULT_DIR="$HOME/projects"
[ -d "$DEFAULT_DIR" ] || DEFAULT_DIR="$HOME"

echo "🚀 Initializing project: $PROJECT_NAME"

# 1️⃣ Ensure src/ directory exists or prompt
if [ ! -d src ]; then
    echo "🗂️ No src/ directory found."
    SRC_DIR=$(zenity --file-selection --directory \
        --title="Select or create a source directory for your project" \
        --filename="$DEFAULT_DIR/" 2>/dev/null) || {
        echo "❌ No directory selected. Exiting."
        exit 1
    }
    echo "📁 Using $SRC_DIR as source directory."
    ln -s "$SRC_DIR" src
else
    echo "✅ src/ directory already exists."
fi

# 2️⃣ Git setup
if [ -d .git ]; then
    echo "✅ Git repository already initialized."
else
    echo "📘 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit"

    # 🪄 Ask user whether to make the repo public or private
    VISIBILITY=$(zenity --list \
        --radiolist \
        --title="GitHub Repository Visibility" \
        --text="Choose visibility for the new GitHub repository:" \
        --column="Select" --column="Visibility" \
        TRUE "Public" FALSE "Private" \
        --height=200 --width=400 2>/dev/null)

    if [ -z "$VISIBILITY" ]; then
        echo "❌ No visibility selected. Exiting."
        exit 1
    fi

    # Convert to lowercase for gh command
    VISIBILITY_FLAG="--public"
    if [ "$VISIBILITY" = "Private" ]; then
        VISIBILITY_FLAG="--private"
    fi

    echo "🌐 Creating GitHub repository ($VISIBILITY)..."
    gh repo create "$PROJECT_NAME" "$VISIBILITY_FLAG" --source=. --remote=origin --push
fi

# 3️⃣ Ensure main branch is set
git branch -M main

# 4️⃣ Enable tag-based versioning if not present
if ! git describe --tags >/dev/null 2>&1; then
    echo "🏷️ No tags found. Creating initial tag v0.1.0..."
    git tag v0.1.0
else
    echo "✅ Git tags already present."
fi

# 5️⃣ Build setup tools
echo "🧱 Ensuring build tools installed..."
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel build setuptools-scm

echo
echo "🎉 Project $PROJECT_NAME initialized successfully!"
