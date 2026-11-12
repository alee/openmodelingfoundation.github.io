#!/bin/sh
set -eu

# Resolve manifests without touching the image-owned node_modules volume.
operation=${1:-install}
case "$operation" in
    install|update) ;;
    *) echo "Expected install or update, got: $operation" >&2; exit 1 ;;
esac

project_dir=$PWD
workspace=$(mktemp -d)
trap 'rm -rf "$workspace"' EXIT
cp package.json package-lock.json "$workspace/"
cp -R packages "$workspace/packages"
cd "$workspace"
npm "$operation" --package-lock-only --ignore-scripts --no-audit --no-fund
# Leave the project lockfile intact if dependency resolution fails.
cp package-lock.json "$project_dir/package-lock.json"
