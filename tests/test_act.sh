#!/usr/bin/env bash
# Test: clone loudbinary/.github to its own folder and use act to execute
# loudbinary-start.yaml, verifying that sync.py runs through to completion.
set -euo pipefail

REPO_URL="https://github.com/loudbinary/.github.git"

# ---------------------------------------------------------------------------
# Allow running against a local checkout (e.g. during CI on a PR branch).
# Usage:  ./tests/test_act.sh [/path/to/local/repo]
# ---------------------------------------------------------------------------
if [ -n "${1:-}" ]; then
    REPO_DIR="$1"
    echo "Using local repo at $REPO_DIR"
    CLEANUP_NEEDED=false
else
    CLONE_DIR=$(mktemp -d)
    REPO_DIR="$CLONE_DIR/.github"
    CLEANUP_NEEDED=true
    echo "Cloning loudbinary/.github → $REPO_DIR ..."
    git clone "$REPO_URL" "$REPO_DIR"
fi

cleanup() {
    if [ "${CLEANUP_NEEDED:-false}" = true ]; then
        rm -rf "${CLONE_DIR:-}"
    fi
}
trap cleanup EXIT

cd "$REPO_DIR"

echo ""
echo "Running act on loudbinary-start.yaml ..."
OUTPUT=$(act workflow_dispatch \
    -W .github/workflows/loudbinary-start.yaml \
    -P ubuntu-latest=catthehacker/ubuntu:act-latest \
    2>&1)

echo "$OUTPUT"

echo ""
if echo "$OUTPUT" | grep -qi "sync complete"; then
    echo "PASS: sync.py ran and completed successfully"
    exit 0
else
    echo "FAIL: expected 'Sync complete' output from sync.py — sync did not run as expected"
    exit 1
fi
