#!/usr/bin/env bash
# ======================================================
# cleanproj.sh
# ------------------------------------------------------
# Safely clean up a Python project initialized with
# newproj-init.sh
# - Removes virtual environment
# - Removes build/ and dist/ directories
# - Removes *.egg-info directories
# - Leaves src/ and tests/ intact
# ======================================================

set -euo pipefail

echo "🧹 Cleaning project..."

# Remove virtual environment
[ -d .venv ] && echo "🗑️ Removing .venv/" && rm -rf .venv

# Remove build artifacts
for dir in build dist; do
    [ -d "$dir" ] && echo "🗑️ Removing $dir/" && rm -rf "$dir"
done

# Remove egg-info
for egg in *.egg-info; do
    [ -d "$egg" ] || [ -f "$egg" ] && echo "🗑️ Removing $egg" && rm -rf "$egg"
done

echo "✅ Cleanup complete!"
