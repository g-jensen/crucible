# Crucible - Agent Evaluation Orchestrator

Crucible runs AI agents inside Docker containers with controlled inputs and captures their outputs for evaluation. It separates task definitions (what to run) from agent implementations (how to run), enabling systematic agent testing across different tasks and configurations.

## Features

- **Isolated Execution**: Runs agents in Docker containers with clean, reproducible environments
- **Task-Agent Separation**: Define tasks once, test multiple agent implementations
- **Results Preservation**: Runs are saved to a directory for analysis
- **Seed Workspaces**: Initialize containers with pre-populated files and directories
- **Flexible Agent Integration**: Minimal requirements - just provide init.sh and docker-compose.yml

## Requirements

- Python 3.12+
- Docker with Compose V2 (`docker compose` command)
- Bash shell (for agent init scripts)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/g-jensen/crucible.git
cd crucible
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

3. Verify Docker is running:
```bash
docker compose version
```

### Build

```bash
pip3 install pyinstall
```

Then, build main.py:
```bash
pyinstaller --onefile src/main.py -n crucible
```

Make sure you're in your venv when you run this command.

## Quick Start

Run the included example task with the OpenCode agent:

```bash
crucible \
  --run-dir ./result \
  --task example/task.yml \
  --agent-dir agents/opencode
```

This will:
1. Create `result/` and start a container
2. Copy the seed workspace into `result/` and mount it onto the container
3. Run the OpenCode agent in the container with the specified config and the task prompt
4. Save all outputs to `result/`
5. Clean up Docker resources

## Usage

### Basic Command

With `--results-dir` (creates timestamped subdirectory):
```bash
crucible \
  --results-dir <results-directory> \
  --task <path-to-task.yml> \
  --agent-dir <path-to-agent-directory>
```

With `--run-dir` (uses exact directory):
```bash
crucible \
  --run-dir <exact-output-directory> \
  --task <path-to-task.yml> \
  --agent-dir <path-to-agent-directory>
```

### Command-Line Options

