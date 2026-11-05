#!/bin/sh
# Homepage radial opening (S9, AC10a): collision probes at 1100-1920, before and after the full reveal.
# Hyphae against curved-label glyphs, pills and discs (tools/ringnet.js), hyphae against the title, intro, slip,
# tape and note, and the title block against the medallions (tools/ringlabel.js). The reveal is a focus inside the
# opening, which completes the drawing (js/home.js).
# usage: sh tools/ringprobes.sh <homepage url>      Expected at every width: "net 0 (N paths) label 0 rev net 0 (N paths) label 0".
# Adapted from .impeccable/tools/radiaal/probes.sh (the prototype's version).
D=$(cd "$(dirname "$0")" && pwd)
U=${1:?usage: tools/ringprobes.sh <homepage url>}
REV="(()=>{const n=document.querySelector('.ring .med-link');n&&n.focus();return 'rev'})()"
for w in 1100 1180 1279 1280 1440 1600 1680 1920; do
  printf '== %s ' "$w"
  python3 -I "$D/check.py" "$U" "$w" "$(cat "$D/ringnet.js")" "$(cat "$D/ringlabel.js")" "$REV" "$(cat "$D/ringnet.js")" "$(cat "$D/ringlabel.js")" | sed 's/.*=> //' | python3 -I -c "
import sys,json
for l in sys.stdin:
  l=l.strip()
  if l.startswith('errors:'):
    if l!='errors: []': print(l)
    continue
  try: d=json.loads(l)
  except Exception: print(l); continue
  if isinstance(d,dict): print('net', ({k:v for k,v in d['hits'].items() if v} or 0) if not any(d['hits'].values()) else d, '(%d paths)' % d['paths'] if not any(d['hits'].values()) else '')
  else: print('label', d or 0)" | tr '\n' ' '
  echo
done
