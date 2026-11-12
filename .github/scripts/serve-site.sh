#!/bin/sh
set -eu
sh .github/scripts/prepare-content.sh
exec hugo server --bind 0.0.0.0 "$@"
