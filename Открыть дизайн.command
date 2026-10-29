#!/bin/zsh
set -e
FITTRACK_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
exec "$FITTRACK_ROOT/.venv/bin/pyside6-designer" "$FITTRACK_ROOT/ui/main_window.ui"
