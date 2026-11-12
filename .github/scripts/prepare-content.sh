#!/bin/sh
set -eu
# Generate in the active workspace, after Compose mounts are applied.
uv run .github/scripts/bibtex_to_json.py \
  --input "${PUBLICATIONS_BIB_PATH:-assets/bibliographies/publications.bib}" \
  --output "${PUBLICATIONS_JSON_PATH:-data/publications.json}"
