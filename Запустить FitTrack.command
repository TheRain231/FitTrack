#!/bin/zsh
set -e
FITTRACK_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
exec "$FITTRACK_ROOT/.venv/bin/python" "$FITTRACK_ROOT/main.py"
