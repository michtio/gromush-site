#!/bin/sh
# Standard gate (plan "Standard gate and per-page bar", AD16) on a list of page paths.
#
#   tools/qa.sh /                          one page
#   tools/qa.sh / /zwammen/ /proefbox/     several pages
#   tools/qa.sh --all                      every page in docs/ (every index.html)
#
# Site-wide steps once: build (--base $QA_BASE, default /gromush-site/), unit tests (src/gen/tests
# and tools/tests), lint_content.py docs, check_links.py docs (pending pages from tools/pending_pages.txt
# reported apart from broken ones, then --same-chrome), check_depth.py docs (R7), check_seo.py docs (R40). Then it serves docs/ with
# tools/serve.sh on a free port (never 8765, which the prototype server uses) and runs per page:
# overflow.py, check.py + sweep.js + netreq.js at 390 and 1440, nojs.py at 390, and a
# FONT_SIZE=32 fullshot at 320 (200 % text: the browser's default font size in the profile, see tools/cdp.py)
# that fails on any tools/textfit.js problem: a word off screen, clipped, broken mid-word without a hyphen, or a
# horizontal scroll. Screenshots go to $QA_OUT (default: a new temp folder, printed).
# Lighthouse runs only through the chrome-devtools MCP; the script prints a reminder.
#
# Prints PASS/FAIL per step and a summary; exit 0 only when every step passes. Env: QA_BASE,
# QA_PORT, QA_OUT. Python 3 stdlib and headless Chrome only (tools/cdp.py).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 2
BASE="${QA_BASE:-/gromush-site/}"
OUT="${QA_OUT:-$(mktemp -d "${TMPDIR:-/tmp}/gromush-qa.XXXXXX")}"
mkdir -p "$OUT"
FAILS=0
RESULTS=""

[ $# -gt 0 ] || { echo "usage: tools/qa.sh [--all] <page-path>..." >&2; exit 2; }

# run <label> <expect-regex-or-empty> <command...>: runs, shows output, judges by exit code
# and, when given, by every ';'-separated extended regex matching the output.
run() {
  label="$1"; expect="$2"; shift 2
  echo "== $label"
  output="$("$@" 2>&1)"; code=$?
  printf '%s\n' "$output"
  ok=1
  [ "$code" -eq 0 ] || ok=0
  if [ -n "$expect" ]; then
    old_ifs="$IFS"; IFS=';'
    for pattern in $expect; do
      printf '%s\n' "$output" | grep -Eq -- "$pattern" || ok=0
    done
    IFS="$old_ifs"
  fi
  if [ "$ok" -eq 1 ]; then status=PASS; else status=FAIL; FAILS=$((FAILS + 1)); fi
  RESULTS="$RESULTS
$status  $label"
}

# --- site-wide steps ---
run "build --base $BASE" "^[0-9]+ pages written to " python3 -I build.py --base "$BASE"
run "unit tests src/gen/tests" "^OK" python3 -I -m unittest discover -s src/gen/tests
run "unit tests tools/tests" "^OK" python3 -I -m unittest discover -s tools/tests
run "lint_content docs" "^0 hits$" python3 -I tools/lint_content.py docs
# pages of sitemap.md that are linked but not built yet (tools/pending_pages.txt) are counted apart, not as broken
run "check_links docs" "^0 broken, 0 off-base(, [0-9]+ pending)?$" \
  python3 -I tools/check_links.py docs --base "$BASE" --pending tools/pending_pages.txt
run "check_links --same-chrome" "^0 broken, 0 off-base, 0 chrome differences" \
  python3 -I tools/check_links.py docs --base "$BASE" --pending tools/pending_pages.txt --same-chrome
run "check_depth (R7, AC9)" "^29 of 29 sitemap pages within 2 clicks" python3 -I tools/check_depth.py docs --base "$BASE"
run "check_seo (R40)" "^0 problems$" python3 -I tools/check_seo.py docs --base "$BASE"

# --- pages ---
if [ "$1" = "--all" ]; then
  PAGES="$(cd docs && find . -name index.html | sed 's#^\.##; s#index\.html$##' | sort)"
else
  PAGES="$*"
fi

PORT="${QA_PORT:-$(python3 -I -c '
import socket
while True:
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close()
    if p != 8765:
        print(p); break')}"
[ "$PORT" != 8765 ] || { echo "QA_PORT must not be 8765 (the prototype server)" >&2; exit 2; }
PREFIX="http://127.0.0.1:$PORT${BASE%/}"

sh tools/serve.sh "$PORT" "$BASE" > "$OUT/serve.log" 2>&1 &
SERVER=$!
trap 'kill "$SERVER" 2>/dev/null; wait "$SERVER" 2>/dev/null' EXIT
trap 'exit 130' INT TERM
if ! python3 -I -c '
import sys, time, urllib.request
for _ in range(50):
    try:
        urllib.request.urlopen(sys.argv[1], timeout=1); sys.exit(0)
    except Exception:
        time.sleep(0.2)
sys.exit(1)' "$PREFIX/"; then
  echo "server did not start on port $PORT:"; cat "$OUT/serve.log"; exit 1
fi
echo "== serving docs/ at $PREFIX/ (screenshots in $OUT)"

SWEEP="$(cat tools/sweep.js)"
NETREQ="$(cat tools/netreq.js)"
for page in $PAGES; do
  url="$PREFIX$page"
  slug="$(printf '%s' "$page" | sed 's#^/##; s#/$##; s#/#-#g')"
  slug="${slug:-home}"
  run "$page overflow" "320 ok 390 ok 768 ok 1024 ok 1440 ok" python3 -I tools/overflow.py "$url"
  for w in 390 1440; do
    run "$page sweep + netreq $w" 'errors: \[\]$;"n":0;"thirdParty":\[\];"cookie":""' \
      python3 -I tools/check.py "$url" "$w" "$SWEEP" "$NETREQ"
  done
  run "$page nojs 390" "^nojs ok$" python3 -I tools/nojs.py "$url" 390 "$OUT/$slug-nojs.png"
  run "$page 200% text 320" "unloaded_imgs=0 .*scrollWidth=320 textfit=0$" \
    env FONT_SIZE=32 python3 -I tools/fullshot.py "$url" "$OUT/$slug-font32" 320
done

echo
echo "== summary$RESULTS"
echo
echo "Lighthouse (chrome-devtools MCP only, not run here): serve with 'tools/serve.sh 8766' and run"
echo "lighthouse_audit (mobile) on each page above; bar: all four scores >= 90, LCP < 2.5 s, CLS < 0.1."
echo "Manual: glance at $OUT/*-font32-320*.png (200 % text at 320 px); textfit.js does not see overlaps or dialogs."
echo
if [ "$FAILS" -eq 0 ]; then echo "qa: all steps passed"; else echo "qa: $FAILS step(s) failed"; fi
[ "$FAILS" -eq 0 ]
