from pathlib import Path
import yaml


REQUIRED_FIELDS = ["id", "docker_image", "prompt"]


def load_task(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())


def validate_task(task: dict):
    for field in REQUIRED_FIELDS:
        if field not in task:
            raise ValueError()
