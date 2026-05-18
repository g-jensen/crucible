import subprocess
import os


def run_init_sh(agent_dir: str, result_dir: str) -> int:
    env = os.environ.copy()
    env["ABSOLUTE_RESULT_DIR"] = result_dir
    result = subprocess.run(["./init.sh"], cwd=agent_dir, env=env)
    return result.returncode
