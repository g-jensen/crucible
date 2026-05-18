#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR=$(mktemp -d -t crucible-test-XXXXXX)

echo "=== Crucible Integration Test ==="
echo "Results directory: $RESULTS_DIR"
echo

cleanup() {
    echo "Cleaning up results directory: $RESULTS_DIR"
    rm -rf "$RESULTS_DIR"
}

trap cleanup EXIT

cd "$SCRIPT_DIR"

echo "Running Crucible..."
if ! python3 src/main.py --results-dir "$RESULTS_DIR" --task example/task.yml --agent-dir agents/opencode; then
    echo "ERROR: Crucible execution failed"
    exit 1
fi

echo
echo "=== Verifying Results ==="

RUN_DIR=$(find "$RESULTS_DIR" -maxdepth 1 -type d -name "run_*" | head -n 1)
if [ -z "$RUN_DIR" ]; then
    echo "ERROR: No run directory created"
    exit 1
fi
echo "✓ Run directory created: $(basename "$RUN_DIR")"

WORKSPACE_DIR="$RUN_DIR/workspace"
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "ERROR: Workspace directory not created"
    exit 1
fi
echo "✓ Workspace directory created"

RESULT_FILE="$WORKSPACE_DIR/result.txt"
if [ ! -f "$RESULT_FILE" ]; then
    echo "ERROR: result.txt not found in workspace"
    exit 1
fi
echo "✓ result.txt exists"

EXPECTED_CONTENT="Task completed successfully"
ACTUAL_CONTENT=$(cat "$RESULT_FILE")
if [ "$ACTUAL_CONTENT" != "$EXPECTED_CONTENT" ]; then
    echo "ERROR: result.txt content mismatch"
    echo "  Expected: $EXPECTED_CONTENT"
    echo "  Actual: $ACTUAL_CONTENT"
    exit 1
fi
echo "✓ result.txt contains expected content"

echo
echo "=== Integration Test PASSED ==="
exit 0
