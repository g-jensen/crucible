from pathlib import Path


def validate_agent_dir(agent_dir: str):
    init_sh = Path(agent_dir) / "init.sh"
    if not init_sh.exists():
        raise ValueError()
    docker_compose = Path(agent_dir) / "docker" / "docker-compose.yml"
    if not docker_compose.exists():
        raise ValueError()
