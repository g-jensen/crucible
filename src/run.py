from datetime import datetime
from pathlib import Path
import secrets


def create_run_dir(results_dir: str, task_id: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_value = secrets.token_hex(4)
    dir_name = f"{task_id}_{timestamp}_{hash_value}"
    full_path = Path(results_dir) / dir_name
    full_path.mkdir(parents=True, exist_ok=True)
    return str(full_path)
