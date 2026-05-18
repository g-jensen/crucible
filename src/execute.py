import subprocess
import os


def run_init_sh(agent_dir: str, result_dir: str) -> int:
    env = os.environ.copy()
    env["ABSOLUTE_RESULT_DIR"] = result_dir
    result = subprocess.run(["./init.sh"], cwd=agent_dir, env=env)
    return result.returncode


def run_docker_compose(agent_dir: str, result_dir: str, image: str, prompt: str) -> int:
    env = os.environ.copy()
    env["IMAGE_NAME"] = image
    env["WORKING_DIR"] = "/workspace"
    env["ABSOLUTE_RESULT_DIR"] = result_dir
    env["TASK_PROMPT"] = prompt
    result = subprocess.run(
        ["docker", "compose", "up"], cwd=agent_dir + "/docker", env=env
    )
    return result.returncode


def run_docker_compose_down(agent_dir: str):
    subprocess.run(["docker", "compose", "down"], cwd=agent_dir + "/docker")
