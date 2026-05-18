#!/bin/bash
set -euo pipefail

echo "=== OpenCode Agent Entrypoint ==="
echo "Task: $TASK_PROMPT"
echo ""

echo "Installing dependencies..."
apt-get update -qq
apt-get install -y -qq curl ca-certificates > /dev/null 2>&1

echo "Installing OpenCode..."
curl -fsSL https://opencode.ai/install | bash

export PATH="$HOME/.opencode/bin:$PATH"

echo "OpenCode installed successfully"
echo ""

echo "Running OpenCode with task prompt..."
opencode "$TASK_PROMPT"

EXIT_CODE=$?
echo ""
echo "OpenCode exited with code: $EXIT_CODE"
exit $EXIT_CODE