**Output Directory (choose one):**
- `--results-dir <dir>`: Creates a timestamped subdirectory for this run (e.g., `results/example_task_20260518143022_a3f9/`)
- `--run-dir <dir>`: Uses the exact directory specified (creates it if it doesn't exist)

**Required:**
- `--task <path>`: Path to task YAML file
- `--agent-dir <path>`: Path to agent directory

**Note:** `--results-dir` and `--run-dir` are mutually exclusive - you must specify exactly one.

### Example Workflow

1. **Create a task file** (`my-task.yml`):
```yaml
id: code_review
docker_image: python:3.11-slim
seed_path: ./code_to_review
prompt: "Review the Python code in the workspace and suggest improvements"
```

2. **Prepare seed directory** (`code_to_review/`):
```
code_to_review/
  main.py
  utils.py
  README.md
```

3. **Run Crucible**:
```bash
crucible \
  --results-dir ./results \
  --task my-task.yml \
  --agent-dir agents/opencode
```

4. **Check results**:
```bash
ls results/code_review_*/workspace/
cat results/code_review_*/workspace/review.txt
```

### More Command Examples

**Standard run with automatic naming:**
```bash
crucible \
  --results-dir ./results \
  --task example/task.yml \
  --agent-dir agents/opencode
# Creates: ./results/example_task_20260518143022_a3f9/
```

**Run with specific output directory:**
```bash
crucible \
  --run-dir /tmp/my-test-run \
  --task example/task.yml \
  --agent-dir agents/opencode
# Creates: /tmp/my-test-run/
```

## Task Files

Tasks are defined in YAML files with the following structure:

```yaml
id: example_task
name: Example Task                    # optional
description: Basic Python I/O task    # optional
docker_image: python:3.11-slim
seed_path: ./seed                      # optional, relative to task.yml
prompt: "Write and run a simple Python script that writes 'hello' to result.txt"
```

### Required Fields

- `id`: Unique task identifier (used in run directory naming)
- `docker_image`: Base Docker image for the container
- `prompt`: Task instructions passed to the agent

### Optional Fields

- `name`: Human-readable task name
- `description`: Detailed task description
- `seed_path`: Path to seed directory (relative to task.yml location)
  - If specified, contents are copied to `/workspace` in the container
  - If omitted, an empty workspace is created

### Example Task Files

**Simple task (no seed):**
```yaml
id: hello_world
docker_image: python:3.11-slim
prompt: "Create a Python script that prints 'Hello, World!'"
```

**Task with seed workspace:**
```yaml
id: data_processing
docker_image: python:3.11-slim
seed_path: ./seed_data
prompt: "Process the CSV file in the workspace and output summary statistics"
```

## Agent Directories

Agent directories must contain two required files:

```
agents/my-agent/
├── init.sh                      # Host-side setup script (executable)
├── docker/
│   ├── docker-compose.yml       # Container orchestration
│   └── entrypoint.sh            # Container entry point script
└── ... (other agent-specific files)
```

### init.sh Contract

Runs on the **host machine** before starting the container.

**Environment variables:**
- `ABSOLUTE_RESULT_DIR`: Absolute path to this run's result directory

**Responsibilities:**
- Prepare agent-specific files in `$ABSOLUTE_RESULT_DIR`
- Copy configuration files
- Generate environment files
- Must be executable (`chmod +x init.sh`)
- Must include shebang: `#!/bin/bash`

**Example:**
```bash
#!/bin/bash
cp -r ./config $ABSOLUTE_RESULT_DIR/agent_config
echo "API_KEY=test" > $ABSOLUTE_RESULT_DIR/.env
```

### docker-compose.yml Contract

**Environment variables available:**
- `IMAGE_NAME`: Base Docker image (from task.yml)
- `WORKING_DIR`: Container workspace path (fixed: `/workspace`)
- `ABSOLUTE_RESULT_DIR`: Absolute path to run directory
- `TASK_PROMPT`: Task prompt string (from task.yml)

**Expected structure:**
```yaml
services:
  agent:
    image: ${IMAGE_NAME}
    working_dir: ${WORKING_DIR}
    environment:
      - TASK_PROMPT=${TASK_PROMPT}
    volumes:
      - ./entrypoint.sh:/entrypoint.sh:ro
      - ${ABSOLUTE_RESULT_DIR}/workspace:${WORKING_DIR}:rw
      - ${ABSOLUTE_RESULT_DIR}/agent_config:/config:rw
    command: ["/entrypoint.sh"]
```

### entrypoint.sh

Runs **inside the container**.

**Responsibilities:**
- Install the agent (from internet, package manager, etc.)
- Configure the agent
- Execute the agent with `$TASK_PROMPT`
- Exit with appropriate code (0 = success)

**Example:**
```bash
#!/bin/bash
set -euo pipefail

# Install agent
apt-get update && apt-get install -y curl
npm install -g my-ai-agent

# Run agent
my-ai-agent run "$TASK_PROMPT"
```

## Run Directory Structure

### With --results-dir (automatic naming)

Each run creates a timestamped subdirectory:

```
results/
  example_task_20260518143022_a3f9/
    workspace/                    # Seed files + agent outputs
      result.txt
      script.py
    agent_config/                 # Created by init.sh
      config.json
    logs/                         # Created by agent
      agent.log
```

**Naming convention:** `{task_id}_{timestamp}_{hash}`
- `task_id`: From task.yml
- `timestamp`: YYYYMMDDHHmmss format
- `hash`: 8-character random hex for uniqueness

### With --run-dir (exact directory)

Uses the exact directory specified:

```
/tmp/my-test-run/
  workspace/                      # Seed files + agent outputs
    result.txt
    script.py
  agent_config/                   # Created by init.sh
    config.json
  logs/                           # Created by agent
    agent.log
```

The directory is created if it doesn't exist. No timestamp or hash is added.

### General Notes

Run directories are **never deleted** by Crucible, even on error.

## Troubleshooting

### Permission Errors in Results Directory

Docker creates files as root inside containers. If you see permission errors when cleaning up, this is normal. Results are still saved correctly.

To clean up manually:
```bash
sudo rm -rf results/example_task_*/
```

### "refers to undefined volume" Error

This usually means paths are relative instead of absolute. Crucible automatically converts relative paths, but if you see this error, check that you're running from the project root.

### Container Exits Immediately

Check the agent's entrypoint.sh script:
1. Verify it has a shebang: `#!/bin/bash`
2. Verify it's executable: `chmod +x agents/*/docker/entrypoint.sh`
3. Check logs in the run directory

### Task Fails but Container Succeeds

This is expected behavior. Crucible logs task failures (exit code ≠ 0) but continues to preserve results. Check:
- `docker logs` output (shown during run)
- Files in the run directory's workspace
- Agent-specific log files

## Running Tests

Run the unit test suite:
```bash
source .venv/bin/activate
pytest src/test/ -v
```

Run the integration test:
```bash
./test_integration.sh
```