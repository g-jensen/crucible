#!/bin/bash
set -euo pipefail

echo "=== Pi Agent Entrypoint ==="
echo "Task: $TASK_PROMPT"
echo ""

echo "Installing dependencies..."
apt-get update -qq
apt-get install -y -qq curl ca-certificates > /dev/null 2>&1
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 24

echo "Installing Pi..."
curl -fsSL https://pi.dev/install.sh | sh

export PATH="$HOME/.opencode/bin:$PATH"

echo "Pi installed successfully"
echo ""

echo "Running Pi with task prompt..."
pi -p "$TASK_PROMPT"

EXIT_CODE=$?
echo ""
echo "Pi exited with code: $EXIT_CODE"
exit $EXIT_CODE