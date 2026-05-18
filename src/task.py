from pathlib import Path
import yaml


def load_task(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())


def validate_task(task: dict):
    if "id" not in task:
        raise ValueError()
