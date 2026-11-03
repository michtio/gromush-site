#!/bin/sh
# Serve the built site from docs/ under the real GitHub Pages sub-path.
#   tools/serve.sh [port] [base]     defaults: 8765 /gromush-site/
#   tools/serve.sh 8766              -> http://127.0.0.1:8766/gromush-site/
#   tools/serve.sh 8766 /            -> http://127.0.0.1:8766/   (for a --base / build)
# Python stdlib only. Ctrl-C stops the server and removes the temporary folder.
set -eu
PORT="${1:-8765}"
BASE="$(printf '%s' "${2:-/gromush-site/}" | sed 's#^/*##; s#/*$##')"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$ROOT/docs/index.html" ] || { echo "no docs/index.html: run python3 -I build.py first" >&2; exit 1; }
if [ -n "$BASE" ]; then
  DIR="$(mktemp -d)"
  ln -s "$ROOT/docs" "$DIR/$BASE"
else
  DIR="$ROOT/docs"
fi
cleanup() { [ -n "${PID:-}" ] && kill "$PID" 2>/dev/null || true; [ -n "$BASE" ] && rm -rf "$DIR"; }
trap cleanup EXIT
trap 'exit 130' INT TERM
echo "Serving $ROOT/docs at http://127.0.0.1:$PORT/${BASE:+$BASE/}"
python3 -I -m http.server "$PORT" --bind 127.0.0.1 --directory "$DIR" &
PID=$!
wait "$PID"
