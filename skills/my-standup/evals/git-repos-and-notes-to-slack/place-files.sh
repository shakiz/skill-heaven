#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
python3 setup_fixture.py git-notes
