#!/bin/bash
set -e
cd "$(dirname "$0")/.."
python3 scripts/prepare_docs.py
python3 scripts/generate_indexes.py
python3 scripts/validate_docs.py
python3 -m mkdocs build --strict
