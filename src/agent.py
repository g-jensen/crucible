from pathlib import Path


def validate_agent_dir(agent_dir: str):
    init_sh = Path(agent_dir) / "init.sh"
    if not init_sh.exists():
        raise ValueError()
