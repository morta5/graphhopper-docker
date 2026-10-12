#!/usr/bin/env bash
# Bestehendes Fahrzeugprofil und persistente Eingaben prüfen.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mode="${1:---full}"
[[ "$mode" == --fast || "$mode" == --full ]] || exit 2
py="${PYTHON:-python3}"
"$py" -c 'import yaml' || exit 3
export PYTHONDONTWRITEBYTECODE=1
"$py" -m unittest discover -s tests -v
