#!/usr/bin/env bash
# Nur Konfiguration und Tests kopieren; keine lokalen Daten oder Zugänge.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mode="${1:---full}"
[[ "$mode" == --fast || "$mode" == --full ]] || exit 2
docker run --rm --tmpfs /work:rw,exec,size=128m -v "$(pwd):/source:ro" \
 -e TEST_MODE="$mode" python:3.13-slim bash -ec '
  cd /work
  mkdir scripts tests
  cp /source/config.yml .
  cp /source/tests/*.py tests/
  cp /source/scripts/test.sh scripts/
  python -m pip install --no-cache-dir pyyaml==6.0.3
  scripts/test.sh "$TEST_MODE"
 '
