# Crucible

## High-level Overview

You define a [task file](https://github.com/g-jensen/crucible/blob/master/example/task.yml) and an [agent directory](https://github.com/g-jensen/crucible/tree/master/agents/pi) (only OpenCode and Pi support for now) that includes both agent configuration and installation scripts. Crucible starts a Docker container, installs the agent, injects specified task information and/or volumes, and waits for the agent to complete the task. It copies relevant output from the agent's environment into a directory of your choosing.

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
pip install pyinstall
```

Then, build main.py:
```bash
pyinstaller --onefile src/main.py -n crucible
```

Make sure you're in your venv when you run this command.

Add the executable to your PATH somehow
```bash
sudo cp dist/crucible /usr/local/bin/crucible
```


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

## Task Files

Tasks are defined in YAML files with the following structure:

```yaml
id: example_task
name: Example Task                    # optional
description: Basic Python I/O task    # optional
docker_image: python:3.11-slim
seed_path: ./seed                      # optional. Path is relative to this file
prompt: "Write and run a simple Python script that writes 'hello' to result.txt"
```

## Agent Directories

Agent directories only *require* an `init.sh` and a `docker/docker-compose.yml`:

```
agents/my-agent/
├── init.sh                      # Host-side setup script (executable)
├── docker/
│   ├── docker-compose.yml       # Container orchestration
│   └── entrypoint.sh            # Entry point script for docker-compose.yml. Could be stored anywhere.
└── ... (other agent-specific files)
```

### init.sh Contract

Runs on the **host machine** before starting the container.

**Environment variables available:**
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

This can be shared between agent directories and runs **inside the container** as defined in `docker-compose.yml`.

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

## Troubleshooting

### Permission Errors in Results Directory

Docker creates files as root inside containers. If you see permission errors when cleaning up, this is normal. Results are still saved correctly.

To clean up manually:
```bash
sudo rm -rf results/example_task_*/
```

### Container Exits Immediately

Check the agent's entrypoint.sh script:
1. Verify it has a shebang: `#!/bin/bash`
2. Verify it's executable: `chmod +x agents/*/docker/entrypoint.sh`
3. Check any logs in the run directory

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
