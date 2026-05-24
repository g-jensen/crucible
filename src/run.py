from datetime import datetime
from pathlib import Path
import secrets
import shutil
import os


def create_run_dir(results_dir: str, task_id: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_value = secrets.token_hex(4)
    dir_name = f"{timestamp}_{hash_value}_{task_id}"
    full_path = Path(results_dir) / dir_name
    full_path.mkdir(parents=True, exist_ok=True)
    return str(full_path.resolve())


def copy_seed_to_workspace(seed_path: str, workspace_path: str):
    for item in os.listdir(seed_path):
        source = os.path.join(seed_path, item)
        destination = os.path.join(workspace_path, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
