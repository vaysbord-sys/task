#!/bin/sh
# Copies the LAZA deck (built in laza/r4) into the VAYS STUDIOS site at /projects/laza/.
set -e
cd "$(dirname "$0")"
mkdir -p projects/laza/old
cp ../laza/r4/index.html projects/laza/index.html
cp ../laza/r4/old/index.html projects/laza/old/index.html
# Inside the VAYS site, the deck gets a way back to the projects grid.
python3 - <<'PY'
import pathlib
p = pathlib.Path("projects/laza/index.html")
s = p.read_text()
s = s.replace('  <a href="#brief">Brief</a>', '  <a href="/projects/">← Projects</a>\n  <span class="sep"></span>\n  <a href="#brief">Brief</a>', 1)
p.write_text(s)
PY
