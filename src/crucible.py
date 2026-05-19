from pathlib import Path
import task
import agent
import run as run_module
from execute import run_init_sh, run_docker_compose, run_docker_compose_down


def run(args):
    task_data = task.load_task(args.task)
    task.validate_task(task_data)
    agent.validate_agent_dir(args.agent_dir)
    run_dir = run_module.create_run_dir(args.results_dir, task_data["id"])
    workspace_path = Path(run_dir) / "workspace"
    workspace_path.mkdir()

    if "seed_path" in task_data:
        resolved_seed = task.resolve_seed_path(args.task, task_data["seed_path"])
        task.validate_seed_path(resolved_seed)
        run_module.copy_seed_to_workspace(resolved_seed, str(workspace_path))

    run_init_sh(args.agent_dir, run_dir)
    run_docker_compose(
        args.agent_dir, run_dir, task_data["docker_image"], task_data["prompt"]
    )

    if not args.keep:
        run_docker_compose_down(
            args.agent_dir, run_dir, task_data["docker_image"], task_data["prompt"]
        )
